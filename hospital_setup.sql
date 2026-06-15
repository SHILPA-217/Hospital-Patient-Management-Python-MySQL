-- ============================================
-- Hospital Patient Data Management System
-- MySQL Database Setup Script
-- ============================================

CREATE DATABASE IF NOT EXISTS HospitalDB;
USE HospitalDB;

-- -----------------------------------------------
-- TABLE 1: Patient Records (Outdoor Patients)
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS Patient_Records (
    PSrno          NUMERIC(7) PRIMARY KEY,
    pname          CHAR(35),
    Address        VARCHAR(40),
    city           CHAR(20),
    Country        VARCHAR(20),
    outdoor        CHAR(1),
    indoor         CHAR(1),
    Dateofconsultation DATE,
    Consulting_drname  CHAR(25),
    other_drname_consult CHAR(25),
    health_Prblm   CHAR(40),
    diagnosis      CHAR(40),
    cellno         NUMERIC(12),
    email          CHAR(40),
    Amount         NUMERIC(18,2)
);

-- -----------------------------------------------
-- TABLE 2: Doctors Main Details
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS doctors_Main_Details (
    Drno               NUMERIC(9) PRIMARY KEY,
    drName             CHAR(40),
    Education          VARCHAR(25),
    Medical_spelization CHAR(40),
    Core_spelization   CHAR(20),
    Experience         NUMERIC(3),
    Date_of_join       DATE,
    Day_available      CHAR(20),
    Address            CHAR(40),
    City               CHAR(20),
    Country            CHAR(20),
    Dr_Nationality     CHAR(20),
    Dr_cellNo          NUMERIC(12),
    dr_home_no         NUMERIC(15),
    dr_email           CHAR(40)
);

-- -----------------------------------------------
-- TABLE 3: Inhouse/Hospitalized Patient Master
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS Inhouse_Patient_Master (
    Hsptpno                NUMERIC(9) PRIMARY KEY,
    patient_fName          CHAR(40),
    Patient_lname          CHAR(30),
    attender_name          CHAR(40),
    attender_contact_no    NUMERIC(12),
    alternate_contactNo    NUMERIC(15),
    adm_doctor             CHAR(20),
    treatment              CHAR(25),
    diagnosis              CHAR(50),
    icu                    CHAR(1),
    MiCU                   CHAR(1),
    CCU                    CHAR(1),
    causality              CHAR(1),
    room_no                NUMERIC(3),
    room_floor             NUMERIC(3),
    room_type              CHAR(20),
    dateof_hospitalization DATE,
    admission_time         TIME,
    discharge_date         DATE,
    Room_charges_perday    NUMERIC(16,2),
    nofDays_hospitalized   NUMERIC(4),
    advance_amount         NUMERIC(18,2),
    medical_insurance      CHAR(1),
    Insurance_name         CHAR(20),
    Insurance_no           CHAR(20)
);

-- -----------------------------------------------
-- TABLE 4: Payment Table
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS Payment_Table (
    srno               NUMERIC(7) PRIMARY KEY,
    Hsptpno            NUMERIC(9),
    total_no_of_day    NUMERIC(5),
    Total_payment      NUMERIC(19,2),
    mode_of_Payment    CHAR(20),
    Payment_insurance  CHAR(1),
    Discharge_Date     DATE,
    FOREIGN KEY (Hsptpno) REFERENCES Inhouse_Patient_Master(Hsptpno)
);

-- -----------------------------------------------
-- TABLE 5: Patient Rehab Table
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS Patient_Rehab_Table (
    snro             NUMERIC(9) PRIMARY KEY,
    dateofvisit      DATE,
    Hsptpno          NUMERIC(9),
    rehab_dr_name    CHAR(20),
    exercise_facilityUsed CHAR(1),
    medicines        CHAR(125),
    visitpayment     NUMERIC(18,2),
    insurance_cover  CHAR(1),
    insurancename    CHAR(30),
    insurance_no     CHAR(20),
    whosename        CHAR(40),
    insurance_TPA    CHAR(30),
    contact_No       NUMERIC(12),
    FOREIGN KEY (Hsptpno) REFERENCES Inhouse_Patient_Master(Hsptpno)
);
