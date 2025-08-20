# ===============================
# Food Waste Management - app.py
# ===============================
# ---- imports (only imports before page_config) ----
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Initialize database
def init_db():
    conn = sqlite3.connect('food_waste.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS providers (
        Provider_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        City TEXT,
        Contact TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receivers (
        Receiver_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        City TEXT,
        Contact TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_listings (
        Food_ID INTEGER PRIMARY KEY,
        Food_Name TEXT,
        Quantity INTEGER,
        Expiry_Date DATE,
        Provider_ID INTEGER,
        Provider_Type TEXT,
        Location TEXT,
        Food_Type TEXT,
        Meal_Type TEXT,
        FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS claims (
        Claim_ID INTEGER PRIMARY KEY,
        Food_ID INTEGER,
        Receiver_ID INTEGER,
        Status TEXT,
        Timestamp DATETIME,
        FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
        FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
    )
    ''')
    
    # Load data from CSV if tables are empty
    if cursor.execute("SELECT COUNT(*) FROM providers").fetchone()[0] == 0:
        providers_df = pd.read_csv('providers.csv')
        providers_df.to_sql('providers', conn, if_exists='append', index=False)
    
    if cursor.execute("SELECT COUNT(*) FROM receivers").fetchone()[0] == 0:
        receivers_df = pd.read_csv('receivers.csv')
        receivers_df.to_sql('receivers', conn, if_exists='append', index=False)
    
    if cursor.execute("SELECT COUNT(*) FROM food_listings").fetchone()[0] == 0:
        food_df = pd.read_csv('food_listings.csv')
        food_df.to_sql('food_listings', conn, if_exists='append', index=False)
    
    if cursor.execute("SELECT COUNT(*) FROM claims").fetchone()[0] == 0:
        claims_df = pd.read_csv('claims.csv')
        claims_df.to_sql('claims', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Database connection
def get_connection():
    return sqlite3.connect('food_waste.db')

# CRUD Functions
def create_provider(name, type_, address, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO providers (Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?)",
                 (name, type_, address, city, contact))
    conn.commit()
    conn.close()

def get_providers():
    conn = get_connection()
    providers = pd.read_sql("SELECT * FROM providers", conn)
    conn.close()
    return providers

def update_provider(provider_id, name, type_, address, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE providers SET Name = ?, Type = ?, Address = ?, City = ?, Contact = ? WHERE Provider_ID = ?",
                 (name, type_, address, city, contact, provider_id))
    conn.commit()
    conn.close()

def delete_provider(provider_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM providers WHERE Provider_ID = ?", (provider_id,))
    conn.commit()
    conn.close()

# Similar CRUD functions for receivers, food_listings, and claims
def create_receiver(name, type_, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO receivers (Name, Type, City, Contact) VALUES (?, ?, ?, ?)",
                 (name, type_, city, contact))
    conn.commit()
    conn.close()

def get_receivers():
    conn = get_connection()
    receivers = pd.read_sql("SELECT * FROM receivers", conn)
    conn.close()
    return receivers

def update_receiver(receiver_id, name, type_, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE receivers SET Name = ?, Type = ?, City = ?, Contact = ? WHERE Receiver_ID = ?",
                 (name, type_, city, contact, receiver_id))
    conn.commit()
    conn.close()

def delete_receiver(receiver_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receivers WHERE Receiver_ID = ?", (receiver_id,))
    conn.commit()
    conn.close()

def create_food_listing(food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                 (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
    conn.commit()
    conn.close()

def get_food_listings():
    conn = get_connection()
    food_listings = pd.read_sql("SELECT * FROM food_listings", conn)
    conn.close()
    return food_listings

def update_food_listing(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE food_listings SET Food_Name = ?, Quantity = ?, Expiry_Date = ?, Provider_ID = ?, Provider_Type = ?, Location = ?, Food_Type = ?, Meal_Type = ? WHERE Food_ID = ?",
                 (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type, food_id))
    conn.commit()
    conn.close()

def delete_food_listing(food_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_listings WHERE Food_ID = ?", (food_id,))
    conn.commit()
    conn.close()

def create_claim(food_id, receiver_id, status, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO claims (Food_ID, Receiver_ID, Status, Timestamp) VALUES (?, ?, ?, ?)",
                 (food_id, receiver_id, status, timestamp))
    conn.commit()
    conn.close()

def get_claims():
    conn = get_connection()
    claims = pd.read_sql("SELECT * FROM claims", conn)
    conn.close()
    return claims

def update_claim(claim_id, food_id, receiver_id, status, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE claims SET Food_ID = ?, Receiver_ID = ?, Status = ?, Timestamp = ? WHERE Claim_ID = ?",
                 (food_id, receiver_id, status, timestamp, claim_id))
    conn.commit()
    conn.close()

def delete_claim(claim_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM claims WHERE Claim_ID = ?", (claim_id,))
    conn.commit()
    conn.close()

# Analytics functions
def get_kpi_data():
    conn = get_connection()
    
    # Total food items
    total_food = pd.read_sql("SELECT COUNT(*) FROM food_listings", conn).iloc[0,0]
    
    # Total providers
    total_providers = pd.read_sql("SELECT COUNT(*) FROM providers", conn).iloc[0,0]
    
    # Total receivers
    total_receivers = pd.read_sql("SELECT COUNT(*) FROM receivers", conn).iloc[0,0]
    
    # Total claims
    total_claims = pd.read_sql("SELECT COUNT(*) FROM claims", conn).iloc[0,0]
    
    # Claimed items
    claimed_items = pd.read_sql("SELECT COUNT(DISTINCT Food_ID) FROM claims WHERE Status = 'Claimed'", conn).iloc[0,0]
    
    # Pending claims
    pending_claims = pd.read_sql("SELECT COUNT(*) FROM claims WHERE Status = 'Pending'", conn).iloc[0,0]
    
    # Cancelled claims
    cancelled_claims = pd.read_sql("SELECT COUNT(*) FROM claims WHERE Status = 'Cancelled'", conn).iloc[0,0]
    
    # Expired food
    expired_food = pd.read_sql("SELECT COUNT(*) FROM food_listings WHERE Expiry_Date < date('now')", conn).iloc[0,0]
    
    conn.close()
    
    return {
        "total_food": total_food,
        "total_providers": total_providers,
        "total_receivers": total_receivers,
        "total_claims": total_claims,
        "claimed_items": claimed_items,
        "pending_claims": pending_claims,
        "cancelled_claims": cancelled_claims,
        "expired_food": expired_food
    }

def get_food_type_distribution():
    conn = get_connection()
    food_types = pd.read_sql("SELECT Food_Type, COUNT(*) as Count FROM food_listings GROUP BY Food_Type", conn)
    conn.close()
    return food_types

def get_meal_type_distribution():
    conn = get_connection()
    meal_types = pd.read_sql("SELECT Meal_Type, COUNT(*) as Count FROM food_listings GROUP BY Meal_Type", conn)
    conn.close()
    return meal_types

def get_provider_type_distribution():
    conn = get_connection()
    provider_types = pd.read_sql("SELECT Provider_Type, COUNT(*) as Count FROM food_listings GROUP BY Provider_Type", conn)
    conn.close()
    return provider_types

def get_claim_status_distribution():
    conn = get_connection()
    claim_status = pd.read_sql("SELECT Status, COUNT(*) as Count FROM claims GROUP BY Status", conn)
    conn.close()
    return claim_status

def get_expiry_trend():
    conn = get_connection()
    expiry_trend = pd.read_sql("""
        SELECT 
            CASE 
                WHEN Expiry_Date < date('now') THEN 'Expired'
                WHEN Expiry_Date BETWEEN date('now') AND date('now', '+3 days') THEN 'Expiring Soon'
                WHEN Expiry_Date BETWEEN date('now', '+4 days') AND date('now', '+7 days') THEN 'Expiring This Week'
                ELSE 'Fresh'
            END as Expiry_Status,
            COUNT(*) as Count
        FROM food_listings
        GROUP BY Expiry_Status
    """, conn)
    conn.close()
    return expiry_trend

def get_city_distribution():
    conn = get_connection()
    city_dist = pd.read_sql("""
        SELECT p.City, COUNT(f.Food_ID) as Food_Count
        FROM providers p
        LEFT JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.City
        ORDER BY Food_Count DESC
    """, conn)
    conn.close()
    return city_dist

def get_recommendations():
    conn = get_connection()
    
    # Get food items expiring soon
    expiring_soon = pd.read_sql("""
        SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date, p.Name as Provider_Name, p.City
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE f.Expiry_Date BETWEEN date('now') AND date('now', '+3 days')
        ORDER BY f.Expiry_Date
    """, conn)
    
    # Get most active receivers
    active_receivers = pd.read_sql("""
        SELECT r.Name, r.City, COUNT(c.Claim_ID) as Claim_Count
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Receiver_ID
        ORDER BY Claim_Count DESC
        LIMIT 5
    """, conn)
    
    # Get food types with high demand
    high_demand = pd.read_sql("""
        SELECT f.Food_Type, COUNT(c.Claim_ID) as Claim_Count
        FROM food_listings f
        JOIN claims c ON f.Food_ID = c.Food_ID
        GROUP BY f.Food_Type
        ORDER BY Claim_Count DESC
        LIMIT 5
    """, conn)
    
    # Get providers with high cancellation rates
    high_cancellation = pd.read_sql("""
        SELECT p.Name, p.City, 
               COUNT(c.Claim_ID) as Total_Claims,
               SUM(CASE WHEN c.Status = 'Cancelled' THEN 1 ELSE 0 END) as Cancelled_Claims,
               (SUM(CASE WHEN c.Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(c.Claim_ID)) as Cancellation_Rate
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        JOIN claims c ON f.Food_ID = c.Food_ID
        GROUP BY p.Provider_ID
        HAVING Cancellation_Rate > 20
        ORDER BY Cancellation_Rate DESC
    """, conn)
    
    conn.close()
    
    return {
        "expiring_soon": expiring_soon,
        "active_receivers": active_receivers,
        "high_demand": high_demand,
        "high_cancellation": high_cancellation
    }

# Page setup
st.set_page_config(
    page_title="Food Wastage Management System",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #6c757d;
    }
    .chart-container {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .dataframe-container {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .recommendation-card {
        background-color: #E3F2FD;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: #333333;  /* Changed to dark grey */
    }
    .recommendation-title {
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 4px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
</style>
""", unsafe_allow_html=True)

# Main app
st.markdown('<h1 class="main-header">Food Wastage Management System</h1>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", [
    "Dashboard", 
    "Providers", 
    "Receivers", 
    "Food Listings", 
    "Claims",
    "Analytics",
    "Map View",
    "Recommendations"
])

# Dashboard
if page == "Dashboard":
    st.header("Dashboard Overview")
    
    # Get KPI data
    kpi_data = get_kpi_data()
    
    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Food Items</div>
        </div>
        """.format(kpi_data["total_food"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Providers</div>
        </div>
        """.format(kpi_data["total_providers"]), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Receivers</div>
        </div>
        """.format(kpi_data["total_receivers"]), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Claims</div>
        </div>
        """.format(kpi_data["total_claims"]), unsafe_allow_html=True)
    
    # Second row of KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Claimed Items</div>
        </div>
        """.format(kpi_data["claimed_items"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Pending Claims</div>
        </div>
        """.format(kpi_data["pending_claims"]), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Cancelled Claims</div>
        </div>
        """.format(kpi_data["cancelled_claims"]), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Expired Food</div>
        </div>
        """.format(kpi_data["expired_food"]), unsafe_allow_html=True)
    
    # Charts
    st.subheader("Food Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_types = get_food_type_distribution()
        fig_food_type = px.pie(food_types, values='Count', names='Food_Type', title="Food Type Distribution")
        st.plotly_chart(fig_food_type, use_container_width=True)
    
    with col2:
        meal_types = get_meal_type_distribution()
        fig_meal_type = px.pie(meal_types, values='Count', names='Meal_Type', title="Meal Type Distribution")
        st.plotly_chart(fig_meal_type, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        provider_types = get_provider_type_distribution()
        fig_provider_type = px.bar(provider_types, x='Provider_Type', y='Count', title="Provider Type Distribution")
        st.plotly_chart(fig_provider_type, use_container_width=True)
    
    with col2:
        claim_status = get_claim_status_distribution()
        fig_claim_status = px.bar(claim_status, x='Status', y='Count', title="Claim Status Distribution")
        st.plotly_chart(fig_claim_status, use_container_width=True)
    
    # Expiry trend
    st.subheader("Expiry Status")
    expiry_trend = get_expiry_trend()
    fig_expiry = px.bar(expiry_trend, x='Expiry_Status', y='Count', title="Food Expiry Status")
    st.plotly_chart(fig_expiry, use_container_width=True)

# Providers Management
elif page == "Providers":
    st.header("Providers Management")
    
    # Create new provider
    with st.expander("Add New Provider"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Provider Name")
            type_ = st.selectbox("Type", ["Restaurant", "Grocery Store", "Catering Service", "Supermarket", "NGO", "Individual"])
            address = st.text_input("Address")
        
        with col2:
            city = st.text_input("City")
            contact = st.text_input("Contact")
        
        if st.button("Add Provider"):
            create_provider(name, type_, address, city, contact)
            st.success("Provider added successfully!")
    
    # Display providers
    st.subheader("Providers List")
    providers = get_providers()
    st.dataframe(providers, use_container_width=True)
    
    # Update provider
    st.subheader("Update Provider")
    provider_id = st.number_input("Provider ID to Update", min_value=1)
    
    if provider_id in providers['Provider_ID'].values:
        provider_data = providers[providers['Provider_ID'] == provider_id].iloc[0]
        
        with st.form("update_provider_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Provider Name", value=provider_data['Name'])
                type_ = st.selectbox("Type", ["Restaurant", "Grocery Store", "Catering Service", "Supermarket", "NGO", "Individual"], 
                                      index=["Restaurant", "Grocery Store", "Catering Service", "Supermarket", "NGO", "Individual"].index(provider_data['Type']))
                address = st.text_input("Address", value=provider_data['Address'])
            
            with col2:
                city = st.text_input("City", value=provider_data['City'])
                contact = st.text_input("Contact", value=provider_data['Contact'])
            
            if st.form_submit_button("Update Provider"):
                update_provider(provider_id, name, type_, address, city, contact)
                st.success("Provider updated successfully!")
    else:
        st.warning("Provider ID not found")
    
    # Delete provider
    st.subheader("Delete Provider")
    delete_id = st.number_input("Provider ID to Delete", min_value=1)
    
    if st.button("Delete Provider"):
        if delete_id in providers['Provider_ID'].values:
            delete_provider(delete_id)
            st.success("Provider deleted successfully!")
        else:
            st.warning("Provider ID not found")

# Receivers Management
elif page == "Receivers":
    st.header("Receivers Management")
    
    # Create new receiver
    with st.expander("Add New Receiver"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Receiver Name")
            type_ = st.selectbox("Type", ["Shelter", "NGO", "Individual", "Charity", "Community Center"])
        
        with col2:
            city = st.text_input("City")
            contact = st.text_input("Contact")
        
        if st.button("Add Receiver"):
            create_receiver(name, type_, city, contact)
            st.success("Receiver added successfully!")
    
    # Display receivers
    st.subheader("Receivers List")
    receivers = get_receivers()
    st.dataframe(receivers, use_container_width=True)
    
    # Update receiver
    st.subheader("Update Receiver")
    receiver_id = st.number_input("Receiver ID to Update", min_value=1)
    
    if receiver_id in receivers['Receiver_ID'].values:
        receiver_data = receivers[receivers['Receiver_ID'] == receiver_id].iloc[0]
        
        with st.form("update_receiver_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Receiver Name", value=receiver_data['Name'])
                type_ = st.selectbox("Type", ["Shelter", "NGO", "Individual", "Charity", "Community Center"], 
                                      index=["Shelter", "NGO", "Individual", "Charity", "Community Center"].index(receiver_data['Type']))
            
            with col2:
                city = st.text_input("City", value=receiver_data['City'])
                contact = st.text_input("Contact", value=receiver_data['Contact'])
            
            if st.form_submit_button("Update Receiver"):
                update_receiver(receiver_id, name, type_, city, contact)
                st.success("Receiver updated successfully!")
    else:
        st.warning("Receiver ID not found")
    
    # Delete receiver
    st.subheader("Delete Receiver")
    delete_id = st.number_input("Receiver ID to Delete", min_value=1)
    
    if st.button("Delete Receiver"):
        if delete_id in receivers['Receiver_ID'].values:
            delete_receiver(delete_id)
            st.success("Receiver deleted successfully!")
        else:
            st.warning("Receiver ID not found")

# Food Listings Management
elif page == "Food Listings":
    st.header("Food Listings Management")
    
    # Create new food listing
    with st.expander("Add New Food Listing"):
        col1, col2 = st.columns(2)
        
        with col1:
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1)
            provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Catering Service", "Supermarket", "NGO", "Individual"])
        
        with col2:
            location = st.text_input("Location")
            food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        
        if st.button("Add Food Listing"):
            create_food_listing(food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            st.success("Food listing added successfully!")
    
    # Display food listings
    st.subheader("Food Listings")
    food_listings = get_food_listings()
    st.dataframe(food_listings, use_container_width=True)
    
    # Update food listing
    st.subheader("Update Food Listing")
    food_id = st.number_input("Food ID to Update", min_value=1)
    
    if food_id in food_listings['Food_ID'].values:
        food_data = food_listings[food_listings['Food_ID'] == food_id].iloc[0]
        
        with st.form("update_food_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                food_name = st.text_input("Food Name", value=food_data['Food_Name'])
                quantity = st.number_input("Quantity", min_value=1, value=int(food_data['Quantity']))
                expiry_date = st.date_input("Expiry Date", value=pd.to_datetime(food_data['Expiry_Date']).date())
                provider_id = st.number_input("Provider ID", min_value=1, value=int(food_data['Provider_ID']))
                provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Catering Service", "Supermarket", "NGO", "Individual"], 
                                      index=["Restaurant", "Grocery Store", "Catering Service", "Supermarket", "NGO", "Individual"].index(food_data['Provider_Type']))
            
            with col2:
                location = st.text_input("Location", value=food_data['Location'])
                food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"], 
                                      index=["Vegetarian", "Non-Vegetarian", "Vegan"].index(food_data['Food_Type']))
                meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"], 
                                      index=["Breakfast", "Lunch", "Dinner", "Snacks"].index(food_data['Meal_Type']))
            
            if st.form_submit_button("Update Food Listing"):
                update_food_listing(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                st.success("Food listing updated successfully!")
    else:
        st.warning("Food ID not found")
    
    # Delete food listing
    st.subheader("Delete Food Listing")
    delete_id = st.number_input("Food ID to Delete", min_value=1)
    
    if st.button("Delete Food Listing"):
        if delete_id in food_listings['Food_ID'].values:
            delete_food_listing(delete_id)
            st.success("Food listing deleted successfully!")
        else:
            st.warning("Food ID not found")

# Claims Management
elif page == "Claims":
    st.header("Claims Management")
    
    # Create new claim
    with st.expander("Add New Claim"):
        col1, col2 = st.columns(2)
        
        with col1:
            food_id = st.number_input("Food ID", min_value=1)
            receiver_id = st.number_input("Receiver ID", min_value=1)
        
        with col2:
            status = st.selectbox("Status", ["Pending", "Claimed", "Cancelled"])
            timestamp = st.date_input("Timestamp")
        
        if st.button("Add Claim"):
            create_claim(food_id, receiver_id, status, timestamp)
            st.success("Claim added successfully!")
    
    # Display claims
    st.subheader("Claims List")
    claims = get_claims()
    st.dataframe(claims, use_container_width=True)
    
    # Update claim
    st.subheader("Update Claim")
    claim_id = st.number_input("Claim ID to Update", min_value=1)
    
    if claim_id in claims['Claim_ID'].values:
        claim_data = claims[claims['Claim_ID'] == claim_id].iloc[0]
        
        with st.form("update_claim_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                food_id = st.number_input("Food ID", min_value=1, value=int(claim_data['Food_ID']))
                receiver_id = st.number_input("Receiver ID", min_value=1, value=int(claim_data['Receiver_ID']))
            
            with col2:
                status = st.selectbox("Status", ["Pending", "Claimed", "Cancelled"], 
                                      index=["Pending", "Claimed", "Cancelled"].index(claim_data['Status']))
                timestamp = st.date_input("Timestamp", value=pd.to_datetime(claim_data['Timestamp']).date())
            
            if st.form_submit_button("Update Claim"):
                update_claim(claim_id, food_id, receiver_id, status, timestamp)
                st.success("Claim updated successfully!")
    else:
        st.warning("Claim ID not found")
    
    # Delete claim
    st.subheader("Delete Claim")
    delete_id = st.number_input("Claim ID to Delete", min_value=1)
    
    if st.button("Delete Claim"):
        if delete_id in claims['Claim_ID'].values:
            delete_claim(delete_id)
            st.success("Claim deleted successfully!")
        else:
            st.warning("Claim ID not found")

# Analytics
elif page == "Analytics":
    st.header("Food Wastage Analytics")
    
    # Get KPI data
    kpi_data = get_kpi_data()
    
    # Calculate rates
    claim_rate = (kpi_data["claimed_items"] / kpi_data["total_food"]) * 100 if kpi_data["total_food"] > 0 else 0
    pending_rate = (kpi_data["pending_claims"] / kpi_data["total_claims"]) * 100 if kpi_data["total_claims"] > 0 else 0
    cancellation_rate = (kpi_data["cancelled_claims"] / kpi_data["total_claims"]) * 100 if kpi_data["total_claims"] > 0 else 0
    expiry_rate = (kpi_data["expired_food"] / kpi_data["total_food"]) * 100 if kpi_data["total_food"] > 0 else 0
    
    # Display rates
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Claim Rate", f"{claim_rate:.1f}%")
    
    with col2:
        st.metric("Pending Rate", f"{pending_rate:.1f}%")
    
    with col3:
        st.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")
    
    with col4:
        st.metric("Expiry Rate", f"{expiry_rate:.1f}%")
    
    # System Overview
    st.subheader("System Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        city_dist = get_city_distribution()
        fig_city = px.bar(city_dist, x='City', y='Food_Count', title="Food Distribution by City")
        st.plotly_chart(fig_city, use_container_width=True)
    
    with col2:
        expiry_trend = get_expiry_trend()
        fig_expiry = px.bar(expiry_trend, x='Expiry_Status', y='Count', title="Expiry Status Distribution")
        st.plotly_chart(fig_expiry, use_container_width=True)
    
    # Donation Analysis
    st.subheader("Donation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_types = get_food_type_distribution()
        fig_food_type = px.pie(food_types, values='Count', names='Food_Type', title="Food Type Distribution")
        st.plotly_chart(fig_food_type, use_container_width=True)
    
    with col2:
        meal_types = get_meal_type_distribution()
        fig_meal_type = px.pie(meal_types, values='Count', names='Meal_Type', title="Meal Type Distribution")
        st.plotly_chart(fig_meal_type, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        provider_types = get_provider_type_distribution()
        fig_provider_type = px.bar(provider_types, x='Provider_Type', y='Count', title="Provider Type Distribution")
        st.plotly_chart(fig_provider_type, use_container_width=True)
    
    with col2:
        claim_status = get_claim_status_distribution()
        fig_claim_status = px.bar(claim_status, x='Status', y='Count', title="Claim Status Distribution")
        st.plotly_chart(fig_claim_status, use_container_width=True)
    
    # Claim Analysis
    st.subheader("Claim Analysis")
    
    conn = get_connection()
    
    # Claims by receiver
    claims_by_receiver = pd.read_sql("""
        SELECT r.Name, r.City, COUNT(c.Claim_ID) as Claim_Count
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Receiver_ID
        ORDER BY Claim_Count DESC
        LIMIT 10
    """, conn)
    
    # Claims by city
    claims_by_city = pd.read_sql("""
        SELECT r.City, COUNT(c.Claim_ID) as Claim_Count
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.City
        ORDER BY Claim_Count DESC
    """, conn)
    
    conn.close()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_receiver = px.bar(claims_by_receiver, x='Name', y='Claim_Count', title="Top Receivers by Claim Count")
        st.plotly_chart(fig_receiver, use_container_width=True)
    
    with col2:
        fig_city = px.bar(claims_by_city, x='City', y='Claim_Count', title="Claims by City")
        st.plotly_chart(fig_city, use_container_width=True)
    
    # Expiry Analysis
    st.subheader("Expiry Analysis")
    
    conn = get_connection()
    
    # Expired food
    expired_food = pd.read_sql("""
        SELECT f.Food_Name, f.Expiry_Date, p.Name as Provider_Name, p.City
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE f.Expiry_Date < date('now')
        ORDER BY f.Expiry_Date DESC
    """, conn)
    
    # Food expiring soon
    expiring_soon = pd.read_sql("""
        SELECT f.Food_Name, f.Expiry_Date, p.Name as Provider_Name, p.City
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE f.Expiry_Date BETWEEN date('now') AND date('now', '+3 days')
        ORDER BY f.Expiry_Date
    """, conn)
    
    conn.close()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Expired Food")
        st.dataframe(expired_food, use_container_width=True)
    
    with col2:
        st.subheader("Food Expiring Soon")
        st.dataframe(expiring_soon, use_container_width=True)

# Map View
elif page == "Map View":
    st.header("Food Distribution Map")
    
    # Get city distribution data
    city_dist = get_city_distribution()
    
    # Create a simple map using Plotly
    # Note: This is a simplified map using city names
    # In a real application, you would use actual coordinates
    
    # Create a dataframe with sample coordinates for demonstration
    # In a real app, you would have actual lat/lon data
    cities = city_dist['City'].tolist()
    counts = city_dist['Food_Count'].tolist()
    
    # Sample coordinates for major cities (in a real app, you would use actual coordinates)
    city_coords = {
        "New York": [40.7128, -74.0060],
        "Los Angeles": [34.0522, -118.2437],
        "Chicago": [41.8781, -87.6298],
        "Houston": [29.7604, -95.3698],
        "Phoenix": [33.4484, -112.0740],
        "Philadelphia": [39.9526, -75.1652],
        "San Antonio": [29.4241, -98.4936],
        "San Diego": [32.7157, -117.1611],
        "Dallas": [32.7767, -96.7970],
        "San Jose": [37.3382, -121.8863]
    }
    
    # Create a dataframe with coordinates
    map_data = []
    for city, count in zip(cities, counts):
        if city in city_coords:
            map_data.append({
                "City": city,
                "Food_Count": count,
                "Lat": city_coords[city][0],
                "Lon": city_coords[city][1]
            })
    
    map_df = pd.DataFrame(map_data)
    
    # Create map
    fig = px.scatter_mapbox(
        map_df,
        lat="Lat",
        lon="Lon",
        size="Food_Count",
        color="Food_Count",
        hover_name="City",
        hover_data=["Food_Count"],
        zoom=3,
        height=500,
        title="Food Distribution by City",
        color_continuous_scale=px.colors.sequential.Blues,
        size_max=50
    )
    
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
    
    # Display city distribution data
    st.subheader("City Distribution Data")
    st.dataframe(city_dist, use_container_width=True)

# Recommendations
elif page == "Recommendations":
    st.header("Recommendations")
    
    # Get recommendations data
    recommendations = get_recommendations()
    
    # Food expiring soon
    st.subheader("Food Items Expiring Soon")
    st.dataframe(recommendations["expiring_soon"], use_container_width=True)
    
    st.markdown("""
    <div class="recommendation-card">
        <div class="recommendation-title">Recommendation</div>
        <div>Prioritize distribution of food items expiring within the next 3 days to minimize waste.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Most active receivers
    st.subheader("Most Active Receivers")
    st.dataframe(recommendations["active_receivers"], use_container_width=True)
    
    st.markdown("""
    <div class="recommendation-card">
        <div class="recommendation-title">Recommendation</div>
        <div>Consider partnering with the most active receivers to ensure efficient food distribution.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # High demand food types
    st.subheader("Food Types with High Demand")
    st.dataframe(recommendations["high_demand"], use_container_width=True)
    
    st.markdown("""
    <div class="recommendation-card">
        <div class="recommendation-title">Recommendation</div>
        <div>Encourage providers to donate more of the high-demand food types to better meet community needs.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Providers with high cancellation rates
    st.subheader("Providers with High Cancellation Rates")
    st.dataframe(recommendations["high_cancellation"], use_container_width=True)
    
    st.markdown("""
    <div class="recommendation-card">
        <div class="recommendation-title">Recommendation</div>
        <div>Work with providers who have high cancellation rates to improve their donation process and reliability.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional insights
    st.subheader("Additional Insights")
    
    conn = get_connection()
    
    # Most claimed food items
    most_claimed = pd.read_sql("""
        SELECT f.Food_Name, COUNT(c.Claim_ID) as Claim_Count
        FROM food_listings f
        JOIN claims c ON f.Food_ID = c.Food_ID
        WHERE c.Status = 'Claimed'
        GROUP BY f.Food_ID
        ORDER BY Claim_Count DESC
        LIMIT 10
    """, conn)
    
    # Unclaimed food items
    unclaimed = pd.read_sql("""
        SELECT f.Food_Name, f.Quantity, f.Expiry_Date, p.Name as Provider_Name
        FROM food_listings f
        LEFT JOIN claims c ON f.Food_ID = c.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Claim_ID IS NULL AND f.Expiry_Date >= date('now')
        ORDER BY f.Expiry_Date
    """, conn)
    
    conn.close()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Most Claimed Food Items")
        st.dataframe(most_claimed, use_container_width=True)
    
    with col2:
        st.subheader("Unclaimed Food Items")
        st.dataframe(unclaimed, use_container_width=True)