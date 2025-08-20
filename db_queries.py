import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path='food_waste.db'):
        self.db_path = db_path
    
    def get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def execute_query(self, query, params=None):
        conn = self.get_connection()
        if conn is None:
            print("Database connection failed")
            return pd.DataFrame()
        
        try:
            if params:
                df = pd.read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            print(f"Query: {query}")
            if params:
                print(f"Params: {params}")
            return pd.DataFrame()
        finally:
            conn.close()
    
    # Query 1: Get all food listings
    def get_all_food_listings(self):
        query = '''
        SELECT fl.*, p.Name as Provider_Name, p.Contact as Provider_Contact, p.City as Provider_City
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        '''
        return self.execute_query(query)
    
    # Query 2: Get food listings by city
    def get_food_by_city(self, city):
        query = '''
        SELECT fl.*, p.Name as Provider_Name, p.Contact as Provider_Contact
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE p.City = ?
        '''
        return self.execute_query(query, (city,))
    
    # Query 3: Get food listings by food type
    def get_food_by_type(self, food_type):
        query = '''
        SELECT fl.*, p.Name as Provider_Name, p.Contact as Provider_Contact
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE fl.Food_Type = ?
        '''
        return self.execute_query(query, (food_type,))
    
    # Query 4: Get food listings by meal type
    def get_food_by_meal_type(self, meal_type):
        query = '''
        SELECT fl.*, p.Name as Provider_Name, p.Contact as Provider_Contact
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE fl.Meal_Type = ?
        '''
        return self.execute_query(query, (meal_type,))
    
    # Query 5: Get food listings by provider type
    def get_food_by_provider_type(self, provider_type):
        query = '''
        SELECT fl.*, p.Name as Provider_Name, p.Contact as Provider_Contact
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE fl.Provider_Type = ?
        '''
        return self.execute_query(query, (provider_type,))
    
    # Query 6: Get food listings expiring soon
    def get_food_expiring_soon(self, days=3):
        query = '''
        SELECT fl.*, p.Name as Provider_Name, p.Contact as Provider_Contact
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE date(fl.Expiry_Date) <= date('now', '+{} days')
        ORDER BY fl.Expiry_Date
        '''.format(days)
        return self.execute_query(query)
    
    # Query 7: Get claims by status
    def get_claims_by_status(self, status):
        query = '''
        SELECT c.*, fl.Food_Name, r.Name as Receiver_Name, r.Contact as Receiver_Contact
        FROM claims c
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        WHERE c.Status = ?
        '''
        return self.execute_query(query, (status,))
    
    # Query 8: Get providers by city
    def get_providers_by_city(self, city):
        query = '''
        SELECT * FROM providers
        WHERE City = ?
        '''
        return self.execute_query(query, (city,))
    
    # Query 9: Get receivers by city
    def get_receivers_by_city(self, city):
        query = '''
        SELECT * FROM receivers
        WHERE City = ?
        '''
        return self.execute_query(query, (city,))
    
    # Query 10: Get food waste statistics by food type
    def get_waste_stats_by_food_type(self):
        query = '''
        SELECT 
            Food_Type,
            COUNT(*) as Total_Listings,
            SUM(Quantity) as Total_Quantity,
            AVG(Quantity) as Avg_Quantity
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Total_Quantity DESC
        '''
        return self.execute_query(query)
    
    # Query 11: Get food waste statistics by provider type
    def get_waste_stats_by_provider_type(self):
        query = '''
        SELECT 
            Provider_Type,
            COUNT(*) as Total_Listings,
            SUM(Quantity) as Total_Quantity,
            AVG(Quantity) as Avg_Quantity
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY Total_Quantity DESC
        '''
        return self.execute_query(query)
    
    # Query 12: Get food waste statistics by city
    def get_waste_stats_by_city(self):
        query = '''
        SELECT 
            p.City,
            COUNT(*) as Total_Listings,
            SUM(fl.Quantity) as Total_Quantity,
            AVG(fl.Quantity) as Avg_Quantity
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        GROUP BY p.City
        ORDER BY Total_Quantity DESC
        '''
        return self.execute_query(query)
    
    # Query 13: Get claims statistics
    def get_claims_statistics(self):
        query = '''
        SELECT 
            Status,
            COUNT(*) as Total_Claims,
            COUNT(DISTINCT Food_ID) as Unique_Food_Items,
            COUNT(DISTINCT Receiver_ID) as Unique_Receivers
        FROM claims
        GROUP BY Status
        '''
        return self.execute_query(query)
    
    # Query 14: Get top providers by quantity
    def get_top_providers(self, limit=10):
        query = '''
        SELECT 
            p.Name,
            p.City,
            COUNT(fl.Food_ID) as Total_Listings,
            SUM(fl.Quantity) as Total_Quantity
        FROM providers p
        JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
        GROUP BY p.Provider_ID
        ORDER BY Total_Quantity DESC
        LIMIT ?
        '''
        return self.execute_query(query, (limit,))
    
    # Query 15: Get expiring food by city
    def get_expiring_food_by_city(self, city, days=3):
        query = '''
        SELECT 
            fl.Food_Name,
            fl.Quantity,
            fl.Expiry_Date,
            p.Name as Provider_Name,
            p.Contact as Provider_Contact
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE p.City = ? AND date(fl.Expiry_Date) <= date('now', '+{} days')
        ORDER BY fl.Expiry_Date
        '''.format(days)
        return self.execute_query(query, (city,))
# Add these methods to your db_queries.py file

def get_available_food(self):
    """Get all available (non-expired) food listings"""
    query = """
    SELECT *
    FROM food_listings
    WHERE Expiry_Date >= date('now')
    """
    return self.execute_query(query)

def get_expired_food(self):
    """Get all expired food items"""
    query = """
    SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date, p.Name AS Provider_Name
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE f.Expiry_Date < date('now')
    """
    return self.execute_query(query)

def get_donations_by_city(self):
    """Count total donations per city"""
    query = """
    SELECT p.City, COUNT(*) AS Total_Donations
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.City
    ORDER BY Total_Donations DESC
    """
    return self.execute_query(query)

def get_donations_by_food_type(self):
    """Count donations by food type"""
    query = """
    SELECT f.Food_Type, COUNT(*) AS Total_Donations
    FROM food_listings f
    GROUP BY f.Food_Type
    ORDER BY Total_Donations DESC
    """
    return self.execute_query(query)

def get_donations_by_meal_type(self):
    """Donations per meal type"""
    query = """
    SELECT f.Meal_Type, COUNT(*) AS Total_Donations
    FROM food_listings f
    GROUP BY f.Meal_Type
    ORDER BY Total_Donations DESC
    """
    return self.execute_query(query)

def get_most_active_providers(self):
    """Most active providers (by number of donations)"""
    query = """
    SELECT p.Name AS Provider_Name, COUNT(*) AS Total_Donations
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.Name
    ORDER BY Total_Donations DESC
    """
    return self.execute_query(query)

def get_total_quantity_by_city(self):
    """Total quantity donated per city"""
    query = """
    SELECT p.City, SUM(f.Quantity) AS Total_Quantity
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.City
    ORDER BY Total_Quantity DESC
    """
    return self.execute_query(query)

def get_claims_by_receiver(self):
    """Claims count by receiver"""
    query = """
    SELECT r.Name AS Receiver_Name, COUNT(*) AS Total_Claims
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    GROUP BY r.Name
    ORDER BY Total_Claims DESC
    """
    return self.execute_query(query)

def get_claims_by_receiver_city(self):
    """Claims by city (based on receiver city)"""
    query = """
    SELECT r.City, COUNT(*) AS Total_Claims
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    GROUP BY r.City
    ORDER BY Total_Claims DESC
    """
    return self.execute_query(query)

def get_unclaimed_food(self):
    """Unclaimed food donations"""
    query = """
    SELECT f.Food_ID, f.Food_Name, f.Quantity, p.Name AS Provider_Name
    FROM food_listings f
    LEFT JOIN claims c ON f.Food_ID = c.Food_ID
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE c.Claim_ID IS NULL
    """
    return self.execute_query(query)

def get_claims_by_food_type(self):
    """Number of claims per food type"""
    query = """
    SELECT f.Food_Type, COUNT(c.Claim_ID) AS Total_Claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Type
    ORDER BY Total_Claims DESC
    """
    return self.execute_query(query)

def get_avg_quantity_by_food_type(self):
    """Average quantity donated per food type"""
    query = """
    SELECT f.Food_Type, AVG(f.Quantity) AS Avg_Quantity
    FROM food_listings f
    GROUP BY f.Food_Type
    ORDER BY Avg_Quantity DESC
    """
    return self.execute_query(query)

def get_most_claimed_food(self):
    """Top most claimed food items"""
    query = """
    SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claim_Count
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Name
    ORDER BY Claim_Count DESC
    """
    return self.execute_query(query)

def get_claim_status_breakdown(self):
    """Claims status breakdown"""
    query = """
    SELECT Status, COUNT(*) AS Status_Count
    FROM claims
    GROUP BY Status
    """
    return self.execute_query(query)

def get_donation_vs_claimed(self):
    """Total donations vs. claimed donations"""
    query = """
    SELECT 
        (SELECT COUNT(*) FROM food_listings) AS Total_Donations,
        (SELECT COUNT(DISTINCT Food_ID) FROM claims) AS Claimed_Donations
    """
    return self.execute_query(query)

def get_claims_daily_trend(self):
    """Daily trend of claims"""
    query = """
    SELECT date(Timestamp) AS Claim_Date, COUNT(*) AS Total_Claims
    FROM claims
    GROUP BY Claim_Date
    ORDER BY Claim_Date
    """
    return self.execute_query(query)

def get_food_nearing_expiry(self):
    """Food items nearing expiry in the next 2 days"""
    query = """
    SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date, p.Name AS Provider_Name, p.City
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE f.Expiry_Date BETWEEN date('now') AND date('now', '+2 days')
    ORDER BY f.Expiry_Date ASC
    """
    return self.execute_query(query)

def get_expiry_date_range(self):
    """See the earliest and latest expiry dates"""
    query = """
    SELECT MIN(Expiry_Date) AS Earliest, MAX(Expiry_Date) AS Latest
    FROM food_listings
    """
    return self.execute_query(query)

def get_null_expiry_count(self):
    """See how many have NULL expiry dates"""
    query = """
    SELECT COUNT(*) AS Null_Expiry
    FROM food_listings
    WHERE Expiry_Date IS NULL
    """
    return self.execute_query(query)

def get_food_with_provider_details(self):
    """Get food listings with provider details"""
    query = """
    SELECT
        f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date,
        f.Provider_ID, f.Provider_Type, f.Location,
        f.Food_Type, f.Meal_Type,
        p.Name AS Provider_Name,
        p.City AS Provider_City
    FROM food_listings f
    JOIN providers p ON p.Provider_ID = f.Provider_ID
    """
    return self.execute_query(query)

def get_claims_full_details(self):
    """Get claims with full details"""
    query = """
    SELECT
        c.Claim_ID, c.Status, c.Timestamp,
        f.Food_ID, f.Food_Name, f.Food_Type, f.Meal_Type, f.Quantity, f.Expiry_Date,
        p.Provider_ID, p.Name AS Provider_Name, p.City AS Provider_City,
        r.Receiver_ID, r.Name AS Receiver_Name, r.City AS Receiver_City
    FROM claims c
    JOIN food_listings f ON f.Food_ID = c.Food_ID
    JOIN providers p ON p.Provider_ID = f.Provider_ID
    JOIN receivers r ON r.Receiver_ID = c.Receiver_ID
    """
    return self.execute_query(query)    