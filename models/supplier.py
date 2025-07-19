from db import get_db_connection

def add_supplier(supplier_name, phone=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Supplier (supplier_name, phone)
            VALUES (%s, %s)
        """, (supplier_name, phone))
    conn.commit()
    conn.close()

def get_all_suppliers():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Supplier")
        suppliers = cursor.fetchall()
    conn.close()
    return suppliers

def get_supplier_by_id(supplier_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Supplier WHERE supplier_id = %s", (supplier_id,))
        supplier = cursor.fetchone()
    conn.close()
    return supplier

def update_supplier(supplier_id, supplier_name, phone=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Supplier 
            SET supplier_name=%s, phone=%s
            WHERE supplier_id=%s
        """, (supplier_name, phone, supplier_id))
    conn.commit()
    conn.close()

def delete_supplier(supplier_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Supplier WHERE supplier_id = %s", (supplier_id,))
    conn.commit()
    conn.close()

def search_suppliers(query):
    query = f"%{query}%"  # Prepare for LIKE wildcards
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Supplier
            WHERE
                CAST(supplier_id AS CHAR) LIKE %s OR
                supplier_name LIKE %s OR
                phone LIKE %s
        """, (query, query, query))
        results = cursor.fetchall()
    conn.close()
    return results
