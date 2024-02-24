import time
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from src.objects.Game import Game

#########################
### DATAFRAME METHODS ###
#########################

def format_dataframe(df):
    # Change date entered from date object to just "YYYY-MM-DD" format
    df['Date'] = df['Date'].astype(str).str[:10]

    # Reverse dataframe so oldest game is indexed first
    df = df.iloc[::-1].reset_index(drop=True)

    # If 'Home Line Close' and 'Away Line Close' are empty, replace them with 'Home Line Open' and 'Home Line Open * -1'
    df['Home Line Close'].fillna(df['Home Line Open'], inplace=True)
    df['Total Score Close'].fillna(df['Total Score Open'], inplace=True)

    # Delete unnecessary columns
    df.drop(columns=[
        # Don't need any moneyline odds columns
        'Home Odds Open', 'Home Odds Min', 'Home Odds Max', 'Home Odds Close',
        'Away Odds Open', 'Away Odds Min', 'Away Odds Max', 'Away Odds Close',

        # Don't need spread columns besides closing home lines
        'Home Line Open', 'Home Line Min', 'Home Line Max',
        'Away Line Open', 'Away Line Min', 'Away Line Max', 'Away Line Close',

        # Don't need any spread odds columns
        'Home Line Odds Open', 'Home Line Odds Min', 'Home Line Odds Max', 'Home Line Odds Close',
        'Away Line Odds Open', 'Away Line Odds Min', 'Away Line Odds Max', 'Away Line Odds Close',

        # Don't need any total columns besides closing total
        'Total Score Open', 'Total Score Min', 'Total Score Max',

        # Don't need any total score odds columns
        'Total Score Over Open', 'Total Score Over Min', 'Total Score Over Max', 'Total Score Over Close',
        'Total Score Under Open', 'Total Score Under Min', 'Total Score Under Max', 'Total Score Under Close',

        # Don't need overtime, neutral venue, or notes
        'Overtime?', 'Neutral Venue?', 'Notes'
    ], inplace = True)

    # Replace 
    df.rename(columns={
        'Home Line Close': 'Home Spread', 
        'Total Score Close': 'Total',
        'Playoff Game?': 'Season Phase',
        'Neutral Venue?': 'Neutral Venue'
    }, inplace=True)

    # Replace Y and N (or NaN) with True and False
    df.fillna(False, inplace=True)
    df.replace('Y', True, inplace=True)

    # Replace True and False with Regular Season and Playoffs for season type
    df['Season Phase'] = df['Season Phase'].replace(True, 'Playoffs')
    df['Season Phase'] = df['Season Phase'].replace(False, 'Regular Season')

    # Keep team names and locations consistent
    name_change_dict = {
        'Washington': 'Washington Commanders', 
        'Rams': 'Los Angeles Rams',
        'Raiders': 'Las Vegas Raiders',
        'Chargers': 'Los Angeles Chargers'
    }

    for key, value in name_change_dict.items():
        home_mask = df['Home Team'].str.contains(key)
        away_mask = df['Away Team'].str.contains(key)
        df.loc[home_mask, 'Home Team'] = value
        df.loc[away_mask, 'Away Team'] = value

    # Save this new, cleaned, and condensed dataframe to a csv
    df.to_csv('datafiles/csv/nfl_condensed.csv')
    return df

########################
### DATABASE METHODS ###
########################

def make_games_table(cur, df, conn):
    cur.execute(
    '''
        CREATE TABLE IF NOT EXISTS games (
            id VARCHAR(14) PRIMARY KEY,
            date VARCHAR(10),
            month VARCHAR(10),
            day INT,
            year INT,
            season VARCHAR(9),
            day_of_week VARCHAR(9),
            phase VARCHAR(14),
            home_team VARCHAR(25),
            home_abbreviation VARCHAR(3),
            home_division VARCHAR(9),
            away_team VARCHAR(25),
            away_abbreviation VARCHAR(3),
            away_division VARCHAR(9),
            divisional BOOLEAN,
            home_score INT,
            away_score INT,
            combined_score INT,
            tie BOOLEAN,
            winner VARCHAR(25),
            loser VARCHAR(25),
            spread INT,
            home_spread INT,
            home_spread_result INT,
            away_spread INT,
            away_spread_result INT,
            spread_push BOOLEAN,
            pk BOOLEAN,
            total INT,
            total_push BOOLEAN,
            home_favorite BOOLEAN,
            away_underdog BOOLEAN,
            away_favorite BOOLEAN,
            home_underdog BOOLEAN,
            home_win BOOLEAN,
            away_win BOOLEAN,
            favorite_win BOOLEAN,
            underdog_win BOOLEAN,
            home_favorite_win BOOLEAN,
            away_underdog_win BOOLEAN,
            away_favorite_win BOOLEAN,
            home_underdog_win BOOLEAN,
            home_cover BOOLEAN,
            away_cover BOOLEAN,
            favorite_cover BOOLEAN,
            underdog_cover BOOLEAN,
            home_favorite_cover BOOLEAN,
            away_underdog_cover BOOLEAN,
            away_favorite_cover BOOLEAN,
            home_underdog_cover BOOLEAN,
            over_hit BOOLEAN,
            under_hit BOOLEAN
        )
    ''')

    # Add Games to `games` table in database
    games = []
    for index, row in df.iterrows():
        if index % 100 == 0:
            end_time = time.time()
            print(f'Added games {index-100}-{index} -- Elapsed Time: {end_time - start_time}')
            start_time = time.time()
        game = Game(
            row['Date'], 
            row['Season Phase'], 
            row['Home Team'], row['Away Team'],
            row['Home Score'], row['Away Score'],
            row['Home Spread'],
            row['Total']
        )
        games.append(game.to_tuple())

    games_df = pd.DataFrame(games, columns=[
        'id', 'date', 'month', 'day', 'year', 'season', 'day_of_week', 'phase', 
        'home_team', 'home_abbreviation', 'home_division', 'away_team', 'away_abbreviation', 
        'away_division', 'divisional', 'home_score', 'away_score', 'combined_score', 'tie', 
        'winner', 'loser', 'spread', 'home_spread', 'home_spread_result', 'away_spread', 
        'away_spread_result', 'spread_push', 'pk', 'total', 'total_push', 'home_favorite', 
        'away_underdog', 'away_favorite', 'home_underdog', 'home_win', 'away_win', 
        'favorite_win', 'underdog_win', 'home_favorite_win', 'away_underdog_win', 
        'away_favorite_win', 'home_underdog_win', 'home_cover', 'away_cover', 
        'favorite_cover', 'underdog_cover', 'home_favorite_cover', 'away_underdog_cover', 
        'away_favorite_cover', 'home_underdog_cover', 'over_hit', 'under_hit'
    ])

    games_df.to_sql('games', conn, if_exists='replace', index=False)

def make_trends_table(cur):
    cur.execute('''
       drop table if exists trends         
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            id VARCHAR(250) PRIMARY KEY,
            category VARCHAR(25),
            phase VARCHAR(15),
            month VARCHAR(10),
            day_of_week VARCHAR(8),
            divisional BOOLEAN,
            spread DECIMAL(4, 1),
            total DECIMAL(4, 1),
            seasons DECIMAL(9),
            wins INT,
            losses INT,
            pushes INT,
            total_games INT GENERATED ALWAYS AS (
                wins + losses + pushes
            ) STORED,
            win_pct DECIMAL(5, 2) GENERATED ALWAYS AS (
                ROUND((100.0 * wins / NULLIF(wins + losses + (pushes / 2.0), 0)), 2)
            ) STORED
        )
    ''')

def populate_trends_table(cur):
    return

#################
### EXECUTION ###
#################

df = pd.read_excel('datafiles/excel/nfl.xlsx')

# Clean dataframe
df = format_dataframe(df)

conn_string = 'postgresql://postgres:bangarang19@localhost:5432/postgres'
db = create_engine(conn_string)
conn1 = db.connect()

# Connect to sql database
conn = psycopg2.connect(
    host = 'localhost',
    dbname = 'postgres',
    user = 'postgres',
    password = 'bangarang19',
    port = 5432
)
cur = conn.cursor()

# make_games_table(cur, df, conn1)
make_trends_table(cur)

# Commit database changes
conn.commit()

# Close cursor and connection
cur.close()
conn.close()
