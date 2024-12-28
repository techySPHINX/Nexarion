-- 1. Switch to the auth database if not already there
\c auth;

-- 2. Create the 'user' table (Make sure the table name is in quotes to avoid conflicts with reserved keywords in PostgreSQL)
CREATE TABLE IF NOT EXISTS "user" (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

-- 3. Insert a test user into the 'user' table
INSERT INTO "user" (email, password) VALUES ('jagan@email.com', 'Admin123')
ON CONFLICT (email) DO NOTHING;  -- Prevents inserting duplicate users
