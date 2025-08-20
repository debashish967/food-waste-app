import sqlite3
import pandas as pd
import os

def create_sample_data():
    """Create sample data if CSV files are empty or missing"""
    conn = sqlite3.connect('food_waste.db')
    cursor = conn.cursor()
    
    # Check if we already have data
    cursor.execute("SELECT COUNT(*) FROM providers")
    providers_count = cursor.fetchone()[0]
    
    if providers_count > 0:
        print("Database already has data. Skipping sample data creation.")
        conn.close()
        return
    
    # Sample providers data
    providers_data = [
        (1, "Green Grocery", "Grocery Store", "123 Main St", "New York", "+1-123-456-7890"),
        (2, "Fresh Restaurant", "Restaurant", "456 Oak Ave", "Los Angeles", "+1-234-567-8901"),
        (3, "Helping Hands", "NGO", "789 Pine Rd", "Chicago", "+1-345-678-9012"),
        (4, "City Market", "Supermarket", "321 Elm St", "New York", "+1-456-789-0123"),
        (5, "Community Kitchen", "Catering Service", "654 Maple Dr", "Chicago", "+1-567-890-1234"),
    ]
    
    # Sample food listings data
    food_listings_data = [
        (1, "Apples", 10, "2025-03-20", 1, "Grocery Store", "123 Main St", "Fruits", "Snacks"),
        (2, "Bread", 5, "2025-03-18", 1, "Grocery Store", "123 Main St", "Bakery", "Breakfast"),
        (3, "Rice", 20, "2025-03-25", 2, "Restaurant", "456 Oak Ave", "Grains", "Lunch"),
        (4, "Vegetables", 15, "2025-03-22", 2, "Restaurant", "456 Oak Ave", "Vegetables", "Dinner"),
        (5, "Milk", 8, "2025-03-19", 4, "Supermarket", "321 Elm St", "Dairy", "Breakfast"),
        (6, "Chicken", 12, "2025-03-21", 2, "Restaurant", "456 Oak Ave", "Meat", "Dinner"),
        (7, "Pasta", 7, "2025-03-24", 5, "Catering Service", "654 Maple Dr", "Grains", "Lunch"),
        (8, "Salad", 10, "2025-03-23", 3, "NGO", "789 Pine Rd", "Vegetables", "Lunch"),
        (9, "Soup", 15, "2025-03-26", 5, "Catering Service", "654 Maple Dr", "Soup", "Dinner"),
        (10, "Yogurt", 6, "2025-03-20", 4, "Supermarket", "321 Elm St", "Dairy", "Snacks"),
    ]
    
    # Sample receivers data
    receivers_data = [
        (1, "City Shelter", "Shelter", "New York", "+1-111-222-3333"),
        (2, "Food Bank", "NGO", "Los Angeles", "+1-222-333-4444"),
        (3, "John Doe", "Individual", "Chicago", "+1-333-444-5555"),
        (4, "Community Center", "Charity", "New York", "+1-444-555-6666"),
        (5, "Salvation Army", "NGO", "Los Angeles", "+1-555-666-7777"),
    ]
    
    # Sample claims data
    claims_data = [
        (1, 1, 1, "Completed", "2025-03-10 10:00:00"),
        (2, 2, 2, "Pending", "2025-03-11 11:00:00"),
        (3, 3, 3, "Cancelled", "2025-03-12 12:00:00"),
        (4, 4, 4, "Completed", "2025-03-13 13:00:00"),
        (5, 5, 5, "Pending", "2025-03-14 14:00:00"),
        (6, 6, 1, "Completed", "2025-03-15 15:00:00"),
        (7, 7, 2, "Completed", "2025-03-16 16:00:00"),
        (8, 8, 3, "Pending", "2025-03-17 17:00:00"),
        (9, 9, 4, "Completed", "2025-03-18 18:00:00"),
        (10, 10, 5, "Cancelled", "2025-03-19 19:00:00"),
    ]
    
    # Insert sample data
    cursor.executemany("INSERT OR IGNORE INTO providers VALUES (?, ?, ?, ?, ?, ?)", providers_data)
    cursor.executemany("INSERT OR IGNORE INTO food_listings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", food_listings_data)
    cursor.executemany("INSERT OR IGNORE INTO receivers VALUES (?, ?, ?, ?, ?)", receivers_data)
    cursor.executemany("INSERT OR IGNORE INTO claims VALUES (?, ?, ?, ?, ?)", claims_data)
    
    conn.commit()
    conn.close()
    print("Sample data inserted successfully!")

if __name__ == "__main__":
    create_sample_data()