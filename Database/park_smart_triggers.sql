-- Log Parking Lot Updates
CREATE TABLE parking_lot_update_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parking_lot_id INT NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER log_parking_lot_update
AFTER UPDATE ON parking_lot
FOR EACH ROW
BEGIN
    INSERT INTO parking_lot_update_log (parking_lot_id, old_status, new_status)
    VALUES (OLD.id, OLD.status, NEW.status);
END$$
DELIMITER ;

-- Log Deletion of Users
CREATE TABLE user_deletion_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(30),
    client_id VARCHAR(255),
    deletion_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER log_user_deletion
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_deletion_log (user_id, name, client_id)
    VALUES (OLD.id, OLD.name, OLD.client_id);
END$$
DELIMITER ;

-- Prevent Duplicate Parking Spot Occupancy
DELIMITER $$
CREATE TRIGGER prevent_duplicate_occupancy
BEFORE INSERT ON parking_lot
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM parking_lot
        WHERE parking_spot = NEW.parking_spot AND status = 'occupied'
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Parking spot is already occupied!';
    END IF;
END$$
DELIMITER ;


