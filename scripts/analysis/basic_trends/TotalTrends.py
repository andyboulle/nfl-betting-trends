#################################################################################
# TotalTrends.py                                                                #
#                                                                               #
# This file calculates the record for trends that have to do with totals. It    # 
# takes a named dataframe then calculates the record for overs/unders. It then  #
# stores these records in an array called trends. The toString method prints    #
# all of these records on their own line.                                       #                              
#################################################################################
import sys
sys.path.append('..')
from helpers.filter_functions import *
from objects.Record import Record
import pandas as pd

class TotalTrends:

    over_hits = None
    under_hits = None

    trends = None

    def __init__(self, named_df):
        self.over_hits = self.get_over_hits(named_df)
        self.under_hits = self.get_under_hits(named_df)
        self.trends = [
            self.over_hits, self.under_hits
        ]


    ###########################################
    #          Over/Under Calculators         # 
    ###########################################  
    def get_over_hits(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Total Push?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        over_hits = (df_clean['Over Hit?'] == 'Y').sum()
        over_misses = (df_clean['Over Hit?'] == 'N').sum()
        over_pushes = (df['Total Push?'] == 'Y').sum()
        over_record = Record(f'Overs Record in {identifiers}', over_hits, over_misses, over_pushes)

        return over_record
    
    def get_under_hits(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Total Push?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        under_hits = (df_clean['Under Hit?'] == 'Y').sum()
        under_misses = (df_clean['Under Hit?'] == 'N').sum()
        under_pushes = (df['Total Push?'] == 'Y').sum()
        under_record = Record(f'Unders Record in {identifiers}', under_hits, under_misses, under_pushes)

        return under_record
    

    ###########################################
    #                ToString                 # 
    ###########################################

    def __str__(self):
        returner = ''
        for hit in self.trends:
            returner += str(hit) + '\n'
        return returner