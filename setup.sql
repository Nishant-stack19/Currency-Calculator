-- Create the database
CREATE DATABASE IF NOT EXISTS currency_converter_app_db;

-- Use the database
USE currency_converter_app_db;

-- Create the table for conversion history
CREATE TABLE IF NOT EXISTS conversion_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_currency VARCHAR(10) NOT NULL,
    to_currency VARCHAR(10) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    converted_amount DECIMAL(15, 2) NOT NULL,
    rate DECIMAL(15, 6) NOT NULL,
    converted_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
