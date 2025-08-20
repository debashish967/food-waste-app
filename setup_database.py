import sqlite3
import pandas as pd
import os

def create_database():
    try:
        # Connect to SQLite database (or create if it doesn't exist)
        conn = sqlite3.connect('food_waste.db')
        cursor = conn.cursor()
        
        # Drop existing tables if they exist
        cursor.execute('DROP TABLE IF EXISTS claims')
        cursor.execute('DROP TABLE IF EXISTS food_listings')
        cursor.execute('DROP TABLE IF EXISTS providers')
        cursor.execute('DROP TABLE IF EXISTS receivers')
        
        # Create tables based on your CSV structure
        cursor.execute('''
        CREATE TABLE providers (
            Provider_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Type TEXT,
            Address TEXT,
            City TEXT,
            Contact TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE food_listings (
            Food_ID INTEGER PRIMARY KEY,
            Food_Name TEXT NOT NULL,
            Quantity INTEGER,
            Expiry_Date TEXT,
            Provider_ID INTEGER,
            Provider_Type TEXT,
            Location TEXT,
            Food_Type TEXT,
            Meal_Type TEXT,
            FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE receivers (
            Receiver_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Type TEXT,
            City TEXT,
            Contact TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE claims (
            Claim_ID INTEGER PRIMARY KEY,
            Food_ID INTEGER,
            Receiver_ID INTEGER,
            Status TEXT,
            Timestamp TEXT,
            FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
            FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
        )
        ''')
        
        # Load CSV data into DataFrames
        print("Loading CSV files...")
        
        # Check if files exist
        files = ['providers.csv', 'food_listings.csv', 'receivers.csv', 'claims.csv']
        for file in files:
            if os.path.exists(file):
                print(f"Found {file}")
            else:
                print(f"Warning: {file} not found!")
        
        # Load data with error handling
        try:
            providers_df = pd.read_csv('providers.csv')
            print(f"Providers CSV shape: {providers_df.shape}")
            print(f"Providers columns: {list(providers_df.columns)}")
        except Exception as e:
            print(f"Error loading providers.csv: {e}")
            providers_df = pd.DataFrame()
        
        try:
            food_listings_df = pd.read_csv('food_listings.csv')
            print(f"Food Listings CSV shape: {food_listings_df.shape}")
            print(f"Food Listings columns: {list(food_listings_df.columns)}")
        except Exception as e:
            print(f"Error loading food_listings.csv: {e}")
            food_listings_df = pd.DataFrame()
        
        try:
            receivers_df = pd.read_csv('receivers.csv')
            print(f"Receivers CSV shape: {receivers_df.shape}")
            print(f"Receivers columns: {list(receivers_df.columns)}")
        except Exception as e:
            print(f"Error loading receivers.csv: {e}")
            receivers_df = pd.DataFrame()
        
        try:
            claims_df = pd.read_csv('claims.csv')
            print(f"Claims CSV shape: {claims_df.shape}")
            print(f"Claims columns: {list(claims_df.columns)}")
        except Exception as e:
            print(f"Error loading claims.csv: {e}")
            claims_df = pd.DataFrame()
        
        # Insert data into tables if DataFrames are not empty
        if not providers_df.empty:
            providers_df.to_sql('providers', conn, if_exists='append', index=False)
            print(f"Inserted {len(providers_df)} providers")
        
        if not food_listings_df.empty:
            food_listings_df.to_sql('food_listings', conn, if_exists='append', index=False)
            print(f"Inserted {len(food_listings_df)} food listings")
        
        if not receivers_df.empty:
            receivers_df.to_sql('receivers', conn, if_exists='append', index=False)
            print(f"Inserted {len(receivers_df)} receivers")
        
        if not claims_df.empty:
            claims_df.to_sql('claims', conn, if_exists='append', index=False)
            print(f"Inserted {len(claims_df)} claims")
        
        # Verify data insertion
        print("\nVerifying data insertion:")
        cursor.execute("SELECT COUNT(*) FROM providers")
        providers_count = cursor.fetchone()[0]
        print(f"Providers: {providers_count} rows")
        
        cursor.execute("SELECT COUNT(*) FROM food_listings")
        food_count = cursor.fetchone()[0]
        print(f"Food Listings: {food_count} rows")
        
        cursor.execute("SELECT COUNT(*) FROM receivers")
        receivers_count = cursor.fetchone()[0]
        print(f"Receivers: {receivers_count} rows")
        
        cursor.execute("SELECT COUNT(*) FROM claims")
        claims_count = cursor.fetchone()[0]
        print(f"Claims: {claims_count} rows")
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print("\nDatabase created and populated successfully!")
        
    except Exception as e:
        print(f"Error creating database: {e}")
        raise

if __name__ == "__main__":
    create_database()