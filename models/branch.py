from db import get_db_connection

def add_branch(branch_name, location, manager_id=None, contact_number=None):
    """Add a new branch to the database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Branch (branch_name, location, manager_id, contact_number)
                VALUES (%s, %s, %s, %s)
            """, (branch_name, location, manager_id, contact_number))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_branches():
    """Get all branches from the database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Branch ORDER BY branch_id")
            branches = cursor.fetchall()
        return branches
    finally:
        conn.close()

def get_branch_by_id(branch_id):
    """Get a specific branch by ID"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Branch WHERE branch_id = %s", (branch_id,))
            branch = cursor.fetchone()
        return branch
    finally:
        conn.close()

def update_branch(branch_id, branch_name, location, manager_id=None, contact_number=None):
    """Update an existing branch"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Branch 
                SET branch_name=%s, location=%s, manager_id=%s, contact_number=%s
                WHERE branch_id=%s
            """, (branch_name, location, manager_id, contact_number, branch_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_branch(branch_id):
    """Delete a branch from the database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # First delete associated warehouses
            cursor.execute("DELETE FROM Warehouse WHERE branch_id = %s", (branch_id,))
            # Then delete the branch
            cursor.execute("DELETE FROM Branch WHERE branch_id = %s", (branch_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def search_branches(search_query):
    """Search branches by name or location"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Branch 
                WHERE branch_name LIKE %s OR location LIKE %s
                ORDER BY branch_id
            """, (f"%{search_query}%", f"%{search_query}%"))
            branches = cursor.fetchall()
        return branches
    finally:
        conn.close()

# Warehouse management functions for the branch
def add_warehouse(branch_id, location, capacity):
    """Add a new warehouse to a branch"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Warehouse (branch_id, location, capacity)
                VALUES (%s, %s, %s)
            """, (branch_id, location, capacity))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_warehouses_by_branch(branch_id):
    """Get all warehouses for a specific branch"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Warehouse 
                WHERE branch_id = %s 
                ORDER BY warehouse_id
            """, (branch_id,))
            warehouses = cursor.fetchall()
        return warehouses
    finally:
        conn.close()

def get_warehouse_by_id(warehouse_id):
    """Get a specific warehouse by ID"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Warehouse WHERE warehouse_id = %s", (warehouse_id,))
            warehouse = cursor.fetchone()
        return warehouse
    finally:
        conn.close()

def update_warehouse(warehouse_id, location, capacity):
    """Update an existing warehouse"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Warehouse 
                SET location=%s, capacity=%s
                WHERE warehouse_id=%s
            """, (location, capacity, warehouse_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_warehouse(warehouse_id):
    """Delete a warehouse from the database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Warehouse WHERE warehouse_id = %s", (warehouse_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_branch_count():
    """Get total number of branches"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM Branch")
            result = cursor.fetchone()
        return result['count'] if result else 0
    finally:
        conn.close()

def get_warehouse_count_by_branch(branch_id):
    """Get total number of warehouses for a specific branch"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM Warehouse WHERE branch_id = %s", (branch_id,))
            result = cursor.fetchone()
        return result['count'] if result else 0
    finally:
        conn.close()

def branch_exists(branch_id):
    """Check if a branch exists"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM Branch WHERE branch_id = %s", (branch_id,))
            result = cursor.fetchone()
        return result is not None
    finally:
        conn.close()

def get_branch_with_warehouse_count():
    """Get all branches with their warehouse count"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT b.*, 
                       COALESCE(w.warehouse_count, 0) as warehouse_count
                FROM Branch b
                LEFT JOIN (
                    SELECT branch_id, COUNT(*) as warehouse_count
                    FROM Warehouse
                    GROUP BY branch_id
                ) w ON b.branch_id = w.branch_id
                ORDER BY b.branch_id
            """)
            branches = cursor.fetchall()
        return branches
    finally:
        conn.close()


def get_warehouses_by_branch_id(branch_id):
    """Get all warehouses for a specific branch"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT warehouse_id, location, capacity FROM Warehouse WHERE branch_id = %s", (branch_id,))
            warehouses = cursor.fetchall()
        return warehouses
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


def get_available_managers():
    """Get list of all managers that can be assigned to branches"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Adjust the SQL query based on your actual managers table structure
        cursor.execute("""
            SELECT manager_id, first_name, last_name, email 
            FROM manager m join staff s on s.staff_id = m.manager_id
            ORDER BY first_name, last_name
        """)
        
        managers = cursor.fetchall()
        conn.close()
        return managers
        
    except Exception as e:
        print(f"Error fetching managers: {e}")
        return []