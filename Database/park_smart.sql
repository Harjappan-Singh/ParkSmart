-- Create Database
DROP DATABASE IF EXISTS park_smart;

CREATE DATABASE park_smart;

USE park_smart;

-- Create tables
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30),
    client_id VARCHAR(255) UNIQUE NOT NULL,
    token TEXT,
    login INT DEFAULT 0,
    read_access INT DEFAULT 0,
    write_access INT DEFAULT 0,
    email VARCHAR(255)
);

CREATE TABLE parking_lot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    parking_spot VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Sample Insertion
INSERT INTO users (id, name, client_id, token, login, read_access, write_access, email)
VALUES (1, 'John', '109565775953816462122', NULL, 1, 0, 0, 'john@gmail.com');

-- Insert these giving gaps 
INSERT INTO parking_lot (user_id, parking_spot, status)
VALUES 
(2, 'P1', 'occupied');

INSERT INTO parking_lot (user_id, parking_spot, status)
VALUES 
(2, 'P2', 'occupied');

INSERT INTO parking_lot (user_id, parking_spot, status)
VALUES 
(2, 'P1', 'available');

INSERT INTO parking_lot (user_id, parking_spot, status)
VALUES 
(2, 'P3', 'occupied');

INSERT INTO parking_lot (user_id, parking_spot, status)
VALUES 
(2, 'P2', 'available');

INSERT INTO parking_lot (user_id, parking_spot, status)
VALUES 
(2, 'P3', 'available');