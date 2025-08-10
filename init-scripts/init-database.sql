-- Database initialization script for CivicShield

-- Create database
CREATE DATABASE civicshield;

-- Connect to the database
\c civicshield;

-- Create users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    agency_id UUID,
    role_id UUID,
    security_clearance_level INTEGER CHECK (security_clearance_level BETWEEN 1 AND 4),
    phone_number VARCHAR(20),
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_method VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    password_hash VARCHAR(255) NOT NULL
);

-- Create agencies table
CREATE TABLE agencies (
    agency_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_name VARCHAR(100) NOT NULL,
    agency_type VARCHAR(50),
    jurisdiction VARCHAR(100),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create roles table
CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_name VARCHAR(50) NOT NULL,
    role_description TEXT,
    access_level INTEGER CHECK (access_level BETWEEN 1 AND 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create user_roles table
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(user_id),
    role_id UUID REFERENCES roles(role_id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    assigned_by UUID REFERENCES users(user_id),
    PRIMARY KEY (user_id, role_id)
);

-- Create threats table
CREATE TABLE threats (
    threat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    threat_type VARCHAR(50),
    threat_source VARCHAR(50),
    threat_title VARCHAR(200) NOT NULL,
    threat_description TEXT,
    severity_score DECIMAL(3,2) CHECK (severity_score BETWEEN 0 AND 10),
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0 AND 10),
    geolocation VARCHAR(100),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    assigned_to UUID REFERENCES users(user_id),
    agency_id UUID REFERENCES agencies(agency_id)
);

-- Create incidents table
CREATE TABLE incidents (
    incident_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_title VARCHAR(200) NOT NULL,
    incident_description TEXT,
    incident_type VARCHAR(50),
    severity_level VARCHAR(20),
    priority_level VARCHAR(20) DEFAULT 'OPEN',
    status VARCHAR(20) DEFAULT 'OPEN',
    geolocation VARCHAR(100),
    reported_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_by UUID REFERENCES users(user_id),
    assigned_to UUID REFERENCES users(user_id),
    agency_id UUID REFERENCES agencies(agency_id)
);

-- Create incident_threats table
CREATE TABLE incident_threats (
    incident_id UUID REFERENCES incidents(incident_id),
    threat_id UUID REFERENCES threats(threat_id),
    associated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    associated_by UUID REFERENCES users(user_id),
    PRIMARY KEY (incident_id, threat_id)
);

-- Create sensors table
CREATE TABLE sensors (
    sensor_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sensor_name VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50),
    location VARCHAR(100),
    installation_date TIMESTAMP WITH TIME ZONE,
    last_maintenance_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    agency_id UUID REFERENCES agencies(agency_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create sensor_data table
CREATE TABLE sensor_data (
    sensor_id UUID REFERENCES sensors(sensor_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    data TEXT,
    processed BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (sensor_id, timestamp)
);

-- Create secure_messages table
CREATE TABLE secure_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(user_id),
    recipient_id UUID REFERENCES users(user_id),
    message_content TEXT,
    message_hash VARCHAR(64),
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP WITH TIME ZONE,
    read_at TIMESTAMP WITH TIME ZONE,
    is_deleted BOOLEAN DEFAULT FALSE,
    encryption_key_id UUID,
    message_type VARCHAR(20) DEFAULT 'TEXT'
);

-- Create communication_channels table
CREATE TABLE communication_channels (
    channel_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_name VARCHAR(100) NOT NULL,
    channel_type VARCHAR(20),
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create channel_members table
CREATE TABLE channel_members (
    channel_id UUID REFERENCES communication_channels(channel_id),
    user_id UUID REFERENCES users(user_id),
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    role_in_channel VARCHAR(20) DEFAULT 'MEMBER',
    PRIMARY KEY (channel_id, user_id)
);

-- Create indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_threats_status ON threats(status);
CREATE INDEX idx_threats_severity ON threats(severity_score);
CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_severity ON incidents(severity_level);
CREATE INDEX idx_sensor_data_timestamp ON sensor_data(timestamp);
CREATE INDEX idx_secure_messages_sender ON secure_messages(sender_id);
CREATE INDEX idx_secure_messages_recipient ON secure_messages(recipient_id);

-- Insert default roles
INSERT INTO roles (role_name, role_description, access_level) VALUES
('Administrator', 'Full system access, user management, system configuration', 4),
('Security Analyst', 'Threat monitoring, analysis tools, report generation', 3),
('Incident Commander', 'Crisis management tools, resource allocation, communication coordination', 3),
('Field Agent', 'Field reporting, real-time communication, location tracking', 2),
('Intelligence Officer', 'Intelligence data access, pattern analysis, threat correlation', 3),
('Audit Specialist', 'Audit logs access, compliance reporting, activity monitoring', 2);

-- Insert default agency
INSERT INTO agencies (agency_name, agency_type, jurisdiction) VALUES
('CivicShield Admin', 'ADMIN', 'GLOBAL');

-- Insert default admin user
INSERT INTO users (username, email, first_name, last_name, agency_id, role_id, security_clearance_level, password_hash) 
SELECT 'admin', 'admin@civicshield.example.com', 'Admin', 'User', 
       (SELECT agency_id FROM agencies WHERE agency_name = 'CivicShield Admin'),
       (SELECT role_id FROM roles WHERE role_name = 'Administrator'),
       4, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S';