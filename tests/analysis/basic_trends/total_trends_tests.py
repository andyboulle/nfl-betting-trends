from src.analysis.objects.NamedDataframe import NamedDataframe
from src.analysis.objects.Game import Game
from src.analysis.basic_trends.TotalTrends import TotalTrends
import unittest
import pandas as pd
from io import StringIO

class TestTotalTrends(unittest.TestCase):

    # Data set that contains all possible moneyline, spread, and total combinations
    data = """
    Season,Date,Day of Week,Month,Day,Year,Home Team,Home Division,Away Team,Away Division,Home Score,Away Score,Total Score,Winner,Loser,Divisional Game?,Tie?,Overtime?,Playoff Game?,Neutral Venue?,Spread,Home Spread,Away Spread,PK?,Home Spread Result,Away Spread Result,Spread Push?,Home Favorite?,Away Underdog?,Away Favorite?,Home Underdog?,Home Team Win?,Away Team Win?,Favorite Win?,Underdog Win?,Home Favorite Win?,Away Underdog Win?,Away Favorite Win?,Home Underdog Win?,Home Team Cover?,Away Team Cover?,Favorite Cover?,Underdog Cover?,Home Favorite Cover?,Away Underdog Cover?,Away Favorite Cover?,Home Underdog Cover?,Total Score Open,Total Push?,Over Hit?,Under Hit?
    2023-2024,2024-01-07,Sunday,1,7,2024,Miami Dolphins,AFC East,Buffalo Bills,AFC East,14,21,35,Buffalo Bills,Miami Dolphins,Y,N,N,N,N,3.0,3.0,-3.0,N,7,-7,N,N,N,Y,Y,N,Y,Y,N,N,N,Y,N,N,Y,Y,N,N,N,Y,N,50.0,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Arizona Cardinals,NFC West,Seattle Seahawks,NFC West,20,21,41,Seattle Seahawks,Arizona Cardinals,Y,N,N,N,N,3.0,3.0,-3.0,N,1,-1,N,N,N,Y,Y,N,Y,Y,N,N,N,Y,N,Y,N,N,Y,N,N,N,Y,47.5,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Carolina Panthers,NFC South,Tampa Bay Buccaneers,NFC South,0,9,9,Tampa Bay Buccaneers,Carolina Panthers,Y,N,N,N,N,6.0,6.0,-6.0,N,9,-9,N,N,N,Y,Y,N,Y,Y,N,N,N,Y,N,N,Y,Y,N,N,N,Y,N,37.0,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Cincinnati Bengals,AFC North,Cleveland Browns,AFC North,31,14,45,Cincinnati Bengals,Cleveland Browns,Y,N,N,N,N,4.0,-4.0,4.0,N,-17,17,N,Y,Y,N,N,Y,N,Y,N,Y,N,N,N,Y,N,Y,N,Y,N,N,N,40.0,N,Y,N
    2023-2024,2024-01-07,Sunday,1,7,2024,Detroit Lions,NFC North,Minnesota Vikings,NFC North,30,20,50,Detroit Lions,Minnesota Vikings,Y,N,N,N,N,4.0,-4.0,4.0,N,-10,10,N,Y,Y,N,N,Y,N,Y,N,Y,N,N,N,Y,N,Y,N,Y,N,N,N,44.0,N,Y,N
    2023-2024,2024-01-07,Sunday,1,7,2024,Green Bay Packers,NFC North,Chicago Bears,NFC North,17,9,26,Green Bay Packers,Chicago Bears,Y,N,N,N,N,1.5,-1.5,1.5,N,-8,8,N,Y,Y,N,N,Y,N,Y,N,Y,N,N,N,Y,N,Y,N,Y,N,N,N,44.0,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Indianapolis Colts,AFC South,Houston Texans,AFC South,19,23,42,Houston Texans,Indianapolis Colts,Y,N,N,N,N,1.5,-1.5,1.5,N,4,-4,N,Y,Y,N,N,N,Y,N,Y,N,Y,N,N,N,Y,N,Y,N,Y,N,N,46.5,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Los Angeles Chargers,AFC West,Kansas City Chiefs,AFC West,12,13,25,Kansas City Chiefs,Los Angeles Chargers,Y,N,N,N,N,1.0,-1.0,1.0,N,1,-1,N,Y,Y,N,N,N,Y,N,Y,N,Y,N,N,N,Y,N,Y,N,Y,N,N,35.5,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Las Vegas Raiders,AFC West,Denver Broncos,AFC West,27,14,41,Las Vegas Raiders,Denver Broncos,Y,N,N,N,N,2.5,-2.5,2.5,N,-13,13,N,Y,Y,N,N,Y,N,Y,N,Y,N,N,N,Y,N,Y,N,Y,N,N,N,38.0,N,Y,N
    2023-2024,2024-01-07,Sunday,1,7,2024,New England Patriots,AFC East,New York Jets,AFC East,3,17,20,New York Jets,New England Patriots,Y,N,N,N,N,2.0,-2.0,2.0,N,14,-14,N,Y,Y,N,N,N,Y,N,Y,N,Y,N,N,N,Y,N,Y,N,Y,N,N,37.5,N,N,Y
    """
    df = pd.read_csv(StringIO(data))
    named_df = NamedDataframe(df, "test data")

    total_trends = TotalTrends(named_df)

    # Test records for overs
    def test_over_record(self):
        expected_over_wins = 3
        expected_over_losses = 7

        actual_over_wins = self.total_trends.over_hits.wins
        actual_over_losses = self.total_trends.over_hits.losses

        self.assertEqual(expected_over_wins, actual_over_wins)
        self.assertEqual(expected_over_losses, actual_over_losses)

    # Test records for unders
    def test_under_record(self):
        expected_under_wins = 7
        expected_under_losses = 3

        actual_under_wins = self.total_trends.under_hits.wins
        actual_under_losses = self.total_trends.under_hits.losses

        self.assertEqual(expected_under_wins, actual_under_wins)
        self.assertEqual(expected_under_losses, actual_under_losses)
