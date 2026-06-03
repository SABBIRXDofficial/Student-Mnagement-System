-- ============================================
-- Student Management System - MySQL Schema
-- Based on ER Diagram
-- ============================================

CREATE DATABASE IF NOT EXISTS student_management_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_management_db;

-- ============================================
-- ROLES TABLE
-- ============================================
CREATE TABLE roles (
    role_id     INT AUTO_INCREMENT PRIMARY KEY,
    role_name   VARCHAR(100) NOT NULL,
    role_desc   TEXT
);

-- ============================================
-- PERMISSION TABLE
-- ============================================
CREATE TABLE permission (
    per_id      INT AUTO_INCREMENT PRIMARY KEY,
    per_role_id INT NOT NULL,
    per_name    VARCHAR(100) NOT NULL,
    per_module  VARCHAR(100) NOT NULL,
    CONSTRAINT fk_permission_role FOREIGN KEY (per_role_id)
        REFERENCES roles(role_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- USER TABLE
-- ============================================
CREATE TABLE user (
    user_id      INT AUTO_INCREMENT PRIMARY KEY,
    user_name    VARCHAR(150) NOT NULL,
    user_mobile  VARCHAR(20),
    user_email   VARCHAR(255) UNIQUE NOT NULL,
    user_address TEXT
);

-- ============================================
-- LOGIN TABLE
-- ============================================
CREATE TABLE login (
    login_id       INT AUTO_INCREMENT PRIMARY KEY,
    login_role_id  INT NOT NULL,
    login_username VARCHAR(150) UNIQUE NOT NULL,
    user_password  VARCHAR(255) NOT NULL,
    user_id        INT NOT NULL,
    CONSTRAINT fk_login_role FOREIGN KEY (login_role_id)
        REFERENCES roles(role_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_login_user FOREIGN KEY (user_id)
        REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- USER HAS ROLES (junction for Has relationship)
-- ============================================
CREATE TABLE user_has_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_uhr_user FOREIGN KEY (user_id)
        REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_uhr_role FOREIGN KEY (role_id)
        REFERENCES roles(role_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- COURSE TABLE
-- ============================================
CREATE TABLE course (
    crs_id      INT AUTO_INCREMENT PRIMARY KEY,
    crs_stu_id  INT,               -- will FK to student after student is created
    crs_name    VARCHAR(200) NOT NULL,
    crs_desc    TEXT,
    crs_type    VARCHAR(100)
);

-- ============================================
-- FEES TABLE
-- ============================================
CREATE TABLE fees (
    fee_id      INT AUTO_INCREMENT PRIMARY KEY,
    fee_desc    TEXT,
    fee_type    VARCHAR(100) NOT NULL,
    fee_crs_id  INT NOT NULL,
    fee_amt     DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_fees_course FOREIGN KEY (fee_crs_id)
        REFERENCES course(crs_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================
-- STUDENT TABLE
-- ============================================
CREATE TABLE student (
    stu_id      INT AUTO_INCREMENT PRIMARY KEY,
    stu_name    VARCHAR(150) NOT NULL,
    stu_mobile  VARCHAR(20),
    stu_add     TEXT,
    stu_email   VARCHAR(255) UNIQUE NOT NULL,
    stu_pass    VARCHAR(255) NOT NULL
);

-- ============================================
-- EXAM TABLE
-- ============================================
CREATE TABLE exam (
    exam_id     INT AUTO_INCREMENT PRIMARY KEY,
    exam_desc   TEXT,
    exam_type   VARCHAR(100) NOT NULL
);

-- ============================================
-- STUDENT HAS EXAM (Has relationship)
-- ============================================
CREATE TABLE student_has_exam (
    stu_id  INT NOT NULL,
    exam_id INT NOT NULL,
    PRIMARY KEY (stu_id, exam_id),
    CONSTRAINT fk_she_student FOREIGN KEY (stu_id)
        REFERENCES student(stu_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_she_exam FOREIGN KEY (exam_id)
        REFERENCES exam(exam_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- USER MANAGES STUDENT (Manage relationship)
-- ============================================
CREATE TABLE user_manages_student (
    user_id INT NOT NULL,
    stu_id  INT NOT NULL,
    PRIMARY KEY (user_id, stu_id),
    CONSTRAINT fk_ums_user FOREIGN KEY (user_id)
        REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ums_student FOREIGN KEY (stu_id)
        REFERENCES student(stu_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- Update COURSE to reference STUDENT
-- ============================================
ALTER TABLE course
    ADD CONSTRAINT fk_course_student FOREIGN KEY (crs_stu_id)
        REFERENCES student(stu_id) ON DELETE SET NULL ON UPDATE CASCADE;

-- ============================================
-- SEED DATA (optional defaults)
-- ============================================
INSERT INTO roles (role_name, role_desc) VALUES
    ('Admin', 'Full system access'),
    ('Teacher', 'Manage students and exams'),
    ('Student', 'View own records');

INSERT INTO permission (per_role_id, per_name, per_module) VALUES
    (1, 'Full Access', 'All'),
    (2, 'Read-Write', 'Student'),
    (2, 'Read-Write', 'Exam'),
    (3, 'Read Only', 'Course'),
    (3, 'Read Only', 'Fees');
