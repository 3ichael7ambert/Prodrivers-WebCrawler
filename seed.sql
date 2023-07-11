-- Table for Drivers
CREATE TABLE drivers (
    id VARCHAR(255) PRIMARY KEY,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    driverType VARCHAR(255),
    currentAvailability VARCHAR(255),
    isAssigned BOOLEAN
);

-- Table for Clients
CREATE TABLE clients (
    id VARCHAR(255) PRIMARY KEY,
    jobName VARCHAR(255),
    jobDescription VARCHAR(255),
    jobSchedule VARCHAR(255),
    jobRateOfPay VARCHAR(255),
    otherJobDetails VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    companyID VARCHAR(255)
);

-- Table for Dispatchers
CREATE TABLE dispatchers (
    id VARCHAR(255) PRIMARY KEY,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255)
);

-- Table for Companies
CREATE TABLE companies (
    id VARCHAR(255) PRIMARY KEY,
    companyName VARCHAR(255)
);

-- Table for Managers
CREATE TABLE managers (
    id VARCHAR(255) PRIMARY KEY,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    companyID VARCHAR(255)
);

-- Table for Hidden Jobs
CREATE TABLE hidden_jobs (
    id VARCHAR(255) PRIMARY KEY,
    jobName VARCHAR(255),
    jobDescription VARCHAR(255),
    jobSchedule VARCHAR(255),
    jobRateOfPay VARCHAR(255),
    otherJobDetails VARCHAR(255),
    isHidden BOOLEAN
);
