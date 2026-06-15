
import mysql.connector
import sys
from datetime import date, datetime


# DATABASE CONFIGURATION  

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",        
    "password": "mysql1234",  
    "database": "HospitalDB"
}

CORRECT_PASSWORD = "hospital123"   
MAX_PASSWORD_ATTEMPTS = 4



def get_connection():
    """Return a live MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


def pause():
    input("\n  Press Enter to continue...")


def clear_screen():
    print("\n" + "=" * 60)


def yn_input(prompt):
    """Ask a Y/N question and return 'Y' or 'N'."""
    while True:
        val = input(prompt).strip().upper()
        if val in ("Y", "N"):
            return val
        print("  Please enter Y or N.")


def safe_int(prompt, length=None):
    """Read an integer, optionally checking digit length."""
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            if length and len(val) != length:
                print(f"  Must be exactly {length} digits.")
                continue
            return int(val)
        print("  Please enter a valid number.")


def safe_float(prompt):
    """Read a float value."""
    while True:
        val = input(prompt).strip()
        try:
            return float(val)
        except ValueError:
            print("  Please enter a valid amount.")


def safe_date(prompt):
    """Read a date in YYYY-MM-DD format."""
    while True:
        val = input(prompt + " (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("  Invalid date. Use YYYY-MM-DD format.")


def safe_time(prompt):
    """Read time in HH:MM format."""
    while True:
        val = input(prompt + " (HH:MM): ").strip()
        try:
            datetime.strptime(val, "%H:%M")
            return val
        except ValueError:
            print("  Invalid time. Use HH:MM format.")


def print_separator():
    print("-" * 60)


# ══════════════════════════════════════════════
#  Q9 — PASSWORD PROTECTION
# ══════════════════════════════════════════════

def password_check():
    """
    Ask for password up to MAX_PASSWORD_ATTEMPTS times.
    Terminates the program if all attempts fail.
    """
    print("\n" + "=" * 60)
    print("   HOSPITAL PATIENT DATA MANAGEMENT SYSTEM")
    print("=" * 60)
    print("   Secure Login")
    print("-" * 60)

    for attempt in range(1, MAX_PASSWORD_ATTEMPTS + 1):
        pwd = input(f"  Enter Password (Attempt {attempt}/{MAX_PASSWORD_ATTEMPTS}): ").strip()
        if pwd == CORRECT_PASSWORD:
            print("\n  ✔  Login successful! Welcome.\n")
            return True
        else:
            remaining = MAX_PASSWORD_ATTEMPTS - attempt
            if remaining > 0:
                print(f"  ✘  Wrong password. {remaining} attempt(s) left.")
            else:
                print("\n  ✘  Too many wrong attempts. Program terminated.")
                sys.exit()

    return False


# ══════════════════════════════════════════════
#  Q1 — ADD DOCTOR RECORDS
# ══════════════════════════════════════════════

def add_doctor_records():
    """Program 1: Add one or more doctor records to doctors_Main_Details."""
    clear_screen()
    print("  PROGRAM 1 — ADD DOCTOR RECORDS")
    print_separator()

    conn = get_connection()
    cursor = conn.cursor()

    while True:
        print("\n  Enter Doctor Details:")
        print_separator()

        drno      = safe_int("  Doctor No (e.g. 7001): ")
        drName    = input("  Doctor Name           : ").strip()
        education = input("  Education (MBBS/MD…)  : ").strip()
        med_spl   = input("  Medical Specialization: ").strip()
        core_spl  = input("  Core Specialization   : ").strip()
        exp       = safe_int("  Experience (years)    : ")
        doj       = safe_date("  Date of Joining       ")
        day_avail = input("  Days Available        : ").strip()
        address   = input("  Address               : ").strip()
        city      = input("  City                  : ").strip()
        country   = input("  Country               : ").strip()
        nat       = input("  Nationality           : ").strip()
        cell_no   = safe_int("  Cell No (10 digits)   : ")
        home_no   = safe_int("  Home No               : ")
        email     = input("  Email                 : ").strip()

        sql = """INSERT INTO doctors_Main_Details
                 (Drno, drName, Education, Medical_spelization, Core_spelization,
                  Experience, Date_of_join, Day_available, Address, City, Country,
                  Dr_Nationality, Dr_cellNo, dr_home_no, dr_email)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        values = (drno, drName, education, med_spl, core_spl, exp, doj,
                  day_avail, address, city, country, nat, cell_no, home_no, email)
        try:
            cursor.execute(sql, values)
            conn.commit()
            print("\n  ✔  Doctor record added successfully!")
        except mysql.connector.Error as e:
            print(f"\n  ✘  Error: {e}")

        more = yn_input("\n  Do you want to add more doctor records? (Y/N): ")
        if more == "N":
            break

    cursor.close()
    conn.close()
    pause()


# ══════════════════════════════════════════════
#  Q2 — ADD HOSPITALIZED PATIENT
# ══════════════════════════════════════════════

def add_hospitalized_patient():
    """Program 2: Add inhouse/hospitalized patient details."""
    clear_screen()
    print("  PROGRAM 2 — ADD HOSPITALIZED PATIENT")
    print_separator()

    conn = get_connection()
    cursor = conn.cursor()

    print("\n  Enter Hospitalized Patient Details:")
    print_separator()

    hsptpno   = safe_int("  Hospital Patient No    : ")
    fname     = input("  First Name             : ").strip()
    lname     = input("  Last Name              : ").strip()
    attender  = input("  Attender Name          : ").strip()
    att_cont  = safe_int("  Attender Contact No    : ")
    alt_cont  = safe_int("  Alternate Contact No   : ")
    adm_dr    = input("  Admitting Doctor       : ").strip()
    treatment = input("  Treatment              : ").strip()
    diagnosis = input("  Diagnosis              : ").strip()
    icu       = yn_input("  ICU? (Y/N)             : ")
    micu      = yn_input("  MICU? (Y/N)            : ")
    ccu       = yn_input("  CCU? (Y/N)             : ")
    casualty  = yn_input("  Casualty? (Y/N)        : ")
    room_no   = safe_int("  Room No                : ")
    room_fl   = safe_int("  Room Floor             : ")

    print("  Room Types: general / semispecial / special ward / vip ward")
    room_type = input("  Room Type              : ").strip()

    doh       = safe_date("  Date of Hospitalization")
    adm_time  = safe_time("  Admission Time         ")
    dis_date  = input("  Discharge Date (YYYY-MM-DD or leave blank): ").strip() or None
    charges   = safe_float("  Room Charges per Day   : ")
    no_days   = safe_int("  No. of Days            : ")
    advance   = safe_float("  Advance Amount         : ")
    insurance = yn_input("  Medical Insurance? (Y/N): ")
    ins_name  = input("  Insurance Name (if any): ").strip() or None
    ins_no    = input("  Insurance No (if any)  : ").strip() or None

    sql = """INSERT INTO Inhouse_Patient_Master
             (Hsptpno, patient_fName, Patient_lname, attender_name,
              attender_contact_no, alternate_contactNo, adm_doctor,
              treatment, diagnosis, icu, MiCU, CCU, causality,
              room_no, room_floor, room_type, dateof_hospitalization,
              admission_time, discharge_date, Room_charges_perday,
              nofDays_hospitalized, advance_amount, medical_insurance,
              Insurance_name, Insurance_no)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                     %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    values = (hsptpno, fname, lname, attender, att_cont, alt_cont, adm_dr,
              treatment, diagnosis, icu, micu, ccu, casualty,
              room_no, room_fl, room_type, doh, adm_time, dis_date,
              charges, no_days, advance, insurance, ins_name, ins_no)
    try:
        cursor.execute(sql, values)
        conn.commit()
        print("\n  ✔  Hospitalized patient record added successfully!")
    except mysql.connector.Error as e:
        print(f"\n  ✘  Error: {e}")

    cursor.close()
    conn.close()
    pause()


# ══════════════════════════════════════════════
#  Q3 — DISPLAY ALL OUTDOOR PATIENT RECORDS
# ══════════════════════════════════════════════

def display_outdoor_patients():
    """Program 3: Display all records from Patient_Records one by one."""
    clear_screen()
    print("  PROGRAM 3 — ALL OUTDOOR PATIENT RECORDS")
    print_separator()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patient_Records ORDER BY PSrno")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    if not rows:
        print("  No outdoor patient records found.")
        cursor.close()
        conn.close()
        pause()
        return

    total = len(rows)
    for idx, row in enumerate(rows, start=1):
        clear_screen()
        print(f"  OUTDOOR PATIENT RECORD  [{idx} of {total}]")
        print_separator()
        for col, val in zip(columns, row):
            print(f"  {col:<30}: {val}")
        print_separator()

        if idx < total:
            cont = input("  Press Enter for next record (or Q to quit): ").strip().upper()
            if cont == "Q":
                break
        else:
            print("\n  ✔  All records displayed.")
            pause()

    cursor.close()
    conn.close()


# ══════════════════════════════════════════════
#  Q4 — PATIENT DISCHARGE & BILL CALCULATION
# ══════════════════════════════════════════════

def discharge_patient():
    """Program 4 (Optional): Discharge a patient and calculate final bill."""
    clear_screen()
    print("  PROGRAM 4 — PATIENT DISCHARGE & BILL")
    print_separator()

    conn = get_connection()
    cursor = conn.cursor()

    hsptpno = safe_int("  Enter Hospital Patient No to discharge: ")

    cursor.execute("SELECT * FROM Inhouse_Patient_Master WHERE Hsptpno = %s", (hsptpno,))
    patient = cursor.fetchone()

    if not patient:
        print("  ✘  Patient not found.")
        cursor.close()
        conn.close()
        pause()
        return

    columns = [desc[0] for desc in cursor.description]
    p = dict(zip(columns, patient))

    print("\n  Patient Found:")
    print_separator()
    print(f"  Name      : {p['patient_fName']} {p['Patient_lname']}")
    print(f"  Doctor    : {p['adm_doctor']}")
    print(f"  Room Type : {p['room_type']}")
    print(f"  Charges/Day: ₹{p['Room_charges_perday']}")

    no_days = safe_int("  Total Days Hospitalized: ")
    room_charges = float(p['Room_charges_perday']) * no_days
    advance = float(p['advance_amount'])

    print("\n  Additional Charges:")
    medicine_cost  = safe_float("  Medicine Cost       : ₹")
    test_cost      = safe_float("  Lab/Test Charges    : ₹")
    other_cost     = safe_float("  Other Charges       : ₹")

    total_bill  = room_charges + medicine_cost + test_cost + other_cost
    balance_due = total_bill - advance

    print("\n" + "=" * 60)
    print("  HOSPITAL FINAL BILL")
    print("=" * 60)
    print(f"  Patient   : {p['patient_fName']} {p['Patient_lname']}")
    print(f"  Patient No: {hsptpno}")
    print_separator()
    print(f"  Room Charges ({no_days} days × ₹{p['Room_charges_perday']}): ₹{room_charges:,.2f}")
    print(f"  Medicine Cost                          : ₹{medicine_cost:,.2f}")
    print(f"  Lab/Test Charges                       : ₹{test_cost:,.2f}")
    print(f"  Other Charges                          : ₹{other_cost:,.2f}")
    print_separator()
    print(f"  TOTAL BILL                             : ₹{total_bill:,.2f}")
    print(f"  Advance Paid                           : ₹{advance:,.2f}")
    print(f"  BALANCE DUE                            : ₹{balance_due:,.2f}")
    print("=" * 60)

    print("\n  Mode of Payment: debit / credit / cash / upi / insurance")
    mode = input("  Payment Mode: ").strip()
    ins  = yn_input("  Insurance Payment? (Y/N): ")
    dis_date = safe_date("  Discharge Date")

    # Save to payment table
    cursor.execute("SELECT MAX(srno) FROM Payment_Table")
    max_srno = cursor.fetchone()[0]
    srno = (max_srno or 0) + 1

    sql = """INSERT INTO Payment_Table
             (srno, Hsptpno, total_no_of_day, Total_payment,
              mode_of_Payment, Payment_insurance, Discharge_Date)
             VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    try:
        cursor.execute(sql, (srno, hsptpno, no_days, total_bill, mode, ins, dis_date))

        # Update discharge date in master table
        cursor.execute("""UPDATE Inhouse_Patient_Master
                          SET discharge_date = %s, nofDays_hospitalized = %s
                          WHERE Hsptpno = %s""", (dis_date, no_days, hsptpno))
        conn.commit()
        print("\n  ✔  Discharge record saved successfully!")
    except mysql.connector.Error as e:
        print(f"\n  ✘  Error: {e}")

    cursor.close()
    conn.close()
    pause()


# ══════════════════════════════════════════════
#  Q5 — DISPLAY ALL REHAB RECORDS
# ══════════════════════════════════════════════

def display_rehab_records():
    """Program 5: Print all records from Patient_Rehab_Table."""
    clear_screen()
    print("  PROGRAM 5 — ALL PATIENT REHAB RECORDS")
    print_separator()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patient_Rehab_Table ORDER BY snro")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    if not rows:
        print("  No rehab records found.")
    else:
        for row in rows:
            print_separator()
            for col, val in zip(columns, row):
                print(f"  {col:<30}: {val}")
        print_separator()
        print(f"\n  Total records: {len(rows)}")

    cursor.close()
    conn.close()
    pause()


# ══════════════════════════════════════════════
#  Q6 — ADD OUTDOOR PATIENT RECORD
# ══════════════════════════════════════════════

def add_outdoor_patient():
    """Program 6: Add a single outdoor patient record."""
    clear_screen()
    print("  PROGRAM 6 — ADD OUTDOOR PATIENT RECORD")
    print_separator()

    conn = get_connection()
    cursor = conn.cursor()

    print("\n  Enter Outdoor Patient Details:")
    print_separator()

    psrno     = safe_int("  Serial No              : ")
    pname     = input("  Patient Name           : ").strip()
    address   = input("  Address                : ").strip()
    city      = input("  City                   : ").strip()
    country   = input("  Country                : ").strip()
    outdoor   = yn_input("  Outdoor? (Y/N)         : ")
    indoor    = yn_input("  Indoor?  (Y/N)         : ")
    doc_date  = safe_date("  Date of Consultation   ")
    cons_dr   = input("  Consulting Doctor      : ").strip()
    other_dr  = input("  Other Consulting Dr    : ").strip() or None
    health_pb = input("  Health Problem         : ").strip()
    diagnosis = input("  Diagnosis              : ").strip()
    cellno    = safe_int("  Cell No                : ")
    email     = input("  Email                  : ").strip()
    amount    = safe_float("  Amount (₹)            : ")

    sql = """INSERT INTO Patient_Records
             (PSrno, pname, Address, city, Country, outdoor, indoor,
              Dateofconsultation, Consulting_drname, other_drname_consult,
              health_Prblm, diagnosis, cellno, email, Amount)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    values = (psrno, pname, address, city, country, outdoor, indoor,
              doc_date, cons_dr, other_dr, health_pb, diagnosis,
              cellno, email, amount)
    try:
        cursor.execute(sql, values)
        conn.commit()
        print("\n  ✔  Outdoor patient record added successfully!")
    except mysql.connector.Error as e:
        print(f"\n  ✘  Error: {e}")

    cursor.close()
    conn.close()
    pause()


# ══════════════════════════════════════════════
#  Q7 — TOTAL AMOUNT PAID BY OUTDOOR PATIENTS
# ══════════════════════════════════════════════

def total_outdoor_amount():
    """Program 7: Calculate total amount paid by all outdoor patients."""
    clear_screen()
    print("  PROGRAM 7 — TOTAL AMOUNT: OUTDOOR PATIENTS")
    print_separator()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT PSrno, pname, Amount
                      FROM Patient_Records
                      ORDER BY PSrno""")
    rows = cursor.fetchall()

    if not rows:
        print("  No outdoor patient records found.")
        cursor.close()
        conn.close()
        pause()
        return

    cursor.execute("SELECT COUNT(*), SUM(Amount) FROM Patient_Records")
    count, total = cursor.fetchone()

    print(f"\n  {'SrNo':<8} {'Patient Name':<35} {'Amount (₹)':>12}")
    print_separator()
    for row in rows:
        amt = row[2] if row[2] is not None else 0.0
        print(f"  {row[0]:<8} {row[1]:<35} {float(amt):>12,.2f}")
    print_separator()
    print(f"  {'Total Patients:':<44} {count}")
    print(f"  {'TOTAL AMOUNT COLLECTED (₹):':<44} {float(total or 0):>12,.2f}")
    print_separator()

    cursor.close()
    conn.close()
    pause()


# ══════════════════════════════════════════════
#  Q8 — MAIN MENU (connects all 6 programs)
# ══════════════════════════════════════════════

def main_menu():
    """Program 8: Main menu connecting all programs."""
    while True:
        clear_screen()
        print("=" * 60)
        print("    HOSPITAL PATIENT DATA MANAGEMENT SYSTEM")
        print("=" * 60)
        print("  1. Add Doctor Records")
        print("  2. Add Hospitalized Patient")
        print("  3. Display All Outdoor Patient Records")
        print("  4. Patient Discharge & Bill Calculation")
        print("  5. Display All Rehab Records")
        print("  6. Add Outdoor Patient Record")
        print("  7. Total Amount — Outdoor Patients")
        print("  0. Exit")
        print("=" * 60)

        choice = input("  Enter your choice: ").strip()

        if   choice == "1": add_doctor_records()
        elif choice == "2": add_hospitalized_patient()
        elif choice == "3": display_outdoor_patients()
        elif choice == "4": discharge_patient()
        elif choice == "5": display_rehab_records()
        elif choice == "6": add_outdoor_patient()
        elif choice == "7": total_outdoor_amount()
        elif choice == "0":
            print("\n  Goodbye! Stay healthy. 🏥\n")
            sys.exit()
        else:
            print("  Invalid choice. Please try again.")
            pause()


# ══════════════════════════════════════════
#  PROGRAM ENTRY POINT
# ══════════════════════════════════════════════

if __name__ == "__main__":
    password_check()   # Q9 — password gate
    main_menu()        # Q8 — launch main menu
