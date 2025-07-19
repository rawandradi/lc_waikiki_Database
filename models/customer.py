from db import get_db_connection

def add_customer(first_name, last_name, email, password, phone, birth_date):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Customer (first_name, last_name, email, password, phone, birth_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, password, phone, birth_date))
    conn.commit()
    conn.close()

def get_all_customers():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Customer")
        customers = cursor.fetchall()
    conn.close()
    return customers

def get_customer_by_id(customer_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
    conn.close()
    return customer

def update_customer(customer_id, first_name, last_name, email, phone, birth_date):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Customer 
            SET first_name=%s, last_name=%s, email=%s, phone=%s, birth_date=%s
            WHERE customer_id=%s
        """, (first_name, last_name, email, phone, birth_date, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Customer WHERE customer_id = %s", (customer_id,))
    conn.commit()
    conn.close()

def search_customers(query):
    query = f"%{query}%"  # Prepare for LIKE wildcards
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Customer
            WHERE
                CAST(customer_id AS CHAR) LIKE %s OR
                first_name LIKE %s OR
                last_name LIKE %s OR
                email LIKE %s OR
                phone LIKE %s
        """, (query, query, query, query, query))
        results = cursor.fetchall()
    conn.close()
    return results

