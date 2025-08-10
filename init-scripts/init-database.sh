#!/bin/bash
# Database initialization script for CivicShield

set -e

# Database connection parameters
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-civicshield}
DB_USER=${DB_USER:-civicshield_user}
DB_PASSWORD=${DB_PASSWORD:-civicshield_pass}

echo "Initializing database..."

# Wait for database to be ready
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready. Creating tables..."

# Create tables (this would be replaced with actual table creation SQL)
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<-EOSQL
    -- Create tables for CivicShield
    -- This is a simplified example. In a real application, you would use Alembic migrations.
    
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        agency_id UUID,
        role_id UUID,
        security_clearance_level INTEGER NOT NULL,
        phone_number VARCHAR(20),
        mfa_enabled BOOLEAN DEFAULT FALSE,
        mfa_method VARCHAR(20),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP WITH TIME ZONE,
        is_active BOOLEAN DEFAULT TRUE,
        failed_login_attempts INTEGER DEFAULT 0,
        locked_until TIMESTAMP WITH TIME ZONE
    );
    
    -- Agencies table
    CREATE TABLE IF NOT EXISTS agencies (
        agency_id UUID PRIMARY KEY,
        agency_name VARCHAR(100) NOT NULL,
        agency_type VARCHAR(50),
        jurisdiction VARCHAR(100),
        contact_email VARCHAR(100),
        contact_phone VARCHAR(20),
        address TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
    
    -- Roles table
    CREATE TABLE IF NOT EXISTS roles (
        role_id UUID PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL,
        role_description TEXT,
        access_level INTEGER NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Add more table creation statements as needed
    -- For example: threats, incidents, sensors, communications, analytics tables
    
    -- Insert initial data
    INSERT INTO agencies (agency_id, agency_name, agency_type, jurisdiction) 
    VALUES ('123e4567-e89b-12d3-a456-426614174000', 'Defense Department', 'NATIONAL_DEFENSE', 'Federal') 
    ON CONFLICT DO NOTHING;
    
    INSERT INTO roles (role_id, role_name, role_description, access_level) 
    VALUES ('123e4567-e89b-12d3-a456-426614174001', 'Administrator', 'Full system access', 4) 
    ON CONFLICT DO NOTHING;
    
    INSERT INTO roles (role_id, role_name, role_description, access_level) 
    VALUES ('123e4567-e89b-12d3-a456-426614174002', 'Security Analyst', 'Threat monitoring and analysis', 3) 
    ON CONFLICT DO NOTHING;
    
    INSERT INTO roles (role_id, role_name, role_description, access_level) 
    VALUES ('123e4567-e89b-12d3-a456-426614174003', 'Incident Commander', 'Crisis management and response', 3) 
    ON CONFLICT DO NOTHING;
    
    INSERT INTO roles (role_id, role_name, role_description, access_level) 
    VALUES ('123e4567-e89b-12d3-a456-426614174004', 'Field Agent', 'On-ground reporting and execution', 2) 
    ON CONFLICT DO NOTHING;
    
    INSERT INTO roles (role_id, role_name, role_description, access_level) 
    VALUES ('123e4567-e89b-12d3-a456-426614174005', 'Intelligence Officer', 'Intelligence data access and analysis', 3) 
    ON CONFLICT DO NOTHING;
    
    INSERT INTO roles (role_id, role_name, role_description, access_level) 
    VALUES ('123e4567-e89b-12d3-a456-426614174006', 'Audit Specialist', 'Compliance and audit functions', 2) 
    ON CONFLICT DO NOTHING;
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    CREATE INDEX IF NOT EXISTS idx_users_agency ON users(agency_id);
    CREATE INDEX IF NOT EXISTS idx_users_role ON users(role_id);
    
    -- Add more indexes as needed
    
    -- Grant permissions
    GRANT ALL PRIVILEGES ON TABLE users TO $DB_USER;
    GRANT ALL PRIVILEGES ON TABLE agencies TO $DB_USER;
    GRANT ALL PRIVILEGES ON TABLE roles TO $DB_USER;
    
    -- Add more GRANT statements as needed
    
    -- Create initial admin user (in a real application, this would be done through a secure process)
    -- INSERT INTO users (user_id, username, email, password_hash, first_name, last_name, security_clearance_level, is_active)
    -- VALUES ('123e4567-e89b-12d3-a456-426614174007', 'admin', 'admin@civicshield.example.com', 
    --         '\$2b\$12\$example_hash', 'Admin', 'User', 4, TRUE)
    -- ON CONFLICT DO NOTHING;
    
    -- Add more initial data as needed
EOSQL

echo "Database initialization completed successfully!"