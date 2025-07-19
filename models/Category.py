# Category.py
from db import get_db_connection

def add_category(category_name, category_description=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Category (category_name, category_description)
            VALUES (%s, %s)
        """, (category_name, category_description))
    conn.commit()
    conn.close()

def get_all_categories():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Category")
        categories = cursor.fetchall()
    conn.close()
    return categories

def get_category_by_id(category_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Category WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
    conn.close()
    return category

def update_category(category_id, category_name, category_description=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Category 
            SET category_name=%s, category_description=%s
            WHERE category_id=%s
        """, (category_name, category_description, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Category WHERE category_id = %s", (category_id,))
    conn.commit()
    conn.close()

def search_categories(query):
    query = f"%{query}%"
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Category
            WHERE
                CAST(category_id AS CHAR) LIKE %s OR
                category_name LIKE %s OR
                category_description LIKE %s
        """, (query, query, query))
        results = cursor.fetchall()
    conn.close()
    return results