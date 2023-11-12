-- Creating users table
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(10) NOT NULL,
	password VARCHAR(50) NOT NULL,
	created DATE
);

-- Creating character table
CREATE TABLE characters (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    character_name VARCHAR(30) NOT NULL,
    character_class VARCHAR(30) NOT NULL,
    race VARCHAR(30) NOT NULL,
    lvl INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Creating Stats table
CREATE TABLE characters_stats (
    id INT NOT NULL AUTO_INCREMENT,
    character_id INT NOT NULL,
    vigor INT NOT NULL,
    mind INT NOT NULL,
    intelligence INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (character_id) REFERENCES characters(id)
);

ALTER TABLE characters
ADD exp INT;