# 🍱 Local Food Wastage Management System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-blueviolet?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

> **A data-driven platform that bridges the gap between surplus food providers and those in need — reducing food wastage through SQL-powered analytics and an interactive Streamlit web application.**

🔗 **Live App:** [food-waste-app on Streamlit Cloud](https://food-waste-app-vjf2knlzkhwdy4uwulsh3b.streamlit.app/)

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Business Use Cases](#-business-use-cases)
- [Project Architecture](#-project-architecture)
- [Tech Stack](#-tech-stack)
- [Dataset Description](#-dataset-description)
- [Features](#-features)
- [SQL Queries & Analysis](#-sql-queries--analysis)
- [File Structure](#-file-structure)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [App Pages Overview](#-app-pages-overview)
- [Results & Outcomes](#-results--outcomes)
- [Project Evaluation Metrics](#-project-evaluation-metrics)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 🚨 Problem Statement

Food wastage is a significant global issue. Households, restaurants, and grocery stores regularly discard surplus edible food while millions of people struggle with food insecurity. The core challenge is not a shortage of food — it is a **broken connection** between those who have surplus and those who need it.

This project aims to solve that by developing a **Local Food Wastage Management System** where:

- 🏪 Restaurants and individuals can **list surplus food**
- 🤝 NGOs or individuals in need can **claim the food**
- 🗄️ **SQL stores** all food details, provider information, and locations
- 📊 A **Streamlit app** enables interaction, filtering, CRUD operations, and visualization

---

## 💼 Business Use Cases

| Use Case | Description |
|---|---|
| 🔗 Connecting Providers & Receivers | A structured platform linking surplus food donors with those in need |
| ♻️ Reducing Food Waste | Redistributing excess food efficiently before it expires |
| 📍 Geolocation Accessibility | Locate nearby food availability using city-based filtering |
| 📈 Data-Driven Decisions | Analyze wastage trends to improve future food distribution strategies |

---

## 🏗️ Project Architecture

```
Data Sources (CSV Files)
        │
        ▼
SQLite Database (food_waste.db)
    ├── providers
    ├── receivers
    ├── food_listings
    └── claims
        │
        ▼
Python Backend (app.py)
    ├── CRUD Operations
    ├── SQL Query Engine (15 Queries)
    ├── Analytics Functions
    └── Recommendations Engine
        │
        ▼
Streamlit Frontend
    ├── Dashboard
    ├── Providers / Receivers Management
    ├── Food Listings / Claims Management
    ├── Analytics Page
    ├── Map View
    └── Recommendations
        │
        ▼
Streamlit Cloud Deployment (Live App)
```

**Data Flow:**
1. CSV datasets are loaded into SQLite tables on first run
2. CRUD operations update the database in real-time through the UI
3. SQL queries are executed dynamically to power all charts and analytics
4. Plotly renders interactive visualizations inside Streamlit

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Core programming language |
| **Streamlit** | Web application framework |
| **SQLite3** | Relational database for data storage |
| **Pandas** | Data manipulation and analysis |
| **Plotly Express** | Interactive data visualizations |
| **Plotly Graph Objects** | Custom chart components |
| **NumPy** | Numerical operations |
| **Datetime** | Date and expiry calculations |

---

## 📂 Dataset Description

The project uses **4 interlinked CSV datasets** that are loaded into SQLite tables on application startup.

### 1. `providers.csv` — Food Providers

| Column | Type | Description |
|---|---|---|
| Provider_ID | Integer | Unique identifier for each provider |
| Name | String | Name of the food provider (restaurant, store, etc.) |
| Type | String | Category: Restaurant, Grocery Store, Supermarket, etc. |
| Address | String | Physical address |
| City | String | City where the provider is located |
| Contact | String | Phone number or contact info |

### 2. `receivers.csv` — Food Receivers

| Column | Type | Description |
|---|---|---|
| Receiver_ID | Integer | Unique identifier for each receiver |
| Name | String | Name of the receiver (individual or organization) |
| Type | String | Category: NGO, Community Center, Individual, Shelter |
| City | String | City where the receiver is located |
| Contact | String | Contact details |

### 3. `food_listings.csv` — Available Food Items

| Column | Type | Description |
|---|---|---|
| Food_ID | Integer | Unique identifier for each food item |
| Food_Name | String | Name of the food item |
| Quantity | Integer | Available quantity for distribution |
| Expiry_Date | Date | Expiry date of the food item |
| Provider_ID | Integer | Foreign key → providers table |
| Provider_Type | String | Type of provider offering the food |
| Location | String | City where food is available |
| Food_Type | String | Vegetarian / Non-Vegetarian / Vegan |
| Meal_Type | String | Breakfast / Lunch / Dinner / Snacks |

### 4. `claims.csv` — Food Claims Tracking

| Column | Type | Description |
|---|---|---|
| Claim_ID | Integer | Unique identifier for each claim |
| Food_ID | Integer | Foreign key → food_listings table |
| Receiver_ID | Integer | Foreign key → receivers table |
| Status | String | Pending / Claimed / Cancelled |
| Timestamp | Datetime | Date and time the claim was made |

---

## ✨ Features

### 📊 Interactive Dashboard
- 8 KPI metric cards (Total Food Items, Providers, Receivers, Claims, Claimed, Pending, Cancelled, Expired)
- Pie charts: Food Type Distribution, Meal Type Distribution
- Bar charts: Provider Type Distribution, Claim Status Distribution
- Expiry Status visualization

### 🗄️ Full CRUD Operations
Complete **Create, Read, Update, Delete** for all 4 entities:
- ✅ Providers
- ✅ Receivers
- ✅ Food Listings
- ✅ Claims

### 📈 Analytics Page
- Claim Rate, Pending Rate, Cancellation Rate, Expiry Rate
- City-wise food distribution
- Top receivers by claim count
- Claims by city
- Expired food and food expiring soon tables

### 🗺️ Map View
- Geolocation-based visualization of food availability across cities

### 🤖 Recommendations Engine
- Lists food items expiring within 3 days — for urgent redistribution
- Identifies the most active receivers (top 5)
- Highlights high-demand food types
- Flags providers with cancellation rates above 20%

### 🔍 Filtering Options
- Filter by city, provider type, food type, and meal type
- Contact details of providers and receivers for direct coordination

---

## 📋 SQL Queries & Analysis

The project answers **15 key business questions** using SQL:

| # | Question | Category |
|---|---|---|
| 1 | How many food providers and receivers are there in each city? | Providers & Receivers |
| 2 | Which type of food provider contributes the most food? | Providers & Receivers |
| 3 | What is the contact info of food providers in a specific city? | Providers & Receivers |
| 4 | Which receivers have claimed the most food? | Providers & Receivers |
| 5 | What is the total quantity of food available from all providers? | Food Listings |
| 6 | Which city has the highest number of food listings? | Food Listings |
| 7 | What are the most commonly available food types? | Food Listings |
| 8 | How many food claims have been made for each food item? | Claims & Distribution |
| 9 | Which provider has the highest number of successful food claims? | Claims & Distribution |
| 10 | What percentage of claims are Completed vs Pending vs Cancelled? | Claims & Distribution |
| 11 | What is the average quantity of food claimed per receiver? | Analysis & Insights |
| 12 | Which meal type (breakfast, lunch, dinner, snacks) is claimed the most? | Analysis & Insights |
| 13 | What is the total quantity of food donated by each provider? | Analysis & Insights |
| 14 | Which food items are expiring within 3 days? | Expiry Analysis |
| 15 | Which providers have a cancellation rate above 20%? | Expiry Analysis |

**Example SQL Join used in the app:**

```sql
SELECT p.Name, p.City,
       COUNT(c.Claim_ID) as Total_Claims,
       SUM(CASE WHEN c.Status = 'Cancelled' THEN 1 ELSE 0 END) as Cancelled_Claims,
       (SUM(CASE WHEN c.Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(c.Claim_ID)) as Cancellation_Rate
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY p.Provider_ID
HAVING Cancellation_Rate > 20
ORDER BY Cancellation_Rate DESC;
```

---

## 📁 File Structure

```
food-waste-app/
│
├── app.py                  # Main Streamlit application (8 pages, full UI)
├── db_queries.py           # All 15 SQL queries as reusable functions
├── setup_database.py       # Database initialization and table creation
├── init_data.py            # Loads CSV data into SQLite on first run
├── deploy.py               # Deployment configuration
├── check_db.py             # Database health check utility
│
├── food_waste.db           # SQLite database file (auto-generated)
│
├── providers.csv           # Providers dataset
├── receivers.csv           # Receivers dataset
├── food_listings.csv       # Food listings dataset
├── claims.csv              # Claims dataset
│
├── requirements.txt        # Python dependencies
└── .gitignore              # Git ignore rules
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/debashish967/food-waste-app.git
cd food-waste-app
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies (`requirements.txt`)

```
streamlit
pandas
plotly
numpy
```

> **Note:** `sqlite3` is part of Python's standard library — no separate installation needed.

---

## ▶️ How to Run

```bash
streamlit run app.py
```

The app will open automatically in your browser at:
```
http://localhost:8501
```

On the **first run**, the database (`food_waste.db`) is automatically created and populated from the CSV files. No manual setup required.

---

## 📱 App Pages Overview

| Page | Description |
|---|---|
| **Dashboard** | KPI metrics overview + distribution charts |
| **Providers** | Full CRUD for food providers |
| **Receivers** | Full CRUD for food receivers |
| **Food Listings** | Full CRUD for food availability records |
| **Claims** | Full CRUD for food claims and status tracking |
| **Analytics** | Deep-dive analytics with rates, city trends, expiry analysis |
| **Map View** | Geolocation-based food availability map |
| **Recommendations** | Smart engine for expiry alerts and high-demand insights |

---

## ✅ Results & Outcomes

- 🟢 **Fully deployed Streamlit app** accessible via public URL
- 🟢 **Relational SQLite database** with 4 interconnected tables and foreign key integrity
- 🟢 **15 analytical SQL queries** with outputs covering all business questions
- 🟢 **CRUD operations** working live across all 4 entity types
- 🟢 **Interactive Plotly dashboards** with pie charts, bar charts, and KPI cards
- 🟢 **Recommendations engine** flagging expiring food and problematic providers
- 🟢 **Map View** for geolocation-based food discovery

---

## 📏 Project Evaluation Metrics

| Metric | Status |
|---|---|
| Completeness of SQL database with all food donation records | ✅ Done |
| Accuracy of SQL queries in analyzing food donation trends | ✅ Done |
| Functionality of CRUD operations for food listings and claims | ✅ Done |
| User-friendliness of the Streamlit interface | ✅ Done |
| Deployment and public accessibility | ✅ Done |

---

## 🚀 Future Enhancements

- 🔐 **User Authentication** — separate login portals for providers and receivers
- 📧 **Email/SMS Notifications** — alert receivers when food near them is about to expire
- 🗺️ **Real-time GPS Map** — integrate actual geolocation coordinates with live maps
- 📱 **Mobile-Responsive UI** — improve layout for mobile users
- 🤖 **ML-based Demand Forecasting** — predict which food types will be claimed fastest by city
- 📦 **Food Category Expansion** — support packaged goods, dry rations, beverages
- 🌐 **Multi-language Support** — for broader accessibility across regions

---

## 🏷️ Technical Tags

`Python` `SQL` `SQLite` `Streamlit` `Plotly` `Pandas` `Data Analysis` `CRUD` `Food Management` `Data Engineering` `Social Impact`

---

## 👨‍💻 Author

**Debashish**

- 🔗 GitHub: [@debashish967](https://github.com/debashish967)
- 🌐 Live App: [food-waste-app on Streamlit Cloud](https://food-waste-app-vjf2knlzkhwdy4uwulsh3b.streamlit.app/)

---

> *"Data is not just numbers — it can connect surplus to need, and turn waste into nourishment."*

---

⭐ If you found this project useful, consider giving it a **star** on GitHub!
