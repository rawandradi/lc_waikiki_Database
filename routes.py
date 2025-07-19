from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session
)
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import login_required, login_user, logout_user, current_user
import pymysql
from config import Config
from functools import wraps

from models.customer import *
from models.staff import *
from models.branch import *
from models.customer_order import *
from models.product import *
from db import get_db_connection


main_bp = Blueprint('main', __name__)

@main_bp.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Forms
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    birth_date = DateField('Birth Date', format='%Y-%m-%d')
    branch_id = SelectField('Branch', coerce=int)
    submit = SubmitField('Register')

    def validate_email(self, email):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check if email exists in Customer or Staff tables
                cursor.execute('SELECT email FROM Customer WHERE email = %s UNION SELECT email FROM Staff WHERE email = %s', 
                             (email.data, email.data))
                if cursor.fetchone():
                    raise ValidationError('Email already registered.')
        finally:
            conn.close()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def welcome():
    
    return render_template('welcome.html')

@main_bp.route('/about')
def about():
    """About Us page."""
    return render_template('about.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        user_type = request.form.get('user_type')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate required fields
        if not all([first_name, last_name, email, phone, password, confirm_password]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html', branches=get_branches())

        # Validate password match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', branches=get_branches())

        # Validate email format
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'danger')
            return render_template('register.html', branches=get_branches())

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check if email already exists in customer or staff tables
                cursor.execute('SELECT email FROM Customer WHERE email = %s UNION SELECT email FROM Staff WHERE email = %s', 
                             (email, email))
                if cursor.fetchone():
                    flash('Email already registered. Please use a different email.', 'danger')
                    return render_template('register.html', branches=get_branches())

                # Hash password
                hashed_password = generate_password_hash(password)

                if user_type == 'customer':
                    birth_date = request.form.get('birth_date')
                    if not birth_date:
                        flash('Birth date is required for customers.', 'danger')
                        return render_template('register.html', branches=get_branches())

                    # Insert into Customer table
                    cursor.execute('''
                        INSERT INTO Customer (first_name, last_name, email, phone, password, birth_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (first_name, last_name, email, phone, hashed_password, birth_date))
                    
                    user_id = cursor.lastrowid
                    user_type = 'customer'

                else:  # manager
                    branch_id = request.form.get('branch_id')
                    position = request.form.get('position')
                    custom_position = request.form.get('custom_position')
                    
                    if not branch_id:
                        flash('Please select a branch for the manager.', 'danger')
                        return render_template('register.html', branches=get_branches())
                    
                    if not position:
                        flash('Please select a position.', 'danger')
                        return render_template('register.html', branches=get_branches())
                    
                    # Handle custom position
                    final_position = custom_position if position == 'Custom' and custom_position else position
                    if position == 'Custom' and not custom_position:
                        flash('Please enter the custom position.', 'danger')
                        return render_template('register.html', branches=get_branches())

                    # Check if branch already has a manager
                    cursor.execute('SELECT manager_id FROM Branch WHERE branch_id = %s AND manager_id IS NOT NULL', (branch_id,))
                    if cursor.fetchone():
                        flash('This branch already has a manager assigned.', 'danger')
                        return render_template('register.html', branches=get_branches())

                    # Insert into Staff table with default salary and actual position
                    default_salary = 4000.00  # or whatever default you prefer
                    cursor.execute('''
                        INSERT INTO Staff (first_name, last_name, position, email, phone, salary)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (first_name, last_name, final_position, email, phone, default_salary))
                    
                    staff_id = cursor.lastrowid

                    # Insert into Manager table with password
                    cursor.execute('''
                        INSERT INTO Manager (manager_id, since, password)
                        VALUES (%s, CURDATE(), %s)
                    ''', (staff_id, hashed_password))

                    # Assign manager to branch
                    cursor.execute('''
                        UPDATE Branch SET manager_id = %s WHERE branch_id = %s
                    ''', (staff_id, branch_id))
                    
                    user_id = staff_id
                    user_type = 'manager'

                conn.commit()
                
                # Set session
                session['user_id'] = user_id
                session['user_type'] = user_type
                session['user_name'] = f"{first_name} {last_name}"
                
                flash('Registration successful! Welcome to LC Wakiki Store.', 'success')
                return redirect(url_for('main.login'))  # Fixed: removed leading slash

        except Exception as e:
            conn.rollback()
            flash(f'Registration error: {str(e)}', 'danger')
            return render_template('register.html', branches=get_branches())
        finally:
            conn.close()
    
    # GET request - show registration form
    return render_template('register.html', branches=get_branches())

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        if not email or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html')

        conn = get_db_connection()
        try:
            # Use dictionary=True cursor for consistent results
            cursor = conn.cursor()
            
            # Check Customer table first
            cursor.execute('SELECT * FROM Customer WHERE email = %s', (email,))
            user = cursor.fetchone()
            user_type = None
            stored_password = None

            if user:
                # Customer found
                stored_password = user['password']
                user_type = 'customer'
                print(f"Customer found: {user['first_name']} {user['last_name']}")
            else:
                # If not found in Customer table, check Staff table for managers
                cursor.execute('''
                    SELECT s.staff_id, s.first_name, s.last_name, s.position, s.salary,
                           s.email, s.phone, m.since, m.password as manager_password,
                           m.manager_id
                    FROM Staff s 
                    JOIN Manager m ON s.staff_id = m.manager_id 
                    WHERE s.email = %s
                ''', (email,))
                user = cursor.fetchone()
                
                if user:
                    # Manager found
                    stored_password = user['manager_password']
                    user_type = 'manager'
                    print(f"Manager found: {user['first_name']} {user['last_name']}")
                else:
                    print(f"No user found with email: {email}")

            # Debug: Check if password exists
            if user:
                print(f"User type: {user_type}")
                print(f"Has stored password: {bool(stored_password)}")
            
            # Verify password and login
            if user and stored_password and check_password_hash(stored_password, password):
                user_id = user['customer_id'] if user_type == 'customer' else user['staff_id']
                
                session['user_id'] = user_id
                session['user_type'] = user_type
                session['user_name'] = f"{user['first_name']} {user['last_name']}"
                
                if remember:
                    session.permanent = True
                
                flash(f'Welcome back, {user["first_name"]}!', 'success')
                
                # Redirect based on user type
                if user_type == 'customer':
                    return redirect(url_for('main.customer_dashboard'))
                else:  # manager
                    return redirect(url_for('dashboard'))
                    
            else:
                if not user:
                    flash('No account found with that email address.', 'danger')
                elif not stored_password:
                    flash('Account configuration error. Please contact support.', 'danger')
                else:
                    flash('Invalid email or password.', 'danger')
                    
        except Exception as e:
            import traceback
            print(f"Login error: {e}")
            print(f"Full traceback: {traceback.format_exc()}")
            flash(f'Login error: {str(e)}', 'danger')
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

    return render_template('login.html')

@main_bp.route('/customer/dashboard')
@login_required
def customer_dashboard():
    if session.get('user_type') != 'customer':
        flash('Access denied. This page is for customers only.', 'danger')
        return redirect(url_for('main.welcome'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get customer's orders
            cursor.execute('''
                SELECT o.*, a.city, a.street_address
                FROM Customer_Order o
                JOIN Address a ON o.address_id = a.address_id
                WHERE o.customer_id = %s
                ORDER BY o.order_date DESC
            ''', (session['user_id'],))
            orders = cursor.fetchall()

            # Get customer's profile
            cursor.execute('SELECT * FROM Customer WHERE customer_id = %s', (session['user_id'],))
            customer = cursor.fetchone()

            return render_template('customer_dashboard.html', 
                                customer=customer,
                                orders=orders,
                                loyalty_points=150,  # Placeholder value
                                next_level_points=300, # Placeholder value
                                available_rewards=[    # Placeholder list
                                    {'name': '10% Off Next Purchase', 'points': 200, 'description': 'Save on your next order!'},
                                    {'name': 'Free Shipping', 'points': 100, 'description': 'Get free delivery on any order.'}
                                ]
                                )
    except Exception as e:
        flash(f'An error occurred while loading the customer dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.welcome'))
    finally:
        conn.close()

@main_bp.route('/manager/dashboard')
@login_required
def manager_dashboard():
    if session.get('user_type') != 'manager':
        flash('Access denied. This page is for managers only.', 'danger')
        return redirect(url_for('main.welcome'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get manager's branch and details
            cursor.execute('''
                SELECT s.*, b.branch_name, b.location, b.branch_id, m.since
                FROM Staff s
                JOIN Manager m ON s.staff_id = m.manager_id
                JOIN Worker w ON s.staff_id = w.worker_id
                JOIN Branch b ON w.branch_id = b.branch_id
                WHERE s.staff_id = %s
            ''', (session['user_id'],))
            manager = cursor.fetchone()

            if not manager:
                flash('Manager details not found.', 'danger')
                return redirect(url_for('main.welcome'))

            # Get recent customer orders for manager's branch (simplified - just get recent orders)
            cursor.execute('''
                SELECT co.*, c.first_name, c.last_name, a.city, a.street_address
                FROM Customer_Order co
                JOIN Customer c ON co.customer_id = c.customer_id
                JOIN Address a ON co.address_id = a.address_id
                ORDER BY co.order_date DESC
                LIMIT 10
            ''')
            recent_orders = cursor.fetchall()

            return render_template('dashboard.html',
                                manager=manager,
                                recent_orders=recent_orders)
    except Exception as e:
        flash(f'An error occurred while loading the manager dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.welcome'))
    finally:
        conn.close()

@main_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.welcome'))

def get_branches():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT branch_id, branch_name, location FROM Branch')
            return cursor.fetchall()
    finally:
        conn.close()