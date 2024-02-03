from src.analysis.objects.NamedDataframe import NamedDataframe
from src.analysis.objects.Game import Game
from src.analysis.basic_trends.SpreadTrends import SpreadTrends
import unittest
import pandas as pd
from io import StringIO

class TestSpreadTrends(unittest.TestCase):

    # Data set that contains all possible moneyline, spread, and total combinations
    data = """
    Season,Date,Day of Week,Month,Day,Year,Home Team,Home Division,Away Team,Away Division,Home Score,Away Score,Total Score,Home Spread Result,Away Spread Result,Winner,Loser,Divisional Game?,Tie?,Overtime?,Playoff Game?,Neutral Venue?,Home Moneyline Open,Away Moneyline Open,Favorite Moneyline,Underdog Moneyline,Equal Moneyline?,Home Favorite?,Home Underdog?,Away Favorite?,Away Underdog?,Home Team Win?,Away Team Win?,Favorite Win?,Underdog Win?,Home Favorite Win?,Home Underdog Win?,Away Favorite Win?,Away Underdog Win?,Line Open,Home Line Open,Away Line Open,PK?,Home Favored?,Home Not Favored?,Away Favored?,Away Not Favored?,Spread Push?,Home Cover?,Away Cover?,Favored Cover?,Not Favored Cover?,Home Favored Cover?,Home Not Favored Cover?,Away Favored Cover?,Away Not Favored Cover?,Total Score Open,Total Push?,Over Hit?,Under Hit?
    2023-2024,2024-01-07,Sunday,1,7,2024,Miami Dolphins,AFC East,Buffalo Bills,AFC East,14,21,35,7,-7,Buffalo Bills,Miami Dolphins,Y,N,N,N,N,+135,-160,-160,+135,N,N,Y,Y,N,N,Y,Y,N,N,N,Y,N,3.0,3.0,-3.0,N,N,Y,Y,N,N,N,Y,Y,N,N,N,Y,N,50.0,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Arizona Cardinals,NFC West,Seattle Seahawks,NFC West,20,21,41,1,-1,Seattle Seahawks,Arizona Cardinals,Y,N,N,N,N,+145,-170,-170,+145,N,N,Y,Y,N,N,Y,Y,N,N,N,Y,N,3.0,3.0,-3.0,N,N,Y,Y,N,N,Y,N,N,Y,N,Y,N,N,47.5,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Carolina Panthers,NFC South,Tampa Bay Buccaneers,NFC South,0,9,9,9,-9,Tampa Bay Buccaneers,Carolina Panthers,Y,N,N,N,N,+195,-240,-240,+195,N,N,Y,Y,N,N,Y,Y,N,N,N,Y,N,6.0,6.0,-6.0,N,N,Y,Y,N,N,N,Y,Y,N,N,N,Y,N,37.0,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Cincinnati Bengals,AFC North,Cleveland Browns,AFC North,31,14,45,-17,17,Cincinnati Bengals,Cleveland Browns,Y,N,N,N,N,-180,+150,-180,+150,N,Y,N,N,Y,Y,N,Y,N,Y,N,N,N,4.0,-4.0,4.0,N,Y,N,N,Y,N,Y,N,Y,N,Y,N,N,N,40.0,N,Y,N
    2023-2024,2024-01-07,Sunday,1,7,2024,Detroit Lions,NFC North,Minnesota Vikings,NFC North,30,20,50,-10,10,Detroit Lions,Minnesota Vikings,Y,N,N,N,N,-185,+155,-185,+155,N,Y,N,N,Y,Y,N,Y,N,Y,N,N,N,4.0,-4.0,4.0,N,Y,N,N,Y,N,Y,N,Y,N,Y,N,N,N,44.0,N,Y,N
    2023-2024,2024-01-07,Sunday,1,7,2024,Green Bay Packers,NFC North,Chicago Bears,NFC North,17,9,26,-8,8,Green Bay Packers,Chicago Bears,Y,N,N,N,N,-125,+105,-125,+105,N,Y,N,N,Y,Y,N,Y,N,Y,N,N,N,1.5,-1.5,1.5,N,Y,N,N,Y,N,Y,N,Y,N,Y,N,N,N,44.0,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Indianapolis Colts,AFC South,Houston Texans,AFC South,19,23,42,4,-4,Houston Texans,Indianapolis Colts,Y,N,N,N,N,-125,+105,-125,+105,N,Y,N,N,Y,N,Y,N,Y,N,N,N,Y,1.5,-1.5,1.5,N,Y,N,N,Y,N,N,Y,N,Y,N,N,N,Y,46.5,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Los Angeles Chargers,AFC West,Kansas City Chiefs,AFC West,12,13,25,1,-1,Kansas City Chiefs,Los Angeles Chargers,Y,N,N,N,N,-115,-105,-115,-105,N,Y,N,N,Y,N,Y,N,Y,N,N,N,Y,1.0,-1.0,1.0,N,Y,N,N,Y,N,N,Y,N,Y,N,N,N,Y,35.5,N,N,Y
    2023-2024,2024-01-07,Sunday,1,7,2024,Las Vegas Raiders,AFC West,Denver Broncos,AFC West,27,14,41,-13,13,Las Vegas Raiders,Denver Broncos,Y,N,N,N,N,-140,+120,-140,+120,N,Y,N,N,Y,Y,N,Y,N,Y,N,N,N,2.5,-2.5,2.5,N,Y,N,N,Y,N,Y,N,Y,N,Y,N,N,N,38.0,N,Y,N
    2023-2024,2024-01-07,Sunday,1,7,2024,New England Patriots,AFC East,New York Jets,AFC East,3,17,20,14,-14,New York Jets,New England Patriots,Y,N,N,N,N,-130,+110,-130,+110,N,Y,N,N,Y,N,Y,N,Y,N,N,N,Y,2.0,-2.0,2.0,N,Y,N,N,Y,N,N,Y,N,Y,N,N,N,Y,37.5,N,N,Y
    """
    df = pd.read_csv(StringIO(data))
    named_df = NamedDataframe(df, "test data")

    # Game with a home favored/away not favored
    home_favored_game = Game('2023-2024', '2023-09-12', 'New York Jets', 'New England Patriots', -330, 265, -6.5, 6.5, 49.5)

    # Game with a home not favored/away favored
    away_favored_game = Game('2023-2024', '2023-09-12', 'New England Patriots', 'New York Jets', 265, -330, 6.5, -6.5, 49.5)

    home_favored_spread_trends = SpreadTrends(named_df, home_favored_game)
    away_favored_spread_trends = SpreadTrends(named_df, away_favored_game)

    # Test records for home teams ATS
    def test_home_record(self):

        expected_home_wins = 5
        expected_home_losses = 5

        actual_home_wins = self.home_favored_spread_trends.home_covers.wins
        actual_home_losses = self.home_favored_spread_trends.home_covers.losses

        self.assertEqual(expected_home_wins, actual_home_wins)
        self.assertEqual(expected_home_losses, actual_home_losses)

    # Test records for away teams ATS
    def test_away_record(self):

        expected_away_wins = 5
        expected_away_losses = 5

        actual_away_wins = self.home_favored_spread_trends.away_covers.wins
        actual_away_losses = self.home_favored_spread_trends.away_covers.losses
        
        self.assertEqual(expected_away_wins, actual_away_wins)
        self.assertEqual(expected_away_losses, actual_away_losses)

    # Test records for favored teams ATS
    def test_favored_record(self):

        expected_favored_wins = 6
        expected_favored_losses = 4

        actual_favored_wins = self.home_favored_spread_trends.favored_covers.wins
        actual_favored_losses = self.home_favored_spread_trends.favored_covers.losses
        
        self.assertEqual(expected_favored_wins, actual_favored_wins)
        self.assertEqual(expected_favored_losses, actual_favored_losses)

    # Test records for not favored teams ATS
    def test_not_favored_record(self):

        expected_not_favored_wins = 4
        expected_not_favored_losses = 6

        actual_not_favored_wins = self.home_favored_spread_trends.not_favored_covers.wins
        actual_not_favored_losses = self.home_favored_spread_trends.not_favored_covers.losses
        
        self.assertEqual(expected_not_favored_wins, actual_not_favored_wins)
        self.assertEqual(expected_not_favored_losses, actual_not_favored_losses)

    # Test records for home favored teams ATS
    def test_home_favored_record(self):

        expected_home_favored_wins = 4
        expected_home_favored_losses = 3

        actual_home_favored_wins = self.home_favored_spread_trends.home_favored_covers.wins
        actual_home_favored_losses = self.home_favored_spread_trends.home_favored_covers.losses
        
        self.assertEqual(expected_home_favored_wins, actual_home_favored_wins)
        self.assertEqual(expected_home_favored_losses, actual_home_favored_losses)

    # Test records for home not favored teams ATS
    def test_home_not_favored_record(self):

        expected_home_not_favored_wins = 1
        expected_home_not_favored_losses = 2

        actual_home_not_favored_wins = self.away_favored_spread_trends.home_not_favored_covers.wins
        actual_home_not_favored_losses = self.away_favored_spread_trends.home_not_favored_covers.losses
        
        self.assertEqual(expected_home_not_favored_wins, actual_home_not_favored_wins)
        self.assertEqual(expected_home_not_favored_losses, actual_home_not_favored_losses)

    # Test records for away favored teams ATS
    def test_away_favored_record(self):

        expected_away_favored_wins = 2
        expected_away_favored_losses = 1

        actual_away_favored_wins = self.away_favored_spread_trends.away_favored_covers.wins
        actual_away_favored_losses = self.away_favored_spread_trends.away_favored_covers.losses
        
        self.assertEqual(expected_away_favored_wins, actual_away_favored_wins)
        self.assertEqual(expected_away_favored_losses, actual_away_favored_losses)

    # Test records for away not favored teams ATS
    def test_away_not_favored_record(self):

        expected_away_not_favored_wins = 3
        expected_away_not_favored_losses = 4

        actual_away_not_favored_wins = self.home_favored_spread_trends.away_not_favored_covers.wins
        actual_away_not_favored_losses = self.home_favored_spread_trends.away_not_favored_covers.losses
        
        self.assertEqual(expected_away_not_favored_wins, actual_away_not_favored_wins)
        self.assertEqual(expected_away_not_favored_losses, actual_away_not_favored_losses)
