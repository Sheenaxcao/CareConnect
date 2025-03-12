use Care_Connect;

go
CREATE TABLE patients (
    PatientID INT PRIMARY KEY IDENTITY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Gender NVARCHAR(10),
    Email NVARCHAR(120),
    PhoneNumber NVARCHAR(15),
    Address NVARCHAR(100),
    ZipCode NVARCHAR(20),
    ContactPersonName NVARCHAR(50),
    ContactPersonPhoneNumber NVARCHAR(15),
    PaymentInformation NVARCHAR(150),
    PasswordHash NVARCHAR(200)
);

CREATE TABLE physicians (
    PhysicianID INT PRIMARY KEY IDENTITY,
    FirstName NVARCHAR(150) NOT NULL,
    LastName NVARCHAR(150) NOT NULL,
    Email NVARCHAR(200),
    Gender NVARCHAR(10),
    PhoneNumber NVARCHAR(15),
    Address NVARCHAR(100),
    ZipCode NVARCHAR(20),
    Availability NVARCHAR(150),
    Specialty NVARCHAR(150),
    PhysicianRank NVARCHAR(50),
    HospitalAttached NVARCHAR(150),
    PasswordHash NVARCHAR(200)
);

CREATE TABLE services (
    ServiceID INT PRIMARY KEY IDENTITY,
    ServiceName NVARCHAR(200) NOT NULL,
    ServiceDescription NVARCHAR(255),
    ServiceCost FLOAT,
    PhysicianID INT FOREIGN KEY REFERENCES physicians(PhysicianID)
);

CREATE TABLE billing_rates (
    BillingRateID INT PRIMARY KEY IDENTITY,
    PhysicianRank NVARCHAR(50),
    HourlyRate FLOAT
);

CREATE TABLE appointments (
    AppointmentID INT PRIMARY KEY IDENTITY,
    PatientID INT FOREIGN KEY REFERENCES patients(PatientID),
    PatientFirstName NVARCHAR(50) NOT NULL,
    PatientLastName NVARCHAR(50) NOT NULL,
    PatientAddress NVARCHAR(100) NOT NULL,
    PhysicianID INT FOREIGN KEY REFERENCES physicians(PhysicianID),
    PhysicianFirstName NVARCHAR(150) NOT NULL,
    PhysicianLastName NVARCHAR(150) NOT NULL,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    AmountBilled FLOAT
);
go
DELETE FROM patients;
go
ALTER TABLE patients
ADD CONSTRAINT UQ_Email UNIQUE (Email);
go
ALTER TABLE physicians
ADD CONSTRAINT UQ_Email UNIQUE (Email);
go
SELECT * FROM services;

INSERT INTO services (ServiceName, ServiceDescription, ServiceCost, PhysicianID)
VALUES 
('Wound dressing', 'Assistance with daily living activities, including grooming and hygiene.', 75.00, 1);
go
INSERT INTO services (ServiceName, ServiceDescription, ServiceCost, PhysicianID)
VALUES 
('Companionship', 'Providing social interaction and support for individuals in their home.', 50.00, 1);
go

SELECT * FROM billing_rates;