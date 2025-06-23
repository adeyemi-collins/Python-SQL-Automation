import pyodbc


# Reusable connection function
def get_connection(database="PhoneDB"):
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=CYBERCROWN\\SQLEXPRESS;'
            f'DATABASE={database};'
            'UID=python_user;'
            'PWD=YourSecurePassword123!;'
            'TrustServerCertificate=yes;',
            timeout=5
        )
        print(f"✅ Connected to {database}")
        return conn
    except pyodbc.Error as e:
        print(f"❌ Could not connect to {database}: {e}")
        raise  # Stop the program or let you debug


def create_database():
    try:
        # Connect to the server without specifying a database
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=CYBERCROWN\\SQLEXPRESS;'
            'UID=python_user;'
            'PWD=YourSecurePassword123!;'
            'TrustServerCertificate=yes;',
            autocommit=True
        )
        cursor = conn.cursor()
        cursor.execute("IF DB_ID('PhoneDB') IS NULL CREATE DATABASE PhoneDB;")
        print("✅ Database created or already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error creating database:", e)

def create_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        IF OBJECT_ID('phone', 'U') IS NULL
        CREATE TABLE phone (
            phone_id INT PRIMARY KEY,
            country_code INT NOT NULL,
            phone_number BIGINT NOT NULL,
            phone_type VARCHAR(12)
        );
        """)
        conn.commit()
        print("✅ Table created.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error creating table:", e)

def select_us_numbers():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM phone WHERE country_code = 1")
        rows = cursor.fetchall()
        for row in rows:
            print("📞 US Number:", row.phone_number)
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error selecting rows:", e)

def update_phone_types():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE phone SET phone_type = 'MOBILE' WHERE phone_type = 'CELLULAR'")
        conn.commit()
        print("✅ Phone types updated.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error updating phone types:", e)

def delete_xx_records():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM phone WHERE country_code = 99")  # Assuming 99 is 'XX'
        conn.commit()
        print("✅ XX records deleted.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error deleting records:", e)

def drop_phone_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        #cursor.execute("DROP TABLE IF EXISTS phone")
        conn.commit()
        #print("✅ Phone table dropped.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error dropping table:", e)

def insert_sample_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO phone (phone_id, country_code, phone_number, phone_type)
            VALUES (?, ?, ?, ?)
        """, [
            (1, 1, 5551234567, 'CELLULAR'),
            (2, 1, 5557654321, 'HOME'),
            (3, 44, 2071234567, 'WORK'),
            (4, 99, 9999999999, 'UNKNOWN')  # This will be deleted by your XX delete step
        ])
        conn.commit()
        print("✅ Sample data inserted.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error inserting sample data:", e)


def main():
    create_database()
    create_table()
    insert_sample_data()  
    select_us_numbers()
    update_phone_types()
    delete_xx_records()
    # drop_phone_table()  ← You may want to COMMENT THIS OUT while testing

if __name__ == "__main__":
    main()
