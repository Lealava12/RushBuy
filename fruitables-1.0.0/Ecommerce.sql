Create Database Ecommerce;
-- Users Table
use Ecommerce;
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mobile_no VARCHAR(15) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_blocked BOOLEAN DEFAULT FALSE
);

SHOW COLUMNS FROM Users LIKE 'confirm_password';
SELECT * 
FROM information_schema.KEY_COLUMN_USAGE 
WHERE TABLE_NAME = 'Users' 
AND COLUMN_NAME = 'confirm_password';
SELECT * 
FROM information_schema.CHECK_CONSTRAINTS 
WHERE CONSTRAINT_NAME LIKE '%confirm_password%'; 
SELECT DATABASE();
SHOW COLUMNS FROM Users;

describe Users;
ALTER TABLE Users DROP COLUMN confirm_password;
DROP TABLE Users;
ALTER TABLE Users 
ADD COLUMN mobile_no VARCHAR(15) NOT NULL AFTER email,
ADD COLUMN confirm_password VARCHAR(255) NOT NULL AFTER password_hash;

-- Categories Table
CREATE TABLE Categories (
    category_id VARCHAR(10) PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
);

-- SubCategories Table
CREATE TABLE SubCategories (
    subcategory_id varchar(10) PRIMARY KEY AUTO_INCREMENT,
    category_id varchar(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);
describe SubCategories; 
-- Products Table
CREATE TABLE Products (
    product_id varchar(10) PRIMARY KEY AUTO_INCREMENT,
    subcategory_id varchar(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0.00,
    stock_quantity INT NOT NULL,
    weight DECIMAL(10,2) , -- For Product Weight
	dimensions VARCHAR(50) , -- For Product Dimensions (LxWxH)
	specifications TEXT, -- For Product Specifications
	tags VARCHAR(255), -- For Product Tags
	status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (subcategory_id) REFERENCES SubCategories(subcategory_id)
);

-- Product Images Table
CREATE TABLE ProductImages (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id varchar(10) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Carts Table
CREATE TABLE Carts (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Cart Items Table
CREATE TABLE CartItems (
    cart_item_id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES Carts(cart_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Orders Table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('Pending', 'Shipped', 'Delivered', 'Canceled') DEFAULT 'Pending',
    delivery_address TEXT NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    delivery_time_preference VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Order Items Table
CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Payments Table
CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    status ENUM('Pending', 'Completed', 'Failed') DEFAULT 'Pending',
    payment_date DATETIME,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Inquiries Table
CREATE TABLE Inquiries (
    inquiry_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('Open', 'Closed') DEFAULT 'Open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Staff Roles Table
CREATE TABLE Roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    permissions TEXT
);

-- Staff Table
CREATE TABLE Staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

-- Replies Table
CREATE TABLE Replies (
    reply_id INT PRIMARY KEY AUTO_INCREMENT,
    inquiry_id INT NOT NULL,
    staff_id INT NOT NULL,
    message TEXT NOT NULL,
    replied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inquiry_id) REFERENCES Inquiries(inquiry_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- Delivery Partners Table
CREATE TABLE DeliveryPartners (
    partner_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    operational_area VARCHAR(100),
    availability_status BOOLEAN DEFAULT TRUE
);

-- Order Delivery Table
CREATE TABLE OrderDelivery (
    delivery_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    partner_id INT NOT NULL,
    assigned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_status ENUM('Assigned', 'In Transit', 'Delivered') DEFAULT 'Assigned',
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (partner_id) REFERENCES DeliveryPartners(partner_id)
);

-- Low Stock Alerts Table
CREATE TABLE LowStockAlerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    alert_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Indexes
CREATE INDEX idx_products_subcategory ON Products(subcategory_id);
CREATE INDEX idx_orders_user ON Orders(user_id);
CREATE INDEX idx_payments_order ON Payments(order_id);
CREATE INDEX idx_inquiries_user ON Inquiries(user_id);
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO admin (email, password, created_at)
VALUES ('admin@gmail.com', '123456', NOW());

ALTER TABLE Categories
ADD COLUMN status ENUM('active', 'inactive') NOT NULL DEFAULT 'active';

ALTER TABLE SubCategories
ADD COLUMN priority_order INT DEFAULT 1, -- For Sub-Category Priority/Order
ADD COLUMN status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'; -- For Sub-Category Status

ALTER TABLE Products
-- Add the discount_percentage column after price
ADD COLUMN discount_percentage DECIMAL(5,2) DEFAULT 0.00 AFTER price,

-- Remove the low_stock_threshold column
DROP COLUMN low_stock_threshold,

-- Add additional columns for weight, dimensions, specifications, tags, and status
ADD COLUMN weight DECIMAL(10,2) AFTER stock_quantity, -- For Product Weight
ADD COLUMN dimensions VARCHAR(50) AFTER weight, -- For Product Dimensions (LxWxH)
ADD COLUMN specifications TEXT AFTER dimensions, -- For Product Specifications
ADD COLUMN tags VARCHAR(255) AFTER specifications, -- For Product Tags
ADD COLUMN status ENUM('active', 'inactive') NOT NULL DEFAULT 'active' AFTER tags; 

SELECT AUTO_INCREMENT 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_NAME = 'Categories' AND TABLE_SCHEMA = 'Ecommerce';

ALTER TABLE Categories
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;
DESCRIBE Products;

ALTER TABLE Categories MODIFY category_id VARCHAR(10);

-- Update Categories table
ALTER TABLE Categories 
MODIFY category_id VARCHAR(10) PRIMARY KEY;

-- Drop foreign key in SubCategories table
ALTER TABLE SubCategories 
DROP FOREIGN KEY subcategories_category_id_fk;


-- Modify category_id column in SubCategories table
ALTER TABLE SubCategories 
MODIFY category_id VARCHAR(10);

SELECT 
    CONSTRAINT_NAME, 
    TABLE_NAME 
FROM 
    information_schema.KEY_COLUMN_USAGE 
WHERE 
    REFERENCED_TABLE_NAME = 'Categories' 
    AND REFERENCED_COLUMN_NAME = 'category_id';
    
ALTER TABLE SubCategories 
DROP FOREIGN KEY SubCategories_ibfk_1;

ALTER TABLE Categories 
MODIFY category_id VARCHAR(10);

describe SubCategories;

ALTER TABLE SubCategories 
MODIFY category_id VARCHAR(10);

ALTER TABLE SubCategories 
ADD CONSTRAINT SubCategories_ibfk_1 
FOREIGN KEY (category_id) REFERENCES Categories(category_id);

ALTER TABLE Products 
DROP FOREIGN KEY Products_ibfk_1;

ALTER TABLE SubCategories 
DROP FOREIGN KEY SubCategories_ibfk_1;

ALTER TABLE SubCategories 
MODIFY subcategory_id VARCHAR(10);

ALTER TABLE SubCategories 
MODIFY category_id VARCHAR(10);

ALTER TABLE Products 
MODIFY product_id VARCHAR(10);

SELECT CONSTRAINT_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_NAME = 'Products'
  AND REFERENCED_COLUMN_NAME = 'product_id';

ALTER TABLE ProductImages DROP FOREIGN KEY ProductImages_ibfk_1;
ALTER TABLE CartItems DROP FOREIGN KEY CartItems_ibfk_2;
ALTER TABLE OrderItems DROP FOREIGN KEY OrderItems_ibfk_2;
ALTER TABLE LowStockAlerts DROP FOREIGN KEY LowStockAlerts_ibfk_1;

-- Modify product_id column in Products table
ALTER TABLE Products MODIFY product_id VARCHAR(10);

-- Modify referencing columns in other tables
ALTER TABLE ProductImages MODIFY product_id VARCHAR(10);
ALTER TABLE CartItems MODIFY product_id VARCHAR(10);
ALTER TABLE OrderItems MODIFY product_id VARCHAR(10);
ALTER TABLE LowStockAlerts MODIFY product_id VARCHAR(10);

-- Re-add foreign key constraints
ALTER TABLE ProductImages ADD CONSTRAINT ProductImages_ibfk_1 FOREIGN KEY (product_id) REFERENCES Products(product_id);
ALTER TABLE CartItems ADD CONSTRAINT CartItems_ibfk_2 FOREIGN KEY (product_id) REFERENCES Products(product_id);
ALTER TABLE OrderItems ADD CONSTRAINT OrderItems_ibfk_2 FOREIGN KEY (product_id) REFERENCES Products(product_id);
ALTER TABLE LowStockAlerts ADD CONSTRAINT LowStockAlerts_ibfk_1 FOREIGN KEY (product_id) REFERENCES Products(product_id);

ALTER TABLE Products 
MODIFY subcategory_id VARCHAR(10);

ALTER TABLE Products 
ADD CONSTRAINT Products_ibfk_1 
FOREIGN KEY (subcategory_id) REFERENCES SubCategories(subcategory_id);

ALTER TABLE SubCategories 
ADD CONSTRAINT SubCategories_ibfk_1 
FOREIGN KEY (category_id) REFERENCES Categories(category_id);

describe product;
describe CartItems;
describe Carts;