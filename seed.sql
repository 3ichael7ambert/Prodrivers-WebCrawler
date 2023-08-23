DROP DATABASE IF EXISTS  driver_jobs_db;
CREATE DATABASE driver_jobs_db;

\c driver_jobs_db



-- Table for Users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(50) NOT NULL,
    license_type VARCHAR(50),
    company_name VARCHAR(100)
);

-- Table for Drivers
DROP TABLE IF EXISTS drivers;
CREATE TABLE drivers (
    id INTEGER PRIMARY KEY REFERENCES users(id),
    assigned_manager_id INTEGER REFERENCES managers(id),
    otherJobDetails VARCHAR,
    companyID VARCHAR,
    driverType VARCHAR,
    currentAvailability VARCHAR,
    isAssigned BOOLEAN,
    FOREIGN KEY (assigned_manager_id) REFERENCES managers(id)
);

-- Table for Driver Jobs
DROP TABLE IF EXISTS driver_jobs;
CREATE TABLE driver_jobs (
    id SERIAL PRIMARY KEY,
    driver_id INTEGER REFERENCES drivers(id),
    job_id INTEGER REFERENCES jobs(id)
);

-- Table for Clients
DROP TABLE IF EXISTS clients;
CREATE TABLE clients (
    id INTEGER PRIMARY KEY REFERENCES users(id),
    manager_id INTEGER REFERENCES managers(id),
    otherJobDetails VARCHAR,
    FOREIGN KEY (manager_id) REFERENCES managers(id)
);

-- Table for Jobs
DROP TABLE IF EXISTS jobs;
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    jobName VARCHAR,
    jobDescription VARCHAR,
    jobSchedule VARCHAR,
    jobRateOfPay VARCHAR,
    client_id INTEGER REFERENCES clients(id),
    manager_id INTEGER REFERENCES managers(id),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (manager_id) REFERENCES managers(id)
);

-- Table for Managers
DROP TABLE IF EXISTS managers;
CREATE TABLE managers (
    id INTEGER PRIMARY KEY REFERENCES users(id),
    firstName VARCHAR,
    lastName VARCHAR,
    FOREIGN KEY (id) REFERENCES users(id)
);

-- Table for Dispatchers
DROP TABLE IF EXISTS dispatchers;
CREATE TABLE dispatchers (
    id INTEGER PRIMARY KEY REFERENCES users(id),
    firstName VARCHAR,
    lastName VARCHAR,
    manager_id INTEGER NOT NULL REFERENCES managers(id),
    FOREIGN KEY (manager_id) REFERENCES managers(id)
);

-- Table for Companies
DROP TABLE IF EXISTS companies;
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    companyName VARCHAR,
    name VARCHAR(120) UNIQUE NOT NULL
);

-- Table for Hidden Jobs
DROP TABLE IF EXISTS hidden_jobs;
CREATE TABLE hidden_jobs (
    id SERIAL PRIMARY KEY,
    jobName VARCHAR,
    jobDescription VARCHAR,
    jobSchedule VARCHAR,
    jobRateOfPay VARCHAR,
    otherJobDetails VARCHAR,
    isHidden BOOLEAN
);
