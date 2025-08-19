-- Snowflake Database Setup Script
-- Run these commands in your Snowflake worksheet

-- Create database
CREATE DATABASE IF NOT EXISTS bootcamp_rally;
USE DATABASE bootcamp_rally;

-- Create schema
CREATE SCHEMA IF NOT EXISTS rally_management;
USE SCHEMA rally_management;

-- Create racing teams table
CREATE TABLE IF NOT EXISTS racing_teams (
    team_id INT AUTOINCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    members VARCHAR(500),
    budget DECIMAL(10,2) DEFAULT 10000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Create racing cars table
CREATE TABLE IF NOT EXISTS racing_cars (
    car_id INT AUTOINCREMENT PRIMARY KEY,
    car_name VARCHAR(100) NOT NULL,
    team_id INT,
    engine_power INT DEFAULT 200,
    weight_kg INT DEFAULT 1200,
    aerodynamics INT DEFAULT 50,
    tire_quality INT DEFAULT 70,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (team_id) REFERENCES racing_teams(team_id)
);

-- Create race results table
CREATE TABLE IF NOT EXISTS race_results (
    race_id INT AUTOINCREMENT PRIMARY KEY,
    race_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    winning_team_id INT,
    total_participants INT,
    prize_amount DECIMAL(10,2),
    race_details VARCHAR(1000),
    FOREIGN KEY (winning_team_id) REFERENCES racing_teams(team_id)
);

-- Insert racing teams (20 teams)
INSERT INTO racing_teams (team_name, members, budget) VALUES
('Speed Demons', 'Alex Johnson, Maria Garcia, Tommy Speed', 25000.00),
('Thunder Racers', 'John Smith, Sarah Wilson, Mike Thunder', 22000.00),
('Lightning Bolts', 'Mike Brown, Lisa Davis, Emma Lightning', 28000.00),
('Velocity Vipers', 'Carlos Rodriguez, Anna Kim, Jake Viper', 19500.00),
('Turbo Titans', 'David Chen, Sophie Miller, Ryan Turbo', 31000.00),
('Nitro Nights', 'Marcus Williams, Kelly Johnson, Nina Nitro', 17800.00),
('Blazing Bulls', 'Antonio Lopez, Rachel Green, Max Blaze', 24500.00),
('Storm Riders', 'James Anderson, Olivia Taylor, Storm Peterson', 26200.00),
('Fire Foxes', 'Robert Martinez, Jessica White, Felix Fire', 20300.00),
('Ice Wolves', 'Daniel Thompson, Amanda Lewis, Wolf Ice', 23100.00),
('Desert Eagles', 'Christopher Garcia, Megan Clark, Eagle Desert', 29800.00),
('Mountain Lions', 'Matthew Rodriguez, Lauren Hill, Leo Mountain', 21700.00),
('Ocean Sharks', 'Andrew Wilson, Brittany Adams, Shark Ocean', 27400.00),
('Sky Hawks', 'Joseph Moore, Samantha Baker, Hawk Sky', 18600.00),
('Forest Tigers', 'Michael Taylor, Ashley Turner, Tiger Forest', 32500.00),
('River Dolphins', 'William Jackson, Stephanie Phillips, Dolphin River', 16900.00),
('Canyon Cougars', 'Richard Brown, Michelle Campbell, Cougar Canyon', 25800.00),
('Valley Falcons', 'Charles Davis, Jennifer Parker, Falcon Valley', 22900.00),
('Peak Panthers', 'Thomas Miller, Kimberly Evans, Panther Peak', 30200.00),
('Wild Stallions', 'Kevin Wilson, Lisa Rodriguez, Stallion Wild', 19100.00);

-- Insert racing cars (50+ cars with variety)
INSERT INTO racing_cars (car_name, team_id, engine_power, weight_kg, aerodynamics, tire_quality) VALUES
-- Speed Demons cars
('Red Thunder', 1, 280, 1080, 85, 92),
('Crimson Fury', 1, 260, 1120, 78, 88),
('Ruby Rocket', 1, 290, 1050, 90, 95),

-- Thunder Racers cars
('Blue Lightning', 2, 250, 1150, 75, 85),
('Azure Storm', 2, 240, 1180, 70, 80),
('Cobalt Crusher', 2, 270, 1100, 82, 90),

-- Lightning Bolts cars
('Green Fury', 3, 300, 1040, 88, 94),
('Emerald Flash', 3, 285, 1070, 85, 91),

-- Velocity Vipers cars
('Venom Strike', 4, 265, 1130, 80, 87),
('Serpent Speed', 4, 255, 1160, 76, 83),
('Cobra Rush', 4, 275, 1110, 84, 89),

-- Turbo Titans cars
('Titan Force', 5, 320, 1020, 92, 97),
('Mega Power', 5, 310, 1060, 89, 95),
('Ultra Beast', 5, 295, 1090, 87, 93),

-- Nitro Nights cars
('Night Rider', 6, 245, 1170, 72, 78),
('Dark Phoenix', 6, 260, 1140, 79, 86),

-- Blazing Bulls cars
('Bull Charge', 7, 285, 1080, 86, 90),
('Fire Bull', 7, 270, 1120, 81, 87),
('Inferno Beast', 7, 290, 1070, 88, 92),

-- Storm Riders cars
('Storm Chaser', 8, 275, 1100, 83, 89),
('Hurricane', 8, 265, 1130, 80, 86),
('Cyclone Fury', 8, 280, 1090, 85, 91),

-- Fire Foxes cars
('Firefox', 9, 255, 1150, 77, 84),
('Flame Runner', 9, 270, 1110, 82, 88),

-- Ice Wolves cars
('Arctic Wolf', 10, 250, 1160, 74, 81),
('Frost Bite', 10, 265, 1130, 79, 87),
('Ice Storm', 10, 275, 1100, 83, 90),

-- Desert Eagles cars
('Eagle Soar', 11, 295, 1060, 89, 94),
('Desert Wind', 11, 280, 1090, 86, 91),
('Sand Storm', 11, 290, 1070, 88, 93),

-- Mountain Lions cars
('Lion Roar', 12, 260, 1140, 78, 85),
('Peak Climber', 12, 275, 1110, 84, 89),

-- Ocean Sharks cars
('Shark Attack', 13, 285, 1080, 87, 92),
('Tidal Wave', 13, 270, 1120, 82, 88),
('Deep Blue', 13, 295, 1050, 90, 95),

-- Sky Hawks cars
('Sky Striker', 14, 240, 1180, 71, 77),
('Wind Rider', 14, 255, 1150, 76, 83),

-- Forest Tigers cars
('Tiger Claw', 15, 310, 1030, 91, 96),
('Jungle King', 15, 300, 1060, 88, 94),
('Wild Cat', 15, 290, 1080, 86, 92),

-- River Dolphins cars
('Dolphin Dive', 16, 235, 1190, 68, 75),
('River Rush', 16, 250, 1160, 74, 81),

-- Canyon Cougars cars
('Cougar Strike', 17, 275, 1100, 84, 90),
('Canyon Runner', 17, 265, 1130, 80, 87),
('Rock Climber', 17, 280, 1090, 85, 91),

-- Valley Falcons cars
('Falcon Flight', 18, 270, 1110, 82, 88),
('Valley Racer', 18, 260, 1140, 79, 85),

-- Peak Panthers cars
('Panther Prowl', 19, 305, 1050, 89, 95),
('Summit Racer', 19, 295, 1070, 87, 93),
('Alpine Beast', 19, 285, 1090, 85, 91),

-- Wild Stallions cars
('Stallion Gallop', 20, 245, 1170, 73, 79),
('Wild Runner', 20, 260, 1140, 78, 85),
('Mustang Fury', 20, 275, 1110, 83, 89);

-- Insert some historical race results
INSERT INTO race_results (winning_team_id, total_participants, prize_amount, race_details) VALUES
(15, 18, 10800.00, 'Winner: Tiger Claw - Time: 95.4 minutes - Track: Mountain Circuit'),
(5, 16, 9600.00, 'Winner: Titan Force - Time: 89.2 minutes - Track: Desert Sprint'),
(11, 20, 12000.00, 'Winner: Eagle Soar - Time: 92.1 minutes - Track: Coastal Rally'),
(3, 14, 8400.00, 'Winner: Green Fury - Time: 90.8 minutes - Track: Forest Trail'),
(1, 17, 10200.00, 'Winner: Ruby Rocket - Time: 88.5 minutes - Track: City Circuit'),
(19, 19, 11400.00, 'Winner: Panther Prowl - Time: 91.3 minutes - Track: Alpine Challenge'),
(13, 15, 9000.00, 'Winner: Shark Attack - Time: 93.7 minutes - Track: Seaside Sprint'),
(7, 16, 9600.00, 'Winner: Bull Charge - Time: 94.2 minutes - Track: Prairie Run');

-- Check if data was inserted correctly
SELECT * FROM racing_teams;
SELECT * FROM racing_cars;
SELECT * FROM race_results;