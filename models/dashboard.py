from db import get_db_connection

def execute_query(query, params=None, fetch_one=False, fetch_all=True):
    """Execute database query with better error handling"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            print(f"Executing query: {query[:100]}...")  
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
                print(f"Fetch one result: {result}")  
            elif fetch_all:
                result = cursor.fetchall()
                print(f"Fetch all result count: {len(result) if result else 0}")  # Debug print
            else:
                connection.commit()
                result = cursor.rowcount
        connection.close()
        return result
    except Exception as e:
        print(f"Database error in execute_query: {e}")
        print(f"Query was: {query}")
        return None


def get_dashboard_stats():
    """Get main dashboard statistics - FIXED VERSION"""
    stats = {
        'total_revenue': '0.00',
        'total_orders': 0,
        'total_products': 0,  # Fixed: was total_product
        'total_customers': 0   # Fixed: was total_customer
    }
    
    try:
        # Total Revenue
        revenue_query = """
            SELECT COALESCE(SUM(totalAmount), 0) as total_revenue 
            FROM Customer_Order 
            WHERE status != 'cancelled'
        """
        result = execute_query(revenue_query, fetch_one=True)
        if result and result['total_revenue'] is not None:
            stats['total_revenue'] = f"{float(result['total_revenue']):.2f}"
        
        # Total Orders
        orders_query = "SELECT COUNT(*) as total_orders FROM Customer_Order WHERE status != 'cancelled'"
        result = execute_query(orders_query, fetch_one=True)
        if result and result['total_orders'] is not None:
            stats['total_orders'] = int(result['total_orders'])
        
        # Total Products
        product_query = "SELECT COUNT(*) as total_products FROM Product"
        result = execute_query(product_query, fetch_one=True)
        if result and result['total_products'] is not None:
            stats['total_products'] = int(result['total_products'])
        
        # Total Customers
        customer_query = "SELECT COUNT(*) as total_customers FROM Customer"
        result = execute_query(customer_query, fetch_one=True)
        if result and result['total_customers'] is not None:
            stats['total_customers'] = int(result['total_customers'])
        
        print(f"Dashboard stats: {stats}") 
        return stats
        
    except Exception as e:
        print(f"Error in get_dashboard_stats: {e}")
        return stats


def get_best_selling_product():
    """Get top 5 best selling products with actual categories"""
    try:
        query = """
            SELECT 
                p.product_name as name,
                COALESCE(c.category_name, 'Uncategorized') as category,
                COALESCE(SUM(oi.quantity), 0) as quantity,
                CONCAT('$', FORMAT(COALESCE(SUM(oi.quantity * p.price), 0), 2)) as revenue
            FROM Product p
            LEFT JOIN Category c ON p.category_id = c.category_id
            LEFT JOIN Customer_Order_Item oi ON p.product_id = oi.product_id
            LEFT JOIN Customer_Order co ON oi.order_id = co.order_id
            WHERE co.status != 'cancelled' OR co.status IS NULL
            GROUP BY p.product_id, p.product_name, c.category_name
            ORDER BY COALESCE(SUM(oi.quantity), 0) DESC
            LIMIT 5
        """
        
        result = execute_query(query)
        
        print(f"Best selling products: {result}")  
        return result or []
        
    except Exception as e:
        print(f"Error in get_best_selling_product: {e}")
        return []

def get_stock_alerts():
    """Get products with low stock"""
    try:
        query = """
            SELECT 
                product_name as name,
                stock_quantity as stock,
                CASE 
                    WHEN stock_quantity = 0 THEN 'Out of Stock'
                    WHEN stock_quantity <= 10 THEN 'Critical'
                    WHEN stock_quantity <= 20 THEN 'Low'
                    ELSE 'Warning'
                END as status,
                CASE 
                    WHEN stock_quantity = 0 THEN 'danger'
                    WHEN stock_quantity <= 10 THEN 'danger'
                    WHEN stock_quantity <= 20 THEN 'warning'
                    ELSE 'info'
                END as status_class
            FROM Product
            WHERE stock_quantity <= 50
            ORDER BY stock_quantity ASC
            LIMIT 10
        """
        
        result = execute_query(query) or []
        print(f"Stock alerts: {result}")  # Debug print
        return result
        
    except Exception as e:
        print(f"Error in get_stock_alerts: {e}")
        return []


def get_recent_orders():
    """Get recent customer orders """
    try:
        query = """
            SELECT 
    CONCAT('#', co.order_id) AS id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer,
    DATE(co.order_date) AS date,
    CONCAT('$', FORMAT(COALESCE(co.totalAmount, 0), 2)) AS amount,
    co.status,
    CASE 
        WHEN co.status = 'pending' THEN 'warning'
        WHEN co.status = 'Shipped' THEN 'info'
        WHEN co.status = 'Delivered' THEN 'success'
        WHEN co.status = 'cancelled' THEN 'danger'
        ELSE 'secondary'
    END AS status_class,
    COALESCE(co.payment_method, 'Cash') AS payment
FROM Customer_Order co
LEFT JOIN Customer c ON co.customer_id = c.customer_id
WHERE co.status != 'cancelled'
ORDER BY co.order_date DESC
LIMIT 10;
"""
        
        result = execute_query(query) or []
        return result
        
    except Exception as e:
        print(f"Error in get_recent_orders: {e}")
        return []


def get_branch_performance():
    """Get branch performance data"""
    try:
        query = """
            SELECT 
    b.branch_name AS name,
    COALESCE(SUM(co.totalAmount), 0) AS revenue,
    COUNT(DISTINCT co.order_id) AS orders,
    CASE 
        WHEN SUM(co.totalAmount) >= 1000 THEN 'success'
        WHEN SUM(co.totalAmount) >= 500 THEN 'info'
        WHEN SUM(co.totalAmount) > 0 THEN 'warning'
        ELSE 'secondary'
    END AS color
FROM Branch b
LEFT JOIN Warehouse w ON b.branch_id = w.branch_id
LEFT JOIN Product p ON p.warehouse_id = w.warehouse_id
LEFT JOIN Customer_Order_Item coi ON coi.product_id = p.product_id
LEFT JOIN Customer_Order co ON co.order_id = coi.order_id AND co.status != 'cancelled'
GROUP BY b.branch_id, b.branch_name
ORDER BY b.branch_name;

        """
        
        results = execute_query(query) or []
        
        if results:
            max_revenue = max([r['revenue'] for r in results]) if results else 1
            for result in results:
                result['percentage'] = int((result['revenue'] / max_revenue) * 100) if max_revenue > 0 else 0
                result['revenue'] = f"${result['revenue']:.2f}"
        
        print(f"Branch performance: {results}")  # Debug print
        return results
        
    except Exception as e:
        print(f"Error in get_branch_performance: {e}")
        return []


def get_top_supplier():
    """Get top suppliers"""
    try:
        query = """
 SELECT 
    s.supplier_name AS name,
    COUNT(p.product_id) AS products,
    COALESCE(s.phone, 'N/A') AS contact,
    'Active' AS status,
    'success' AS status_class
FROM Supplier s
LEFT JOIN Product p ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_id, s.supplier_name, s.phone
ORDER BY COUNT(p.product_id) DESC
LIMIT 5;
        """
        
        result = execute_query(query) or []
        print(f"Top suppliers: {result}")  # Debug print
        return result
        
    except Exception as e:
        print(f"Error in get_top_supplier: {e}")
        return []


def get_branch_chart_data():
    try:
        query = """
            SELECT
    b.branch_name AS name,
    COALESCE(SUM(co.totalAmount), 0) AS revenue,
    COUNT(DISTINCT co.order_id) AS orders
FROM Branch b
LEFT JOIN Warehouse w ON w.branch_id = b.branch_id
LEFT JOIN Product p ON p.warehouse_id = w.warehouse_id
LEFT JOIN Customer_Order_Item coi ON coi.product_id = p.product_id
LEFT JOIN Customer_Order co ON co.order_id = coi.order_id AND co.status != 'cancelled'
GROUP BY b.branch_id, b.branch_name
ORDER BY b.branch_name;

        """
        
        result = execute_query(query) or []
        return result
        
    except Exception as e:
        print(f"Error in get_branch_chart_data: {e}")
        return []


def get_payment_methods_data():
    """Get payment methods distribution"""
    try:
        query = """
            SELECT 
                COALESCE(payment_method, 'Cash') as name,
                COUNT(*) as count
            FROM Customer_Order
            WHERE status != 'cancelled'
            GROUP BY payment_method
            ORDER BY count DESC
        """
        
        result = execute_query(query) or []
        
        print(f"Payment methods: {result}")  # Debug print
        return result
        
    except Exception as e:
        print(f"Error in get_payment_methods_data: {e}")
        return [{'name': 'Cash', 'count': 1}]  # Fallback data



# Keep your existing functions for manager orders and warehouse capacity
def get_manager_orders():
    """Get manager orders data"""
    query = """
        SELECT 
            CONCAT('#', mo.order_id) as id,
            CONCAT(s.first_name, ' ', s.last_name) as staff_name,
            w.location as warehouse,
            mo.order_type,
            DATE(mo.order_date) as order_date,
            DATE(mo.delivery_date) as delivery_date,
            mo.order_status as status,
            CASE 
                WHEN mo.order_status = 'Pending' THEN 'warning'
                WHEN mo.order_status = 'Processing' THEN 'info'
                WHEN mo.order_status = 'Delivered' THEN 'success'
                WHEN mo.order_status = 'Cancelled' THEN 'danger'
                ELSE 'secondary'
            END as status_class
        FROM Manager_Order mo
        JOIN Staff s ON mo.staff_id = s.staff_id
        JOIN Warehouse w ON mo.warehouse_id = w.warehouse_id
        ORDER BY mo.order_date DESC
        LIMIT 10
    """
    return execute_query(query) or []

def get_warehouse_capacity():
    """Get warehouse capacity information"""
    query = """
        SELECT 
            w.location as name,
            w.capacity,
            COUNT(p.product_id) as products_stored,
            ROUND((COUNT(p.product_id) / w.capacity) * 100, 2) as utilization_percentage,
            b.branch_name as branch
        FROM Warehouse w
        LEFT JOIN Product p ON w.warehouse_id = p.warehouse_id
        LEFT JOIN Branch b ON w.branch_id = b.branch_id
        GROUP BY w.warehouse_id, w.location, w.capacity, b.branch_name
        ORDER BY utilization_percentage DESC
    """
    return execute_query(query) or []