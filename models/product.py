from db import get_db_connection

def add_product(product_name, description=None, price=0.0, stock_quantity=0, category_id=None, supplier_id=None, warehouse_id=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Product (product_name, description, price, stock_quantity, category_id, supplier_id, warehouse_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product_name, description, price, stock_quantity, category_id, supplier_id, warehouse_id))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, c.category_name, s.supplier_name, w.location as warehouse_name
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
            LEFT JOIN Warehouse w ON p.warehouse_id = w.warehouse_id
            ORDER BY p.product_id
        """)
        products = cursor.fetchall()
    conn.close()
    return products



def get_all_warehouses():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT w.warehouse_id, w.location, w.capacity, w.branch_id, 
                   COUNT(p.product_id) as product_count
            FROM Warehouse w
            LEFT JOIN Product p ON w.warehouse_id = p.warehouse_id
            GROUP BY w.warehouse_id, w.location, w.capacity, w.branch_id
            ORDER BY w.warehouse_id
        """)
        warehouses = cursor.fetchall()
    conn.close()
    return warehouses

def get_product_by_id(product_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, c.category_name, s.supplier_name, w.warehouse_name
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
            LEFT JOIN Warehouse w ON p.warehouse_id = w.warehouse_id
            WHERE p.product_id = %s
        """, (product_id,))
        product = cursor.fetchone()
    conn.close()
    return product

def update_product(product_id, product_name, description=None, price=0.0, stock_quantity=0, category_id=None, supplier_id=None, warehouse_id=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Product 
            SET product_name=%s, description=%s, price=%s, stock_quantity=%s, 
                category_id=%s, supplier_id=%s, warehouse_id=%s
            WHERE product_id=%s
        """, (product_name, description, price, stock_quantity, category_id, supplier_id, warehouse_id, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Product WHERE product_id = %s", (product_id,))
    conn.commit()
    conn.close()

def search_products(query):
    query = f"%{query}%"  
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, c.category_name, s.supplier_name, w.location
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
            LEFT JOIN Warehouse w ON p.warehouse_id = w.warehouse_id
            WHERE 
                CAST(p.product_id AS CHAR) LIKE %s OR
                p.product_name LIKE %s OR
                p.stock_quantity LIKE %s OR
                p.description LIKE %s OR
                p.price LIKE %s OR
                c.category_name LIKE %s OR
                s.supplier_name LIKE %s OR
                w.location LIKE %s
            ORDER BY p.product_id
        """, (query, query,query,query,query,query, query, query))
        results = cursor.fetchall()
    conn.close()
    return results

def get_products_by_category(category_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, c.category_name, s.supplier_name, w.warehouse_name
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
            LEFT JOIN Warehouse w ON p.warehouse_id = w.warehouse_id
            WHERE p.category_id = %s
            ORDER BY p.product_id
        """, (category_id,))
        products = cursor.fetchall()
    conn.close()
    return products

def get_products_by_supplier(supplier_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, c.category_name, s.supplier_name, w.warehouse_name
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
            LEFT JOIN Warehouse w ON p.warehouse_id = w.warehouse_id
            WHERE p.supplier_id = %s
            ORDER BY p.product_id
        """, (supplier_id,))
        products = cursor.fetchall()
    conn.close()
    return products

def get_products_by_warehouse(warehouse_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, c.category_name, s.supplier_name, w.warehouse_name
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
            LEFT JOIN Warehouse w ON p.warehouse_id = w.warehouse_id
            WHERE p.warehouse_id = %s
            ORDER BY p.product_id
        """, (warehouse_id,))
        products = cursor.fetchall()
    conn.close()
    return products

def get_low_stock_products(threshold=10):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, c.category_name, s.supplier_name, w.warehouse_name
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
            LEFT JOIN Warehouse w ON p.warehouse_id = w.warehouse_id
            WHERE p.stock_quantity < %s
            ORDER BY p.stock_quantity ASC
        """, (threshold,))
        products = cursor.fetchall()
    conn.close()
    return products

def update_product_stock(product_id, new_stock_quantity):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Product 
            SET stock_quantity = %s
            WHERE product_id = %s
        """, (new_stock_quantity, product_id))
    conn.commit()
    conn.close()

def get_product_count():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as count FROM Product")
        result = cursor.fetchone()
    conn.close()
    return result['count'] if result else 0

def get_total_product_value():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT SUM(price * stock_quantity) as total_value FROM Product")
        result = cursor.fetchone()
    conn.close()
    return result['total_value'] if result and result['total_value'] else 0.0