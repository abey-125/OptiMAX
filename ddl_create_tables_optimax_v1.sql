---------------------------------------------------------------------------------------------------------
-- Script Name : ddl_create_tables_optimax_v1.sql
-- Purpose     : DDL for creating tables for Optimax database
-- Date        : Nov 08, 2022
-- Author      : Amanpreet Kaur
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 1. ROLES : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE roles (
    role_id INT NOT NULL PRIMARY KEY,
    role_type CHAR(6) NOT NULL);

ALTER TABLE roles
ADD CONSTRAINT CK_role_type CHECK (role_type IN ('Store', 'Vendor'));
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 2. USERS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE users ( 
    user_id INT NOT NULL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(500) UNIQUE,
    contact_number VARCHAR(15) NOT NULL UNIQUE,
    role_id INT NOT NULL);

ALTER TABLE users
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 3. MEDICINES : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE medicines ( 
    medicine_id INT NOT NULL PRIMARY KEY,
    medicine_name VARCHAR(100) NOT NULL,
    expiry_date DATE NOT NULL,
    manufactured_date date NOT NULL,
    medicine_type VARCHAR(50) NOT NULL,
    key_ingredient VARCHAR(100) NOT NULL,
    standard_price SMALLMONEY NOT NULL,
    role_id INT NOT NULL)

ALTER TABLE medicines
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 4. MEDICINE_EXPENSE : 
---------------------------------------------------------------------------------------------------------

CREATE TABLE medicine_expense (
    expense_id INT NOT NULL PRIMARY KEY, 
    medicine_id INT NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    ship_method CHAR(5) NOT NULL,
    freight_amount SMALLMONEY NOT NULL,
    role_id INT NOT NULL,);

ALTER TABLE medicine_expense
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);

ALTER TABLE medicine_expense
ADD FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE medicine_expense
ADD CONSTRAINT CK_ship_method CHECK (ship_method IN ('Air', 'Ocean', 'Truck'));
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 5. STORES : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE stores (
    store_id INT NOT NULL PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    store_branch VARCHAR(100) NOT NULL,
    store_address VARCHAR(100) NOT NULL,
    store_contact VARCHAR(15) NOT NULL UNIQUE,
    store_email VARCHAR(100) UNIQUE,
    role_id INT NOT NULL);

ALTER TABLE stores
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 6. MED_STORE : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE med_store (
    medicine_id INT NOT NULL,
    store_id INT NOT NULL,
    stock_in_hand INT NOT NULL,
    transit_quantity INT NOT NULL,
    role_id INT NOT NULL,
    CONSTRAINT PK_MED_STORE PRIMARY KEY (medicine_id, store_id));

ALTER TABLE med_store
ADD FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE med_store
ADD FOREIGN KEY (store_id) REFERENCES stores(store_id);

ALTER TABLE med_store
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 7. MED_THRESHOLD : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE med_threshold (
    medicine_id INT NOT NULL,
    store_id INT NOT NULL,
    max_threshold INT NOT NULL,
    min_threshold INT NOT NULL,
    role_id INT NOT NULL);

ALTER TABLE med_threshold
ADD FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE med_threshold
ADD FOREIGN KEY (store_id) REFERENCES stores(store_id);

ALTER TABLE med_threshold
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 8. TRANSIT_DAYS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE transit_days (
    transit_id INT NOT NULL PRIMARY KEY,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    ship_method char(5) NOT NULL,
    days INT NOT NULL,
    role_id INT NOT NULL);

ALTER TABLE transit_days
ADD CONSTRAINT CK_ship_method_transit CHECK (ship_method IN ('Air', 'Ocean', 'Truck'));

ALTER TABLE transit_days
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 9. VENDORS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE vendors ( 
    vendor_id INT NOT NULL PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    vendor_location VARCHAR(100) NOT NULL,
    vendor_address VARCHAR(100) NOT NULL,
    vendor_email VARCHAR(100) UNIQUE, 
    vendor_contact VARCHAR(15) NOT NULL UNIQUE,
    role_id INT NOT NULL);

ALTER TABLE vendors
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 10. VENDOR_MED : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE vendor_med ( 
    medicine_id INT NOT NULL,
    vendor_id INT NOT NULL,
    med_unit_price SMALLMONEY NOT NULL,
    role_id INT NOT NULL,
    CONSTRAINT PK_vendor_med PRIMARY KEY (medicine_id, vendor_id));

ALTER TABLE vendor_med
ADD FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE vendor_med
ADD FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id);

ALTER TABLE vendor_med
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 11. RATINGS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE ratings ( 
    rating_id INT NOT NULL PRIMARY KEY,
    store_id INT NOT NULL,
    rating INT NOT NULL,
    review_comment VARCHAR(100),
    ratings_date datetime,
    role_id INT NOT NULL,);

ALTER TABLE ratings
ADD FOREIGN KEY (store_id) REFERENCES stores(store_id);

ALTER TABLE ratings
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 12. ORDERS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE orders (
    order_id INT NOT NULL PRIMARY KEY,
    vendor_id INT NOT NULL,
    store_id INT NOT NULL,
    date_created datetime NOT NULL,
    order_status char(1) NOT NULL,
    total_price smallmoney NOT NULL,
    role_id INT NOT NULL);

ALTER TABLE orders
ADD FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id);

ALTER TABLE orders
ADD FOREIGN KEY (store_id) REFERENCES stores(store_id);

ALTER TABLE orders
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 13. ORDER_DETAILS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE order_details (
    order_id INT NOT NULL,
    medicine_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price SMALLMONEY NOT NULL,
    role_id INT NOT NULL,
    CONSTRAINT PK_ord_med PRIMARY KEY (order_id, medicine_id));


ALTER TABLE order_details
ADD FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_details
ADD FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE order_details
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 14. ORD_RETURNS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE ord_returns (
    return_id INT NOT NULL PRIMARY KEY,
    vendor_id INT NOT NULL,
    store_id INT NOT NULL,
    total_price SMALLMONEY NOT NULL,
    returned_date datetime,
    role_id INT NOT NULL);

ALTER TABLE ord_returns
ADD FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id);

ALTER TABLE ord_returns
ADD FOREIGN KEY (store_id) REFERENCES stores(store_id);

ALTER TABLE ord_returns
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- 15. RETURN_DETAILS : 
---------------------------------------------------------------------------------------------------------
CREATE TABLE return_details (
    return_id INT NOT NULL PRIMARY KEY,
    medicine_id INT NOT NULL,
    role_id INT NOT NULL,
    quantity INT NOT NULL, 
    unit_price SMALLMONEY NOT NULL);

ALTER TABLE return_details
ADD FOREIGN KEY (return_id) REFERENCES ord_returns(return_id);

ALTER TABLE return_details
ADD FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id);

ALTER TABLE return_details
ADD FOREIGN KEY (role_id) REFERENCES roles(role_id);
---------------------------------------------------------------------------------------------------------
