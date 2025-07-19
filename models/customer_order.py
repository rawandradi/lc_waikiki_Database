# ------------------- Order Functions ----------------
from db import get_db_connection


def add_order(customer_id, address_id, order_date, status, totalAmount, payment_method):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Customer_Order (customer_id, address_id, order_date, status, totalAmount, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (customer_id, address_id, order_date, status, totalAmount, payment_method))
    conn.commit()
    conn.close()


def get_all_orders():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Customer_Order")
        orders = cursor.fetchall()
    conn.close()
    return orders


def get_order_by_id(order_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Customer_Order WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
    conn.close()
    return order


def update_order(order_id, customer_id, address_id, order_date, status, totalAmount, payment_method):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Customer_Order
            SET customer_id=%s, address_id=%s, order_date=%s, status=%s, totalAmount=%s, payment_method=%s
            WHERE order_id=%s
        """, (customer_id, address_id, order_date, status, totalAmount, payment_method, order_id))
    conn.commit()
    conn.close()


def delete_order(order_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Customer_Order WHERE order_id = %s", (order_id,))
    conn.commit()
    conn.close()


def search_orders(query):
    query = f"%{query}%"
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Customer_Order
            WHERE
                CAST(order_id AS CHAR) LIKE %s OR
                CAST(customer_id AS CHAR) LIKE %s OR
                CAST(address_id AS CHAR) LIKE %s OR
                status LIKE %s OR
                CAST(totalAmount AS CHAR) LIKE %s OR
                payment_method LIKE %s
        """, (query, query, query, query, query, query))
        results = cursor.fetchall()
    conn.close()
    return results



import db

def get_orders_with_details():
    """Get all orders with customer and address information"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    co.order_id,
                    co.customer_id,
                    co.address_id,
                    co.order_date,
                    co.status,
                    co.totalAmount,
                    co.payment_method,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    c.email as customer_email,
                    c.phone as customer_phone,
                    CONCAT(a.street_address, ', ', a.city) as address_display,
                    a.city,
                    a.street_address,
                    a.address_type
                FROM customer_order co
                LEFT JOIN customer c ON co.customer_id = c.customer_id
                LEFT JOIN Address a ON co.address_id = a.address_id
                ORDER BY co.order_date DESC
            """)
            orders = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        order_list = []
        for order in orders:
            order_list.append({
                'order_id': order[0],
                'customer_id': order[1],
                'address_id': order[2],
                'order_date': order[3],
                'status': order[4],
                'totalAmount': order[5],
                'payment_method': order[6],
                'customer_name': order[7] or 'Unknown Customer',
                'customer_email': order[8] or '',
                'customer_phone': order[9] or '',
                'address_display': order[10] or 'No Address',
                'city': order[11] or '',
                'street_address': order[12] or '',
                'address_type': order[13] or ''
            })
        
        return order_list
    except Exception as e:
        print(f"Error fetching orders with details: {str(e)}")
        return []

def get_customer_orders(customer_id):
    """Get all orders for a specific customer"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    co.order_id,
                    co.customer_id,
                    co.address_id,
                    co.order_date,
                    co.status,
                    co.totalAmount,
                    co.payment_method,
                    CONCAT(a.street_address, ', ', a.city) as address_display
                FROM customer_order co
                LEFT JOIN Address a ON co.address_id = a.address_id
                WHERE co.customer_id = %s
                ORDER BY co.order_date DESC
            """, (customer_id,))
            orders = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        order_list = []
        for order in orders:
            order_list.append({
                'order_id': order[0],
                'customer_id': order[1],
                'address_id': order[2],
                'order_date': order[3],
                'status': order[4],
                'totalAmount': order[5],
                'payment_method': order[6],
                'address_display': order[7] or 'No Address'
            })
        
        return order_list
    except Exception as e:
        print(f"Error fetching customer orders: {str(e)}")
        return []

def validate_customer_exists(customer_id):
    """Check if a customer exists"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT customer_id FROM customer WHERE customer_id = %s", (customer_id,))
            result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error validating customer: {str(e)}")
        return False

def validate_address_exists(address_id, customer_id=None):
    """Check if an address exists and optionally belongs to a specific customer"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            if customer_id:
                cursor.execute("""
                    SELECT address_id FROM Address 
                    WHERE address_id = %s AND customer_id = %s
                """, (address_id, customer_id))
            else:
                cursor.execute("SELECT address_id FROM Address WHERE address_id = %s", (address_id,))
            result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error validating address: {str(e)}")
        return False

def get_order_statistics():
    """Get order statistics for dashboard"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            # Total orders
            cursor.execute("SELECT COUNT(*) FROM customer_order")
            total_orders = cursor.fetchone()[0]
            
            # Total revenue
            cursor.execute("SELECT SUM(totalAmount) FROM customer_order")
            total_revenue = cursor.fetchone()[0] or 0
            
            # Orders by status
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM customer_order 
                GROUP BY status
            """)
            status_counts = cursor.fetchall()
            
            # Recent orders (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM customer_order 
                WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            """)
            recent_orders = cursor.fetchone()[0]
            
            # Average order value
            cursor.execute("SELECT AVG(totalAmount) FROM customer_order")
            avg_order_value = cursor.fetchone()[0] or 0
            
        conn.close()
        
        return {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'status_counts': dict(status_counts),
            'recent_orders': recent_orders,
            'avg_order_value': float(avg_order_value)
        }
    except Exception as e:
        print(f"Error fetching order statistics: {str(e)}")
        return {}

def search_orders_enhanced(query):
    """Enhanced search function for orders"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    co.order_id,
                    co.customer_id,
                    co.address_id,
                    co.order_date,
                    co.status,
                    co.totalAmount,
                    co.payment_method,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    c.email as customer_email,
                    CONCAT(a.street_address, ', ', a.city) as address_display
                FROM customer_order co
                LEFT JOIN customer c ON co.customer_id = c.customer_id
                LEFT JOIN Address a ON co.address_id = a.address_id
                WHERE 
                    co.order_id LIKE %s OR
                    CONCAT(c.first_name, ' ', c.last_name) LIKE %s OR
                    c.email LIKE %s OR
                    co.status LIKE %s OR
                    co.payment_method LIKE %s OR
                    a.city LIKE %s OR
                    a.street_address LIKE %s
                ORDER BY co.order_date DESC
            """, (f'%{query}%', f'%{query}%', f'%{query}%', 
                  f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
            orders = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        order_list = []
        for order in orders:
            order_list.append({
                'order_id': order[0],
                'customer_id': order[1],
                'address_id': order[2],
                'order_date': order[3],
                'status': order[4],
                'totalAmount': order[5],
                'payment_method': order[6],
                'customer_name': order[7] or 'Unknown Customer',
                'customer_email': order[8] or '',
                'address_display': order[9] or 'No Address'
            })
        
        return order_list
    except Exception as e:
        print(f"Error searching orders: {str(e)}")
        return []

def get_orders_by_date_range(start_date, end_date):
    """Get orders within a specific date range"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    co.order_id,
                    co.customer_id,
                    co.address_id,
                    co.order_date,
                    co.status,
                    co.totalAmount,
                    co.payment_method,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name
                FROM customer_order co
                LEFT JOIN customer c ON co.customer_id = c.customer_id
                WHERE co.order_date BETWEEN %s AND %s
                ORDER BY co.order_date DESC
            """, (start_date, end_date))
            orders = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        order_list = []
        for order in orders:
            order_list.append({
                'order_id': order[0],
                'customer_id': order[1],
                'address_id': order[2],
                'order_date': order[3],
                'status': order[4],
                'totalAmount': order[5],
                'payment_method': order[6],
                'customer_name': order[7] or 'Unknown Customer'
            })
        
        return order_list
    except Exception as e:
        print(f"Error fetching orders by date range: {str(e)}")
        return []

def get_orders_by_status(status):
    """Get all orders with a specific status"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    co.order_id,
                    co.customer_id,
                    co.address_id,
                    co.order_date,
                    co.status,
                    co.totalAmount,
                    co.payment_method,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name
                FROM customer_order co
                LEFT JOIN customer c ON co.customer_id = c.customer_id
                WHERE co.status = %s
                ORDER BY co.order_date DESC
            """, (status,))
            orders = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        order_list = []
        for order in orders:
            order_list.append({
                'order_id': order[0],
                'customer_id': order[1],
                'address_id': order[2],
                'order_date': order[3],
                'status': order[4],
                'totalAmount': order[5],
                'payment_method': order[6],
                'customer_name': order[7] or 'Unknown Customer'
            })
        
        return order_list
    except Exception as e:
        print(f"Error fetching orders by status: {str(e)}")
        return []

def update_order_status(order_id, new_status):
    """Update only the status of an order"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE customer_order 
                SET status = %s 
                WHERE order_id = %s
            """, (new_status, order_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating order status: {str(e)}")
        return False

# ===============================
# ORDER ITEMS ROUTES AND FUNCTIONS
# ===============================

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import json
from db import get_db_connection

# ------------------- Order Items Database Functions ----------------


def get_Customer_Order_Items(order_id):
    """Get all order items for a specific order"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    oi.Order_Item_id,
                    oi.order_id,
                    oi.product_id,
                    oi.quantity,
                    p.product_name as product_name,
                    p.price as product_price,
                    (oi.quantity * p.price) as subtotal
                FROM Customer_Order_Item oi
                LEFT JOIN Product p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
                ORDER BY oi.Order_Item_id
            """, (order_id,))
            items = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        item_list = []
        for item in items:
            item_list.append({
                'Order_Item_id': item[0],
                'order_id': item[1],
                'product_id': item[2],
                'quantity': item[3],
                'product_name': item[4] or 'Unknown Product',
                'product_price': float(item[5]) if item[5] else 0.0,
                'subtotal': float(item[6]) if item[6] else 0.0
            })
        
        return item_list
    except Exception as e:
        print(f"Error fetching order items: {str(e)}")
        return []

def get_Customer_Order_Item_by_id(Order_Item_id):
    """Get specific order item by ID"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    oi.Order_Item_id,
                    oi.order_id,
                    oi.product_id,
                    oi.quantity,
                    p.product_name as product_name,
                    p.price as product_price
                FROM Customer_Order_Item oi
                LEFT JOIN Product p ON oi.product_id = p.product_id
                WHERE oi.Order_Item_id = %s
            """, (Order_Item_id,))
            item = cursor.fetchone()
        conn.close()
        
        if item:
            return {
                'Order_Item_id': item[0],
                'order_id': item[1],
                'product_id': item[2],
                'quantity': item[3],
                'product_name': item[4] or 'Unknown Product',
                'product_price': float(item[5]) if item[5] else 0.0
            }
        return None
    except Exception as e:
        print(f"Error fetching order item: {str(e)}")
        return None

def add_Customer_Order_Item(order_id, product_id, quantity):
    """Add a new order item"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Customer_Order_Item (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (order_id, product_id, quantity))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding order item: {str(e)}")
        return False

def update_Customer_Order_Item(Order_Item_id, product_id, quantity):
    """Update an existing order item"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Customer_Order_Item 
                SET product_id = %s, quantity = %s
                WHERE Order_Item_id = %s
            """, (product_id, quantity, Order_Item_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating order item: {str(e)}")
        return False

def delete_Customer_Order_Item(Order_Item_id):
    """Delete an order item"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Customer_Order_Item WHERE Order_Item_id = %s", (Order_Item_id,))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting order item: {str(e)}")
        return False

def validate_product_exists(product_id):
    """Check if product exists"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT product_id FROM Product WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error validating product: {str(e)}")
        return False

def check_product_stock(product_id, required_quantity):
    """Check if product has sufficient stock"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT stock_quantity FROM Product WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
        conn.close()
        
        if result and result[0] >= required_quantity:
            return True
        return False
    except Exception as e:
        print(f"Error checking product stock: {str(e)}")
        return False

def get_product_name(product_id):
    """Get product name by ID"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM Product WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'Unknown Product'
    except Exception as e:
        print(f"Error getting product name: {str(e)}")
        return 'Unknown Product'

def add_order_with_items(customer_id, address_id, order_date, status, total_amount, payment_method, Customer_Order_Items):
    """Add order with items in a transaction"""
    try:
        conn = get_db_connection()
        conn.begin()
        
        with conn.cursor() as cursor:
            # Insert order
            cursor.execute("""
                INSERT INTO Customer_Order (customer_id, address_id, order_date, status, totalAmount, payment_method)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (customer_id, address_id, order_date, status, total_amount, payment_method))
            
            order_id = cursor.lastrowid
            
            for item in Customer_Order_Items:
                cursor.execute("""
                    INSERT INTO Customer_Order_Item (order_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                """, (order_id, item['product_id'], item['quantity']))
                
                # Update product stock
                cursor.execute("""
                    UPDATE Product 
                    SET stock_quantity = stock_quantity - %s
                    WHERE product_id = %s
                """, (item['quantity'], item['product_id']))
        
        conn.commit()
        conn.close()
        return order_id
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error adding order with items: {str(e)}")
        return None

def update_order_total(order_id):
    """Update order total based on order items"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Customer_Order 
                SET totalAmount = (
                    SELECT SUM(oi.quantity * p.price)
                    FROM Customer_Order_Item oi
                    JOIN Product p ON oi.product_id = p.product_id
                    WHERE oi.order_id = %s
                )
                WHERE order_id = %s
            """, (order_id, order_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating order total: {str(e)}")
        return False
    


def get_Customer_Order_Items_with_products(order_id):
    """Retrieve all order items for a given order along with product details"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    oi.Order_Item_id,
                    oi.product_id,
                    p.product_name AS product_name,
                    p.price AS product_price,
                    oi.quantity,
                    (oi.quantity * p.price) AS total_price
                FROM Customer_Order_Item oi
                JOIN Product p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
            """, (order_id,))
            
            result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(f"Error retrieving order items with product details: {str(e)}")
        return []

def get_order_item_by_id(order_item_id):
    """Retrieve a specific order item by ID with product details"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    coi.order_item_id,
                    coi.order_id,
                    coi.product_id,
                    p.product_name AS product_name,
                    p.price AS product_price,
                    coi.quantity,
                    (coi.quantity * p.price) AS total_price
                FROM Customer_Order_Item coi
                JOIN Product p ON coi.product_id = p.product_id
                WHERE coi.order_item_id = %s
            """, (order_item_id,))
            
            result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Error retrieving order item by ID: {str(e)}")
        return None
def validate_order_exists(order_id):
    """Check if an order with the given ID exists"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT order_id FROM Customer_Order WHERE order_id = %s", (order_id,))
            result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error validating order existence: {str(e)}")
        return False
    

def add_order_item(order_id, product_id, quantity):
    """Add a new order item"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Customer_Order_Item (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (order_id, product_id, quantity))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding order item: {str(e)}")
        return False
    
def get_orders_with_details():
    """Get orders with customer and address details (enhanced version)"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    o.order_id,
                    o.customer_id,
                    o.address_id,
                    o.order_date,
                    o.status,
                    o.totalAmount,
                    o.payment_method,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    c.email as customer_email,
                    a.street_address,
                    a.city
                FROM customer_Order o
                LEFT JOIN Customer c ON o.customer_id = c.customer_id
                LEFT JOIN Address a ON o.address_id = a.address_id
                ORDER BY o.order_date DESC
            """)
            
            orders = []
            for row in cursor.fetchall():
                order_dict = dict(row)
                orders.append(order_dict)
        
        conn.close()
        return orders
    except Exception as e:
        print(f"Error getting orders with details: {str(e)}")
        # Fallback to basic orders
        return get_all_orders()

def search_orders(query):
    """Search orders by various criteria"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT 
                    o.order_id,
                    o.customer_id,
                    o.address_id,
                    o.order_date,
                    o.status,
                    o.totalAmount,
                    o.payment_method,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    c.email as customer_email
                FROM customer_order o
                LEFT JOIN Customer c ON o.customer_id = c.customer_id
                WHERE 
                    o.order_id LIKE %s OR
                    o.status LIKE %s OR
                    o.payment_method LIKE %s OR
                    CONCAT(c.first_name, ' ', c.last_name) LIKE %s OR
                    c.email LIKE %s
                ORDER BY o.order_date DESC
            """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
            
            columns = [desc[0] for desc in cursor.description]
            orders = []
            for row in cursor.fetchall():
                order_dict = dict(row)
                orders.append(order_dict)
        
        conn.close()
        return orders
    except Exception as e:
        print(f"Error searching orders: {str(e)}")
        return []
def validate_customer_exists(customer_id):
    """Check if customer exists"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT customer_id FROM Customer WHERE customer_id = %s", (customer_id,))
            result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error validating customer: {str(e)}")
        return False

def validate_address_exists(address_id, customer_id=None):
    """Check if address exists and optionally belongs to customer"""
    try:
        conn = db.get_db_connection()
        with conn.cursor() as cursor:
            if customer_id:
                cursor.execute("SELECT address_id FROM Address WHERE address_id = %s AND customer_id = %s", 
                             (address_id, customer_id))
            else:
                cursor.execute("SELECT address_id FROM Address WHERE address_id = %s", (address_id,))
            result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error validating address: {str(e)}")
        return False

def update_order_item(order_item_id, product_id, quantity):
    """Update an existing order item"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Customer_Order_Item 
                SET product_id = %s, quantity = %s
                WHERE order_item_id = %s
            """, (product_id, quantity, order_item_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating order item: {str(e)}")
        return False
def delete_order_item(order_item_id):
    """Delete an order item"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Customer_Order_Item WHERE order_item_id = %s", (order_item_id,))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting order item: {str(e)}")
        return False

