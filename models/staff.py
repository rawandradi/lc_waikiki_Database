# Staff Database Functions using MySQL - Fixed Version
from db import get_db_connection  # Import your database connection function

# --- General Staff Functions ---

def get_all_staff():
    """Get all staff from the database - returns consistent dictionary format"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()  # Force dictionary cursor
        query = """
        SELECT 
            s.staff_id, s.first_name, s.last_name, s.position, s.salary, 
            s.email, s.phone,
            CASE 
                WHEN w.worker_id IS NOT NULL THEN 'worker'
                WHEN m.manager_id IS NOT NULL THEN 'manager'
                ELSE 'staff'
            END as staff_type,
            w.birth_date,
            w.branch_id,
            m.since,
            b.branch_name
        FROM staff s
        LEFT JOIN worker w ON s.staff_id = w.worker_id
        LEFT JOIN manager m ON s.staff_id = m.manager_id
        LEFT JOIN branch b ON w.branch_id = b.branch_id
        ORDER BY s.staff_id
        """
        
        cursor.execute(query)
        staff_list = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return staff_list
    except Exception as e:
        print(f"Error in get_all_staff: {e}")
        if conn:
            conn.close()
        return []

def get_workers():
    """Get all workers - returns consistent dictionary format"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            s.staff_id, s.first_name, s.last_name, s.position, s.salary, 
            s.email, s.phone, w.branch_id, w.birth_date, 'worker' as staff_type,
            b.branch_name
        FROM staff s
        INNER JOIN worker w ON s.staff_id = w.worker_id
        LEFT JOIN branch b ON w.branch_id = b.branch_id
        ORDER BY s.staff_id
        """
        
        cursor.execute(query)
        workers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return workers
    except Exception as e:
        print(f"Error getting workers: {e}")
        if conn:
            conn.close()
        return []

def get_managers():
    """Get all managers - returns consistent dictionary format"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            s.staff_id, s.first_name, s.last_name, s.position, s.salary, 
            s.email, s.phone, m.since, 'manager' as staff_type,
            NULL as branch_id, NULL as birth_date, NULL as branch_name
        FROM staff s
        INNER JOIN manager m ON s.staff_id = m.manager_id
        ORDER BY s.staff_id
        """
        
        cursor.execute(query)
        managers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return managers
    except Exception as e:
        print(f"Error getting managers: {e}")
        if conn:
            conn.close()
        return []

def search_all_staff(search_query):
    """Search all staff members by name, position, or email"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        search_term = f"%{search_query}%"
        
        query = """
        SELECT 
            s.staff_id, s.first_name, s.last_name, s.position, s.salary, 
            s.email, s.phone,
            CASE 
                WHEN w.worker_id IS NOT NULL THEN 'worker'
                WHEN m.manager_id IS NOT NULL THEN 'manager'
                ELSE 'staff'
            END as staff_type,
            w.birth_date,
            w.branch_id,
            m.since,
            b.branch_name
        FROM staff s
        LEFT JOIN worker w ON s.staff_id = w.worker_id
        LEFT JOIN manager m ON s.staff_id = m.manager_id
        LEFT JOIN branch b ON w.branch_id = b.branch_id
        WHERE 
            s.first_name LIKE %s OR 
            s.last_name LIKE %s OR 
            CONCAT(s.first_name, ' ', s.last_name) LIKE %s OR
            s.position LIKE %s OR 
            s.email LIKE %s
        ORDER BY s.staff_id
        """
        
        params = (search_term, search_term, search_term, search_term, search_term)
        
        cursor.execute(query, params)
        staff_list = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return staff_list
    except Exception as e:
        print(f"Error searching all staff: {e}")
        if conn:
            conn.close()
        return []

def search_staff_by_type(staff_type, search_query):
    """Search staff members by type (worker or manager) and search query"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        search_term = f"%{search_query}%"
        
        if staff_type == 'worker':
            query = """
            SELECT 
                s.staff_id, s.first_name, s.last_name, s.position, s.salary, 
                s.email, s.phone, w.branch_id, w.birth_date, 'worker' as staff_type,
                b.branch_name
            FROM staff s
            INNER JOIN worker w ON s.staff_id = w.worker_id
            LEFT JOIN branch b ON w.branch_id = b.branch_id
            WHERE 
                s.first_name LIKE %s OR 
                s.last_name LIKE %s OR 
                CONCAT(s.first_name, ' ', s.last_name) LIKE %s OR
                s.position LIKE %s OR 
                s.email LIKE %s
            ORDER BY s.staff_id
            """
        elif staff_type == 'manager':
            query = """
            SELECT 
                s.staff_id, s.first_name, s.last_name, s.position, s.salary, 
                s.email, s.phone, m.since, 'manager' as staff_type,
                NULL as branch_id, NULL as birth_date, NULL as branch_name
            FROM staff s
            INNER JOIN manager m ON s.staff_id = m.manager_id
            WHERE 
                s.first_name LIKE %s OR 
                s.last_name LIKE %s OR 
                CONCAT(s.first_name, ' ', s.last_name) LIKE %s OR
                s.position LIKE %s OR 
                s.email LIKE %s
            ORDER BY s.staff_id
            """
        else:
            return []
        
        params = (search_term, search_term, search_term, search_term, search_term)
        
        cursor.execute(query, params)
        staff_list = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return staff_list
    except Exception as e:
        print(f"Error searching staff by type: {e}")
        if conn:
            conn.close()
        return []

def get_staff_by_id(staff_id):
    """Get a specific staff member by ID - returns dictionary"""
    conn = None
    cursor = None
    
    try:
        print(f"Looking for staff with ID: {staff_id}")
        
        conn = get_db_connection()
        if not conn:
            print("Failed to get database connection")
            return None
            
        cursor = conn.cursor()
        
        # Convert staff_id to int if it's a string
        try:
            staff_id = int(staff_id)
        except (ValueError, TypeError):
            print(f"Invalid staff_id format: {staff_id}")
            return None
        
        # Get staff with type information
        query = """
        SELECT 
            s.staff_id, s.first_name, s.last_name, s.position, s.salary,
            s.email, s.phone,
            CASE 
                WHEN w.worker_id IS NOT NULL THEN 'worker'
                WHEN m.manager_id IS NOT NULL THEN 'manager'
                ELSE 'staff'
            END as staff_type,
            w.birth_date,
            w.branch_id,
            m.since,
            b.branch_name
        FROM staff s
        LEFT JOIN worker w ON s.staff_id = w.worker_id
        LEFT JOIN manager m ON s.staff_id = m.manager_id
        LEFT JOIN branch b ON w.branch_id = b.branch_id
        WHERE s.staff_id = %s
        """
        
        cursor.execute(query, (staff_id,))
        staff_member = cursor.fetchone()
        
        return staff_member
        
    except Exception as e:
        print(f"Exception in get_staff_by_id: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# --- Worker-specific Functions ---

def add_worker(first_name, last_name, position, salary, email, phone, branch_id, birth_date):
    """Add a new worker"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Start transaction
        conn.autocommit = False
        
        # First, insert into Staff table
        staff_query = """
        INSERT INTO staff (first_name, last_name, position, salary, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        staff_params = (first_name, last_name, position, salary, email, phone)
        cursor.execute(staff_query, staff_params)
        
        # Get the staff_id that was just inserted
        staff_id = cursor.lastrowid
        
        # Then, insert into Worker table
        worker_query = """
        INSERT INTO worker (worker_id, birth_date, branch_id)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(worker_query, (staff_id, birth_date, branch_id))
        conn.commit()
        
        return staff_id
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error adding worker: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_worker(staff_id, first_name, last_name, position, salary, email, phone, branch_id, birth_date):
    """Update an existing worker"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Start transaction
        conn.autocommit = False
        
        # Validate inputs
        if not all([first_name, last_name, position, email, phone]):
            raise ValueError("All required fields must be provided")
        
        if salary <= 0:
            raise ValueError("Salary must be positive")
        
        # Update Staff table
        staff_query = """
        UPDATE staff
        SET first_name = %s, last_name = %s, position = %s, salary = %s, 
            email = %s, phone = %s
        WHERE staff_id = %s
        """
        staff_params = (first_name, last_name, position, salary, email, phone, staff_id)
        cursor.execute(staff_query, staff_params)
        
        # Update Worker table
        worker_query = """
        UPDATE worker
        SET birth_date = %s, branch_id = %s
        WHERE worker_id = %s
        """
        cursor.execute(worker_query, (birth_date, branch_id, staff_id))
        
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error updating worker: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_worker(staff_id):
    """Delete a worker"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Start transaction
        conn.autocommit = False
        
        # Delete from Worker table first (due to foreign key constraint)
        worker_query = "DELETE FROM worker WHERE worker_id = %s"
        cursor.execute(worker_query, (staff_id,))
        
        # Then delete from Staff table
        staff_query = "DELETE FROM staff WHERE staff_id = %s"
        cursor.execute(staff_query, (staff_id,))
        
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error deleting worker: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# --- Manager-specific Functions ---

def add_manager(first_name, last_name, position, salary, email, phone, since, password_hash):
    """Add a new manager with password"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Start transaction
        conn.autocommit = False
        
        # First, insert into Staff table
        staff_query = """
        INSERT INTO staff (first_name, last_name, position, salary, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        staff_params = (first_name, last_name, position, salary, email, phone)
        cursor.execute(staff_query, staff_params)
        
        # Get the staff_id that was just inserted
        staff_id = cursor.lastrowid
        
        # Then, insert into Manager table with password
        manager_query = """
        INSERT INTO manager (manager_id, since, password)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(manager_query, (staff_id, since, password_hash))
        conn.commit()
        
        return staff_id
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error adding manager: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_manager(staff_id, first_name, last_name, position, salary, email, phone, since, password_hash=None):
    """Update an existing manager (optionally update password)"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Start transaction
        conn.autocommit = False
        
        # Update Staff table
        staff_query = """
        UPDATE staff
        SET first_name = %s, last_name = %s, position = %s, salary = %s, 
            email = %s, phone = %s
        WHERE staff_id = %s
        """
        
        staff_params = (first_name, last_name, position, salary, email, phone, staff_id)
        cursor.execute(staff_query, staff_params)
        
        # Update Manager table
        if password_hash:
            # Update with new password
            manager_query = """
            UPDATE manager
            SET since = %s, password = %s
            WHERE manager_id = %s
            """
            cursor.execute(manager_query, (since, password_hash, staff_id))
        else:
            # Update without changing password
            manager_query = """
            UPDATE manager
            SET since = %s
            WHERE manager_id = %s
            """
            cursor.execute(manager_query, (since, staff_id))
        
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error updating manager: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_manager(staff_id):
    """Delete a manager"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Start transaction
        conn.autocommit = False
        
        # Delete from Manager table first
        manager_query = "DELETE FROM manager WHERE manager_id = %s"
        cursor.execute(manager_query, (staff_id,))
        
        # Then delete from Staff table
        staff_query = "DELETE FROM staff WHERE staff_id = %s"
        cursor.execute(staff_query, (staff_id,))
        
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error deleting manager: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_manager_by_email(email):
    """Get manager details by email for authentication"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT s.staff_id, s.first_name, s.last_name, s.position, s.salary,
               s.email, s.phone, m.since, m.password, m.manager_id,
               'manager' as staff_type
        FROM staff s
        INNER JOIN manager m ON s.staff_id = m.manager_id
        WHERE s.email = %s
        """
        
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        
        return result
        
    except Exception as e:
        print(f"Error getting manager by email: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_manager_password(manager_id, password_hash):
    """Update manager password only"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        UPDATE manager
        SET password = %s
        WHERE manager_id = %s
        """
        
        cursor.execute(query, (password_hash, manager_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise ValueError("Manager not found or password not updated")
        
        return True
        
    except Exception as e:
        print(f"Error updating manager password: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_managers():
    """Get all managers"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT s.staff_id, s.first_name, s.last_name, s.position, s.salary,
               s.email, s.phone, m.since, m.manager_id,
               'manager' as staff_type
        FROM staff s
        INNER JOIN manager m ON s.staff_id = m.manager_id
        ORDER BY s.last_name, s.first_name
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        return results
        
    except Exception as e:
        print(f"Error getting managers: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# --- Branch Functions ---

def get_all_branches():
    """Get all branches from the database - returns consistent format"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Try both possible table names
        try:
            cursor.execute("SELECT branch_id, branch_name FROM branch ORDER BY branch_id")
        except:
            # If 'branch' doesn't exist, try 'Branch' (uppercase)
            cursor.execute("SELECT branch_id, branch_name FROM Branch ORDER BY branch_id")
        
        branches = cursor.fetchall()
        return branches
        
    except Exception as e:
        print(f"Error getting branches: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_branch_by_id(branch_id):
    """Get a specific branch by ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Try both possible table names
        try:
            cursor.execute("SELECT branch_id, branch_name FROM branch WHERE branch_id = %s", (branch_id,))
        except:
            cursor.execute("SELECT branch_id, branch_name FROM Branch WHERE branch_id = %s", (branch_id,))
        
        branch = cursor.fetchone()
        return branch
        
    except Exception as e:
        print(f"Error getting branch by ID: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_workers_by_branch(branch_id):
    """Get all workers in a specific branch"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            s.staff_id, s.first_name, s.last_name, s.position, s.salary, 
            s.email, s.phone, w.branch_id, w.birth_date, 'worker' as staff_type,
            b.branch_name
        FROM staff s
        INNER JOIN worker w ON s.staff_id = w.worker_id
        LEFT JOIN branch b ON w.branch_id = b.branch_id
        WHERE w.branch_id = %s
        ORDER BY s.staff_id
        """
        
        cursor.execute(query, (branch_id,))
        workers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return workers
    except Exception as e:
        print(f"Error getting workers by branch: {e}")
        if conn:
            conn.close()
        return []

# --- Utility Functions ---

def is_worker(staff_id):
    """Check if a staff member is a worker"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM worker WHERE worker_id = %s"
        cursor.execute(query, (staff_id,))
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        return count > 0
    except Exception as e:
        print(f"Error checking if worker: {e}")
        return False

def is_manager(staff_id):
    """Check if a staff member is a manager"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM manager WHERE manager_id = %s"
        cursor.execute(query, (staff_id,))
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        return count > 0
    except Exception as e:
        print(f"Error checking if manager: {e}")
        return False