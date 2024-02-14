import json
import pandas as pd

from src.objects.CompletedGame import CompletedGame
from src.objects.CustomEncoder import CustomEncoder

df = pd.read_excel('datafiles/excel/nfl.xlsx')

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

def create_completed_game_collection(df):
    for index, row in df.head(25).iterrows():
        game = CompletedGame(
            row['Date'], 
            row['Season Phase'], 
            row['Home Team'], row['Away Team'],
            row['Home Score'], row['Away Score'],
            row['Home Spread'],
            row['Total']
        )
        
        for description in game.conditions:
            if description == '':
                var = None
            else:
                var = None
    

df = format_dataframe(df)
create_completed_game_collection(df)