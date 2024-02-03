#################################################################################
# BasicTrends.py                                                                #
#                                                                               #
# This file uses the MoneylineTrends, SpreadTrends, and TotalTrends file to     #
# calculate all the basic trend records for moneylines, spreads, and totals. It #
# runs all 3 of those files and runs them for the given game. The toString      #
# method puts all these trends into an array and prints them on their own line. #                              
#################################################################################
from src.analysis.basic_trends.MoneylineTrends import MoneylineTrends
from src.analysis.basic_trends.SpreadTrends import SpreadTrends
from src.analysis.basic_trends.TotalTrends import TotalTrends
import pandas as pd

class BasicTrends:

    named_df = None

    moneyline_trends = None
    spread_trends = None
    total_trends = None

    trends = None

    def __init__(self, named_df, game):
        self.named_df = named_df
        self.moneyline_trends = MoneylineTrends(named_df, game)
        self.spread_trends = SpreadTrends(named_df, game)
        self.total_trends = TotalTrends(named_df)
        self.trends = []
        self.trends += self.moneyline_trends.trends
        self.trends += self.spread_trends.trends
        self.trends += self.total_trends.trends

    def __str__(self):
        returner = ''
        for trend in self.trends:
            returner += str(trend) + '\n'
        return returner