from db import get_db_connection

def add_address(customer_id, address_type, city, street_address):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Address (customer_id, address_type, city, street_address)
            VALUES (%s, %s, %s, %s)
        """, (customer_id, address_type, city, street_address))
    conn.commit()
    conn.close()

def get_all_addresses():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Address")
        addresses = cursor.fetchall()
    conn.close()
    return addresses

def get_address_by_id(address_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Address WHERE address_id = %s", (address_id,))
        address = cursor.fetchone()
    conn.close()
    return address

def update_address(address_id, address_type, city, street_address):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Address 
            SET address_type=%s, city=%s, street_address=%s
            WHERE address_id=%s
        """, (address_type, city, street_address, address_id))
    conn.commit()
    conn.close()

def delete_address(address_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Address WHERE address_id = %s", (address_id,))
        cursor.execute("ALTER TABLE Address AUTO_INCREMENT = 1;")
    conn.commit()
    conn.close()



# Add this function to your address.py file

def get_addresses_by_customer(customer_id):
    """Get all addresses for a specific customer"""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT address_id, customer_id, address_type, city, street_address 
            FROM Address 
            WHERE customer_id = %s 
            ORDER BY address_type
        """, (customer_id,))
        addresses = cursor.fetchall()
    conn.close()
    return addresses