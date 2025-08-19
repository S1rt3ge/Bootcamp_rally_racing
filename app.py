import streamlit as st
import snowflake.connector
import pandas as pd
import random
from datetime import datetime

# tab config
st.set_page_config(
    page_title="Rally Racing Management",
    page_icon="🏁",
    layout="wide"
)

# database connection
@st.cache_resource
def get_snowflake_connection():
    """Connect to Snowflake database"""
    try:
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database="bootcamp_rally",
            schema="rally_management"
        )
        return conn
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return None

def execute_query(query, params=None):
    """Execute SQL query and return results"""
    conn = get_snowflake_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return True
        except Exception as e:
            st.error(f"Query failed: {e}")
            return None
        finally:
            cursor.close()
    return None

def get_teams():
    """Get all racing teams"""
    query = "SELECT team_id, team_name, members, budget FROM racing_teams"
    results = execute_query(query)
    if results:
        return pd.DataFrame(results, columns=['Team ID', 'Team Name', 'Members', 'Budget'])
    return pd.DataFrame()

def get_cars():
    """Get all racing cars with team names"""
    query = """
    SELECT c.car_id, c.car_name, t.team_name, c.engine_power, 
           c.weight_kg, c.aerodynamics, c.tire_quality
    FROM racing_cars c
    JOIN racing_teams t ON c.team_id = t.team_id
    """
    results = execute_query(query)
    if results:
        return pd.DataFrame(results, columns=[
            'Car ID', 'Car Name', 'Team', 'Engine Power', 'Weight (kg)', 'Aerodynamics', 'Tire Quality'
        ])
    return pd.DataFrame()

def add_new_car(car_name, team_id, engine_power, weight_kg, aerodynamics, tire_quality):
    """Add new racing car to database"""
    query = """
    INSERT INTO racing_cars (car_name, team_id, engine_power, weight_kg, aerodynamics, tire_quality)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (car_name, team_id, engine_power, weight_kg, aerodynamics, tire_quality))

def add_new_team(team_name, members, budget):
    """Add new racing team to database"""
    query = "INSERT INTO racing_teams (team_name, members, budget) VALUES (%s, %s, %s)"
    return execute_query(query, (team_name, members, budget))

def calculate_car_speed(engine_power, weight_kg, aerodynamics, tire_quality):
    """Calculate car speed based on characteristics"""
    # speed calculator with randomizer then have 20% variation and min speed > 50
    base_speed = (engine_power * 0.3) + (aerodynamics * 0.2) + (tire_quality * 0.25) - (weight_kg * 0.01)
    random_factor = random.uniform(0.8, 1.2)
    final_speed = base_speed * random_factor
    return max(final_speed, 50)

def simulate_race():
    """Simulate 100km rally race"""
    # taking cars for race
    cars_df = get_cars()
    if cars_df.empty:
        return None, "No cars available for racing!"

    entry_fee = 1000
    
    # race time
    race_results = []
    
    for _, car in cars_df.iterrows():
        speed = calculate_car_speed(
            car['Engine Power'], 
            car['Weight (kg)'], 
            car['Aerodynamics'], 
            car['Tire Quality']
        )
        
        # time to complete race
        time_minutes = (100 / speed) * 60
        
        race_results.append({
            'Car Name': car['Car Name'],
            'Team': car['Team'],
            'Speed (km/h)': round(speed, 2),
            'Time (minutes)': round(time_minutes, 2)
        })
    
    race_results.sort(key=lambda x: x['Time (minutes)'])
    
    # winner get 60% of all money
    if race_results:
        winner = race_results[0]
        total_entry_fees = len(race_results) * entry_fee
        prize_money = total_entry_fees * 0.6 
        
        # update budget
        update_query = """
        UPDATE racing_teams 
        SET budget = budget + %s 
        WHERE team_name = %s
        """
        execute_query(update_query, (prize_money, winner['Team']))
        
        # removal of the entrance fee
        for result in race_results:
            deduct_query = """
            UPDATE racing_teams 
            SET budget = budget - %s 
            WHERE team_name = %s
            """
            execute_query(deduct_query, (entry_fee, result['Team']))
        
        # add money to winner (winner also paid entry fee)
        winner_update_query = """
        UPDATE racing_teams 
        SET budget = budget + %s 
        WHERE team_name = %s
        """
        execute_query(winner_update_query, (prize_money, winner['Team']))
        
        # saving result
        save_race_query = """
        INSERT INTO race_results (winning_team_id, total_participants, prize_amount, race_details)
        SELECT team_id, %s, %s, %s FROM racing_teams WHERE team_name = %s
        """
        race_details = f"Winner: {winner['Car Name']} - Time: {winner['Time (minutes)']} minutes"
        execute_query(save_race_query, (len(race_results), prize_money, race_details, winner['Team']))
        
        return race_results, f"🏆 Winner: {winner['Car Name']} from {winner['Team']}! Prize: ${prize_money:,.2f}"
    
    return None, "Race simulation failed!"

# main
def main():
    st.title("🏁 Bootcamp Rally Racing Management App")
    st.markdown("---")
    
    # connection check
    conn = get_snowflake_connection()
    if not conn:
        st.error("❌ Cannot connect to Snowflake database. Please check your credentials.")
        st.stop()
    
    st.success("✅ Connected to Snowflake database!")
    
    st.sidebar.title("🏎️ Navigation")
    page = st.sidebar.selectbox("Choose page:", [
        "🏠 Dashboard", 
        "🏎️ Manage Cars", 
        "👥 Manage Teams", 
        "🏁 Start Race!"
    ])
    
    if page == "🏠 Dashboard":
        st.header("📊 Rally Racing Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏎️ Racing Cars")
            cars_df = get_cars()
            if not cars_df.empty:
                st.dataframe(cars_df, use_container_width=True)
            else:
                st.info("No cars registered yet!")
        
        with col2:
            st.subheader("👥 Racing Teams")
            teams_df = get_teams()
            if not teams_df.empty:
                st.dataframe(teams_df, use_container_width=True)
            else:
                st.info("No teams registered yet!")
    
    elif page == "🏎️ Manage Cars":
        st.header("🏎️ Car Management")
        
        st.subheader("Current Racing Cars")
        cars_df = get_cars()
        if not cars_df.empty:
            st.dataframe(cars_df, use_container_width=True)
        
        st.markdown("---")

        st.subheader("➕ Add New Racing Car")
        
        teams_df = get_teams()
        if teams_df.empty:
            st.warning("⚠️ Please add teams first before adding cars!")
        else:
            with st.form("add_car_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    car_name = st.text_input("🏎️ Car Name*", placeholder="e.g., Red Thunder")
                    team_choice = st.selectbox("👥 Select Team*", 
                                             options=teams_df['Team Name'].tolist())
                    engine_power = st.slider("🔋 Engine Power", 150, 400, 250)
                    weight_kg = st.slider("⚖️ Weight (kg)", 900, 1500, 1200)
                
                with col2:
                    aerodynamics = st.slider("✈️ Aerodynamics", 30, 100, 70)
                    tire_quality = st.slider("🛞 Tire Quality", 50, 100, 80)
                
                submitted = st.form_submit_button("➕ Add Car", type="primary")
                
                if submitted:
                    if car_name:
                        # receive team id
                        team_id = int(teams_df.loc[teams_df['Team Name'] == team_choice, 'Team ID'].iloc[0])
                        
                        success = add_new_car(car_name, team_id, engine_power, weight_kg, aerodynamics, tire_quality)
                        if success:
                            st.success(f"✅ Car '{car_name}' added successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add car!")
                    else:
                        st.error("❌ Please enter a car name!")
    
    elif page == "👥 Manage Teams":
        st.header("👥 Team Management")
        
        st.subheader("Current Racing Teams")
        teams_df = get_teams()
        if not teams_df.empty:
            st.dataframe(teams_df, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("➕ Add New Racing Team")
        
        with st.form("add_team_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                team_name = st.text_input("👥 Team Name*", placeholder="e.g., Speed Demons")
                members = st.text_area("👨‍👩‍👧‍👦 Team Members*", 
                                     placeholder="e.g., John Smith, Jane Doe")
            
            with col2:
                budget = st.number_input("💰 Initial Budget ($)", 
                                       min_value=5000, max_value=50000, value=15000)
            
            submitted = st.form_submit_button("➕ Add Team", type="primary")
            
            if submitted:
                if team_name and members:
                    success = add_new_team(team_name, members, budget)
                    if success:
                        st.success(f"✅ Team '{team_name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add team!")
                else:
                    st.error("❌ Please fill in all required fields!")
    
    elif page == "🏁 Start Race!":
        st.header("🏁 Rally Race Simulation")
        
        cars_df = get_cars()
        teams_df = get_teams()
        
        if cars_df.empty:
            st.warning("⚠️ No cars available for racing! Please add cars first.")
        else:
            st.info(f"🏎️ {len(cars_df)} cars ready for racing!")
            st.info("💰 Entry fee: $1,000 per team")
            st.info("🏆 Winner takes 60% of total entry fees as prize!")
            
            # show cars that participate
            st.subheader("🏎️ Participating Cars")
            st.dataframe(cars_df, use_container_width=True)
            
            if st.button("🏁 START RACE!", type="primary", use_container_width=True):
                with st.spinner("🏁 Racing in progress... 100km rally!"):
                    race_results, message = simulate_race()
                
                if race_results:
                    st.success(message)
                    
                    # showing result
                    st.subheader("🏁 Race Results")
                    results_df = pd.DataFrame(race_results)
                    
                    results_df.insert(0, 'Position', range(1, len(results_df) + 1))
                    
                    st.dataframe(results_df, use_container_width=True)
                    
                    # update budget
                    st.subheader("💰 Updated Team Budgets")
                    updated_teams = get_teams()
                    st.dataframe(updated_teams, use_container_width=True)
                else:
                    st.error(message)

if __name__ == "__main__":
    main()