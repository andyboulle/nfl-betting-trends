#################################################################################
# column_editor.py                                                              #
#                                                                               #
# This file will add columns necessary to do analysis on the data. It will add  #
# columns with information about the games themselves and the results of the    #
# games. It will also change decimal odds to american odds for all the columns. # 
#################################################################################
import pandas as pd
import numpy as np
from datetime import datetime

afc_east = ['New York Jets', 'Miami Dolphins', 'New England Patriots', 'Buffalo Bills']
afc_north = ['Baltimore Ravens', 'Pittsburgh Steelers', 'Cincinnati Bengals', 'Cleveland Browns']
afc_west = ['Kansas City Chiefs', 'Denver Broncos', 'Los Angeles Chargers', 'Las Vegas Raiders']
afc_south = ['Jacksonville Jaguars', 'Indianapolis Colts', 'Tennessee Titans', 'Houston Texans']
nfc_east = ['Washington Commanders', 'Philadelphia Eagles', 'Dallas Cowboys', 'New York Giants']
nfc_north = ['Detroit Lions', 'Green Bay Packers', 'Minnesota Vikings', 'Chicago Bears']
nfc_west = ['San Francisco 49ers', 'Seattle Seahawks', 'Arizona Cardinals', 'Los Angeles Rams']
nfc_south = ['New Orleans Saints', 'Atlanta Falcons', 'Carolina Panthers', 'Tampa Bay Buccaneers']

# Helper Functions
def round_to_nearest_multiple_of_5(num):
    return 5 * round(num / 5)

def decimal_to_american(decimal_odds):
    if decimal_odds < 2.0:
        american_odds = str(round_to_nearest_multiple_of_5(int(-100 / (decimal_odds - 1))))
    else:
        american_odds = '+' + str(round_to_nearest_multiple_of_5(int((decimal_odds - 1) * 100)))
    return american_odds

# Creates the following columns:
# Year
# Month
# Day
def create_time_columns(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Day of Week'] = df['Date'].dt.strftime('%A')
    return df


# Creates the following columns:
# Season
def create_season_column(df):
    df['Season'] = None

    for index, row in df.iterrows():
        year = int(row['Year'])
        if int(row['Month']) > 8:
            next_year = year + 1
            df.loc[index, 'Season'] = str(year) + '-' + str(next_year)
        else:
            prev_year = year - 1
            df.loc[index, 'Season'] = str(prev_year) + '-' + str(year)

    return df


# Creates the following columns:
# Home Division
# Away Division
# Divisional Game?
def create_division_columns(df):
    df['Home Division'] = None
    df['Away Division'] = None
    df['Divisional Game?'] = None
    
    for index, row in df.iterrows():
        home_team = row['Home Team']
        if home_team in afc_east:
            df.loc[index, 'Home Division'] = 'AFC East'
        elif home_team in afc_north:
            df.loc[index, 'Home Division'] = 'AFC North'
        elif home_team in afc_west:
            df.loc[index, 'Home Division'] = 'AFC West'
        elif home_team in afc_south:
            df.loc[index, 'Home Division'] = 'AFC South'
        elif home_team in nfc_east:
            df.loc[index, 'Home Division'] = 'NFC East'
        elif home_team in nfc_north:
            df.loc[index, 'Home Division'] = 'NFC North'
        elif home_team in nfc_west:
            df.loc[index, 'Home Division'] = 'NFC West'
        elif home_team in nfc_south:
            df.loc[index, 'Home Division'] = 'NFC South'

    for index, row in df.iterrows():
        away_team = row['Away Team']
        if away_team in afc_east:
            df.loc[index, 'Away Division'] = 'AFC East'
        elif away_team in afc_north:
            df.loc[index, 'Away Division'] = 'AFC North'
        elif away_team in afc_west:
            df.loc[index, 'Away Division'] = 'AFC West'
        elif away_team in afc_south:
            df.loc[index, 'Away Division'] = 'AFC South'
        elif away_team in nfc_east:
            df.loc[index, 'Away Division'] = 'NFC East'
        elif away_team in nfc_north:
            df.loc[index, 'Away Division'] = 'NFC North'
        elif away_team in nfc_west:
            df.loc[index, 'Away Division'] = 'NFC West'
        elif away_team in nfc_south:
            df.loc[index, 'Away Division'] = 'NFC South'

    for index, row in df.iterrows():
        if row['Home Division'] == row['Away Division']:
            df.loc[index, 'Divisional Game?'] = 'Y'
        else:
            df.loc[index, 'Divisional Game?'] = 'N'

    return df


# Creates the following columns:
# Total Score
# Home Spread Result
# Away Spread Result
def create_score_result_columns(df):
    df['Total Score'] = df['Home Score'] + df['Away Score']
    df['Home Spread Result'] = df['Away Score'] - df['Home Score']
    df['Away Spread Result'] = df['Home Score'] - df['Away Score']
    return df


# Creates the following columns:
# Tie?
# Winner
# Loser
# Home Team Win?
# Away Team Win?
def create_game_result_columns(df):
    df['Tie?'] = None
    df['Winner'] = None
    df['Loser'] = None
    df['Home Team Win?'] = None
    df['Away Team Win?'] = None

    for index, row in df.iterrows():
        home_score = df.loc[index, 'Home Score']
        away_score = df.loc[index, 'Away Score']
        home_team = df.loc[index, 'Home Team']
        away_team = df.loc[index, 'Away Team']
        if home_score == away_score:
            df.loc[index, 'Tie?'] = 'Y'
            df.loc[index, 'Winner'] = 'NEITHER'
            df.loc[index, 'Loser'] = 'NEITHER'
            df.loc[index, 'Home Team Win?'] = 'N'
            df.loc[index, 'Away Team Win?'] = 'N'
        else:
            df.loc[index, 'Tie?'] = 'N'
            if home_score > away_score:
                df.loc[index, 'Winner'] = home_team
                df.loc[index, 'Loser'] = away_team
                df.loc[index, 'Home Team Win?'] = 'Y'
                df.loc[index, 'Away Team Win?'] = 'N'
            else:
                df.loc[index, 'Winner'] = away_team
                df.loc[index, 'Loser'] = home_team
                df.loc[index, 'Home Team Win?'] = 'N'
                df.loc[index, 'Away Team Win?'] = 'Y'

    return df

# Create the following columns:
# Spread
# Home Spread
# Away Spread
# PK?
def create_spread_columns(df):
    df['Home Spread'] = df['Home Line Open']
    df['Away Spread'] = df['Home Spread'] * -1
    df['Spread'] = df[['Home Spread', 'Away Spread']].max(axis=1)
    df['PK?'] = None

    for index, row in df.iterrows():
        spread = row['Home Spread']
        if spread == 0.0:
            df.loc[index, 'PK?'] = 'Y'
        else:
            df.loc[index, 'PK?'] = 'N'
    return df

# Create the following columns:
# Home Favorite?
# Home Underdog?
# Away Favorite?
# Away Underdog?
def create_favorite_underdog_columns(df):
    for index, row in df.iterrows():
        home_spread = row['Home Spread']
        away_spread = row['Away Spread']
        pk = row['PK?']
        if pk == 'Y':
            df.loc[index, 'Home Favorite?'] = 'N'
            df.loc[index, 'Home Underdog?'] = 'N'
            df.loc[index, 'Away Favorite?'] = 'N'
            df.loc[index, 'Away Underdog?'] = 'N'
        else:
            if home_spread < away_spread:
                df.loc[index, 'Home Favorite?'] = 'Y'
                df.loc[index, 'Home Underdog?'] = 'N'
                df.loc[index, 'Away Favorite?'] = 'N'
                df.loc[index, 'Away Underdog?'] = 'Y'
            else:
                df.loc[index, 'Home Favorite?'] = 'N'
                df.loc[index, 'Home Underdog?'] = 'Y'
                df.loc[index, 'Away Favorite?'] = 'Y'
                df.loc[index, 'Away Underdog?'] = 'N'
    return df

# Create the following columns:
# Favorite Win?
# Underdog Win?
# Home Favorite Win?
# Home Underdog Win?
# Away Favorite Win?
# Away Underdog Win?
def create_moneyline_result_columns(df):
    for index, row in df.iterrows():
        home_team = row['Home Team']
        away_team = row['Away Team']
        winner = row['Winner']
        tie = row['Tie?']
        # If there is a tie or no favorite/underdog, then everything is No
        if tie == True or row['PK?'] == 'Y':
            df.loc[index, 'Favorite Win?'] = 'N'
            df.loc[index, 'Underdog Win?'] = 'N'
            df.loc[index, 'Home Favorite Win?'] = 'N'
            df.loc[index, 'Home Underdog Win?'] = 'N'
            df.loc[index, 'Away Favorite Win?'] = 'N'
            df.loc[index, 'Away Underdog Win?'] = 'N'
        # There is no tie and a favorite/underdog
        else:
            # Home team is the winner, so away team is loser
            if home_team == winner:
                # Home team is the favorite, so away team is underdog
                if row['Home Favorite?'] == 'Y':
                    df.loc[index, 'Favorite Win?'] = 'Y'
                    df.loc[index, 'Underdog Win?'] = 'N'
                    df.loc[index, 'Home Favorite Win?'] = 'Y'
                    df.loc[index, 'Home Underdog Win?'] = 'N'
                    df.loc[index, 'Away Favorite Win?'] = 'N'
                    df.loc[index, 'Away Underdog Win?'] = 'N'
                # Home team is the underdog, so away team is the favorite
                else:
                    df.loc[index, 'Favorite Win?'] = 'N'
                    df.loc[index, 'Underdog Win?'] = 'Y'
                    df.loc[index, 'Home Favorite Win?'] = 'N'
                    df.loc[index, 'Home Underdog Win?'] = 'Y'
                    df.loc[index, 'Away Favorite Win?'] = 'N'
                    df.loc[index, 'Away Underdog Win?'] = 'N'
            # Away team is the winner
            else:
                # Away team is the favorite, so home team is underdog
                if row['Away Favorite?'] == 'Y':
                    df.loc[index, 'Favorite Win?'] = 'Y'
                    df.loc[index, 'Underdog Win?'] = 'N'
                    df.loc[index, 'Home Favorite Win?'] = 'N'
                    df.loc[index, 'Home Underdog Win?'] = 'N'
                    df.loc[index, 'Away Favorite Win?'] = 'Y'
                    df.loc[index, 'Away Underdog Win?'] = 'N'
                # Away team is the underdog, so home team is favorite
                else:
                    df.loc[index, 'Favorite Win?'] = 'N'
                    df.loc[index, 'Underdog Win?'] = 'Y'
                    df.loc[index, 'Home Favorite Win?'] = 'N'
                    df.loc[index, 'Home Underdog Win?'] = 'N'
                    df.loc[index, 'Away Favorite Win?'] = 'N'
                    df.loc[index, 'Away Underdog Win?'] = 'Y'
    return df

# Create the following columns:
# Spread Push?
# Home Team Cover?
# Away Team Cover?
# Favorite Cover?
# Underdog Cover?
# Home Favorite Cover?
# Home Underdog Cover?
# Away Favorite Cover?
# Away Underdog Cover?
def create_spread_result_columns(df):
    df['Spread Push?'] = None
    df['Home Team Cover?'] = None
    df['Away Team Cover?'] = None
    df['Favorite Cover?'] = None
    df['Underdog Cover?'] = None
    df['Home Favorite Cover?'] = None
    df['Home Underdog Cover?'] = None
    df['Away Favorite Cover?'] = None
    df['Away Underdog Cover?'] = None

    for index, row in df.iterrows():
        home_spread = row['Home Spread']
        away_spread = row['Away Spread']
        home_result = row['Home Spread Result']
        away_result = row['Away Spread Result']

        # Line pushed
        if home_spread == home_result:
            df.loc[index, 'Spread Push?'] = 'Y'
            df.loc[index, 'Home Team Cover?'] = 'N'
            df.loc[index, 'Away Team Cover?'] = 'N'
            df.loc[index, 'Favorite Cover?'] = 'N'
            df.loc[index, 'Underdog Cover?'] = 'N'
            df.loc[index, 'Home Favorite Cover?'] = 'N'
            df.loc[index, 'Home Underdog Cover?'] = 'N'
            df.loc[index, 'Away Favorite Cover?'] = 'N'
            df.loc[index, 'Away Underdog Cover?'] = 'N'
        # Spread did not push
        else:
            df.loc[index, 'Spread Push?'] = 'N'
            # Home team covers spread
            if home_result <= home_spread:
                df.loc[index, 'Home Team Cover?'] = 'Y'
                df.loc[index, 'Away Team Cover?'] = 'N'
                # Home team was favored
                if row['Home Favorite?'] == 'Y':
                    df.loc[index, 'Favorite Cover?'] = 'Y'
                    df.loc[index, 'Underdog Cover?'] = 'N'
                    df.loc[index, 'Home Favorite Cover?'] = 'Y'
                    df.loc[index, 'Home Underdog Cover?'] = 'N'
                    df.loc[index, 'Away Favorite Cover?'] = 'N'
                    df.loc[index, 'Away Underdog Cover?'] = 'N'
                # Home team was not favored
                else:
                    df.loc[index, 'Favorite Cover?'] = 'N'
                    df.loc[index, 'Underdog Cover?'] = 'Y'
                    df.loc[index, 'Home Favorite Cover?'] = 'N'
                    df.loc[index, 'Home Underdog Cover?'] = 'Y'
                    df.loc[index, 'Away Favorite Cover?'] = 'N'
                    df.loc[index, 'Away Underdog Cover?'] = 'N'
            # Away team covers spread
            else:
                df.loc[index, 'Home Team Cover?'] = 'N'
                df.loc[index, 'Away Team Cover?'] = 'Y'
                # Away team was favored
                if row['Away Favorite?'] == 'Y':
                    df.loc[index, 'Favorite Cover?'] = 'Y'
                    df.loc[index, 'Underdog Cover?'] = 'N'
                    df.loc[index, 'Home Favorite Cover?'] = 'N'
                    df.loc[index, 'Home Underdog Cover?'] = 'N'
                    df.loc[index, 'Away Favorite Cover?'] = 'Y'
                    df.loc[index, 'Away Underdog Cover?'] = 'N'
                # Away team was not favored
                else:
                    df.loc[index, 'Favorite Cover?'] = 'N'
                    df.loc[index, 'Underdog Cover?'] = 'Y'
                    df.loc[index, 'Home Favorite Cover?'] = 'N'
                    df.loc[index, 'Home Underdog Cover?'] = 'N'
                    df.loc[index, 'Away Favorite Cover?'] = 'N'
                    df.loc[index, 'Away Underdog Cover?'] = 'Y'
    return df


# Create the following columns:
# Total Push?
# Over Hit?
# Under Hit?
def create_total_result_columns(df):
    df['Total Push?'] = None
    df['Over Hit?'] = None
    df['Under Hit?'] = None

    for index, row in df.iterrows():
        total_score = row['Total Score']
        total = row['Total Score Open']

        # Total pushed
        if total_score == total:
            df.loc[index, 'Total Push?'] = 'Y'
            df.loc[index, 'Over Hit?'] = 'N'
            df.loc[index, 'Under Hit?'] = 'N'
        # Total did not push
        else:
            df.loc[index, 'Total Push?'] = 'N'
            if total_score > total:
                df.loc[index, 'Over Hit?'] = 'Y'
                df.loc[index, 'Under Hit?'] = 'N'
            else:
                df.loc[index, 'Over Hit?'] = 'N'
                df.loc[index, 'Under Hit?'] = 'Y'
    return df


# Rearranges columns in desired order
def reorder_columns(df):
    new_order = [
        'Season', 'Date', 'Day of Week', 'Month', 'Day', 'Year',
        'Home Team', 'Home Division', 'Away Team', 'Away Division',
        'Home Score', 'Away Score', 'Total Score', 'Winner', 'Loser',
        'Divisional Game?', 'Tie?', 'Overtime?', 'Playoff Game?', 'Neutral Venue?',
        'Spread', 'Home Spread', 'Away Spread', 'PK?', 'Home Spread Result', 'Away Spread Result', 'Spread Push?',
        'Home Favorite?', 'Away Underdog?', 'Away Favorite?', 'Home Underdog?',
        'Home Team Win?', 'Away Team Win?', 'Favorite Win?', 'Underdog Win?', 'Home Favorite Win?', 'Away Underdog Win?', 'Away Favorite Win?', 'Home Underdog Win?',
        'Home Team Cover?', 'Away Team Cover?', 'Favorite Cover?', 'Underdog Cover?', 'Home Favorite Cover?', 'Away Underdog Cover?', 'Away Favorite Cover?', 'Home Underdog Cover?',
        'Total Score Open', 'Total Push?', 'Over Hit?', 'Under Hit?'
    ]
    df = df[new_order]
    return df


def edit_columns(df):
    df = create_time_columns(df)
    df = create_season_column(df)
    df = create_division_columns(df)
    df = create_score_result_columns(df)
    df = create_game_result_columns(df)
    df = create_spread_columns(df)
    df = create_favorite_underdog_columns(df)
    df = create_moneyline_result_columns(df)
    df = create_spread_result_columns(df)
    df = create_total_result_columns(df)
    df = reorder_columns(df)
    return df
