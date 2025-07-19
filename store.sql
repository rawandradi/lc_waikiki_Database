DROP DATABASE IF EXISTS store;
CREATE DATABASE store;
USE store;



-- Staff
CREATE TABLE Staff (
    staff_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    position VARCHAR(50),
    salary DOUBLE,
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- Manager
CREATE TABLE Manager (
    manager_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    since DATE,
    password VARCHAR(255),
    FOREIGN KEY (manager_id) REFERENCES Staff(staff_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Branch
CREATE TABLE Branch (
    branch_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    branch_name VARCHAR(100),
    location VARCHAR(100),
    manager_id INT,
    contact_number VARCHAR(20),
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id) ON DELETE SET NULL ON UPDATE CASCADE
);


-- Worker
CREATE TABLE Worker (
    worker_id INT PRIMARY KEY,
    birth_date DATE,
    branch_id INT,
    FOREIGN KEY (worker_id) REFERENCES Staff(staff_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Warehouse
CREATE TABLE Warehouse (
    warehouse_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    location VARCHAR(100),
    capacity INT,
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Supplier
CREATE TABLE Supplier (
    supplier_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    supplier_name VARCHAR(100),
    phone VARCHAR(20)
);

-- Category
CREATE TABLE Category (
    category_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100),
    category_description VARCHAR(255)
);

-- Product
CREATE TABLE Product (
    product_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(100),
    description TEXT,
    price FLOAT,
    stock_quantity INT,
    category_id INT,
    supplier_id INT,
    warehouse_id INT,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id) ON DELETE SET NULL ON UPDATE CASCADE
);

DROP TABLE IF EXISTS manager_order;

-- Manager_Order
CREATE TABLE Manager_Order (
    order_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    staff_id INT,
    warehouse_id INT,
    order_type VARCHAR(50),
    order_date DATE,
    delivery_date DATE,
    order_status VARCHAR(50),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id) ON DELETE SET NULL ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Manager_Order_Item;

-- Manager_Order_Item
CREATE TABLE Manager_Order_Item (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Manager_Order(order_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Customer
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255),
    phone VARCHAR(20),
    birth_date DATE
);

-- Address
CREATE TABLE Address (
    address_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    customer_id INT,
    address_type VARCHAR(50),
    city VARCHAR(100),
    street_address VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Customer_Order
CREATE TABLE Customer_Order (
    order_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    customer_id INT,
    address_id INT,
    order_date DATE,
    status VARCHAR(50),
    totalAmount INT,
    payment_method VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (address_id) REFERENCES Address(address_id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Customer_Order_Item
CREATE TABLE Customer_Order_Item (
    order_item_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Customer_Order(order_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE ON UPDATE CASCADE
);
SHOW TABLES;
-- Clear existing data (keeping the structure)
DELETE FROM Customer_Order_Item;
DELETE FROM Customer_Order;
DELETE FROM Manager_Order_Item;
DELETE FROM Manager_Order;
DELETE FROM Address;
DELETE FROM Customer;
DELETE FROM Product;
DELETE FROM Category;
DELETE FROM Supplier;
DELETE FROM Worker;
DELETE FROM Manager;
DELETE FROM Warehouse;
DELETE FROM Staff;
DELETE FROM Branch;

-- Reset AUTO_INCREMENT
ALTER TABLE Branch AUTO_INCREMENT = 1;
ALTER TABLE Staff AUTO_INCREMENT = 1;
ALTER TABLE Manager AUTO_INCREMENT = 1;
ALTER TABLE Warehouse AUTO_INCREMENT = 1;
ALTER TABLE Supplier AUTO_INCREMENT = 1;
ALTER TABLE Category AUTO_INCREMENT = 1;
ALTER TABLE Product AUTO_INCREMENT = 1;
ALTER TABLE Manager_Order AUTO_INCREMENT = 1;
ALTER TABLE Customer AUTO_INCREMENT = 1;
ALTER TABLE Address AUTO_INCREMENT = 1;
ALTER TABLE Customer_Order AUTO_INCREMENT = 1;
ALTER TABLE Customer_Order_Item AUTO_INCREMENT = 1;

-- Insert Branches
INSERT INTO Branch (branch_name, location, manager_id, contact_number) VALUES
('Central Store', 'Ramallah Downtown', NULL, '0599123456'),
('North Outlet', 'Nablus Market', NULL, '0599988776'),
('West Branch', 'Bethlehem Center', NULL, '0599445577'),
('East Store', 'Jenin Plaza', NULL, '0599332244'),
('South Branch', 'Hebron Mall', NULL, '0599667788');

-- Insert Staff
INSERT INTO Staff (first_name, last_name, position, salary, email, phone) VALUES
('Ali', 'Khalil', 'Manager', 5000, 'ali.khalil@example.com', '0599001122'),
('Sara', 'Odeh', 'Manager', 4800, 'sara.odeh@example.com', '0599112233'),
('Hani', 'Qasem', 'Manager', 4900, 'hani.qasem@example.com', '0599223344'),
('Layla', 'Ahmad', 'Cashier', 2500, 'layla.ahmad@example.com', '0599334455'),
('Omar', 'Hassan', 'Stock Keeper', 3000, 'omar.hassan@example.com', '0599445566'),
('Fatima', 'Mansour', 'Sales Assistant', 2800, 'fatima.mansour@example.com', '0599556677'),
('Khalil', 'Nasser', 'Stock Keeper', 3200, 'khalil.nasser@example.com', '0599667788'),
('Nour', 'Salim', 'Cashier', 2600, 'nour.salim@example.com', '0599778899'),
('Samer', 'Khoury', 'Sales Assistant', 2900, 'samer.khoury@example.com', '0599889900'),
('Rania', 'Yousef', 'Stock Keeper', 3100, 'rania.yousef@example.com', '0599990011');

-- Insert Managers
INSERT INTO Manager (manager_id, since) VALUES
(1, '2022-01-10'),
(2, '2022-03-15'),
(3, '2022-05-20');

-- Update branches with managers
UPDATE Branch SET manager_id = 1 WHERE branch_id = 1;
UPDATE Branch SET manager_id = 2 WHERE branch_id = 2;
UPDATE Branch SET manager_id = 3 WHERE branch_id = 3;

-- Insert Workers
INSERT INTO Worker (worker_id, birth_date, branch_id) VALUES
(4, '1995-05-20', 1),
(5, '1990-11-15', 1),
(6, '1993-08-12', 2),
(7, '1992-02-28', 2),
(8, '1994-07-05', 3),
(9, '1991-12-18', 3),
(10, '1996-04-22', 4);

-- Insert Warehouses
INSERT INTO Warehouse (location, capacity, branch_id) VALUES
('Warehouse A - Ramallah', 1000, 1),
('Warehouse B - Nablus', 800, 2),
('Warehouse C - Bethlehem', 600, 3),
('Warehouse D - Jenin', 500, 4),
('Warehouse E - Hebron', 700, 5);

-- Insert Suppliers
INSERT INTO Supplier (supplier_name, phone) VALUES
('Global Textiles Ltd', '0599445566'),
('Comfort Wear Co', '0599332211'),
('Fashion Forward Inc', '0599778899'),
('Style Masters', '0599665544'),
('Trendy Threads', '0599887766'),
('Urban Fashion', '0599112244'),
('Classic Clothing', '0599998877');

-- Insert Categories
INSERT INTO Category (category_name, category_description) VALUES
('T-Shirts', 'Various types of T-shirts for all ages'),
('Jeans', 'All sizes and styles of jeans'),
('Shirts', 'Formal and casual shirts'),
('Dresses', 'Women dresses for all occasions'),
('Jackets', 'Winter and casual jackets'),
('Shoes', 'Footwear for men and women'),
('Accessories', 'Bags, belts, and other accessories'),
('Sportswear', 'Athletic and sports clothing');

-- Insert Products
INSERT INTO Product (product_name, description, price, stock_quantity, category_id, supplier_id, warehouse_id) VALUES
-- T-Shirts
('Basic White T-Shirt', '100% cotton, unisex', 29.99, 150, 1, 1, 1),
('Black V-Neck Tee', 'Soft cotton blend', 34.99, 120, 1, 1, 1),
('Graphic Print Tee', 'Cool designs available', 39.99, 80, 1, 2, 2),
('Long Sleeve Tee', 'Perfect for cooler days', 44.99, 60, 1, 2, 2),

-- Jeans
('Slim Fit Jeans', 'Dark blue denim jeans', 59.99, 100, 2, 2, 2),
('Relaxed Fit Jeans', 'Comfortable loose fit', 54.99, 85, 2, 3, 3),
('Skinny Jeans', 'Trendy tight fit', 64.99, 75, 2, 3, 3),
('Straight Cut Jeans', 'Classic style', 49.99, 90, 2, 4, 4),

-- Shirts
('White Dress Shirt', 'Formal cotton shirt', 69.99, 40, 3, 4, 1),
('Casual Plaid Shirt', 'Comfortable everyday wear', 45.99, 55, 3, 5, 2),
('Business Shirt', 'Professional look', 74.99, 35, 3, 5, 3),

-- Dresses
('Summer Dress', 'Light and breezy', 79.99, 25, 4, 6, 1),
('Evening Dress', 'Elegant for special occasions', 129.99, 15, 4, 6, 2),
('Casual Day Dress', 'Perfect for daily wear', 59.99, 30, 4, 7, 3),

-- Jackets
('Denim Jacket', 'Classic blue denim', 89.99, 45, 5, 3, 4),
('Winter Coat', 'Warm and stylish', 149.99, 20, 5, 4, 5),
('Bomber Jacket', 'Trendy casual jacket', 99.99, 35, 5, 5, 1),

-- Shoes
('Running Shoes', 'Comfortable athletic shoes', 119.99, 60, 6, 1, 2),
('Casual Sneakers', 'Everyday footwear', 79.99, 70, 6, 2, 3),
('Dress Shoes', 'Formal leather shoes', 139.99, 25, 6, 3, 4),

-- Accessories
('Leather Belt', 'Genuine leather belt', 39.99, 100, 7, 7, 5),
('Canvas Backpack', 'Durable school/work bag', 49.99, 40, 7, 6, 1),
('Baseball Cap', 'Adjustable sports cap', 24.99, 80, 7, 1, 2),

-- Sportswear
('Yoga Pants', 'Flexible workout pants', 54.99, 65, 8, 2, 3),
('Sports Bra', 'Supportive athletic wear', 34.99, 50, 8, 3, 4),
('Athletic Shorts', 'Breathable gym shorts', 29.99, 85, 8, 4, 5);

-- Insert Manager Orders
INSERT INTO Manager_Order (staff_id, warehouse_id, order_type, order_date, delivery_date, order_status) VALUES
(1, 1, 'Restock', '2025-05-15', '2025-05-20', 'Delivered'),
(2, 2, 'New Products', '2025-05-20', '2025-05-25', 'Delivered'),
(3, 3, 'Restock', '2025-05-25', '2025-05-30', 'Processing'),
(1, 4, 'Emergency Stock', '2025-06-01', '2025-06-05', 'Delivered'),
(2, 5, 'Seasonal Items', '2025-06-05', '2025-06-10', 'Pending');

-- Insert Manager Order Items
INSERT INTO Manager_Order_Item (order_id, product_id, quantity) VALUES
(1, 1, 50), (1, 2, 30), (1, 5, 25),
(2, 3, 40), (2, 6, 35), (2, 9, 20),
(3, 10, 15), (3, 11, 25), (3, 12, 10),
(4, 16, 30), (4, 17, 20), (4, 18, 15),
(5, 19, 25), (5, 20, 20), (5, 22, 30);

-- Insert Customers
INSERT INTO Customer (first_name, last_name, email, password, phone, birth_date) VALUES
('Leen', 'Ammar', 'leen.ammar@example.com', 'hashedpassword1', '0599887766', '2000-03-22'),
('Omar', 'Suleiman', 'omar.s@example.com', 'hashedpassword2', '0599776655', '1998-07-12'),
('Nadia', 'Khalil', 'nadia.khalil@example.com', 'hashedpassword3', '0599665544', '1995-09-18'),
('Tariq', 'Mansour', 'tariq.mansour@example.com', 'hashedpassword4', '0599554433', '1992-11-25'),
('Laila', 'Ahmad', 'laila.ahmad@example.com', 'hashedpassword5', '0599443322', '1988-05-14'),
('Samir', 'Odeh', 'samir.odeh@example.com', 'hashedpassword6', '0599332211', '1990-12-08'),
('Reem', 'Hassan', 'reem.hassan@example.com', 'hashedpassword7', '0599221100', '1993-04-30'),
('Fadi', 'Nasser', 'fadi.nasser@example.com', 'hashedpassword8', '0599110099', '1985-08-17'),
('Dina', 'Salim', 'dina.salim@example.com', 'hashedpassword9', '0599009988', '1996-01-11'),
('Marwan', 'Khoury', 'marwan.khoury@example.com', 'hashedpassword10', '0599998877', '1991-06-23'),
('Yasmin', 'Yousef', 'yasmin.yousef@example.com', 'hashedpassword11', '0599887755', '1994-10-05'),
('Karim', 'Qasem', 'karim.qasem@example.com', 'hashedpassword12', '0599776644', '1987-02-28');

-- Insert Addresses
INSERT INTO Address (customer_id, address_type, city, street_address) VALUES
(1, 'Home', 'Ramallah', 'Al-Masyoun St. 12'),
(1, 'Work', 'Ramallah', 'Downtown Office Complex'),
(2, 'Home', 'Nablus', 'Main Market Road 5'),
(3, 'Home', 'Bethlehem', 'Manger Square Area'),
(4, 'Home', 'Jenin', 'Freedom Street 18'),
(5, 'Home', 'Hebron', 'Old City Quarter'),
(6, 'Home', 'Ramallah', 'Al-Bireh District'),
(7, 'Home', 'Nablus', 'University Street'),
(8, 'Home', 'Bethlehem', 'Star Street 25'),
(9, 'Home', 'Jenin', 'Market Plaza'),
(10, 'Home', 'Hebron', 'Commercial Center'),
(11, 'Home', 'Ramallah', 'City Center'),
(12, 'Work', 'Nablus', 'Business District');

-- Insert Customer Orders (spread across different dates and statuses)
INSERT INTO Customer_Order (customer_id, address_id, order_date, status, totalAmount, payment_method) VALUES
-- Recent orders (last 2 weeks)
(1, 1, '2025-06-08', 'Shipped', 89, 'Credit Card'),
(2, 3, '2025-06-07', 'Delivered', 159, 'Cash on Delivery'),
(3, 4, '2025-06-06', 'Delivered', 234, 'Credit Card'),
(4, 5, '2025-06-05', 'Shipped', 119, 'PayPal'),
(5, 6, '2025-06-04', 'Delivered', 78, 'Credit Card'),
(6, 7, '2025-06-03', 'Delivered', 145, 'Cash on Delivery'),
(7, 8, '2025-06-02', 'Shipped', 199, 'Credit Card'),
(8, 9, '2025-06-01', 'Delivered', 89, 'PayPal'),
(9, 10, '2025-05-31', 'Delivered', 167, 'Credit Card'),
(10, 11, '2025-05-30', 'Delivered', 134, 'Cash on Delivery'),

-- Older orders (last month)
(11, 12, '2025-05-29', 'Delivered', 245, 'Credit Card'),
(12, 13, '2025-05-28', 'Delivered', 178, 'PayPal'),
(1, 2, '2025-05-27', 'Delivered', 156, 'Credit Card'),
(2, 3, '2025-05-26', 'Delivered', 89, 'Cash on Delivery'),
(3, 4, '2025-05-25', 'Delivered', 267, 'Credit Card'),
(4, 5, '2025-05-24', 'Delivered', 198, 'PayPal'),
(5, 6, '2025-05-23', 'Delivered', 145, 'Credit Card'),
(6, 7, '2025-05-22', 'Delivered', 223, 'Cash on Delivery'),
(7, 8, '2025-05-21', 'Delivered', 134, 'Credit Card'),
(8, 9, '2025-05-20', 'Delivered', 289, 'PayPal'),

-- Even older orders
(9, 10, '2025-05-15', 'Delivered', 167, 'Credit Card'),
(10, 11, '2025-05-10', 'Delivered', 198, 'Cash on Delivery'),
(11, 12, '2025-05-05', 'Delivered', 234, 'Credit Card'),
(12, 13, '2025-04-30', 'Delivered', 156, 'PayPal'),
(1, 1, '2025-04-25', 'Delivered', 189, 'Credit Card');

-- Insert Customer Order Items
INSERT INTO Customer_Order_Item (order_id, product_id, quantity) VALUES
-- Order 1: T-shirts and jeans
(1, 1, 2), (1, 5, 1),
-- Order 2: Dress and shoes
(2, 12, 1), (2, 17, 1),
-- Order 3: Multiple items
(3, 3, 1), (3, 6, 1), (3, 9, 1), (3, 19, 1),
-- Order 4: Shoes and accessories
(4, 16, 1), (4, 19, 1),
-- Order 5: T-shirts
(5, 2, 1), (5, 4, 1),
-- Order 6: Jeans and shirt
(6, 7, 1), (6, 10, 1),
-- Order 7: Dress and jacket
(7, 13, 1), (7, 14, 1),
-- Order 8: T-shirts and accessories
(8, 1, 2), (8, 21, 1),
-- Order 9: Shoes and sportswear
(9, 18, 1), (9, 22, 1), (9, 23, 1),
-- Order 10: Multiple clothing items
(10, 8, 1), (10, 11, 1), (10, 20, 1),

-- Continue with more order items for remaining orders
(11, 14, 1), (11, 15, 1), (11, 16, 1),
(12, 5, 2), (12, 17, 1),
(13, 9, 1), (13, 12, 1), (13, 19, 1),
(14, 1, 1), (14, 6, 1),
(15, 13, 1), (15, 18, 1), (15, 21, 1),
(16, 3, 2), (16, 22, 1), 
(17, 7, 1), (17, 10, 1), (17, 20, 1),
(18, 2, 1), (18, 8, 1), (18, 23, 2),
(19, 11, 1), (19, 15, 1),
(20, 4, 1), (20, 14, 1), (20, 17, 1), (20, 19, 1),

(21, 6, 1), (21, 12, 1), (21, 16, 1),
(22, 1, 3), (22, 18, 1),
(23, 9, 1), (23, 13, 1), (23, 22, 1), (23, 21, 1),
(24, 5, 1), (24, 20, 1),
(25, 3, 1), (25, 7, 1), (25, 11, 1), (25, 15, 1);

-- Add some cancelled orders for testing
INSERT INTO Customer_Order (customer_id, address_id, order_date, status, totalAmount, payment_method) VALUES
(3, 4, '2025-06-06', 'cancelled', 89, 'Credit Card'),
(7, 8, '2025-06-02', 'cancelled', 156, 'PayPal');

INSERT INTO Customer_Order_Item (order_id, product_id, quantity) VALUES
(26, 1, 2), (26, 5, 1),
(27, 9, 1), (27, 16, 1);

-- Display summary
SELECT 'Data Summary' as Info;
SELECT COUNT(*) as Total_Branches FROM Branch;
SELECT COUNT(*) as Total_Staff FROM Staff;
SELECT COUNT(*) as Total_Products FROM Product;
SELECT COUNT(*) as Total_Customers FROM Customer;
SELECT COUNT(*) as Total_Orders FROM Customer_Order;
SELECT COUNT(*) as Orders_Delivered FROM Customer_Order WHERE status = 'Delivered';
SELECT COUNT(*) as Orders_Shipped FROM Customer_Order WHERE status = 'Shipped';
SELECT COUNT(*) as Orders_Cancelled FROM Customer_Order WHERE status = 'cancelled';
SELECT SUM(totalAmount) as Total_Revenue FROM Customer_Order WHERE status != 'cancelled';

select * from staff;
select * from manager;
select * from branch;