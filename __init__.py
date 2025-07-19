from flask import Flask
from flask_login import LoginManager, UserMixin
from config import Config
import pymysql

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

class User(UserMixin):
    def __init__(self, user_id, user_type):
        self.id = f"{user_type}_{user_id}"
        self.user_type = user_type
        self.user_id = user_id

def get_db_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

@login_manager.user_loader
def load_user(user_id):
    user_type, user_id = user_id.split('_')
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if user_type == 'customer':
                cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(user_data['customer_id'], 'customer')
            elif user_type == 'manager':
                cursor.execute('SELECT * FROM manager WHERE manager_id = %s', (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(user_data['manager_id'], 'manager')
    finally:
        conn.close()
    return None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize login manager
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app