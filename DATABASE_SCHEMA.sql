-- Auto Listings Service database schema
-- Target: PostgreSQL

BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username);

CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    color VARCHAR(50) NOT NULL,
    source_url VARCHAR(500) NOT NULL UNIQUE,
    CONSTRAINT uq_cars_source_url UNIQUE (source_url)
);

CREATE INDEX IF NOT EXISTS ix_cars_id ON cars (id);
CREATE INDEX IF NOT EXISTS ix_cars_make ON cars (make);
CREATE INDEX IF NOT EXISTS ix_cars_model ON cars (model);
CREATE INDEX IF NOT EXISTS ix_cars_year ON cars (year);
CREATE INDEX IF NOT EXISTS ix_cars_price ON cars (price);
CREATE INDEX IF NOT EXISTS ix_cars_color ON cars (color);
CREATE UNIQUE INDEX IF NOT EXISTS ix_cars_source_url ON cars (source_url);

COMMIT;
