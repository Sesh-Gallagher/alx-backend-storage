-- Creates a table of unique users
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL  AUTO_INCREMENT,
    email VARCHAR(225) NOT NULL UNIQUE,
    name VARCHAR(225),
    PRIMARY KEY (id)
);
