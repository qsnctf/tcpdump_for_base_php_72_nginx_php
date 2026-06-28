-- CTF SQL Boolean Blind Injection Environment
CREATE DATABASE IF NOT EXISTS app;
USE app;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(64) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, email, role) VALUES
    ('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@ctf.com', 'admin'),
    ('alice', '637d88ea2fcbdf10c5ef7bae4a3b5e0b', 'alice@example.com', 'user'),
    ('bob', '9f9d51bc70ef21ca5c14f307980a29d8', 'bob@example.com', 'user'),
    ('charlie', 'c479e6feb4e6363b8ee9fe1de8e2e040', 'charlie@example.com', 'user'),
    ('dave', '5f4dcc3b5aa765d61d8327deb882cf99', 'dave@example.com', 'user'),
    ('eve', '3856b89e5d1b7f7a6c7e3e7a6d7b8e9f', 'eve@example.com', 'editor'),
    ('frank', 'b1b2b3b4b5b6b7b8b9b0b1b2b3b4b5b6', 'frank@example.com', 'user'),
    ('grace', 'a1a2a3a4a5a6a7a8a9a0a1a2a3a4a5a6', 'grace@example.com', 'user'),
    ('heidi', '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d', 'heidi@example.com', 'moderator'),
    ('ivan', 'f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6', 'ivan@example.com', 'user');
