CREATE DATABASE IF NOT EXISTS cafe
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cafe;

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(60) NOT NULL,
  rating TINYINT UNSIGNED NOT NULL,
  message VARCHAR(600) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  approved BOOLEAN NOT NULL DEFAULT TRUE,

  PRIMARY KEY (id),
  CHECK (rating BETWEEN 1 AND 5),
  INDEX idx_reviews_created (created_at),
  INDEX idx_reviews_approved_created (approved, created_at)
) ENGINE=InnoDB;

INSERT INTO reviews (name, rating, message)
VALUES ('Test User', 5, 'Amazing coffee and cozy vibe!');

SELECT * FROM reviews;

-- Create user (works on MySQL 8+)
CREATE USER IF NOT EXISTS 'cafe_user'@'localhost'
IDENTIFIED BY 'cafe_password_123';

-- If the user already exists but password differs, force it:
ALTER USER 'cafe_user'@'localhost'
IDENTIFIED BY 'cafe_password_123';

-- Give full access to your cafe database
GRANT ALL PRIVILEGES ON cafe.* TO 'cafe_user'@'localhost';

FLUSH PRIVILEGES;

SELECT user, host FROM mysql.user WHERE user = 'cafe_user';

