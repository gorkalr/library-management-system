CREATE DATABASE library_db;
USE library_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(10),
    active BOOLEAN
);

INSERT INTO users VALUES
(1,'adm','adm','admin',1),
(2,'user','user','user',1);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    author VARCHAR(100),
    category VARCHAR(50),
    available BOOLEAN
);

CREATE TABLE issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    issue_date DATE,
    return_date DATE,
    actual_return DATE,
    fine INT
);