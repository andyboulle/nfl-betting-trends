import unittest
import pandas as pd

analysis_data_filename = 'datafiles/csv/analysis_data.csv'

class TestDataProperties(unittest.TestCase):
    
    df = pd.read_csv(analysis_data_filename)

    # Test there are the correct number of columns
    def test_column_count(self):
        expected_column_count = 60
        actual_column_count = len(self.df.columns)
        self.assertEqual(actual_column_count, expected_column_count) 

    # Test the columns are correctly named and in the right order
    def test_existing_columns(self):
        expected_columns = [
        'Season','Date','Day of Week','Month','Day','Year',
        'Home Team','Home Division','Away Team','Away Division',
        'Home Score','Away Score','Total Score','Home Spread Result','Away Spread Result','Winner','Loser',
        'Divisional Game?','Tie?','Overtime?','Playoff Game?','Neutral Venue?',
        'Home Moneyline Open','Away Moneyline Open','Favorite Moneyline', 'Underdog Moneyline', 'Equal Moneyline?',
        'Home Favorite?','Home Underdog?','Away Favorite?','Away Underdog?',
        'Home Team Win?','Away Team Win?','Favorite Win?','Underdog Win?','Home Favorite Win?','Home Underdog Win?','Away Favorite Win?','Away Underdog Win?',
        'Line Open', 'Home Line Open','Away Line Open','PK?','Home Favored?','Home Not Favored?','Away Favored?','Away Not Favored?', 'Spread Push?',
        'Home Cover?','Away Cover?','Favored Cover?','Not Favored Cover?','Home Favored Cover?','Home Not Favored Cover?','Away Favored Cover?','Away Not Favored Cover?',
        'Total Score Open','Total Push?','Over Hit?','Under Hit?'
        ]
        actual_columns = self.df.columns.tolist()
        self.assertEqual(actual_columns, expected_columns)

    def test_no_missing_data(self):
        for col in self.df.columns:
            for idx, value in self.df[col].items():
                if pd.isnull(value):
                    print(self.df.iloc[idx])
                    print(f"Column: {col}, Index: {idx}, Value: {value}")
        table_has_empty_elements = self.df.isnull().values.any()
        self.assertFalse(table_has_empty_elements)
