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
VALUES (1, 'John Loane', '104074606044733428183', NULL, 1, 0, 0, 'johnloaneparksmart@gmail.com');

INSERT INTO parking_lot (user_id, parking_spot, status, timestamp) VALUES
(1, 'P1', 'occupied', '2025-01-01 08:30:00'),
(1, 'P2', 'occupied', '2025-01-01 08:40:00'),
(1, 'P2', 'available', '2025-01-01 09:00:00'),
(1, 'P3', 'occupied', '2025-01-01 09:10:00'),
(1, 'P1', 'available', '2025-01-01 09:30:00'),
(1, 'P4', 'occupied', '2025-01-01 09:45:00'),
(1, 'P5', 'occupied', '2025-01-01 10:00:00'),
(1, 'P3', 'available', '2025-01-01 10:15:00'),
(1, 'P6', 'occupied', '2025-01-01 10:30:00'),
(1, 'P5', 'available', '2025-01-01 11:00:00'),
(1, 'P4', 'available', '2025-01-01 11:15:00'),
(1, 'P7', 'occupied', '2025-01-01 11:30:00'),
(1, 'P8', 'occupied', '2025-01-01 12:00:00'),
(1, 'P7', 'available', '2025-01-01 12:30:00'),
(1, 'P6', 'available', '2025-01-01 13:00:00'),
(1, 'P9', 'occupied', '2025-01-01 13:15:00'),
(1, 'P10', 'occupied', '2025-01-01 13:45:00'),
(1, 'P9', 'available', '2025-01-01 14:15:00'),
(1, 'P8', 'available', '2025-01-01 14:30:00'),
(1, 'P1', 'occupied', '2025-01-01 15:00:00'),
(1, 'P10', 'available', '2025-01-01 15:30:00'),
(1, 'P2', 'occupied', '2025-01-01 16:00:00'),
(1, 'P1', 'available', '2025-01-01 16:30:00'),
(1, 'P3', 'occupied', '2025-01-01 17:00:00'),
(1, 'P2', 'available', '2025-01-01 17:15:00'),
(1, 'P4', 'occupied', '2025-01-01 18:00:00'),
(1, 'P3', 'available', '2025-01-01 18:30:00'),
(1, 'P5', 'occupied', '2025-01-01 19:00:00'),
(1, 'P4', 'available', '2025-01-01 19:30:00');