-- Create Database
DROP DATABASE IF EXISTS park_smart;

CREATE DATABASE park_smart;

USE park_smart;

-- Create tables
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30),
    client_id VARCHAR(255) UNIQUE NOT NULL,
    token VARCHAR(255),
    login INT DEFAULT 0,
    read_access INT DEFAULT 0,
    write_access INT DEFAULT 0,
    email VARCHAR(255)
);

-- Sample Insertion
INSERT INTO users (id, name, client_id, token, login, read_access, write_access, email)
VALUES (1, 'John', '109565775953816462122', NULL, 1, 0, 0, 'john@gmail.com');