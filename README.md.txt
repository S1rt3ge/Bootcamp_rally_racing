# 🏁 Rally Racing Management App

A simple Streamlit app for managing rally racing cars, teams, and simulating races using Snowflake database.

## 🚀 Quick Setup Guide

### Step 1: Snowflake Setup
1. Log into your Snowflake account
2. Run all commands from `setup_database.sql` in a Snowflake worksheet
3. This creates the database, tables, and sample data

### Step 2: Local Setup
1. Create a new folder for your project
2. Copy all files to this folder:
   - `app.py` (main application)
   - `requirements.txt` (Python packages)
   - `setup_database.sql` (database setup)

### Step 3: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 4: Configure Snowflake Connection
1. Create folder: `.streamlit`
2. Inside `.streamlit` folder, create file: `secrets.toml`
3. Add your Snowflake credentials:

```toml
[snowflake]
user = "your_username"
password = "your_password"  
account = "your_account_identifier"
warehouse = "your_warehouse"
```

### Step 5: Run the App
```bash
streamlit run app.py
```

## 📁 File Structure
```
your_project_folder/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── setup_database.sql     # Snowflake database setup
├── .streamlit/
│   └── secrets.toml      # Snowflake credentials (create this)
└── README.md             # This file
```

## 🎮 How to Use

### 1. Dashboard 🏠
- View all cars and teams
- See current status

### 2. Manage Cars 🏎️
- View existing racing cars
- Add new cars with specifications:
  - Engine Power (150-400)
  - Weight (900-1500 kg)
  - Aerodynamics (30-100)
  - Tire Quality (50-100)

### 3. Manage Teams 👥
- View existing teams and budgets
- Add new racing teams
- Each team starts with $15,000 budget

### 4. Start Race! 🏁
- Simulates 100km rally race
- Entry fee: $1,000 per team
- Winner gets 60% of total entry fees
- Race results based on car characteristics + random factors

## 🔧 Features

- **Database**: Snowflake with proper schemas
- **Cars Management**: Add cars with racing specifications
- **Team Management**: Handle racing teams and budgets
- **Race Simulation**: 100km rally with realistic calculations
- **Budget System**: Entry fees and prize money
- **User-friendly**: Simple interface with emojis

## 📊 Database Schema

### racing_teams
- team_id, team_name, members, budget

### racing_cars  
- car_id, car_name, team_id, engine_power, weight_kg, aerodynamics, tire_quality

### race_results
- race_id, race_date, winning_team_id, total_participants, prize_amount, race_details

## 🎯 Race Algorithm

Car speed calculated from:
- Engine Power × 0.3
- Aerodynamics × 0.2  
- Tire Quality × 0.25
- Weight × -0.01
- Random factor (80%-120%)

Time = 100km ÷ speed

Fastest time wins! 🏆

## 🐛 Troubleshooting

1. **Connection Error**: Check Snowflake credentials in `secrets.toml`
2. **Database Error**: Make sure you ran `setup_database.sql` first
3. **Import Error**: Run `pip install -r requirements.txt`

## 📝 For Submission

Your PDF report should include:
1. Your name
2. Code screenshots
3. App screenshots showing:
   - Dashboard with data
   - Adding new car
   - Adding new team  
   - Race results
4. Brief description of what you achieved