#################################################################################
# SpreadTrends.py                                                               #
#                                                                               #
# This file calculates the record for trends that have to do with spreads. It   # 
# takes a game and named dataframe then calculates the record for home/away     # 
# teams, favored/not favored, home favored/away not favored, and                #
# away favored/home not favored against the spread, based on the specifics of   # 
# the game. It then stores these records in an array called trends. The         # 
# toString method prints all of these records on their own line.                #                              
#################################################################################
from src.analysis.helpers.filter_functions import *
from src.analysis.objects.Record import Record
import pandas as pd

class SpreadTrends:

    home_covers = None
    away_covers = None

    favored_covers = None
    not_favored_covers = None

    home_favored_covers = None
    away_not_favored_covers = None

    away_favored_covers = None
    home_not_favored_covers = None

    trends = None

    def __init__(self, named_df, game):
        self.home_covers = self.get_home_covers(named_df)
        self.away_covers = self.get_away_covers(named_df)
        self.favored_covers = self.get_favored_covers(named_df)
        self.not_favored_covers = self.get_not_favored_covers(named_df)
        if game.home_favored == True:
            self.home_favored_covers = self.get_home_favored_covers(named_df)
            self.away_not_favored_covers = self.get_away_not_favored_covers(named_df)
            self.trends = [
                self.home_covers, self.away_covers, 
                self.favored_covers, self.not_favored_covers, 
                self.home_favored_covers, self.away_not_favored_covers
            ]
        elif game.away_favored == True:
            self.away_favored_covers = self.get_away_favored_covers(named_df)
            self.home_not_favored_covers = self.get_home_not_favored_covers(named_df)
            self.trends = [
                self.home_covers, self.away_covers, 
                self.favored_covers, self.not_favored_covers, 
                self.away_favored_covers, self.home_not_favored_covers
            ]


    ###########################################
    #           Home/Away Calculators         # 
    ###########################################     
    def get_home_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Spread Push?': 'N', 'Neutral Venue?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        home_covers = (df_clean['Home Cover?'] == 'Y').sum()
        home_not_covers = (df_clean['Home Cover?'] == 'N').sum()
        home_pushes = (df['Spread Push?'] == 'Y').sum()
        home_covers = Record(f'Home Team Record ATS in {identifiers}', home_covers, home_not_covers, home_pushes)

        return home_covers

    def get_away_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Spread Push?': 'N', 'Neutral Venue?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        away_covers = (df_clean['Away Cover?'] == 'Y').sum()
        away_not_covers = (df_clean['Away Cover?'] == 'N').sum()
        away_pushes = (df['Spread Push?'] == 'Y').sum()
        away_covers = Record(f'Away Team Record ATS in {identifiers}', away_covers, away_not_covers, away_pushes)

        return away_covers


    ###########################################
    #       Favored/Not Favored Calculators   # 
    ###########################################
    def get_favored_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'PK?': 'N'}
        df_no_pk = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Spread Push?': 'N', 'PK?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        favored_covers = (df_clean['Favored Cover?'] == 'Y').sum()
        favored_not_covers = (df_clean['Favored Cover?'] == 'N').sum()
        favored_pushes = (df_no_pk['Spread Push?'] == 'Y').sum()
        favored_covers = Record(f'Favored Record ATS in {identifiers}', favored_covers, favored_not_covers, favored_pushes)

        return favored_covers
    
    def get_not_favored_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'PK?': 'N'}
        df_no_pk = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Spread Push?': 'N', 'PK?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        not_favored_covers = (df_clean['Not Favored Cover?'] == 'Y').sum()
        not_favored_not_covers = (df_clean['Not Favored Cover?'] == 'N').sum()
        not_favored_pushes = (df_no_pk['Spread Push?'] == 'Y').sum()
        not_favored_covers = Record(f'Not Favored Record ATS in {identifiers}', not_favored_covers, not_favored_not_covers, not_favored_pushes)

        return not_favored_covers


    ###########################################
    # Home/Away Favored/Not Favored Calculators # 
    ###########################################
    def get_home_favored_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Favored?': 'Y'}
        home_favored_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Favored?': 'Y', 'Spread Push?': 'N'}
        home_favored_df_clean = filter_dataframe_by_values(df, filter_dict)

        home_favored_covers = (home_favored_df_clean['Home Favored Cover?'] == 'Y').sum()
        home_favored_not_covers = (home_favored_df_clean['Home Favored Cover?'] == 'N').sum()
        home_favored_pushes = (home_favored_df['Spread Push?'] == 'Y').sum()
        home_favored_covers = Record(f'Home Favorite Record ATS in {identifiers}', home_favored_covers, home_favored_not_covers, home_favored_pushes)

        return home_favored_covers

    def get_away_not_favored_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Not Favored?': 'Y'}
        away_not_favored_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Not Favored?': 'Y', 'Spread Push?': 'N'}
        away_not_favored_df_clean = filter_dataframe_by_values(df, filter_dict)

        away_not_favored_covers = (away_not_favored_df_clean['Away Not Favored Cover?'] == 'Y').sum()
        away_not_favored_not_covers = (away_not_favored_df_clean['Away Not Favored Cover?'] == 'N').sum()
        away_not_favored_pushes = (away_not_favored_df['Spread Push?'] == 'Y').sum()
        away_not_favored_covers = Record(f'Away Not Favored Record ATS in {identifiers}', away_not_favored_covers, away_not_favored_not_covers, away_not_favored_pushes)

        return away_not_favored_covers
    
    def get_away_favored_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Favored?': 'Y'}
        away_favored_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Favored?': 'Y', 'Spread Push?': 'N'}
        away_favored_df_clean = filter_dataframe_by_values(df, filter_dict)

        away_favored_covers = (away_favored_df_clean['Away Favored Cover?'] == 'Y').sum()
        away_favored_not_covers = (away_favored_df_clean['Away Favored Cover?'] == 'N').sum()
        away_favored_pushes = (away_favored_df['Spread Push?'] == 'Y').sum()
        away_favored_covers = Record(f'Away Favored Record ATS in {identifiers}', away_favored_covers, away_favored_not_covers, away_favored_pushes)

        return away_favored_covers

    def get_home_not_favored_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Not Favored?': 'Y'}
        home_not_favored_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Not Favored?': 'Y', 'Spread Push?': 'N'}
        home_not_favored_df_clean = filter_dataframe_by_values(df, filter_dict)

        home_not_favored_covers = (home_not_favored_df_clean['Home Not Favored Cover?'] == 'Y').sum()
        home_not_favored_not_covers = (home_not_favored_df_clean['Home Not Favored Cover?'] == 'N').sum()
        home_not_favored_pushes = (home_not_favored_df['Spread Push?'] == 'Y').sum()
        home_not_favored_covers = Record(f'Home Not Favored Record ATS in {identifiers}', home_not_favored_covers, home_not_favored_not_covers, home_not_favored_pushes)

        return home_not_favored_covers


    ###########################################
    #                ToString                 # 
    ###########################################

    def __str__(self):
        returner = ''
        for cover in self.trends:
            returner += str(cover) + '\n'
        return returner 