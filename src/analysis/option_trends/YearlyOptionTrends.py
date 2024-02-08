#################################################################################
# YearlyOptionTrends.py                                                         #
#                                                                               #
# This file calculates the record for trends that have to do with all possible  #
# combinations of betting information and game information about the given game # 
# from every year since 2006. It will create dataframes for these combinations  #
# from these years then get all trends from all these dataframes. The toString  # 
# method prints all of these records on their own line.                         #
#                                                                               #
# Examples:                                                                     #
# - games where the spread is 2.0 or more and the total is 47.5 or lower and    #
#   the month is 10 and it is the regular season since                          #
#   the 2011-2012 season                                                        #
# - games where the spread is 2.0 or more since the 2007-2008 season            #
# - games where the total is 43.5 and the day of the week is Sunday and it is a # 
#   divisional game since the 2023-2024 season                                  #
#################################################################################
from src.analysis.option_trends.GameOptionTrends import GameOptionTrends
from src.analysis.option_trends.BettingOptionTrends import BettingOptionTrends
from src.analysis.option_trends.IntegratedOptionTrends import IntegratedOptionTrends
from src.analysis.basic_trends.BasicTrends import BasicTrends
from src.analysis.objects.NamedDataframe import NamedDataframe
from src.analysis.objects.Game import Game
import pandas as pd

class YearlyOptionTrends:
    
    named_df = None
    df = None

    game = None

    game_option_finder = None
    betting_option_finder = None
    integrated_option_finder = None

    trends = None

    def __init__(self, named_df, game, got=None, bot=None, iot=None):
        self.named_df = named_df
        self.df = named_df.df
        self.game = game

        if got is not None:
            self.game_option_finder = got
        else:
            self.game_option_finder = GameOptionTrends(named_df, game)

        if bot is not None:
            self.betting_option_finder = bot
        else:
            self.betting_option_finder = BettingOptionTrends(named_df, game)

        if iot is not None:
            self.integrated_option_finder = iot
        else:
            self.integrated_option_finder = IntegratedOptionTrends(named_df, game)

        self.trends = self.get_all_trends()



    # RETURNS AN ARRAY OF NAMED DATAFRAMES
    # EX: [ 
    #       Games where the spread is 2.0 or more and the total is 48.0 or lower since the 2023-2024 season, 
    #       Games where the spread is 2.0 or more and the total is 48.0 or lower since the 2022-2023 season, 
    #       Games where the spread is 2.0 or more and the total is 48.0 or lower since the 2021-2022 season, 
    #       etc
    #     ]
    def get_season_dataframes(self, named_df):
        season_combinations = []
        df_string = named_df.description
        df = named_df.df
        unique_seasons = sorted(df['Season'].unique(), reverse=True)

        for i in range(len(unique_seasons)):
            selected_seasons = unique_seasons[:i+1]
            seasons_df = df[df['Season'].isin(selected_seasons)]

            named_seasons_df = NamedDataframe(seasons_df, f'{df_string} since the {selected_seasons[len(selected_seasons) - 1]} season')
            season_combinations.append(named_seasons_df)

        return season_combinations
    
    # RETURNS AN ARRAY OF TRENDS: ALL TRENDS GIVEN BY A NAMED DATAFRAME ARRAY FOR EVERY SEASON
    # EX: [
    #       Home team straight up in games where the spread is 2.0 or more and the total is 48.0 or lower since the 2023-2024 season: 111-109-2,
    #       Away team straight up in games where the spread is 2.0 or more and the total is 48.0 or lower since the 2023-2024 season: 109-111-2,
    #       ...
    #       Favored team ATS in games where the spread is 2.0 or more and the total is 48.0 or lower since the 2009-2010 season: 381-92-10,
    #       Not favored team ATS in games where the spread is 2.0 or more and the total is 48.0 or lower since the 2009-2010 season: 92-381-10,
    #       etc
    #     ]
    def get_season_trends(self, seasons_array):
        season_trends_dfs = []

        for df in seasons_array:
            trends = BasicTrends(df, self.game).trends
            season_trends_dfs += trends

        return season_trends_dfs
    
    def get_game_option_year_trends(self):
        game_option_season_trends = []
        game_option_season_dfs = self.game_option_finder.get_option_combination_dataframes()

        for df in game_option_season_dfs:
            season_dfs = self.get_season_dataframes(df)
            season_trends = self.get_season_trends(season_dfs)
            game_option_season_trends += season_trends

        return game_option_season_trends
    
    def get_betting_option_year_trends(self):
        betting_option_season_trends = []
        betting_option_season_dfs = self.betting_option_finder.get_all_dataframes()

        for option_dfs in betting_option_season_dfs:
            for df in option_dfs:
                season_dfs = self.get_season_dataframes(df)
                season_trends = self.get_season_trends(season_dfs)
                betting_option_season_trends += season_trends

        return betting_option_season_trends
    
    def get_integrated_option_year_trends(self):
        integrated_option_season_trends = []
        integrated_option_season_dfs = self.integrated_option_finder.get_all_dataframes()

        for option_dfs in integrated_option_season_dfs:
            for df in option_dfs:
                season_dfs = self.get_season_dataframes(df)
                season_trends = self.get_season_trends(season_dfs)
                integrated_option_season_trends += season_trends

        return integrated_option_season_trends
    
    def get_all_option_year_trends(self):
        all_dfs = []
        total_season_dfs = self.get_season_dataframes(self.named_df)

        all_dfs = self.get_season_trends(total_season_dfs)
        return all_dfs
    
    def get_all_trends(self):
        all_trends = []

        game_option_trends = self.get_game_option_year_trends()
        betting_option_trends = self.get_betting_option_year_trends()
        integrated_option_trends = self.get_integrated_option_year_trends()
        all_option_trends = self.get_all_option_year_trends()

        all_trends += all_option_trends
        all_trends += game_option_trends
        all_trends += betting_option_trends
        all_trends += integrated_option_trends

        return all_trends

    def __str__(self):
        returner = ''
        for trend in self.trends:
            returner += str(trend) + '\n'
        return returner