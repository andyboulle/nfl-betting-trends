import unittest
import pandas as pd

analysis_data_filename = 'datafiles/csv/analysis_data.csv'

class TestDataProperties(unittest.TestCase):
    
    df = pd.read_csv(analysis_data_filename)

    # Test there are the correct number of columns
    def test_column_count(self):
        expected_column_count = 51
        actual_column_count = len(self.df.columns)
        self.assertEqual(actual_column_count, expected_column_count) 

    # Test the columns are correctly named and in the right order
    def test_existing_columns(self):
        expected_columns = [
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
