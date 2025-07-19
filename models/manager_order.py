from db import get_db_connection
import pymysql
import uuid

# ================ MANAGER ORDER FUNCTIONS ================

def add_manager_order_to_db(staff_id, warehouse_id, order_type, order_date, delivery_date, order_status):
    """Add new manager order and return the generated order_id"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            
            cursor.execute("""
                INSERT INTO Manager_Order (staff_id, warehouse_id, order_type, order_date, delivery_date, order_status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (staff_id, warehouse_id, order_type, order_date, delivery_date, order_status))
            conn.commit()
            return 1
    finally:
        conn.close()

def get_manager_order_by_id(order_id):
    """Get manager order by ID"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM Manager_Order WHERE order_id = %s", (order_id,))
            return cursor.fetchone()
    finally:
        conn.close()

def update_manager_order(order_id, staff_id, warehouse_id, order_type, order_date, delivery_date, order_status):
    """Update existing manager order"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Manager_Order
                SET staff_id = %s, warehouse_id = %s, order_type = %s,
                    order_date = %s, delivery_date = %s, order_status = %s
                WHERE order_id = %s
            """, (staff_id, warehouse_id, order_type, order_date, delivery_date, order_status, order_id))
            conn.commit()
            return cursor.rowcount > 0  # Return True if update was successful
    finally:
        conn.close()

def delete_manager_order_from_db(order_id):
    """Delete manager order"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Manager_Order WHERE order_id = %s", (order_id,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()

# ================ QUERY FUNCTIONS ================

def get_manager_orders_with_details():
    """Get all orders with staff and warehouse details"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT mo.*, s.first_name, s.last_name, w.location AS warehouse_location
                FROM Manager_Order mo
                LEFT JOIN Staff s ON mo.staff_id = s.staff_id
                LEFT JOIN Warehouse w ON mo.warehouse_id = w.warehouse_id
                ORDER BY mo.order_date DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error in get_manager_orders_with_details: {e}")
        return []
    finally:
        conn.close()

def get_all_manager_orders():
    """Get all manager orders (fallback function)"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM Manager_Order ORDER BY order_date DESC")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error in get_all_manager_orders: {e}")
        return []
    finally:
        conn.close()

def search_manager_orders(query):
    """Search orders by various fields"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT mo.*, s.first_name, s.last_name, w.location AS warehouse_location
                FROM Manager_Order mo
                LEFT JOIN Staff s ON mo.staff_id = s.staff_id
                LEFT JOIN Warehouse w ON mo.warehouse_id = w.warehouse_id
                WHERE s.first_name LIKE %s OR s.last_name LIKE %s
                   OR mo.order_status LIKE %s OR mo.order_type LIKE %s
                   OR mo.order_id LIKE %s
                ORDER BY mo.order_date DESC
            """
            like_query = f"%{query}%"
            cursor.execute(sql, (like_query, like_query, like_query, like_query, like_query))
            return cursor.fetchall()
    except Exception as e:
        print(f"Error in search_manager_orders: {e}")
        return []
    finally:
        conn.close()

# ================ ORDER ITEM FUNCTIONS ================

def get_manager_order_items(order_id):
    """Get all items for a specific order"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT moi.*, p.product_name
                FROM Manager_Order_Item moi
                LEFT JOIN Product p ON moi.product_id = p.product_id
                WHERE moi.order_id = %s
            """, (order_id,))
            return cursor.fetchall()
    except Exception as e:
        print(f"Error in get_manager_order_items: {e}")
        return []
    finally:
        conn.close()

def add_manager_order_item_to_db(order_id, product_id, quantity):
    """Add new order item"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Generate composite key
            
            
            cursor.execute("""
                INSERT INTO Manager_Order_Item (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, ( order_id, product_id, quantity))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error adding order item: {e}")
        return False
    finally:
        conn.close()

def update_manager_order_item(order_id, product_id, quantity):
    """Update the quantity of a specific product in a manager's order"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Manager_Order_Item 
                SET quantity = %s
                WHERE order_id = %s AND product_id = %s
            """, (quantity, order_id, product_id))
            conn.commit()
            return cursor.rowcount > 0  # Returns True if any row was updated
    finally:
        conn.close()

def delete_manager_order_item_from_db(order_id, product_id):
    """Delete specific order item"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Manager_Order_Item
                WHERE order_id = %s AND product_id = %s
            """, (order_id, product_id))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()

def delete_manager_order_items(order_id):
    """Delete all items for an order"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Manager_Order_Item WHERE order_id = %s", (order_id,))
            conn.commit()
            return cursor.rowcount
    finally:
        conn.close()

# ================ HELPER FUNCTIONS ================

def get_all_staff_members():
    """Get all staff members for dropdown"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT staff_id, first_name, last_name FROM Staff ORDER BY first_name")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error getting staff members: {e}")
        return []
    finally:
        conn.close()

def get_all_warehouses():
    """Get all warehouses for dropdown"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT warehouse_id, location FROM Warehouse ORDER BY location")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error getting warehouses: {e}")
        return []
    finally:
        conn.close()

def get_all_products_from_manager():
    """Get all products for dropdown"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT product_id, product_name FROM Product ORDER BY product_name")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error getting products: {e}")
        return []
    finally:
        conn.close()

# ================ VALIDATION FUNCTIONS ================

def _record_exists(table, field, value):
    """Generic function to check if record exists"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM {table} WHERE {field} = %s LIMIT 1", (value,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

def validate_staff_exists(staff_id):
    """Check if staff member exists"""
    return _record_exists("Staff", "staff_id", staff_id)

def validate_warehouse_exists(warehouse_id):
    """Check if warehouse exists"""
    return _record_exists("Warehouse", "warehouse_id", warehouse_id)

def validate_product_exists(product_id):
    """Check if product exists"""
    return _record_exists("Product", "product_id", product_id)

def validate_manager_order_exists(order_id):
    """Check if manager order exists"""
    return _record_exists("Manager_Order", "order_id", order_id)

def validate_manager_order_item_exists(order_id, product_id):
    """Check if order item exists"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM Manager_Order_Item
                WHERE order_id = %s AND product_id = %s LIMIT 1
            """, (order_id, product_id))
            return cursor.fetchone() is not None
    finally:
        conn.close()