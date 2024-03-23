"""
Module: upcoming_game.py

This module defines the UpcomingGame class, which represents an upcoming game
with its attributes such as date, teams, spreads, totals, and associated trends.

Classes:
- UpcomingGame: Represents an upcoming game with its attributes and methods.

Usage:
To use this module, import it into your Python script and create instances of
the UpcomingGame class with the required attributes.

Example:
    from upcoming_game import UpcomingGame

    # Create an instance of UpcomingGame
    game = UpcomingGame(date='2024-03-25', home_team='Home Team', away_team='Away Team',
                        home_spread=3.5, home_spread_odds=-110, away_spread_odds=-110,
                        home_moneyline_odds=-150, away_moneyline_odds=130,
                        over=45.5, over_odds=-110, under_odds=-110)

    # Access attributes of the game instance
    print(game.date)
    print(game.home_team)
    print(game.away_team)
    ...

This module requires the following external modules:
- hashlib: Provides cryptographic functionality.
- itertools: Provides functions for creating iterators.
- datetime: Provides classes for manipulating dates and times.
- models.trend: Contains the Trend class for trend data.
- models.game: Contains the Game class for game data.
- config: Contains configuration parameters such as team names, abbreviations, and divisions.
"""

import hashlib
import itertools
from datetime import datetime
from models.trend import Trend
import config

class UpcomingGame:
    """
    Represents an upcoming game with its attributes and methods.

    Attributes:
    - id: The unique identifier for the game.
    - id_string: A string representation of the game's identifier.
    - date: The date of the game.
    - month: The month of the game date.
    - day: The day of the game date.
    - year: The year of the game date.
    - season: The season of the game.
    - day_of_week: The day of the week of the game date.
    - home_team: The home team playing the game.
    - home_abbreviation: The abbreviation of the home team.
    - home_division: The division of the home team.
    - away_team: The away team playing the game.
    - away_abbreviation: The abbreviation of the away team.
    - away_divison: The division of the away team.
    - divisional: A boolean indicating if the game is divisional.
    - spread: The spread value for the game.
    - home_spread: The spread value for the home team.
    - home_spread_odds: The odds for the home spread.
    - away_spread: The spread value for the away team.
    - away_spread_odds: The odds for the away spread.
    - home_moneyline_odds: The moneyline odds for the home team.
    - away_moneyline_odds: The moneyline odds for the away team.
    - total: The total score for the game.
    - over: The over score for the game.
    - over_odds: The odds for the over score.
    - under: The under score for the game.
    - under_odds: The odds for the under score.
    - trends: The trends associated with the game.

    Methods:
    - __init__: Initializes an UpcomingGame object with provided attributes.
    - get_division: Retrieves the division of a given team.
    - to_dict: Converts the UpcomingGame object to a dictionary.
    - to_tuple: Converts the UpcomingGame object to a tuple.
    - __str__: Returns a string representation of the UpcomingGame object.
    """

    id = None
    id_string = None

    # Game info
    date = None
    month = None
    day = None
    year = None
    season = None
    day_of_week = None

    # Team info
    home_team = None
    home_abbreviation = None
    home_division = None
    away_team = None
    away_abbreviation = None
    away_divison = None
    divisional = None

    # Spread info
    spread = None
    home_spread = None
    home_spread_odds = None
    away_spread = None
    away_spread_odds = None

    # Moneyline info
    home_moneyline_odds = None
    away_moneyline_odds = None

    # Total info
    total = None
    over = None
    over_odds = None
    under = None
    under_odds = None

    trends = None

    def __init__(self, date, home_team, away_team, home_spread, \
                  home_spread_odds, away_spread_odds, \
                      home_moneyline_odds, away_moneyline_odds, \
                          over, over_odds, under_odds, trends_indicator=False):
        """
        Initializes an UpcomingGame object with provided attributes.

        Args:
        - date (str): The date of the game in 'YYYY-MM-DD' format.
        - home_team (str): The name of the home team.
        - away_team (str): The name of the away team.
        - home_spread (float): The spread value for the home team.
        - home_spread_odds (int): The odds for the home spread.
        - away_spread_odds (int): The odds for the away spread.
        - home_moneyline_odds (int): The moneyline odds for the home team.
        - away_moneyline_odds (int): The moneyline odds for the away team.
        - over (float): The over score for the game.
        - over_odds (int): The odds for the over score.
        - under_odds (int): The odds for the under score.
        - trends_indicator (bool): Indicator for retrieving trends (default: False).
        """

        # Game info
        self.date = date
        self.month = datetime.strptime(date.split('-')[1], '%m').strftime('%B')
        self.day = date.split('-')[2]
        self.year = date.split('-')[0]
        self.season = f'{self.year}-{int(self.year) + 1}' if int(date.split('-')[1]) > 8 \
              else f'{int(self.year) - 1}-{self.year}'
        self.day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

        # Team info
        self.home_team = home_team if home_team in config.TEAMS \
              else ValueError(f'{home_team} not a valid team')
        self.home_abbreviation = config.ABBREVIATIONS[home_team]
        self.home_division = self.get_division(home_team)
        self.away_team = away_team if away_team in config.TEAMS \
              else ValueError(f'{away_team} not a valid team')
        self.away_abbreviation = config.ABBREVIATIONS[away_team]
        self.away_division = self.get_division(away_team)
        self.divisional = self.home_division == self.away_division

        # Spread info
        self.home_spread = home_spread
        self.home_spread_odds = home_spread_odds
        self.away_spread = home_spread * -1
        self.away_spread_odds = away_spread_odds
        self.spread = max(self.home_spread, self.away_spread)

        # Moneyline info
        self.home_moneyline_odds = home_moneyline_odds
        self.away_moneyline_odds = away_moneyline_odds

        # Total info
        self.total = over
        self.over = over
        self.over_odds = over_odds
        self.under = over
        self.under_odds = under_odds

        # Id info
        self.id_string = f"{self.home_abbreviation}{self.away_abbreviation}{self.year}{str(date.split('-')[1]).zfill(2)}{self.day}"
        self.id = hashlib.sha256(self.id_string.encode()).hexdigest()

        if trends_indicator:
            self.trends = self.get_trends(self.month, self.day_of_week, \
                                           self.divisional, self.spread, self.total, self.season)

    def get_trends(self, month, day_of_week, divisional, spread, total, season):
        """
        Generates a list of trend objects based on specified conditions.

        Args:
        - month (str): Month for which trends are generated.
        - day_of_week (str): Day of the week for which trends are generated.
        - divisional (bool): Indicates whether trends are for divisional games.
        - spread (int): Spread value for which trends are generated.
        - total (int): Total value for which trends are generated.
        - season (str): Season for which trends are generated.

        Returns:
        - list of Trend objects: List of trend objects representing various combinations
        of conditions based on the input parameters.
        """

        spread_conditions = [None, f'{spread}']
        for i in range(1, config.MAX_SPREAD + 1):
            if i < spread:
                spread_conditions.append(f'{i} or more')
            elif i == spread:
                spread_conditions.extend([f'{i} or more', f'{i} or less'])
            else:
                spread_conditions.append(f'{i} or less')
        total_conditions = [None]
        for i in range(config.MIN_TOTAL, config.MAX_TOTAL + 1, 5):
            if i < total:
                total_conditions.append(f'{i} or more')
            elif i == total:
                total_conditions.extend([f'{i} or more', f'{i} or less'])
            else:
                total_conditions.append(f'{i} or less')
        start_year, end_year = map(int, config.OLDEST_SEASON.split('-'))
        season_conditions = [f'since {start_year}-{end_year}']
        while end_year < int(season.split('-')[1]):
            start_year += 1
            end_year += 1
            season_conditions.append(f'since {start_year}-{end_year}')

        categories = [
            'home outright', 'away outright', 
            'home ats', 'away ats',
            'over', 'under'
        ]

        if self.spread != 0:
            categories.extend(['favorite outright', 'underdog outright', \
                                'favorite ats', 'underdog ats'])
            categories.extend(
                ['home favorite outright', 'away underdog outright', \
                  'home favorite ats', 'away underdog ats'] if self.home_spread < 0
                else ['away favorite outright', 'home underdog outright', \
                       'away favorite ats', 'home underdog ats']
            )

        conditions = [categories, [month, None], [day_of_week, None], [divisional, None], \
                       spread_conditions, total_conditions, season_conditions]
        trends = [Trend(*args) for args in itertools.product(*conditions)]

        return trends

    def get_division(self, team):
        """
        Retrieves the division of a given team.

        Args:
        - team (str): The name of the team.

        Returns:
        - str: The division of the team.
        """

        for division, teams in config.DIVISIONS.items():
            if team in teams:
                return division
        return "NOT IN DIVISION"

    def to_dict(self):
        """
        Converts the UpcomingGame object to a dictionary.

        Returns:
        - dict: A dictionary representation of the UpcomingGame object.
        """
        return vars(self)

    def to_tuple(self):
        """
        Converts the UpcomingGame object to a tuple.

        Returns:
        - tuple: A tuple representation of the UpcomingGame object.
        """

        values = (
            self.id,
            self.id_string,
            self.date,
            self.month,
            int(self.day),
            int(self.year),
            self.season,
            self.day_of_week,
            self.home_team,
            self.home_abbreviation,
            self.home_division,
            self.away_team,
            self.away_abbreviation,
            self.away_division,
            self.divisional,
            float(self.spread),
            float(self.home_spread),
            int(self.home_spread_odds),
            float(self.away_spread),
            int(self.away_spread_odds),
            int(self.home_moneyline_odds),
            int(self.away_moneyline_odds),
            float(self.total),
            float(self.over),
            int(self.over_odds),
            float(self.under),
            int(self.under_odds)
        )
        return values

    def __str__(self):
        """
        Returns a string representation of the UpcomingGame object.

        Returns:
        - str: A string representation of the UpcomingGame object.
        """

        returner = ''
        for key, value in vars(self).items():
            returner += f'{key}: '
            if isinstance(value, dict):
                returner += ' {\n'
                for k, v in value.items():
                    returner += f'    {k}: {v}\n'
                returner += '}\n'
            elif isinstance(value, list):
                returner += ' [\n'
                for item in value:
                    returner += f'    {item}\n'
                returner += ']\n'
            else:
                returner += f'{value}\n'
        return returner
