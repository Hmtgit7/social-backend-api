-- Database Initialization Script for Social Backend API

-- Drop tables if they exist
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(255),
  bio TEXT,
  google_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create friends table
CREATE TABLE friends (
  id SERIAL PRIMARY KEY,
  requester_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  addressee_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  status VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, accepted, rejected
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (requester_id, addressee_id)
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_friends_requester ON friends(requester_id);
CREATE INDEX idx_friends_addressee ON friends(addressee_id);
CREATE INDEX idx_friends_status ON friends(status);

-- Create combined index for friend lookups
CREATE INDEX idx_friends_combined ON friends(requester_id, addressee_id, status);

-- Insert sample data (optional, uncomment if needed)
/*
-- Insert sample users with hashed passwords (password = 'password123')
INSERT INTO users (name, email, password, bio) VALUES
('John Doe', 'john@example.com', '$2b$10$1JqT7PtMZ1cflISTUoJ1H.XA.jUNiRFbv7QPceuKpW0KMnVCBcMtG', 'Software developer based in New York'),
('Jane Smith', 'jane@example.com', '$2b$10$1JqT7PtMZ1cflISTUoJ1H.XA.jUNiRFbv7QPceuKpW0KMnVCBcMtG', 'Product designer working remotely'),
('Alice Johnson', 'alice@example.com', '$2b$10$1JqT7PtMZ1cflISTUoJ1H.XA.jUNiRFbv7QPceuKpW0KMnVCBcMtG', 'Data scientist passionate about ML'),
('Bob Wilson', 'bob@example.com', '$2b$10$1JqT7PtMZ1cflISTUoJ1H.XA.jUNiRFbv7QPceuKpW0KMnVCBcMtG', 'Marketing specialist with 5 years experience'),
('Charlie Brown', 'charlie@example.com', '$2b$10$1JqT7PtMZ1cflISTUoJ1H.XA.jUNiRFbv7QPceuKpW0KMnVCBcMtG', 'Full-stack developer and open source contributor');

-- Insert sample friend relationships
INSERT INTO friends (requester_id, addressee_id, status) VALUES
(1, 2, 'accepted'),  -- John and Jane are friends
(1, 3, 'pending'),   -- John sent request to Alice
(4, 1, 'pending'),   -- Bob sent request to John
(2, 5, 'accepted'),  -- Jane and Charlie are friends
(3, 5, 'rejected');  -- Alice rejected Charlie's request
*/