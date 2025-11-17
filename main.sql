-- ===========================================
-- BLOOD AND ORGAN DONATION MANAGEMENT SYSTEM
-- ===========================================

DROP DATABASE IF EXISTS blood_organ_donation;
CREATE DATABASE blood_organ_donation;
USE blood_organ_donation;

-- =========================================================
-- 1. TABLES
-- =========================================================

CREATE TABLE Hospital (
    H_id INT PRIMARY KEY,
    H_name VARCHAR(100),
    H_Ph_no VARCHAR(15),
    ITP BOOLEAN,
    IBB BOOLEAN
);

CREATE TABLE Hospital_address (
    H_id INT,
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(10),
    PRIMARY KEY (H_id, pincode),
    FOREIGN KEY (H_id) REFERENCES Hospital(H_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Hospital_ph_no (
    H_id INT,
    H_ph_no VARCHAR(15),
    PRIMARY KEY (H_id, H_ph_no),
    FOREIGN KEY (H_id) REFERENCES Hospital(H_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Donor (
    D_id INT PRIMARY KEY AUTO_INCREMENT,
    FN VARCHAR(50),
    MN VARCHAR(50),
    LN VARCHAR(50),
    DOB DATE,
    Gender CHAR(1),
    B_grp VARCHAR(5),
    D_type VARCHAR(50),
    D_dateTime DATETIME,
    Eligibility_status BOOLEAN
);

CREATE TABLE Donor_ph_no (
    D_id INT,
    D_Ph_no VARCHAR(15),
    PRIMARY KEY (D_id, D_Ph_no),
    FOREIGN KEY (D_id) REFERENCES Donor(D_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Patient (
    P_id INT PRIMARY KEY AUTO_INCREMENT,
    H_id INT,
    FN VARCHAR(50),
    MN VARCHAR(50),
    LN VARCHAR(50),
    DOB DATE,
    Urgency_level VARCHAR(20),
    Gender CHAR(1),
    B_grp VARCHAR(5),
    FOREIGN KEY (H_id) REFERENCES Hospital(H_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Patient_ph_no (
    P_id INT,
    P_Ph_no VARCHAR(15),
    PRIMARY KEY (P_id, P_Ph_no),
    FOREIGN KEY (P_id) REFERENCES Patient(P_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Donation (
    Do_id INT PRIMARY KEY AUTO_INCREMENT,
    D_id INT,
    H_id INT,
    Do_type VARCHAR(50),
    Do_DT DATE,
    success_status VARCHAR(20),
    FOREIGN KEY (H_id) REFERENCES Hospital(H_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (D_id) REFERENCES Donor(D_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Blood (
    B_id INT PRIMARY KEY AUTO_INCREMENT,
    Do_id INT,
    stor_loc VARCHAR(100),
    B_status VARCHAR(20),
    Expiry_date DATE,
    B_collection_date DATE,
    FOREIGN KEY (Do_id) REFERENCES Donation(Do_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Organ (
    O_id INT PRIMARY KEY AUTO_INCREMENT,
    Do_id INT,
    O_type VARCHAR(50),
    O_DT DATE,
    O_status VARCHAR(20),
    O_collection_DT DATETIME,
    FOREIGN KEY (Do_id) REFERENCES Donation(Do_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Organ_req (
    Organ_req_id INT PRIMARY KEY AUTO_INCREMENT,
    Organ_req_type VARCHAR(50),
    min_max_score INT,
    Organ_req_DT DATETIME,
    Organ_req_status VARCHAR(20),
    H_id INT,
    FOREIGN KEY (H_id) REFERENCES Hospital(H_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Blood_req (
    Blood_req_id INT PRIMARY KEY AUTO_INCREMENT,
    H_id INT,
    Blood_req_grp VARCHAR(5),
    Blood_req_status VARCHAR(20),
    quantity_in_ml INT,
    Blood_req_DT DATE,
    FOREIGN KEY (H_id) REFERENCES Hospital(H_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Blood_issue (
    Blood_req_id INT,
    B_id INT PRIMARY KEY,
    issue_date DATE,
    Quantity_in_ml INT,
    blood_issue_status BOOLEAN,
    FOREIGN KEY (Blood_req_id) REFERENCES Blood_req(Blood_req_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (B_id) REFERENCES Blood(B_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- =========================================================
-- 2. SAMPLE DATA
-- =========================================================

INSERT INTO Hospital VALUES
(1, 'City Hospital', '9876543210', TRUE, TRUE),
(2, 'Green Valley Hospital', '9123456780', TRUE, FALSE),
(3, 'Apollo Hospital', '9988776655', TRUE, TRUE),
(4, 'Sunrise Clinic', '9345678901', FALSE, TRUE),
(5, 'Lotus Medical Center', '9001122334', TRUE, FALSE);

INSERT INTO Hospital_address VALUES
(1, 'Bangalore', 'Karnataka', '560001'),
(2, 'Mysore', 'Karnataka', '570001'),
(3, 'Hyderabad', 'Telangana', '500001'),
(4, 'Chennai', 'Tamil Nadu', '600001'),
(5, 'Pune', 'Maharashtra', '411001');

INSERT INTO Hospital_ph_no VALUES
(1, '9876543210'),
(2, '9123456780'),
(3, '9988776655'),
(4, '9345678901'),
(5, '9001122334');

INSERT INTO Donor VALUES
(1, 'Rahul', 'Kumar', 'Sharma', '1990-05-12', 'M', 'A+', 'Blood', '2025-10-01 09:00:00', TRUE),
(2, 'Anita', 'Rao', 'Patel', '1988-07-20', 'F', 'B+', 'Organ', '2025-09-25 10:30:00', TRUE),
(3, 'Vikram', 'Singh', 'Yadav', '1995-02-14', 'M', 'O-', 'Blood', '2025-08-15 08:15:00', TRUE),
(4, 'Pooja', 'Mehta', 'Kapoor', '1992-11-30', 'F', 'AB+', 'Organ', '2025-10-02 14:45:00', FALSE),
(5, 'Ramesh', 'Naik', 'Gowda', '1985-04-05', 'M', 'O+', 'Blood', '2025-09-10 16:00:00', TRUE);

INSERT INTO Donor_ph_no VALUES
(1, '9876501234'),
(2, '9765409876'),
(3, '9654321098'),
(4, '9543210987'),
(5, '9432109876');

INSERT INTO Patient VALUES
(1, 1, 'Sita', 'Devi', 'Patel', '1985-03-20', 'High', 'F', 'A+'),
(2, 2, 'Arjun', 'Rao', 'Nair', '1990-06-11', 'Medium', 'M', 'B+'),
(3, 3, 'Lakshmi', 'Priya', 'Iyer', '1978-01-30', 'Critical', 'F', 'O-'),
(4, 4, 'Manoj', 'Kumar', 'Verma', '1993-09-19', 'Low', 'M', 'AB+'),
(5, 5, 'Geeta', 'Rani', 'Shah', '2000-12-25', 'High', 'F', 'O+');

INSERT INTO Patient_ph_no VALUES
(1, '9123456789'),
(2, '9234567890'),
(3, '9345678901'),
(4, '9456789012'),
(5, '9567890123');

INSERT INTO Donation VALUES
(1, 1, 1, 'Blood', '2025-10-01', 'Success'),
(2, 2, 2, 'Organ', '2025-09-20', 'Success'),
(3, 3, 3, 'Blood', '2025-09-15', 'Failed'),
(4, 4, 4, 'Organ', '2025-08-25', 'Success'),
(5, 5, 5, 'Blood', '2025-07-30', 'Success');

INSERT INTO Blood VALUES
(1, 1, 'Storage A1', 'Available', '2025-12-31', '2025-10-01'),
(2, 3, 'Storage B2', 'Expired', '2025-09-20', '2025-09-15'),
(3, 5, 'Storage C3', 'Available', '2026-01-10', '2025-07-30'),
(4, 1, 'Storage A2', 'Issued', '2025-11-15', '2025-10-01'),
(5, 2, 'Storage D4', 'Available', '2026-02-20', '2025-09-20');

INSERT INTO Organ VALUES
(1, 2, 'Kidney', '2025-09-20', 'Healthy', '2025-09-20 11:00:00'),
(2, 4, 'Liver', '2025-08-25', 'Healthy', '2025-08-25 13:15:00'),
(3, 2, 'Heart', '2025-09-20', 'Rejected', '2025-09-20 14:30:00'),
(4, 4, 'Cornea', '2025-08-25', 'Healthy', '2025-08-25 15:45:00'),
(5, 2, 'Lung', '2025-09-20', 'Pending', '2025-09-20 17:00:00');

INSERT INTO Organ_req VALUES
(1, 'Kidney', 85, '2025-10-01 09:30:00', 'Pending', 1),
(2, 'Liver', 90, '2025-09-22 11:00:00', 'Approved', 2),
(3, 'Heart', 95, '2025-09-18 14:20:00', 'Pending', 3),
(4, 'Cornea', 70, '2025-09-10 10:10:00', 'Rejected', 4),
(5, 'Lung', 80, '2025-08-30 16:45:00', 'Approved', 5);

INSERT INTO Blood_req VALUES
(1, 1, 'A+', 'Pending', 500, '2025-10-01'),
(2, 2, 'B+', 'Approved', 300, '2025-09-22'),
(3, 3, 'O-', 'Pending', 600, '2025-09-18'),
(4, 4, 'AB+', 'Rejected', 400, '2025-09-10'),
(5, 5, 'O+', 'Approved', 450, '2025-08-30');

INSERT INTO Blood_issue VALUES
(1, 1, '2025-10-02', 500, TRUE),
(2, 2, '2025-09-23', 300, TRUE),
(3, 3, '2025-09-19', 600, FALSE),
(4, 4, '2025-09-11', 400, TRUE),
(5, 5, '2025-08-31', 450, TRUE);

-- =========================================================
-- 3. FUNCTIONS
-- =========================================================

DELIMITER //

CREATE FUNCTION CalculateDonorAge(dob DATE)
RETURNS INT
DETERMINISTIC
RETURN TIMESTAMPDIFF(YEAR, dob, CURDATE());
//

CREATE FUNCTION DonorFullName(fn VARCHAR(50), mn VARCHAR(50), ln VARCHAR(50))
RETURNS VARCHAR(150)
DETERMINISTIC
RETURN CONCAT(fn, ' ', mn, ' ', ln);
//

DELIMITER ;



-- =========================================================
-- 4. TRIGGERS
-- =========================================================

-- Trigger 1 - It ensures that once a donor donates blood (or organ) successfully, they are marked as ineligible for further donations
--  for a certain period (like 3 months, based on medical guidelines).
DELIMITER //
CREATE TRIGGER BeforeDonationSuccess
BEFORE INSERT ON Donation
FOR EACH ROW
BEGIN
  IF NEW.success_status = 'Success' THEN
    UPDATE Donor
    SET Eligibility_status = FALSE
    WHERE D_id = NEW.D_id;
  END IF;
END;
//

-- Trigger 2
 //
CREATE TRIGGER BeforeBloodExpiry
BEFORE UPDATE ON Blood
FOR EACH ROW
BEGIN
  IF NEW.Expiry_date = CURDATE() THEN
    SET NEW.B_status = 'Expired';
  END IF;
END;
//
DELIMITER ;





-- =========================================================
-- 5. STORED PROCEDURES
-- =========================================================

DELIMITER //

CREATE PROCEDURE RegisterNewPatient(
  IN p_H_id INT,
  IN p_FN VARCHAR(50),
  IN p_MN VARCHAR(50),
  IN p_LN VARCHAR(50),
  IN p_DOB DATE,
  IN p_Urgency_level VARCHAR(20),
  IN p_Gender CHAR(1),
  IN p_B_grp VARCHAR(5),
  IN p_P_Ph_no VARCHAR(15)
)
BEGIN
  INSERT INTO Patient (H_id, FN, MN, LN, DOB, Urgency_level, Gender, B_grp)
  VALUES (p_H_id, p_FN, p_MN, p_LN, p_DOB, p_Urgency_level, p_Gender, p_B_grp);
  SET @new_id = LAST_INSERT_ID();
  INSERT INTO Patient_ph_no (P_id, P_Ph_no) VALUES (@new_id, p_P_Ph_no);
END;
//

DELIMITER //

CREATE PROCEDURE AddDonation(
  IN p_D_id INT,
  IN p_H_id INT,
  IN p_Do_type VARCHAR(50),
  IN p_Do_DT DATE,
  IN p_success_status VARCHAR(20),
  IN p_collection_date DATE,
  IN p_storage VARCHAR(100),
  IN p_type_detail VARCHAR(50)  -- organ type or blood group
)
BEGIN
  -- 1Insert donation with donor and hospital linked
  INSERT INTO Donation (D_id, H_id, Do_type, Do_DT, success_status)
  VALUES (p_D_id, p_H_id, p_Do_type, p_Do_DT, p_success_status);

  SET @new_id = LAST_INSERT_ID();

  -- 2️⃣ If it’s a blood donation
  IF p_Do_type = 'Blood' THEN
    INSERT INTO Blood (Do_id, stor_loc, B_status, Expiry_date, B_collection_date)
    VALUES (@new_id, p_storage, 'Available', DATE_ADD(p_collection_date, INTERVAL 3 MONTH), p_collection_date);
  END IF;

  -- 3️⃣ If it’s an organ donation
  IF p_Do_type = 'Organ' THEN
    INSERT INTO Organ (Do_id, O_type, O_DT, O_status, O_collection_DT)
    VALUES (@new_id, p_type_detail, p_Do_DT, 'Healthy', NOW());
  END IF;
END;
//

DELIMITER ;


-- Verify triggers and functions:
SHOW TRIGGERS;
SHOW FUNCTION STATUS WHERE Db = 'blood_organ_donation';
SHOW PROCEDURE STATUS WHERE Db = 'blood_organ_donation';

-- TEST FUNCTIONS!!
-- for CalculateDonorAge
select* from Donor;
SELECT DOB, CalculateDonorAge(DOB) AS DonorAge FROM Donor WHERE D_id = 1;

-- for DonorFullName
select* from Donor;
SELECT FN, MN, LN, DonorFullName(FN, MN, LN) AS FullName FROM Donor WHERE D_id = 2;

-- Test case for TRIGGER 1:
-- Before
select * from donor;
SELECT * FROM Donor WHERE D_id = 3;

INSERT INTO Donation (D_id, H_id, Do_type, Do_DT, success_status)
VALUES (3, 1, 'Blood', CURDATE(), 'Success');

-- After
SELECT * FROM Donor WHERE D_id = 3;
select * from donor;




-- Test case for TRIGGER 2
-- for OnBloodExpiry trigger
SELECT * FROM Blood WHERE B_id = 3;
select *from blood;
UPDATE Blood SET Expiry_date = CURDATE() WHERE B_id = 3;
SELECT * FROM Blood WHERE B_id = 3;

-- Test stored procedures:

CALL RegisterNewPatient(1, 'John', 'M', 'Doe', '1990-01-01', 'High', 'M', 'A+', '9999999999');
select*from patient;
select * from patient_ph_no;
CALL AddDonation(1, 2, 'Blood', CURDATE(), 'Success', CURDATE(), 'Storage Z', 'Available');
select * FROM donation;
select * from blood;




