import sqlite3
import pandas as pd

def check_database():
    try:
        conn = sqlite3.connect('food_waste.db')
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:", [table[0] for table in tables])
        
        # Check each table
        for table in tables:
            table_name = table[0]
            print(f"\n=== Table: {table_name} ===")
            
            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns:", [col[1] for col in columns])
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Row count: {count}")
            
            # Show first 3 rows if available
            if count > 0:
                df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 3", conn)
                print("Sample data:")
                print(df)
            else:
                print("No data in this table")
        
        conn.close()
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_database()