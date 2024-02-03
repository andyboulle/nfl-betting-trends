#################################################################################
# AllOptionTrends.py                                                            #
#                                                                               #
# This file simply combines all the other option trends. It collects all the    #
# basic trends, game option trends, betting option trends, integrated option    #
# trends, and yearly option trends. It then combines all these trends into one  #
# large set of trends. It also allows you to filter and sort the final set of   #
# trends based on key words or phrases. The toString method prints all of these #
# records on their own line.                                                    #
#################################################################################
from src.analysis.option_trends.GameOptionTrends import GameOptionTrends
from src.analysis.option_trends.BettingOptionTrends import BettingOptionTrends
from src.analysis.option_trends.IntegratedOptionTrends import IntegratedOptionTrends
from src.analysis.option_trends.YearlyOptionTrends import YearlyOptionTrends
from src.analysis.basic_trends.BasicTrends import BasicTrends
from src.analysis.objects.NamedDataframe import NamedDataframe
from src.analysis.objects.Game import Game
import pandas as pd
from datetime import datetime

class AllOptionTrends:

    game = None
    df = None
    named_df = None
    trends = None

    all_time_trends_finder = None
    game_option_finder = None
    betting_option_finder = None
    integrated_option_finder = None
    yearly_option_finder = None

    def __init__(self, named_df, game):
        self.named_df = named_df
        self.game = game
        self.df = named_df.df

        print('Starting Basic Trends')
        start_time = datetime.now()
        self.all_time_trends_finder = BasicTrends(named_df, game)
        end_time = datetime.now()
        print('Finished Basic Trends')
        print(f'Elapsed Time: {end_time - start_time}')

        print('Starting Game Option Trends')
        start_time = datetime.now()
        self.game_option_finder = GameOptionTrends(named_df, game)
        end_time = datetime.now()
        print('Finished Game Option Trends')
        print(f'Elapsed Time: {end_time - start_time}')

        print('Starting Betting Option Trends')
        start_time = datetime.now()
        self.betting_option_finder = BettingOptionTrends(named_df, game)
        end_time = datetime.now()
        print('Finished Betting Option Trends')
        print(f'Elapsed Time: {end_time - start_time}')

        print('Starting Integrated Option Trends')
        start_time = datetime.now()
        self.integrated_option_finder = IntegratedOptionTrends(named_df, game)
        end_time = datetime.now()
        print('Finished Integrated Option Trends')
        print(f'Elapsed Time: {end_time - start_time}')

        print('Starting Yearly Option Trends')
        start_time = datetime.now()
        self.yearly_option_trends_finder = YearlyOptionTrends(self.named_df, self.game, self.game_option_finder, self.betting_option_finder, self.integrated_option_finder)
        end_time = datetime.now()
        print('Finished Yearly Option Trends')
        print(f'Elapsed Time: {end_time - start_time}')
        
        self.trends = self.get_all_trends()

    #
    # This function gets the trends for all games ever, no 
    # more specific filters have been applied to the dataframe
    #
    def get_all_time_trends(self):
        all_time_trends = self.all_time_trends_finder.trends

        return all_time_trends
    
    #
    # This function gets the trends for games that fit into
    # the correct criteria that has just 2 options: on/off
    #
    # This criteria includes:
    # Day of the Week:  Given Day or Any Day
    # Month:            Given Month or Any Month
    # Divisional Games: In Divisional Games or In All Games
    #
    def get_game_option_trends(self):
        game_option_trends = self.game_option_finder.trends

        return game_option_trends

    #   
    # This function gets the trends for all games the fit into 
    # the correct criteria for different betting options
    #
    # This criteria includes:
    # Spreads:      All spreads up to and including given spread
    # Moneylines:   All moneylines up to and including given moneylines
    # Totals:       All totals up to and down to given total
    #
    def get_betting_option_trends(self):
        betting_option_trends = self.betting_option_finder.trends

        return betting_option_trends

    #   
    # This function gets the trends for all games the fit into 
    # the criteria for both single option and many options
    # 
    def get_integrated_option_trends(self):
        integrated_option_trends = self.integrated_option_finder.trends

        return integrated_option_trends
    
    #   
    # This function gets the trends for all games the fit into 
    # the criteria for game option trends, betting option trends,
    # and integrated option trends season by season since the
    # 2006-2007 season.
    # 
    def get_yearly_option_trends(self):
        yearly_option_trends = self.yearly_option_trends_finder.trends

        return yearly_option_trends

    def get_all_trends(self):
        all_trends = []

        all_time_trends = self.get_all_time_trends()
        game_option_trends = self.get_game_option_trends()
        betting_option_trends = self.get_betting_option_trends()
        integrated_option_trends = self.get_integrated_option_trends()
        yearly_option_trends = self.get_yearly_option_trends()

        all_trends += all_time_trends
        all_trends += game_option_trends
        all_trends += betting_option_trends
        all_trends += integrated_option_trends
        all_trends += yearly_option_trends

        return all_trends
    
    #
    # This function allows you to filter the data you created based on
    # search terms. You can enter single words or phrases and this
    # function will return only trends whose descriptions contain that
    # word or phrase. It will then sort those by win percentage descending
    #
    # Ex) 
    #       words_to_contain = ["spread", "2008-2009"]
    #       will return only spread related trends from the 2008-2009 season
    #
    def filter_and_write_trends(self, minimum_games, minimum_win_pct, words_to_contain, output_file):
        filtered_trends = []

        for trend in self.trends:
            if trend.total_games >= minimum_games and trend.win_pct >= minimum_win_pct:
                if len(words_to_contain) > 0:
                    for word in words_to_contain:
                        if word in trend.description:
                            filtered_trends.append(trend)
                            break
                else:
                    filtered_trends.append(trend)

        sorted_trends = sorted(filtered_trends, key=lambda trend: trend.win_pct, reverse=True)

        return sorted_trends
    
    def __str__(self):
        returner = ''
        for trend in self.trends:
            returner += str(trend) + '\n'
        return returner
