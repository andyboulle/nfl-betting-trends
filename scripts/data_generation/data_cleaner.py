################################################################################
# clean_data.py                                                                #
#                                                                              #
# This file will clean the initial data from the excel file. It will remove    #
# unnecessary columns, replace NaN values that would cause errors later,       #
# polish columns that have errors, and make consistent teams for any team that # 
# has changed name or location                                                 # 
################################################################################
import pandas as pd

# Remove any unecessary columns
def remove_unnecessary_columns(df):
    del df['Notes']
    return df

# Convert NaN values that will cause problems to N
def convert_nan_values(df):
    yn_columns = []
    for col in df.columns:
        if col[len(col) - 1] == '?':
            yn_columns.append(col)
    
    for col in yn_columns:
        df[col] = df[col].fillna('N')

    return df

# Keep team names and locations consistent
def get_consistent_teams(df):
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

    return df

# Remove "00:00:00" from date column
def clean_dates(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.date
    return df

# Clean data
def clean_data(df):
    df = remove_unnecessary_columns(df)
    df = convert_nan_values(df)
    df = get_consistent_teams(df)
    df = clean_dates(df)

    return df