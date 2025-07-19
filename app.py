from flask import Flask, render_template, request, redirect, flash, url_for,session
from flask import jsonify
from models.customer import add_customer, get_all_customers, get_customer_by_id, update_customer, delete_customer,search_customers
from models.supplier import add_supplier, get_all_suppliers, get_supplier_by_id, update_supplier, delete_supplier,search_suppliers
from models.address import (
    add_address, 
    get_all_addresses, 
    get_address_by_id, 
    update_address, 
    delete_address
)
from models.dashboard import *
from models.Category import add_category,update_category,get_all_categories,get_category_by_id,delete_category,search_categories
from models.staff import *
from models.branch import *
from models.product import *
from models.customer_order import *
from models.manager_order import *
import db
from datetime import datetime
from datetime import date
import os
from flask import jsonify
from routes import main_bp
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = 'a_very_secret_key_1234567890'
app.register_blueprint(main_bp)


# --- customer routes ---

@app.route('/customer')
def customer_management():
    query = request.args.get('search', '')  
    if query:
        customers = search_customers(query)
    else:
        customers = get_all_customers()
    return render_template('customer.html', customers=customers, today=date.today(), search_query=query)


@app.route('/add', methods=['POST'])
def add_customer_route():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    phone = request.form.get('phone') or None
    birth_date = request.form.get('birth_date') or None

    try:
        add_customer(first_name, last_name, email, password, phone, birth_date)
        flash('Customer added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding customer: {e}', 'danger')
    
    return redirect(url_for('customer_management'))



@app.route('/customer/edit/<int:customer_id>', methods=['POST'])
def edit_customer_route(customer_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form.get('phone') or None
    birth_date = request.form.get('birth_date') or None

    try:
        update_customer(customer_id, first_name, last_name, email, phone, birth_date)
        flash('Customer updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating customer: {e}', 'danger')

    return redirect(url_for('customer_management'))

@app.route('/customer/delete/<int:customer_id>', methods=['POST'])
def delete_customer_route(customer_id):
    try:
        delete_customer(customer_id)
        flash('Customer deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting customer: {e}', 'danger')

    return redirect(url_for('customer_management'))


# --- Supplier routes ---

@app.route('/supplier')
@app.route('/supplier/<int:supplier_id>')
def supplier_management(supplier_id=None):
    query = request.args.get('search', '')  
    if query:
        suppliers = search_suppliers(query)
    else:
        suppliers = get_all_suppliers()
    return render_template('supplier.html', suppliers=suppliers, search_query=query)

@app.route('/supplier/add', methods=['POST'])
def add_supplier_route():
    supplier_name = request.form['supplier_name']
    phone = request.form.get('phone') or None
    try:
        add_supplier(supplier_name, phone)
        flash('Supplier added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding supplier: {e}', 'danger')
    return redirect(url_for('supplier_management'))

@app.route('/supplier/edit/<int:supplier_id>', methods=['POST'])
def edit_supplier_route(supplier_id):
    supplier_name = request.form['supplier_name']
    phone = request.form.get('phone') or None
    try:
        update_supplier(supplier_id, supplier_name, phone)
        flash('Supplier updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating supplier: {e}', 'danger')
    return redirect(url_for('supplier_management'))

@app.route('/supplier/delete/<int:supplier_id>', methods=['POST'])
def delete_supplier_route(supplier_id):
    try:
        delete_supplier(supplier_id)
        flash('Supplier deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting supplier: {e}', 'danger')
    return redirect(url_for('supplier_management'))


#---------------------- Address Routes ------------------------


@app.route('/address')
def address_management():
    """Get all addresses - returns JSON for AJAX calls"""
    addresses = get_all_addresses()
    return jsonify(addresses)

@app.route('/address/customer/<int:customer_id>')
def get_customer_addresses(customer_id):
    """Get addresses for a specific customer"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT address_id, customer_id, address_type, city, street_address 
                FROM Address 
                WHERE customer_id = %s 
                ORDER BY address_type
            """, (customer_id,))
            
            columns = [desc[0] for desc in cursor.description]
            
            rows = cursor.fetchall()
            addresses = []
            for row in rows:
                print("Row : ",row)
                address_dict = dict(row)
                print("addrees_dic : ",address_dict)
                addresses.append(address_dict)
            
        conn.close()
        
        for addr in addresses:
            print(f"Address: {addr}")
            
        return jsonify(addresses)
    except Exception as e:
        print(f"Error fetching addresses: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/address/add', methods=['POST'])
def add_address_route():
    customer_id = request.form['customer_id']
    address_type = request.form['address_type']
    city = request.form['city']
    street_address = request.form['street_address']

    try:
        add_address(customer_id, address_type, city, street_address)
        return jsonify({"success": True, "message": "Address added successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error adding address: {e}"}), 500

@app.route('/address/edit/<int:address_id>', methods=['POST'])
def edit_address_route(address_id):
    address_type = request.form['address_type']
    city = request.form['city']
    street_address = request.form['street_address']

    try:
        update_address(address_id, address_type, city, street_address)
        return jsonify({"success": True, "message": "Address updated successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error updating address: {e}"}), 500

@app.route('/address/delete/<int:address_id>', methods=['POST'])
def delete_address_route(address_id):
    try:
        delete_address(address_id)
        return jsonify({"success": True, "message": "Address deleted successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error deleting address: {e}"}), 500

@app.route('/address/<int:address_id>')
def get_address_details(address_id):
    try:
        address = get_address_by_id(address_id)
        if address:
            return jsonify(address)
        else:
            return jsonify({"error": "Address not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# --- Enhanced Customer Order Routes ---

# API Routes for Customer Order Management

@app.route('/api/customer')
def get_customers_api():
    try:
        customers = get_all_customers()
        customer_list = []
        
        for customer in customers:
            customer_list.append({
                'customer_id': customer.get('customer_id'),
                'name': f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip(),
                'email': customer.get('email', ''),
                'phone': customer.get('phone', '')
            })
        
        return jsonify(customer_list)
    except Exception as e:
        print(f"Error fetching customers: {str(e)}")
        return jsonify([]), 500

@app.route('/api/addresses/customer/<int:customer_id>')
def get_customer_addresses_api(customer_id):
    """Get addresses for a specific customer - cascading dropdown functionality"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT address_id, customer_id, address_type, city, street_address
                FROM Address 
                WHERE customer_id = %s 
                ORDER BY address_type, city
            """, (customer_id,))
            addresses = cursor.fetchall()
        conn.close()
        
        address_list = []
        for address in addresses:
            address_parts = []
            if address['street_address']:
                address_parts.append(address['street_address'])
            if address['city']:
                address_parts.append(address['city'])
            if address['address_type']:
                address_parts.append(f"({address['address_type']})")

            
            display_text = ", ".join(address_parts) if address_parts else "Address"
            
            address_list.append({
                    'address_id': address['address_id'],
                    'customer_id': address['customer_id'],
                    'address_type': address['address_type'] or '',
                    'city': address['city'] or '',
                    'street_address': address['street_address'] or '',
                    'display': display_text})


        
        return jsonify(address_list)
    except Exception as e:
        print(f"Error fetching customer addresses: {str(e)}")
        return jsonify([]), 500

@app.route('/api/orders/<int:order_id>')
def get_order_api(order_id):
    """API endpoint to get order details for editing"""
    try:
        order = get_order_by_id(order_id)
        if order:
            if 'order_date' in order and order['order_date']:
                if isinstance(order['order_date'], str):
                    from datetime import datetime
                    try:
                        date_obj = datetime.strptime(order['order_date'], '%Y-%m-%d %H:%M:%S')
                        order['order_date'] = date_obj.strftime('%Y-%m-%d')
                    except:
                        order['order_date'] = order['order_date'].split(' ')[0]  # Take date part only
                else:
                    order['order_date'] = order['order_date'].strftime('%Y-%m-%d')
            
            return jsonify(order)
        else:
            return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        print(f"Error fetching order {order_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/customer_order')
@app.route('/customer_orders')
def customer_orders():
    """Display customer orders page - matches your HTML template"""
    query = request.args.get('search', '')
    print(f"[DEBUG] Search query received: '{query}'")

    orders = search_orders(query)
    print(f"[DEBUG] Orders found: {len(orders)}")

    try:
        if query:
            print("[DEBUG] Executing search_orders()")
            orders = search_orders(query)
            for order in orders:
                try:
                    order['totalAmount'] = float(order['totalAmount'])
                except (ValueError, TypeError):
                    order['totalAmount'] = 0.0

            print(f"[DEBUG] Orders found: {len(orders)}")
        else:
            try:
                print("[DEBUG] Executing get_orders_with_details()")
                orders = get_orders_with_details()
                print(f"[DEBUG] Detailed orders retrieved: {len(orders)}")
            except Exception as inner_e:
                print(f"[WARNING] get_orders_with_details() failed: {inner_e}")
                print("[DEBUG] Falling back to get_all_orders()")
                orders = get_all_orders()
                print(f"[DEBUG] Basic orders retrieved: {len(orders)}")

        print("[DEBUG] Fetching customer list")
        customers = get_all_customers()
        print(f"[DEBUG] Customers retrieved: {len(customers)}")

        return render_template('customer_order.html', 
                               orders=orders, 
                               customers=customers,
                               search_query=query)

    except Exception as e:
        print(f"[ERROR] Exception in /customer_orders route: {str(e)}")
        flash(f'Error loading orders: {str(e)}', 'error')
        return render_template('customer_order.html', orders=[], customers=[], search_query=query)


@app.route('/add_order_route', methods=['POST'])
@app.route('/add_order', methods=['POST'])
def add_order_route():
    """Add new order and its items"""
    try:
        # --- Order Fields ---
        customer_id = request.form.get('customer_id')
        address_id = request.form.get('address_id')
        order_date = request.form.get('order_date')
        status = request.form.get('status')
        total_amount = request.form.get('totalAmount')
        payment_method = request.form.get('payment_method')

        # --- Order Items (lists) ---
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')

        print(f"[DEBUG] Received order items: {list(zip(product_ids, quantities))}")

        if not all([customer_id, address_id, order_date, status, total_amount, payment_method]):
            flash('All order fields are required!', 'error')
            return redirect(url_for('customer_orders'))

        if not product_ids or not quantities or len(product_ids) != len(quantities):
            flash('You must include at least one valid order item.', 'error')
            return redirect(url_for('customer_orders'))

        # --- Convert and Validate ---
        try:
            customer_id = int(customer_id)
            address_id = int(address_id)
            total_amount = float(total_amount)
            quantities = [int(q) for q in quantities]
            product_ids = [int(pid) for pid in product_ids]
        except ValueError:
            flash('Invalid data format in form fields!', 'error')
            return redirect(url_for('customer_orders'))

        if total_amount <= 0:
            flash('Order total amount must be greater than 0!', 'error')
            return redirect(url_for('customer_orders'))

        if not validate_customer_exists(customer_id):
            flash(f'Customer ID {customer_id} does not exist!', 'error')
            return redirect(url_for('customer_orders'))

        if not validate_address_exists(address_id, customer_id):
            flash('Address is invalid or not related to the customer!', 'error')
            return redirect(url_for('customer_orders'))

        # --- Add Order ---
        order_id = add_order(customer_id, address_id, order_date, status, total_amount, payment_method)
        print(f"[DEBUG] New order ID: {order_id}")

        # --- Add Items ---
        for pid, qty in zip(product_ids, quantities):
            if not validate_product_exists(pid):
                flash(f'Product ID {pid} does not exist!', 'error')
                continue  # Skip invalid product
            if qty <= 0:
                flash(f'Invalid quantity ({qty}) for product ID {pid}', 'error')
                continue
            add_order_item(order_id, pid, qty)
            print(f"[DEBUG] Added item: order_id={order_id}, product_id={pid}, quantity={qty}")

        update_order_total(order_id)

        flash('Order and items added successfully!', 'success')

    except Exception as e:
        flash(f'Error adding order and items: {str(e)}', 'error')
        print(f"[EXCEPTION] {e}")

    return redirect(url_for('customer_orders'))


@app.route('/edit_order/<int:order_id>', methods=['POST'])
def edit_order_route(order_id):
    """Edit existing order - matches your HTML form action"""
    try:
        # Get form data
        customer_id = request.form.get('customer_id')
        address_id = request.form.get('address_id')
        order_date = request.form.get('order_date')
        status = request.form.get('status')
        total_amount = request.form.get('totalAmount')
        payment_method = request.form.get('payment_method')
        
        # Validate required fields
        if not all([customer_id, address_id, order_date, status, total_amount, payment_method]):
            flash('All fields are required!', 'error')
            return redirect(url_for('customer_orders'))
        
        # Convert and validate data types
        try:
            customer_id = int(customer_id)
            address_id = int(address_id)
            total_amount = float(total_amount)
        except ValueError:
            flash('Invalid data format provided!', 'error')
            return redirect(url_for('customer_orders'))
        
        # Validate positive amount
        if total_amount <= 0:
            flash('Order amount must be greater than 0!', 'error')
            return redirect(url_for('customer_orders'))
        
        # Validate customer exists
        if not validate_customer_exists(customer_id):
            flash(f'Customer with ID {customer_id} does not exist!', 'error')
            return redirect(url_for('customer_orders'))
        
        # Validate address exists and belongs to customer
        if not validate_address_exists(address_id, customer_id):
            flash(f'Address with ID {address_id} does not exist or does not belong to this customer!', 'error')
            return redirect(url_for('customer_orders'))
        
        # Update the order
        update_order(order_id, customer_id, address_id, order_date, status, total_amount, payment_method)
        flash('Order updated successfully!', 'success')
        
    except Exception as e:
        flash(f'Error updating order: {str(e)}', 'error')
    
    return redirect(url_for('customer_orders'))

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order_route(order_id):
    """Delete order - matches your HTML form action"""
    try:
        order = get_order_by_id(order_id)
        if not order:
            flash(f'Order with ID {order_id} not found!', 'error')
            return redirect(url_for('customer_orders'))
        
        delete_order(order_id)
        flash('Order deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting order: {str(e)}', 'error')
    
    return redirect(url_for('customer_orders'))

@app.route('/customer/<int:customer_id>/orders')
def view_customer_orders(customer_id):
    """View all orders for a specific customer"""
    try:
        orders = get_customer_orders(customer_id)
        customer = get_customer_by_id(customer_id)
        
        if not customer:
            flash('Customer not found!', 'error')
            return redirect(url_for('customer_orders'))
        
        return render_template('customer_orders.html', 
                             orders=orders, 
                             customer=customer)
    except Exception as e:
        flash(f'Error loading customer orders: {str(e)}', 'error')
        return redirect(url_for('customer_orders'))





# ===== Order Items Management Routes =====

# API Routes for Order Items
@app.route('/api/orders/<int:order_id>/items')
def get_Customer_Order_Items_api(order_id):
    """Get all items for a specific order (API endpoint)"""
    try:
        items = get_Customer_Order_Items_with_products(order_id)
        print("DEBUG items =", items)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/Customer_Order_Items/<int:order_item_id>')
def get_order_item_api(order_item_id):
    """Get specific order item details """
    try:
        item = get_order_item_by_id(order_item_id)
        if not item:
            return jsonify({'error': 'Order item not found'}), 404
        return jsonify(item)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products')
def get_products_api():
    """Get all products for dropdowns"""
    try:
        products = get_all_products()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Order Item CRUD Routes
@app.route('/add_order_item', methods=['POST'])
def add_order_item_route():
    """Add new order item"""
    try:
        print("[DEBUG] Received POST to /add_order_item")

        order_id = request.form.get('order_id')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        print(f"[DEBUG] Raw form data - order_id: {order_id}, product_id: {product_id}, quantity: {quantity}")
        
        # Validate required fields
        if not all([order_id, product_id, quantity]):
            flash('All fields are required!', 'error')
            print("[ERROR] Missing required fields")
            return redirect(url_for('customer_orders'))
        
        try:
            order_id = int(order_id)
            product_id = int(product_id)
            quantity = int(quantity)
            print(f"[DEBUG] Converted values - order_id: {order_id}, product_id: {product_id}, quantity: {quantity}")
        except ValueError as ve:
            flash('Invalid data format provided!', 'error')
            print(f"[ERROR] ValueError converting form values: {ve}")
            return redirect(url_for('customer_orders'))
        
        if quantity <= 0:
            flash('Quantity must be greater than 0!', 'error')
            print("[ERROR] Quantity is not positive")
            return redirect(url_for('customer_orders'))
        
        if not validate_order_exists(order_id):
            flash(f'Order with ID {order_id} does not exist!', 'error')
            print(f"[ERROR] Order ID {order_id} does not exist")
            return redirect(url_for('customer_orders'))
        
        if not validate_product_exists(product_id):
            flash(f'Product with ID {product_id} does not exist!', 'error')
            print(f"[ERROR] Product ID {product_id} does not exist")
            return redirect(url_for('customer_orders'))
        
        success = add_order_item(order_id, product_id, quantity)
        print(f"[DEBUG] add_order_item success: {success}")

        if not success:
            flash('Failed to add order item!', 'error')
            print("[ERROR] add_order_item function returned False")
            return redirect(url_for('customer_orders'))
        
        update_order_total(order_id)
        print(f"[DEBUG] Order total updated for order_id: {order_id}")
        
        flash('Order item added successfully!', 'success')
        print("[SUCCESS] Order item added")
        
    except Exception as e:
        flash(f'Error adding order item: {str(e)}', 'error')
        print(f"[EXCEPTION] Unexpected error: {str(e)}")
    
    return redirect(url_for('customer_orders'))

@app.route('/edit_order_item/<int:order_item_id>', methods=['POST'])
def edit_order_item_route(order_item_id):
    """Edit existing order item"""
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        order_id = request.form.get('order_id')
        
        if not all([product_id, quantity]):
            flash('All fields are required!', 'error')
            return redirect(url_for('customer_orders'))
        
        try:
            product_id = int(product_id)
            quantity = int(quantity)
            if order_id:
                order_id = int(order_id)
        except ValueError:
            flash('Invalid data format provided!', 'error')
            return redirect(url_for('customer_orders'))
        
        if quantity <= 0:
            flash('Quantity must be greater than 0!', 'error')
            return redirect(url_for('customer_orders'))
        
        if quantity <= 0:
            flash('Quantity must be greater than 0!', 'error')
            return redirect(url_for('customer_orders'))
        
        if not validate_product_exists(product_id):
            flash(f'Product with ID {product_id} does not exist!', 'error')
            return redirect(url_for('customer_orders'))
        
        update_order_item(order_item_id, product_id, quantity)
        
        if order_id:
            update_order_total(order_id)
        
        flash('Order item updated successfully!', 'success')

    except Exception as e:
        flash(f'Error updating order item: {str(e)}', 'error')
    
    return redirect(url_for('customer_orders'))


@app.route('/delete_order_item/<int:order_item_id>', methods=['POST'])
def delete_order_item_route(order_item_id):
    """Delete an order item"""
    try:
        # Get the order item to find the related order_id
        item = get_order_item_by_id(order_item_id)
        if not item:
            flash('Order item not found!', 'error')
            return redirect(url_for('customer_orders'))
        
        order_id = item['order_id']
        
        # Delete the order item
        delete_order_item(order_item_id)
        
        # Update order total
        update_order_total(order_id)
        
        flash('Order item deleted successfully!', 'success')

    except Exception as e:
        flash(f'Error deleting order item: {str(e)}', 'error')
    
    return redirect(url_for('customer_orders'))



# --- Category routes ---

@app.route('/category')
@app.route('/category/<int:category_id>')
def category_management(category_id =None):
    query = request.args.get('search', '')  
    if query:
        categories = search_categories(query)
    else:
        categories = get_all_categories()
    return render_template('category.html', categories=categories, search_query=query)

@app.route('/category/add', methods=['POST'])
def add_category_route():
    category_name = request.form['category_name']
    category_description = request.form.get('category_description', '')  
    try:
        add_category(category_name, category_description)
        flash('Category added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding category: {e}', 'error')  
    return redirect(url_for('category_management'))

@app.route('/category/edit/<int:category_id>', methods=['POST'])
def edit_category_route(category_id):
    category_name = request.form['category_name']
    category_description = request.form.get('category_description', '')  
    try:
        update_category(category_id, category_name, category_description)
        flash('Category updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating category: {e}', 'error')
    return redirect(url_for('category_management'))

@app.route('/category/delete/<int:category_id>', methods=['POST'])
def delete_category_route(category_id):
    try:
        delete_category(category_id)
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting category: {e}', 'error')
    return redirect(url_for('category_management'))
    
# --- Staff Management Routes ---

@app.route('/staff')
def staff_management():
    staff_type = request.args.get('staff_type','all')
    print(staff_type)
    search_query = request.args.get('search', '')
    
    try:
        print(f"Getting staff - type: {staff_type}, search: {search_query}")
        
        if search_query:
            if staff_type == 'all':
                print("Calling search_all_staff")
                staff_list = search_all_staff(search_query)
            else:
                print(f"Calling search_staff_by_type with {staff_type}")
                staff_list = search_staff_by_type(staff_type, search_query)
        else:
            if staff_type == 'all':
                print("Calling get_all_staff")
                staff_list = get_all_staff()
            elif staff_type == 'worker':
                print("Calling get_workers")
                staff_list = get_workers()
            elif staff_type == 'manager':
                print("Calling get_managers")
                staff_list = get_managers()
            else:
                print("Calling get_all_staff (default)")
                staff_list = get_all_staff()
        
        print(f"Staff list retrieved: {len(staff_list) if staff_list else 0} items")
        if staff_list:
            print(f"First item type: {type(staff_list[0])}")
            print(f"First item: {staff_list[0]}")
        
        # Get branches for the dropdowns in modals
        branches_raw = get_all_branches()
        print(f"Raw branches: {branches_raw}")
        
        branches = []
        if branches_raw:
            for branch in branches_raw:
                print(f"Processing branch: {branch}")
                branches.append({
                    'id': branch['branch_id'],
                    'name': branch['branch_name']
                })
        
        print(f"Converted branches: {branches}")
        print(f"Branches count: {len(branches)}")
        
        return render_template('staff.html', 
                             staff_list=staff_list, 
                             staff_type=staff_type,
                             search_query=search_query,
                             branches=branches)
                             
    except Exception as e:
        print(f"Full error: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error loading staff: {e}', 'error')
        return render_template('staff.html', 
                             staff_list=[], 
                             staff_type=staff_type,
                             search_query=search_query,
                             branches=[])

@app.route('/staff/add', methods=['POST'])
def add_staff():
    staff_type = request.form['staff_type']
    first_name = request.form['first_name'].strip()
    last_name = request.form['last_name'].strip()
    position = request.form['position'].strip()
    email = request.form['email'].strip()
    phone = request.form['phone'].strip()
    
    try:
        # Validate salary
        try:
            salary = float(request.form['salary'])
            if salary <= 0:
                raise ValueError("Salary must be positive")
        except (ValueError, TypeError):
            raise ValueError("Invalid salary value")
        
        # Validate required fields
        if not all([first_name, last_name, position, email, phone]):
            raise ValueError("All fields are required")
        
        if staff_type == 'worker':
            try:
                branch_id = int(request.form['branch_id'])
            except (ValueError, TypeError):
                raise ValueError("Invalid branch selection")
                
            birth_date = request.form['birth_date']
            if not birth_date:
                raise ValueError("Birth date is required for workers")
                
            staff_id = add_worker(first_name, last_name, position, salary, email, phone, branch_id, birth_date)
            
        elif staff_type == 'manager':
            since = request.form['since']
            if not since:
                raise ValueError("Since date is required for managers")
            
            # Password validation for managers
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            
            if not password:
                raise ValueError("Password is required for managers")
            
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            
            if password != confirm_password:
                raise ValueError("Passwords do not match")
            
            # Hash the password
            hashed_password = generate_password_hash(password)
                
            staff_id = add_manager(first_name, last_name, position, salary, email, phone, since, hashed_password)
        else:
            raise ValueError("Invalid staff type")
            
        flash('Staff member added successfully!', 'success')
        
    except Exception as e:
        print(f"Error adding staff: {e}")
        flash(f'Error adding staff member: {str(e)}', 'error')
    
    return redirect(url_for('staff_management'))

@app.route('/staff/edit/<int:staff_id>', methods=['POST'])
def edit_staff(staff_id):
    try:
        staff_member = get_staff_by_id(staff_id)
        if not staff_member:
            raise ValueError("Staff member not found")
        
        # Validate form data
        required_fields = ['first_name', 'last_name', 'position', 'salary', 'email', 'phone']
        for field in required_fields:
            if not request.form.get(field, '').strip():
                raise ValueError(f"{field.replace('_', ' ').title()} is required")
        
        try:
            salary = float(request.form['salary'])
            if salary <= 0:
                raise ValueError("Salary must be positive")
        except (ValueError, TypeError):
            raise ValueError("Invalid salary value")
        
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        position = request.form['position'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()
        
        staff_type = staff_member['staff_type']
        
        if not staff_type:
            raise ValueError("Could not determine staff type")
        
        # Update based on staff type
        if staff_type == 'worker':
            try:
                branch_id = int(request.form['branch_id'])
            except (ValueError, TypeError):
                raise ValueError("Invalid branch ID")
            
            birth_date = request.form.get('birth_date')
            if not birth_date:
                raise ValueError("Birth date is required for workers")
            
            update_worker(staff_id, first_name, last_name, position, salary, 
                         email, phone, branch_id, birth_date)
                         
        elif staff_type == 'manager':
            since = request.form.get('since')
            if not since:
                raise ValueError("Since date is required for managers")
            
            # Handle password update for managers
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            hashed_password = None
            
            if password:  
                if len(password) < 8:
                    raise ValueError("Password must be at least 8 characters long")
                
                if password != confirm_password:
                    raise ValueError("Passwords do not match")
                
                # Hash the new password
                hashed_password = generate_password_hash(password)
            
            update_manager(staff_id, first_name, last_name, position, salary, 
                          email, phone, since, hashed_password)
        else:
            raise ValueError("Invalid staff type")
            
        flash('Staff member updated successfully!', 'success')
        
    except Exception as e:
        print(f"Error updating staff: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Error updating staff member: {str(e)}', 'error')
    
    return redirect(url_for('staff_management'))

@app.route('/staff/delete/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    try:
        staff_member = get_staff_by_id(staff_id)
        if not staff_member:
            raise ValueError("Staff member not found")
        
        # Get staff type from dictionary
        staff_type = staff_member['staff_type']
        
        if not staff_type:
            raise ValueError("Could not determine staff type")
        
        # Delete based on staff type
        if staff_type == 'worker':
            delete_worker(staff_id)
        elif staff_type == 'manager':
            delete_manager(staff_id)
        else:
            raise ValueError("Invalid staff type")
            
        flash('Staff member deleted successfully!', 'success')
        
    except Exception as e:
        print(f"Error in delete_staff: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Error deleting staff member: {str(e)}', 'error')
    
    return redirect(url_for('staff_management'))

@app.route('/staff/details/<int:staff_id>')
def get_staff_details(staff_id):
    """AJAX endpoint to get staff details with proper error handling"""
    try:
        staff_member = get_staff_by_id(staff_id)
        if not staff_member:
            return jsonify({'error': 'Staff member not found'}), 404
        
        staff_data = {
            'staff_id': staff_member['staff_id'],
            'first_name': staff_member['first_name'],
            'last_name': staff_member['last_name'],
            'position': staff_member['position'],
            'salary': float(staff_member['salary']) if staff_member['salary'] else 0,
            'email': staff_member['email'],
            'phone': staff_member['phone'],
            'staff_type': staff_member['staff_type']
        }
        
        if staff_data['staff_type'] == 'worker':
            # Handle birth_date
            birth_date = staff_member.get('birth_date')
            if birth_date:
                try:
                    # Handle different date formats
                    if hasattr(birth_date, 'strftime'):
                        # It's a datetime object
                        staff_data['birth_date'] = birth_date.strftime('%Y-%m-%d')
                    elif isinstance(birth_date, str):
                        # It's already a string, validate and format if needed
                        from datetime import datetime
                        parsed_date = datetime.strptime(birth_date, '%Y-%m-%d')
                        staff_data['birth_date'] = parsed_date.strftime('%Y-%m-%d')
                    else:
                        staff_data['birth_date'] = str(birth_date)
                except Exception as date_error:
                    print(f"Date formatting error: {date_error}")
                    staff_data['birth_date'] = str(birth_date) if birth_date else ''
            else:
                staff_data['birth_date'] = ''
            
            branch_id = staff_member.get('branch_id')
            staff_data['branch_id'] = int(branch_id) if branch_id else None
            
            staff_data['branch_name'] = staff_member.get('branch_name', '')
            
        elif staff_data['staff_type'] == 'manager':
            since = staff_member.get('since')
            if since:
                try:
                    if hasattr(since, 'strftime'):
                        staff_data['since'] = since.strftime('%Y-%m-%d')
                    elif isinstance(since, str):
                        from datetime import datetime
                        parsed_date = datetime.strptime(since, '%Y-%m-%d')
                        staff_data['since'] = parsed_date.strftime('%Y-%m-%d')
                    else:
                        staff_data['since'] = str(since)
                except Exception as date_error:
                    print(f"Since date formatting error: {date_error}")
                    staff_data['since'] = str(since) if since else ''
            else:
                staff_data['since'] = ''
            
            staff_data['has_password'] = bool(staff_member.get('password'))
        
        print(f"Returning staff data: {staff_data}")
        return jsonify(staff_data)
        
    except Exception as e:
        print(f"Error in get_staff_details: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/staff/edit-data/<int:staff_id>')
def get_staff_edit_data(staff_id):
    """AJAX endpoint to get staff data for editing"""
    try:
        staff_member = get_staff_by_id(staff_id)
        if not staff_member:
            return jsonify({'error': 'Staff member not found'}), 404
        
        staff_data = {
            'staff_id': staff_member['staff_id'],
            'first_name': staff_member['first_name'],
            'last_name': staff_member['last_name'],
            'position': staff_member['position'],
            'salary': staff_member['salary'],
            'email': staff_member['email'],
            'phone': staff_member['phone'],
            'staff_type': staff_member['staff_type']
        }
        
        if staff_member['staff_type'] == 'worker':
            birth_date = staff_member.get('birth_date')
            if birth_date:
                try:
                    if hasattr(birth_date, 'strftime'):
                        staff_data['birth_date'] = birth_date.strftime('%Y-%m-%d')
                    else:
                        staff_data['birth_date'] = str(birth_date)
                except:
                    staff_data['birth_date'] = ''
            else:
                staff_data['birth_date'] = ''
            
            staff_data['branch_id'] = staff_member.get('branch_id') or ''
            
        elif staff_member['staff_type'] == 'manager':
            since_date = staff_member.get('since')
            if since_date:
                try:
                    if hasattr(since_date, 'strftime'):
                        staff_data['since'] = since_date.strftime('%Y-%m-%d')
                    else:
                        staff_data['since'] = str(since_date)
                except:
                    staff_data['since'] = ''
            else:
                staff_data['since'] = ''
            
            # Indicate if manager has a password (for security, never return actual password)
            staff_data['has_password'] = bool(staff_member.get('password'))
        
        return jsonify(staff_data)
        
    except Exception as e:
        print(f"Error in get_staff_edit_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/manager/login', methods=['POST'])
def manager_login():
    """Endpoint for manager authentication"""
    try:
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Get manager by email
        manager = get_manager_by_email(email)  # You'll need to implement this function
        
        if not manager:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(manager['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Successful login - you can implement session management here
        return jsonify({
            'success': True,
            'manager_id': manager['manager_id'],
            'name': f"{manager['first_name']} {manager['last_name']}"
        })
        
    except Exception as e:
        print(f"Error in manager_login: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/manager/change-password/<int:manager_id>', methods=['POST'])
def change_manager_password(manager_id):
    """Endpoint for managers to change their own password"""
    try:
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not all([current_password, new_password, confirm_password]):
            raise ValueError("All password fields are required")
        
        if len(new_password) < 8:
            raise ValueError("New password must be at least 8 characters long")
        
        if new_password != confirm_password:
            raise ValueError("New passwords do not match")
        
        manager = get_staff_by_id(manager_id)
        if not manager or manager['staff_type'] != 'manager':
            raise ValueError("Manager not found")
        
        if not check_password_hash(manager['password'], current_password):
            raise ValueError("Current password is incorrect")
        
        hashed_password = generate_password_hash(new_password)
        update_manager_password(manager_id, hashed_password)  
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('manager_dashboard'))  
        
    except Exception as e:
        print(f"Error changing password: {str(e)}")
        flash(f'Error changing password: {str(e)}', 'error')
        return redirect(url_for('manager_dashboard'))  
    

@app.route('/api/branches')
def get_branches_api():
    """API endpoint to get all branches"""
    try:
        branches = get_all_branches()
        branch_list = []
        for branch in branches:
            branch_list.append({
                'branch_id': branch['branch_id'], 
                'branch_name': branch['branch_name']
            })
        return jsonify(branch_list)
    except Exception as e:
        print(f"Error in get_branches_api: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/staff/branch/<int:branch_id>')
def staff_by_branch(branch_id):
    """Get staff members in a specific branch"""
    try:
        workers = get_workers_by_branch(branch_id)
        branches = get_all_branches()
        
        # Get branch name from the branches list
        branch_name = 'Unknown Branch'
        for branch in branches:
            if branch['branch_id'] == branch_id:
                branch_name = branch['branch_name']
                break
        
        # Convert branches for template
        branches_for_template = []
        for branch in branches:
            branches_for_template.append({
                'branch_id': branch['branch_id'],
                'branch_name': branch['branch_name']
            })
        
        return render_template('staff.html', 
                             staff_list=workers, 
                             staff_type='worker',
                             search_query='',
                             branches=branches_for_template,
                             branch_filter=branch_id,
                             branch_name=branch_name)
    except Exception as e:
        print(f"Error loading staff by branch: {e}")
        flash(f'Error loading staff by branch: {e}', 'error')
        return redirect(url_for('staff_management'))

# Utility route for checking staff existence
@app.route('/staff/exists/<int:staff_id>')
def check_staff_exists(staff_id):
    """Check if a staff member exists"""
    try:
        staff_member = get_staff_by_id(staff_id)
        return jsonify({'exists': staff_member is not None})
    except Exception as e:
        print(f"Error checking staff existence: {e}")
        return jsonify({'exists': False, 'error': str(e)})

# --- branch routes ---

@app.route('/branch')
def branch_management():
    query = request.args.get('search', '')  # get search term from URL query params
    if query:
        branches = search_branches(query)
    else:
        branches = get_all_branches()
    
    # Add managers list for the dropdown
    managers = get_available_managers()
    
    return render_template('branch.html', branches=branches, managers=managers, search_query=query)


@app.route('/branch/add', methods=['POST'])
def add_branch_route():
    branch_name = request.form['branch_name']
    location = request.form['location']
    manager_id = request.form.get('manager_id') or None
    contact_number = request.form.get('contact_number') or None

    try:
        # Validate required fields
        if not branch_name.strip():
            flash('Branch name is required', 'danger')
            return redirect(url_for('branch_management'))
        
        if not location.strip():
            flash('Location is required', 'danger')
            return redirect(url_for('branch_management'))
        
        if not manager_id:
            flash('Manager selection is required', 'danger')
            return redirect(url_for('branch_management'))
        
        # Convert manager_id to integer since it comes from dropdown
        try:
            manager_id = int(manager_id)
        except (ValueError, TypeError):
            flash('Invalid manager selection', 'danger')
            return redirect(url_for('branch_management'))
        
        add_branch(branch_name, location, manager_id, contact_number)
        flash('Branch added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding branch: {e}', 'danger')
    
    return redirect(url_for('branch_management'))



@app.route('/branch/edit/<int:branch_id>', methods=['POST'])
def edit_branch_route(branch_id):
    branch_name = request.form['branch_name']
    location = request.form['location']
    manager_id = request.form.get('manager_id') or None
    contact_number = request.form.get('contact_number') or None

    try:
        # Validate required fields
        if not branch_name.strip():
            return jsonify({'success': False, 'message': 'Branch name is required'}), 400
        
        if not location.strip():
            return jsonify({'success': False, 'message': 'Location is required'}), 400
        
        if manager_id:
            try:
                manager_id = int(manager_id)
            except (ValueError, TypeError):
                return jsonify({'success': False, 'message': 'Invalid manager ID'}), 400
        
        update_branch(branch_id, branch_name, location, manager_id, contact_number)
        return jsonify({'success': True})

    except Exception as e:
        print(f'Error updating branch: {e}')
        return jsonify({'success': False, 'message': str(e)}), 500



@app.route('/branch/delete/<int:branch_id>', methods=['POST'])
def delete_branch_route(branch_id):
    try:
        delete_branch(branch_id)
        flash('Branch deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting branch: {e}', 'danger')

    return redirect(url_for('branch_management'))


# --- warehouse routes ---

@app.route('/branch/<int:branch_id>/warehouses')
def get_branch_warehouses(branch_id):
    """Get all warehouses for a specific branch"""
    try:
        print(f"DEBUG: Fetching warehouses for branch_id: {branch_id}")
        print(f"DEBUG: branch_id type: {type(branch_id)}")
        
        warehouses = get_warehouses_by_branch_id(branch_id)  
     
        
        warehouse_list = []
        for i, warehouse in enumerate(warehouses):
            if hasattr(warehouse, 'warehouse_id'):
                warehouse_data = {
                    'warehouse_id': warehouse.warehouse_id,
                    'location': warehouse.location,
                    'capacity': warehouse.capacity
                }
            elif isinstance(warehouse, (tuple, list)):
                warehouse_data = {
                    'warehouse_id': warehouse[0],
                    'location': warehouse[1],
                    'capacity': warehouse[2]
                }
            elif isinstance(warehouse, dict):
                warehouse_data = {
                    'warehouse_id': warehouse.get('warehouse_id') or warehouse.get('id'),
                    'location': warehouse.get('location'),
                    'capacity': warehouse.get('capacity')
                }
            else:
                print(f"DEBUG: Unknown warehouse data structure: {type(warehouse)}")
                continue
                
            print(f"DEBUG: Processed warehouse_data: {warehouse_data}")
            warehouse_list.append(warehouse_data)
        
        print(f"DEBUG: Final warehouse_list: {warehouse_list}")
        return jsonify(warehouse_list)
        
    except Exception as e:
        print(f"ERROR: Full exception details:")
        print(f"ERROR: Exception type: {type(e)}")
        print(f"ERROR: Exception message: {str(e)}")
        import traceback
        print(f"ERROR: Full traceback:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/branch/<int:branch_id>/warehouse/add', methods=['POST'])
def add_warehouse_route(branch_id):
    """Add a warehouse to a specific branch"""
    try:
        location = request.form.get('location', '').strip()
        capacity = request.form.get('capacity', '').strip()
        
        if not location:
            return jsonify({'success': False, 'message': 'Location is required'}), 400
        
        if not capacity or not capacity.isdigit() or int(capacity) <= 0:
            return jsonify({'success': False, 'message': 'Valid capacity is required'}), 400
        
        add_warehouse(branch_id, location, int(capacity))
        return jsonify({'success': True, 'message': 'Warehouse added successfully!'})
        
    except Exception as e:
        print(f"Error adding warehouse: {e}")  
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/warehouse/edit/<int:warehouse_id>', methods=['POST'])
def edit_warehouse_route(warehouse_id):
    """Edit a warehouse"""
    location = request.form['location']
    capacity = request.form['capacity']

    try:
        update_warehouse(warehouse_id, location, capacity)
        
        if (request.is_json or 
            request.headers.get('Content-Type') == 'application/json' or
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
            return jsonify({'success': True, 'message': 'Warehouse updated successfully!'})
        else:
            flash('Warehouse updated successfully!', 'success')
            return redirect(url_for('branch_management'))
            
    except Exception as e:
        if (request.is_json or 
            request.headers.get('Content-Type') == 'application/json' or
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash(f'Error updating warehouse: {e}', 'danger')
            return redirect(url_for('branch_management'))

@app.route('/warehouse/delete/<int:warehouse_id>', methods=['POST'])
def delete_warehouse_route(warehouse_id):
    """Delete a warehouse"""
    try:
        delete_warehouse(warehouse_id)
        
        if (request.is_json or 
            request.headers.get('Content-Type') == 'application/json' or
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
            return jsonify({'success': True, 'message': 'Warehouse deleted successfully!'})
        else:
            flash('Warehouse deleted successfully!', 'success')
            return redirect(url_for('branch_management'))
            
    except Exception as e:
        if (request.is_json or 
            request.headers.get('Content-Type') == 'application/json' or
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash(f'Error deleting warehouse: {e}', 'danger')
            return redirect(url_for('branch_management'))
        

@app.route('/warehouse/<int:warehouse_id>')
def get_warehouse_details(warehouse_id):
    try:
        warehouse = get_warehouse_by_id(warehouse_id)
        if warehouse:
            return jsonify({
                'success': True,
                'warehouse': warehouse
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Warehouse not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    




# --- product routes ---

@app.route('/product')
def product_management():
    query = request.args.get('search', '')  
    if query:
        products = search_products(query)
    else:
        products = get_all_products()
    print(products)
    categories = get_all_categories()
    suppliers = get_all_suppliers()
    warehouses = get_all_warehouses()
    
    return render_template('product.html', 
                         products=products, 
                         categories=categories,
                         suppliers=suppliers,
                         warehouses=warehouses,
                         search_query=query)


@app.route('/product/add', methods=['POST'])
def add_product_route():
    product_name = request.form['product_name']
    description = request.form.get('description') or None
    price = request.form['price']
    stock_quantity = request.form['stock_quantity']
    category_id = request.form.get('category_id') or None
    supplier_id = request.form.get('supplier_id') or None
    warehouse_id = request.form.get('warehouse_id') or None

    try:
        # Validate required fields
        if not product_name.strip():
            flash('Product name is required', 'danger')
            return redirect(url_for('product_management'))
        
        # Validate price
        try:
            price = float(price)
            if price < 0:
                flash('Price cannot be negative', 'danger')
                return redirect(url_for('product_management'))
        except (ValueError, TypeError):
            flash('Invalid price format', 'danger')
            return redirect(url_for('product_management'))
        
        # Validate stock quantity
        try:
            stock_quantity = int(stock_quantity)
            if stock_quantity < 0:
                flash('Stock quantity cannot be negative', 'danger')
                return redirect(url_for('product_management'))
        except (ValueError, TypeError):
            flash('Invalid stock quantity format', 'danger')
            return redirect(url_for('product_management'))
        
        # Validate category_id
        if not category_id:
            flash('Category selection is required', 'danger')
            return redirect(url_for('product_management'))
        
        try:
            category_id = int(category_id)
        except (ValueError, TypeError):
            flash('Invalid category selection', 'danger')
            return redirect(url_for('product_management'))
        
        # Validate supplier_id
        if not supplier_id:
            flash('Supplier selection is required', 'danger')
            return redirect(url_for('product_management'))
        
        try:
            supplier_id = int(supplier_id)
        except (ValueError, TypeError):
            flash('Invalid supplier selection', 'danger')
            return redirect(url_for('product_management'))
        
        # Validate warehouse_id
        if not warehouse_id:
            flash('Warehouse selection is required', 'danger')
            return redirect(url_for('product_management'))
        
        try:
            warehouse_id = int(warehouse_id)
        except (ValueError, TypeError):
            flash('Invalid warehouse selection', 'danger')
            return redirect(url_for('product_management'))
        
        add_product(product_name, description, price, stock_quantity, category_id, supplier_id, warehouse_id)
        flash('Product added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding product: {e}', 'danger')
    
    return redirect(url_for('product_management'))


@app.route('/product/edit/<int:product_id>', methods=['POST'])
def edit_product_route(product_id):
    product_name = request.form['product_name']
    description = request.form.get('description') or None
    price = request.form['price']
    stock_quantity = request.form['stock_quantity']
    category_id = request.form.get('category_id') or None
    supplier_id = request.form.get('supplier_id') or None
    warehouse_id = request.form.get('warehouse_id') or None

    try:
        # Validate required fields
        if not product_name.strip():
            flash('Product name is required', 'danger')
            return redirect(url_for('product_management'))
        
        try:
            price = float(price)
            if price < 0:
                flash('Price cannot be negative', 'danger')
                return redirect(url_for('product_management'))
        except (ValueError, TypeError):
            flash('Invalid price format', 'danger')
            return redirect(url_for('product_management'))
        
        try:
            stock_quantity = int(stock_quantity)
            if stock_quantity < 0:
                flash('Stock quantity cannot be negative', 'danger')
                return redirect(url_for('product_management'))
        except (ValueError, TypeError):
            flash('Invalid stock quantity format', 'danger')
            return redirect(url_for('product_management'))
        
        # Validate category_id
        if category_id:
            try:
                category_id = int(category_id)
            except (ValueError, TypeError):
                flash('Invalid category selection', 'danger')
                return redirect(url_for('product_management'))
        
        # Validate supplier_id
        if supplier_id:
            try:
                supplier_id = int(supplier_id)
            except (ValueError, TypeError):
                flash('Invalid supplier selection', 'danger')
                return redirect(url_for('product_management'))
        
        # Validate warehouse_id
        if warehouse_id:
            try:
                warehouse_id = int(warehouse_id)
            except (ValueError, TypeError):
                flash('Invalid warehouse selection', 'danger')
                return redirect(url_for('product_management'))
        
        update_product(product_id, product_name, description, price, stock_quantity, category_id, supplier_id, warehouse_id)
        flash('Product updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating product: {e}', 'danger')

    return redirect(url_for('product_management'))


@app.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    try:
        delete_product(product_id)
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {e}', 'danger')

    return redirect(url_for('product_management'))


# --- additional product routes ---

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    try:
        product = get_product_by_id(product_id)
        if not product:
            flash('Product not found', 'danger')
            return redirect(url_for('product_management'))
        
        return render_template('product_detail.html', product=product)
    except Exception as e:
        flash(f'Error retrieving product: {e}', 'danger')
        return redirect(url_for('product_management'))


@app.route('/product/stock/update/<int:product_id>', methods=['POST'])
def update_product_stock_route(product_id):
    try:
        new_stock = request.form.get('new_stock')
        
        if not new_stock:
            return jsonify({'success': False, 'message': 'Stock quantity is required'}), 400
        
        try:
            new_stock = int(new_stock)
            if new_stock < 0:
                return jsonify({'success': False, 'message': 'Stock quantity cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Invalid stock quantity format'}), 400
        
        update_product_stock(product_id, new_stock)
        
        if (request.is_json or 
            request.headers.get('Content-Type') == 'application/json' or
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
            return jsonify({'success': True, 'message': 'Stock updated successfully!'})
        else:
            flash('Stock updated successfully!', 'success')
            return redirect(url_for('product_management'))
            
    except Exception as e:
        if (request.is_json or 
            request.headers.get('Content-Type') == 'application/json' or
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash(f'Error updating stock: {e}', 'danger')
            return redirect(url_for('product_management'))


@app.route('/products/low-stock')
def low_stock_products():
    """Get products with low stock"""
    threshold = request.args.get('threshold', 10, type=int)
    try:
        products = get_low_stock_products(threshold)
        return render_template('low_stock_products.html', products=products, threshold=threshold)
    except Exception as e:
        flash(f'Error retrieving low stock products: {e}', 'danger')
        return redirect(url_for('product_management'))


@app.route('/products/by-category/<int:category_id>')
def products_by_category(category_id):
    """Get all products in a specific category"""
    try:
        products = get_products_by_category(category_id)
        category = get_category_by_id(category_id) 
        return render_template('products_by_category.html', products=products, category=category)
    except Exception as e:
        flash(f'Error retrieving products by category: {e}', 'danger')
        return redirect(url_for('product_management'))


@app.route('/products/by-supplier/<int:supplier_id>')
def products_by_supplier(supplier_id):
    """Get all products from a specific supplier"""
    try:
        products = get_products_by_supplier(supplier_id)
        supplier = get_supplier_by_id(supplier_id)  
        return render_template('products_by_supplier.html', products=products, supplier=supplier)
    except Exception as e:
        flash(f'Error retrieving products by supplier: {e}', 'danger')
        return redirect(url_for('product_management'))


@app.route('/products/by-warehouse/<int:warehouse_id>')
def products_by_warehouse(warehouse_id):
    try:
        products = get_products_by_warehouse(warehouse_id)
        warehouse = get_warehouse_by_id(warehouse_id)  
        return render_template('products_by_warehouse.html', products=products, warehouse=warehouse)
    except Exception as e:
        flash(f'Error retrieving products by warehouse: {e}', 'danger')
        return redirect(url_for('product_management'))


@app.route('/api/products/stats')
def product_stats_api():
    """API endpoint for product statistics"""
    try:
        stats = {
            'total_products': get_product_count(),
            'total_value': get_total_product_value(),
            'low_stock_count': len(get_low_stock_products()),
            'categories_count': len(get_all_categories()),
            'suppliers_count': len(get_all_suppliers()),
            'warehouses_count': len(get_all_warehouses())
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/products/search')
def product_search_api():
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify([])
        
        products = search_products(query)
        
        products_data = []
        for product in products:
            if hasattr(product, 'product_id'):
                product_data = {
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'price': float(product.price),
                    'stock_quantity': product.stock_quantity,
                    'category_name': getattr(product, 'category_name', None),
                    'supplier_name': getattr(product, 'supplier_name', None),
                    'warehouse_name': getattr(product, 'warehouse_name', None)
                }
            elif isinstance(product, dict):
                product_data = {
                    'product_id': product.get('product_id'),
                    'product_name': product.get('product_name'),
                    'price': float(product.get('price', 0)),
                    'stock_quantity': product.get('stock_quantity'),
                    'category_name': product.get('category_name'),
                    'supplier_name': product.get('supplier_name'),
                    'warehouse_name': product.get('warehouse_name')
                }
            else:
                continue
                
            products_data.append(product_data)
        
        return jsonify(products_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



#------------------- Manager_orders-------------------------------




@app.route('/Manager_orders')
def Manager_orders():
    """Display manager orders page"""
    query = request.args.get('search', '')
    
    try:
        if query:
            orders = search_manager_orders(query)
        else:
           
            orders = get_manager_orders_with_details()
            if not orders:  
                orders = get_all_manager_orders()
        
        staff_members = get_all_staff_members()
        warehouses = get_all_warehouses()
        products = get_all_products()
        
    
        
        return render_template('Manager_order.html', 
                             orders=orders, 
                             staff_members=staff_members,
                             warehouses=warehouses,
                             products=products,
                             search_query=query)
                             
    except Exception as e:
        print(f'Error loading orders: {str(e)}')
        flash(f'Error loading orders: {str(e)}', 'error')
        return render_template('Manager_order.html', 
                             orders=[], 
                             staff_members=[], 
                             warehouses=[],
                             products=[],
                             search_query=query)

@app.route('/add_manager_order', methods=['POST'])
def add_manager_order():
    """Add new manager order"""
    try:
        staff_id = request.form.get('staff_id')
        warehouse_id = request.form.get('warehouse_id')
        order_type = request.form.get('order_type')
        order_date = request.form.get('order_date')
        delivery_date = request.form.get('delivery_date')
        order_status = request.form.get('order_status')
        
    
        
        # Validate required fields
        if not all([staff_id, warehouse_id, order_type, order_date, delivery_date, order_status]):
            flash('All fields are required!', 'error')
            return redirect(url_for('Manager_orders'))
        
        try:
            staff_id = int(staff_id)
            warehouse_id = int(warehouse_id)
        except ValueError:
            flash('Invalid staff ID or warehouse ID format!', 'error')
            return redirect(url_for('Manager_orders'))
        
        if not validate_staff_exists(staff_id):
            flash(f'Staff member with ID {staff_id} does not exist!', 'error')
            return redirect(url_for('Manager_orders'))
        
        if not validate_warehouse_exists(warehouse_id):
            flash(f'Warehouse with ID {warehouse_id} does not exist!', 'error')
            return redirect(url_for('Manager_orders'))
        
        order_id = add_manager_order_to_db(staff_id, warehouse_id, order_type, order_date, delivery_date, order_status)
        
        if order_id:
            flash(f'Manager order {order_id} added successfully!', 'success')
        else:
            flash('Error: Failed to create manager order!', 'error')
        
    except Exception as e:
        print(f'Error adding manager order: {str(e)}')
        flash(f'Error adding manager order: {str(e)}', 'error')
    
    return redirect(url_for('Manager_orders'))

@app.route('/api/manager_orders/<order_id>')
def get_manager_order_api(order_id):
    """API endpoint to get manager order details for editing"""
    try:
        order = get_manager_order_by_id(order_id)
        if order:
            # Format dates for HTML date input
            if order.get('order_date'):
                if hasattr(order['order_date'], 'strftime'):
                    order['order_date'] = order['order_date'].strftime('%Y-%m-%d')
                elif isinstance(order['order_date'], str):
                    order['order_date'] = order['order_date'].split(' ')[0]
            
            if order.get('delivery_date'):
                if hasattr(order['delivery_date'], 'strftime'):
                    order['delivery_date'] = order['delivery_date'].strftime('%Y-%m-%d')
                elif isinstance(order['delivery_date'], str):
                    order['delivery_date'] = order['delivery_date'].split(' ')[0]
            
            return jsonify(order)
        else:
            return jsonify({'error': 'Order not found'}), 404
            
    except Exception as e:
        print(f"Error fetching manager order {order_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/edit_manager_order/<order_id>', methods=['POST'])
def edit_manager_order(order_id):
    """Edit existing manager order"""
    try:
        # Get form data
        staff_id = request.form.get('staff_id')
        warehouse_id = request.form.get('warehouse_id')
        order_type = request.form.get('order_type')
        order_date = request.form.get('order_date')
        delivery_date = request.form.get('delivery_date')
        order_status = request.form.get('order_status')
        
        # Validate required fields
        if not all([staff_id, warehouse_id, order_type, order_date, delivery_date, order_status]):
            flash('All fields are required!', 'error')
            return redirect(url_for('Manager_orders'))
        
        try:
            staff_id = int(staff_id)
            warehouse_id = int(warehouse_id)
        except ValueError:
            flash('Invalid staff ID or warehouse ID format!', 'error')
            return redirect(url_for('Manager_orders'))
        
        if not validate_staff_exists(staff_id):
            flash(f'Staff member with ID {staff_id} does not exist!', 'error')
            return redirect(url_for('Manager_orders'))
        
        if not validate_warehouse_exists(warehouse_id):
            flash(f'Warehouse with ID {warehouse_id} does not exist!', 'error')
            return redirect(url_for('Manager_orders'))
        
        success = update_manager_order(order_id, staff_id, warehouse_id, order_type, order_date, delivery_date, order_status)
        
        if success:
            flash('Manager order updated successfully!', 'success')
        else:
            flash('Error: Manager order not found or not updated!', 'error')
        
    except Exception as e:
        print(f'Error updating manager order: {str(e)}')
        flash(f'Error updating manager order: {str(e)}', 'error')
    
    return redirect(url_for('Manager_orders'))

@app.route('/delete_manager_order/<order_id>', methods=['POST'])
def delete_manager_order(order_id):
    try:
        # Check if order exists before deletion
        order = get_manager_order_by_id(order_id)
        if not order:
            flash(f'Manager order with ID {order_id} not found!', 'error')
            return redirect(url_for('Manager_orders'))
        
        # Delete order items first
        deleted_items = delete_manager_order_items(order_id)
        print(f"Deleted {deleted_items} order items for order {order_id}")
        
        # Delete the order
        success = delete_manager_order_from_db(order_id)
        
        if success:
            flash('Manager order deleted successfully!', 'success')
        else:
            flash('Error: Failed to delete manager order!', 'error')
            
    except Exception as e:
        print(f'Error deleting manager order: {str(e)}')
        flash(f'Error deleting manager order: {str(e)}', 'error')
    
    return redirect(url_for('Manager_orders'))

# ================ ORDER ITEMS ROUTES ================

@app.route('/api/manager_order_items/<order_id>')
def get_manager_order_items_api(order_id):
    try:
        items = get_manager_order_items(order_id)
        return jsonify(items)
    except Exception as e:
        print(f"Error fetching order items for order {order_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/add_manager_order_item', methods=['POST'])
def add_manager_order_item():
    try:
        order_id = request.form.get('order_id')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        
        if not all([order_id, product_id, quantity]):
            return jsonify({'error': 'All fields are required!'}), 400
        
        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            return jsonify({'error': 'Invalid data format provided!'}), 400
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0!'}), 400
        
        # Validate references exist
        if not validate_manager_order_exists(order_id):
            return jsonify({'error': f'Order with ID {order_id} does not exist!'}), 400
        
        if not validate_product_exists(product_id):
            return jsonify({'error': f'Product with ID {product_id} does not exist!'}), 400
        
        # Check for duplicate items
        if validate_manager_order_item_exists(order_id, product_id):
            return jsonify({'error': 'This product is already in the order!'}), 400
        
        # Add the order item
        success = add_manager_order_item_to_db(order_id, product_id, quantity)
        
        if success:
            return jsonify({'success': 'Order item added successfully!'})
        else:
            return jsonify({'error': 'Failed to add order item!'}), 500
        
    except Exception as e:
        print(f"Error adding order item: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/edit_manager_order_item', methods=['POST'])
def edit_manager_order_item():
    """Edit existing order item"""
    try:
        order_id = request.form.get('order_id')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        
        # Validate required fields
        if not all([order_id,product_id, quantity]):
            return jsonify({'error': 'All fields are required!'}), 400
        
        # Convert and validate data types
        try:
            quantity = int(quantity)
        except ValueError:
            return jsonify({'error': 'Invalid quantity format!'}), 400
        
        # Validate positive quantity
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0!'}), 400
        
        # Update the order item
        success = update_manager_order_item(order_id,product_id, quantity)
        
        if success:
            return jsonify({'success': 'Order item updated successfully!'})
        else:
            return jsonify({'error': 'Order item not found or not updated!'}), 404
        
    except Exception as e:
        print(f"Error updating order item: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_manager_order_item/<order_id>/<int:product_id>', methods=['POST'])
def delete_manager_order_item(order_id, product_id):
    """Delete order item"""
    try:
        # Check if order item exists before deletion
        if not validate_manager_order_item_exists(order_id, product_id):
            return jsonify({'error': 'Order item not found!'}), 404
        
        success = delete_manager_order_item_from_db(order_id, product_id)
        
        if success:
            return jsonify({'success': 'Order item deleted successfully!'})
        else:
            return jsonify({'error': 'Failed to delete order item!'}), 500
            
    except Exception as e:
        print(f"Error deleting order item: {str(e)}")
        return jsonify({'error': str(e)}), 500

#------------- Dashboard--------------------------------

# Dashboard Routes with improved error handling and debugging
@app.route('/overview')
def dashboard():
    """Enhanced dashboard with comprehensive data"""
    from datetime import datetime
    
    try:
        # Get all dashboard data
        stats = get_dashboard_stats()
        best_sellers = get_best_selling_product()
        recent_orders = get_recent_orders()
        stock_alerts = get_stock_alerts()
        branch_performance = get_branch_performance()
        branch_chart_data = get_branch_chart_data()
        payment_methods_data = get_payment_methods_data()
        top_suppliers = get_top_supplier()
        manager_orders = get_manager_orders()
        warehouse_capacity = get_warehouse_capacity()
        
        # Process data for charts
        branch_names = [branch['name'] for branch in branch_chart_data]
        branch_revenues = [branch['revenue'] for branch in branch_chart_data]
        
        payment_labels = [pm['name'] for pm in payment_methods_data]
        payment_counts = [pm['count'] for pm in payment_methods_data]
        
        # Calculate additional metrics
        total_revenue = float(stats['total_revenue']) if stats['total_revenue'] != '0.00' else 0
        avg_order_value = total_revenue / stats['total_orders'] if stats['total_orders'] > 0 else 0
        
        # Get current date and time
        current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        return render_template(
            "dashboard.html",
            stats=stats,
            best_sellers=best_sellers,
            recent_orders=recent_orders,
            stock_alerts=stock_alerts,
            branch_performance=branch_performance,
            branch_chart_data=branch_chart_data,
            payment_methods_data=payment_methods_data,
            top_suppliers=top_suppliers,
            manager_orders=manager_orders,
            warehouse_capacity=warehouse_capacity,
            branch_names=branch_names,
            branch_revenues=branch_revenues,
            payment_labels=payment_labels,
            payment_counts=payment_counts,
            avg_order_value=f"{avg_order_value:.2f}",
            current_time=current_time
        )
    except Exception as e:
        print(f"Error in dashboard route: {e}")
        # Return with empty data if there's an error
        current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        return render_template(
            "dashboard.html",
            stats={'total_revenue': '0.00', 'total_orders': 0, 'total_products': 0, 'total_customers': 0},
            best_sellers=[],
            recent_orders=[],
            stock_alerts=[],
            branch_performance=[],
            branch_chart_data=[],
            payment_methods_data=[],
            category_stats=[],
            top_suppliers=[],
            manager_orders=[],
            warehouse_capacity=[],
            branch_names=[],
            branch_revenues=[],
            payment_labels=[],
            payment_counts=[],
            avg_order_value="0.00",
            current_time=current_time
        )



