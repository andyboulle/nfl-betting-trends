from models.upcoming_game import UpcomingGame
import time
import psycopg2

# This file will run every night at 3:00 AM to update the database with the latest lines.

total_start_time = time.time()
print('Starting...')

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="bangarang19"
)
cur = conn.cursor()

# Check if the table 'upcoming_games' exists
check_table_query = '''
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'upcoming_games'
    )
'''
cur.execute(check_table_query)
table_exists = cur.fetchone()[0]

if table_exists:
    # If the table exists, truncate it
    truncate_table_query = '''
        TRUNCATE TABLE upcoming_games
    '''
    cur.execute(truncate_table_query)
    conn.commit()
else:
    # If the table does not exist, create it
    create_table_query = '''
        CREATE TABLE upcoming_games (
            id VARCHAR(64) PRIMARY KEY,
            id_string VARCHAR(14),
            date VARCHAR(10),
            month VARCHAR(10),
            day INT,
            year INT,
            season VARCHAR(9),
            day_of_week VARCHAR(9),
            home_team VARCHAR(25),
            home_abbreviation VARCHAR(3),
            home_division VARCHAR(9),
            away_team VARCHAR(25),
            away_abbreviation VARCHAR(3),
            away_division VARCHAR(9),
            divisional BOOLEAN,
            spread DECIMAL(4, 1),
            home_spread DECIMAL(4, 1),
            home_spread_odds INT,
            away_spread DECIMAL(4, 1),
            away_spread_odds INT,
            home_moneyline_odds INT,
            away_moneyline_odds INT,
            total DECIMAL(4, 1),
            over DECIMAL(4, 1),
            over_odds INT,
            under DECIMAL(4, 1),
            under_odds INT
        )
    '''
    cur.execute(create_table_query)
    conn.commit()

# Check if the table 'weekly_trends' exists
check_table_query = '''
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'weekly_trends'
    )
'''
cur.execute(check_table_query)
table_exists = cur.fetchone()[0]

if table_exists:
    # If the table exists, truncate it
    truncate_table_query = '''
        TRUNCATE TABLE weekly_trends
    '''
    cur.execute(truncate_table_query)
    conn.commit()
else:
    # If the table does not exist, create it
    create_table_query = '''
        CREATE TABLE weekly_trends (
            id VARCHAR(64),
            id_string VARCHAR(250),
            category VARCHAR(25),
            month VARCHAR(10),
            day_of_week VARCHAR(10),
            divisional BOOLEAN,
            spread VARCHAR(15),
            total VARCHAR(15),
            seasons VARCHAR(15),
            wins INT,
            losses INT,
            pushes INT,
            total_games INT,
            win_percentage DECIMAL(5, 2),
            games_applicable VARCHAR(250)
        )
    '''
    cur.execute(create_table_query)
    conn.commit()

# This is where new lines will be pulled in from the API
# For now, we will just use some dummy data
game1 = UpcomingGame('2024-09-05', 'Kansas City Chiefs', 'Miami Dolphins', -4.5, -110, -110, -220, 190, 47, -110, -110, True)
game2 = UpcomingGame('2024-09-06', 'Philadelphia Eagles', 'Pittsburgh Steelers', -3, -110, -110, -200, 174, 42, -110, -110, True)
game3 = UpcomingGame('2024-09-08', 'Baltimore Ravens', 'Washington Commanders', -8.5, -110, -110, -370, 250, 45.5, -110, -110, True)
game4 = UpcomingGame('2024-09-08', 'Seattle Seahawks', 'Chicago Bears', -1.5, -110, -110, -123, 108, 43.5, -110, -110, True)
game5 = UpcomingGame('2024-09-08', 'Denver Broncos', 'Arizona Cardinals', 0, -110, -110, -104, -104, 42, -110, -110, True)
game6 = UpcomingGame('2024-09-08', 'Green Bay Packers', 'Dallas Cowboys', 2.5, -110, -110, 140, -155, 52.5, -110, -110, True)
game7 = UpcomingGame('2024-09-08', 'Carolina Panthers', 'New York Giants', 3.5, -110, -110, 165, -190, 38.5, -110, -110, True)
game8 = UpcomingGame('2024-09-08', 'San Francisco 49ers', 'New Orleans Saints', -10.5, -110, -110, -430, 365, 49.5, -110, -110, True)
game9 = UpcomingGame('2024-09-08', 'Indianapolis Colts', 'Cincinnati Bengals', 3, -110, -110, 148, -165, 47, -110, -110, True)
game10 = UpcomingGame('2024-09-08', 'New York Jets', 'Los Angeles Chargers', -1.5, -110, -110, -131, 115, 42.5, -110, -110, True)
game11 = UpcomingGame('2024-09-08', 'Los Angeles Rams', 'Tampa Bay Buccaneers', -3.5, -110, -110, -200, 183, 44.5, -110, -110, True)
game12 = UpcomingGame('2024-09-08', 'Cleveland Browns', 'Jacksonville Jaguars', 1, -110, -110, 106, -110, 39.5, -110, -110, True)
game13 = UpcomingGame('2024-09-08', 'Tennessee Titans', 'Minnesota Vikings', 2.5, -110, -110, 140, -168, 34.5, -110, -110, True)
game14 = UpcomingGame('2024-09-08', 'Atlanta Falcons', 'Houston Texans', 4, -110, -110, 185, -205, 46, -110, -110, True)
game15 = UpcomingGame('2024-09-09', 'Detroit Lions', 'Buffalo Bills', 0, -110, -110, -109, -111, 55.5, -110, -110, True)
game16 = UpcomingGame('2024-09-09', 'Las Vegas Raiders', 'New England Patriots', -2, -110, -110, -130, 115, 33.5, -110, -110, True)
games = [game1, game2, game3, game4, game5, game6, game7, game8, game9, game10, game11, game12, game13, game14, game15, game16]

total_games_start_time = time.time()
weekly_trends = {}
for game in games:
    game_start_time = time.time()
    print(f'Processing game {game.id_string}...')
    # Insert game into upcoming_games table
    insert_query = '''
        INSERT INTO upcoming_games VALUES (
            %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, 
            %s, %s, %s, %s, %s
        )
    '''
    cur.execute(insert_query, game.to_tuple())
    conn.commit()

    # Check if table exists
    check_table_query = f'''
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = '{game.id_string.lower()}'
        )
    '''
    cur.execute(check_table_query)
    table_exists = cur.fetchone()[0]

    if table_exists:
        # Truncate table if it exists
        truncate_table_query = f'''
            TRUNCATE TABLE {game.id_string.lower()}
        '''
        cur.execute(truncate_table_query)
        conn.commit()
    else:
        # Create table if it does not exist
        create_table_query = f'''
            CREATE TABLE {game.id_string.lower()} (
                id VARCHAR(64),
                id_string VARCHAR(250),
                category VARCHAR(25),
                month VARCHAR(10),
                day_of_week VARCHAR(10),
                divisional BOOLEAN,
                spread VARCHAR(15),
                total VARCHAR(15),
                seasons VARCHAR(15),
                wins INT,
                losses INT,
                pushes INT,
                total_games INT,
                win_percentage DECIMAL(5, 2)
            )
        '''
        cur.execute(create_table_query)
        conn.commit()

    # Insert trends into individual game trends table
    insert_query = f'''
        INSERT INTO {game.id_string.lower()}
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    trend_tuples = [trend.to_tuple() for trend in game.trends]
    cur.executemany(insert_query, trend_tuples)
    conn.commit()

    # Insert trends into weekly_trends dictionary with updated applicable games
    for trend in game.trends:
        weekly_game_string = f'{game.home_abbreviation}vs{game.away_abbreviation}'
        if trend.trend_id in weekly_trends:
            weekly_trends[trend.trend_id].applicable_games += f', {weekly_game_string}'
        else:
            trend.applicable_games = weekly_game_string
            weekly_trends[trend.trend_id] = trend

    game_end_time = time.time()
    print(f'Game processing took {game_end_time - game_start_time}')

total_games_end_time = time.time()
print(f'Total games processing took {total_games_end_time - total_games_start_time}')

weekly_trends_start_time = time.time()
print('Inserting weekly trends...')
insert_query = '''
    INSERT INTO weekly_trends
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
trend_tuples = [trend.to_tuple() for trend in weekly_trends.values()]
cur.executemany(insert_query, trend_tuples)
conn.commit()
weekly_trends_end_time = time.time()
print(f'Inserting weekly trends took {weekly_trends_end_time - weekly_trends_start_time}')

# Close the cursor and the connection
cur.close()
conn.close()

total_end_time = time.time()
print(f'Total time took {total_end_time - total_start_time}')
