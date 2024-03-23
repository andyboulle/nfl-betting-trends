"""
Module: game.py

This module defines the Game class, which represents a single game in a sports league.
The Game class encapsulates various attributes and methods for analyzing game data,
including game information, team information, score information, betting information, 
win results, cover results, total results, and trends.

Attributes:
    - id: A unique identifier for the game.
    - id_string: A string representation of the game identifier.
    - date: The date of the game.
    - month: The month of the game.
    - day: The day of the month of the game.
    - year: The year of the game.
    - season: The season of the game.
    - day_of_week: The day of the week of the game.
    - home_team: The name of the home team.
    - home_abbreviation: The abbreviation of the home team.
    - home_division: The division of the home team.
    - away_team: The name of the away team.
    - away_abbreviation: The abbreviation of the away team.
    - away_division: The division of the away team.
    - divisional: Indicates whether the game is divisional or not.
    - home_score: The score of the home team.
    - away_score: The score of the away team.
    - combined_score: The combined score of both teams.
    - tie: Indicates whether the game ended in a tie.
    - winner: The winning team.
    - loser: The losing team.
    - home_spread: The spread for the home team.
    - home_spread_result: The result of the spread for the home team.
    - away_spread: The spread for the away team.
    - away_spread_result: The result of the spread for the away team.
    - spread_push: Indicates whether the spread resulted in a push.
    - spread: The maximum spread value.
    - pk: Indicates whether the spread is zero.
    - total: The total score for betting purposes.
    - total_push: Indicates whether the total resulted in a push.
    - home_favorite: Indicates whether the home team is the favorite.
    - away_underdog: Indicates whether the away team is the underdog.
    - away_favorite: Indicates whether the away team is the favorite.
    - home_underdog: Indicates whether the home team is the underdog.
    - home_win: Indicates whether the home team won the game.
    - away_win: Indicates whether the away team won the game.
    - favorite_win: Indicates whether the favorite team won the game.
    - underdog_win: Indicates whether the underdog team won the game.
    - home_favorite_win: Indicates whether the home favorite team won the game.
    - away_underdog_win: Indicates whether the away underdog team won the game.
    - away_favorite_win: Indicates whether the away favorite team won the game.
    - home_underdog_win: Indicates whether the home underdog team won the game.
    - home_cover: Indicates whether the home team covered the spread.
    - away_cover: Indicates whether the away team covered the spread.
    - favorite_cover: Indicates whether the favorite team covered the spread.
    - underdog_cover: Indicates whether the underdog team covered the spread.
    - home_favorite_cover: Indicates whether the home favorite team covered the spread.
    - away_underdog_cover: Indicates whether the away underdog team covered the spread.
    - away_favorite_cover: Indicates whether the away favorite team covered the spread.
    - home_underdog_cover: Indicates whether the home underdog team covered the spread.
    - over_hit: Indicates whether the total score exceeded the betting total.
    - under_hit: Indicates whether the total score fell below the betting total.
    - trends: A list of Trend objects representing various trends for the game.

Methods:
    - __init__: Initializes a Game object with provided attributes.
    - get_trends: Generates trends for the game based on provided parameters.
    - get_division: Retrieves the division of a team.
    - get_win_results: Determines win results for the game based on provided parameters.
    - get_cover_results: Determines cover results for the game based on provided parameters.
    - to_dict: Converts the game object to a dictionary.
    - to_tuple: Converts the game object to a tuple.
    - __str__: Generates a string representation of the game object.
"""

import hashlib
import itertools
from datetime import datetime
from models.trend import Trend
import config

class Game:
    """
    Represents a game with various attributes and methods for analyzing game data.
    """

    # How the game will be selected from database
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

    # Score info
    home_score = None
    away_score = None
    combined_score = None
    tie = None
    winner = None
    loser = None

    # Betting info
    home_spread = None
    home_spread_result = None
    away_spread = None
    away_spread_result = None
    spread_push = None
    spread = None
    pk = None
    total = None
    total_push = None

    # Home/Away Favorite/Underdog info
    home_favorite = None
    away_underdog = None
    away_favorite = None
    home_underdog = None

    # Win Results info
    home_win = None
    away_win = None
    favorite_win = None
    underdog_win = None
    home_favorite_win = None
    away_underdog_win = None
    away_favorite_win = None
    home_underdog_win = None

    # Cover Results info
    home_cover = None
    away_cover = None
    favorite_cover = None
    underdog_cover = None
    home_favorite_cover = None
    away_underdog_cover = None
    away_favorite_cover = None
    home_underdog_cover = None

    # Total Results info
    over_hit = None
    under_hit = None

    trends = None

    def __init__(self, date, home_team, away_team,
                  home_score, away_score, home_spread, total, trends_indicator=False):
        """
        Initializes a Game object with provided attributes.

        Args:
            date (str): The date of the game in 'YYYY-MM-DD' format.
            home_team (str): The name of the home team.
            away_team (str): The name of the away team.
            home_score (int): The score of the home team.
            away_score (int): The score of the away team.
            home_spread (float): The spread of the home team.
            total (float): The total score for betting purposes.
            trends_indicator (bool, optional): Indicator for whether to
            compute trends for the game. Defaults to False.
        """

        # Game info
        self.date = date
        self.month = datetime.strptime(date.split('-')[1], '%m').strftime('%B')
        self.day = date.split('-')[2]
        self.year = date.split('-')[0]
        self.season = f'{self.year}-{int(self.year) + 1}' \
              if int(date.split('-')[1]) > 8 else f'{int(self.year) - 1}-{self.year}'
        self.day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

        # Team info
        self.home_team = home_team if home_team in \
              config.TEAMS else ValueError(f'{home_team} not a valid team')
        self.home_abbreviation = config.ABBREVIATIONS[home_team]
        self.home_division = self.get_division(home_team)
        self.away_team = away_team if away_team in \
              config.TEAMS else ValueError(f'{away_team} not a valid team')
        self.away_abbreviation = config.ABBREVIATIONS[away_team]
        self.away_division = self.get_division(away_team)
        self.divisional = self.home_division == self.away_division

        # Score info
        self.home_score = home_score
        self.away_score = away_score
        self.combined_score = home_score + away_score
        self.tie = home_score == away_score
        if self.tie:
            self.winner = None
            self.loser = None
        else:
            self.winner = home_team if home_score > away_score else away_team
            self.loser = home_team if home_score < away_score else away_team

        # Betting info
        self.home_spread = home_spread
        self.home_spread_result = away_score - home_score
        self.away_spread = home_spread * -1.0
        self.away_spread_result = home_score - away_score
        self.spread_push = self.home_spread_result == self.home_spread
        self.spread = max(self.home_spread, self.away_spread)
        self.pk = self.spread == 0.0
        self.total = total
        self.total_push = self.total == self.combined_score

        # Home/Away Favorite/Underdog info
        self.home_favorite = home_spread < 0
        self.away_underdog = home_spread < 0

        self.away_favorite = home_spread > 0
        self.home_underdog = home_spread > 0

        # Win Results info
        self.home_win, \
        self.away_win, \
        self.favorite_win, \
        self.underdog_win, \
        self.home_favorite_win, \
        self.away_underdog_win, \
        self.away_favorite_win, \
        self.home_underdog_win = self.get_win_results(self.home_score,
                                                       self.away_score, self.home_spread)

        # Cover Results info
        self.home_cover, \
        self.away_cover, \
        self.favorite_cover, \
        self.underdog_cover, \
        self.home_favorite_cover, \
        self.away_underdog_cover, \
        self.away_favorite_cover, \
        self.home_underdog_cover = self.get_cover_results(self.home_spread_result,
                                                           self.home_spread)

        # Total Results info
        self.over_hit = self.combined_score > self.total
        self.under_hit = self.combined_score < self.total

        # Id info
        self.id_string = f"{self.home_abbreviation}{self.away_abbreviation}{self.year}{str(date.split('-')[1]).zfill(2)}{self.day}"
        self.id = hashlib.sha256(self.id_string.encode()).hexdigest()

        if trends_indicator:
            self.trends = self.get_trends(self.month, self.day_of_week,
                                           self.divisional, self.spread, self.total, self.season)

    def get_trends(self, month, day_of_week, divisional, spread, total, season):
        """
        Generates trends for the game based on provided parameters.

        Args:
            month (str): The month of the game.
            day_of_week (str): The day of the week of the game.
            divisional (bool): Indicates if the game is divisional or not.
            spread (float): The spread value for the game.
            total (float): The total score for betting purposes.
            season (str): The season of the game.

        Returns:
            list: List of Trend objects representing various trends for the game.
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

        if not self.pk:
            categories.extend(['favorite outright', 'underdog outright',
                                'favorite ats', 'underdog ats'])
            categories.extend(
                ['home favorite outright', 'away underdog outright',
                  'home favorite ats', 'away underdog ats'] if self.home_favorite 
                else ['away favorite outright', 'home underdog outright',
                       'away favorite ats', 'home underdog ats']
            )

        conditions = [categories, [month, None], [day_of_week, None], [divisional, None],
                       spread_conditions, total_conditions, season_conditions]
        trends = [Trend(*args) for args in itertools.product(*conditions)]

        return trends

    def get_division(self, team):
        """
        Retrieves the division of a team.

        Args:
            team (str): The name of the team.

        Returns:
            str: The division of the team.
        """

        for division, teams in config.DIVISIONS.items():
            if team in teams:
                return division
        return "NOT IN DIVISION"

    def get_win_results(self, home_score, away_score, home_spread):
        """
        Determines win results for the game based on provided parameters.

        Args:
            home_score (int): The score of the home team.
            away_score (int): The score of the away team.
            home_spread (float): The spread of the home team.

        Returns:
            tuple: A tuple containing win results for various scenarios.
        """

        home, away, favorite, underdog, home_favorite, away_underdog, away_favorite, \
              home_underdog = False, False, False, False, False, False, False, False

        if not self.tie:
            home = home_score > away_score
            away = home_score < away_score
            if home_spread != 0:
                favorite = home_score > away_score if home_spread < 0 else home_score < away_score
                underdog = home_score < away_score if home_spread < 0 else home_score > away_score
                if self.home_favorite:
                    home_favorite = home_score > away_score
                    away_underdog = home_score < away_score
                    away_favorite = False
                    home_underdog = False
                else:
                    away_favorite = home_score < away_score
                    home_underdog = home_score > away_score
                    home_favorite = False
                    away_underdog = False
            else:
                favorite = False
                underdog = False
                home_favorite = False
                away_underdog = False
                away_favorite = False
                home_underdog = False

        return home, away, favorite, underdog, home_favorite, \
              away_underdog, away_favorite, home_underdog

    def get_cover_results(self, home_spread_result, home_spread):
        """
        Determines cover results for the game based on provided parameters.

        Args:
            home_spread_result (float): The spread result of the home team.
            home_spread (float): The spread of the home team.

        Returns:
            tuple: A tuple containing cover results for various scenarios.
        """

        home, away, favorite, underdog, home_favorite, away_underdog, away_favorite, \
              home_underdog = False, False, False, False, False, False, False, False

        if not self.spread_push:
            home = home_spread_result < home_spread
            away = home_spread_result > home_spread
            if home_spread != 0:
                favorite = home_spread_result < home_spread if home_spread < 0 \
                      else home_spread_result > home_spread
                underdog = home_spread_result < home_spread if home_spread > 0 \
                      else home_spread_result > home_spread
                if home_spread < 0:
                    home_favorite = home_spread_result < home_spread
                    away_underdog = home_spread_result > home_spread
                    away_favorite = False
                    home_underdog = False
                else:
                    away_favorite = home_spread_result > home_spread
                    home_underdog = home_spread_result < home_spread
                    home_favorite = False
                    away_underdog = False
            else:
                favorite = False
                underdog = False
                home_favorite = False
                away_underdog = False
                away_favorite = False
                home_underdog = False

        return home, away, favorite, underdog, home_favorite, \
              away_underdog, away_favorite, home_underdog

    def to_dict(self):
        """
        Converts the game object to a dictionary.

        Returns:
            dict: A dictionary representation of the game object.
        """

        return vars(self)

    def to_tuple(self):
        """
        Converts the game object to a tuple.

        Returns:
            tuple: A tuple representation of the game object.
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
            int(self.home_score),
            int(self.away_score),
            int(self.combined_score),
            self.tie,
            self.winner,
            self.loser,
            float(self.spread),
            float(self.home_spread),
            int(self.home_spread_result),
            float(self.away_spread),
            int(self.away_spread_result),
            self.spread_push,
            self.pk,
            float(self.total),
            self.total_push,
            self.home_favorite,
            self.away_underdog,
            self.away_favorite,
            self.home_underdog,
            self.home_win,
            self.away_win,
            self.favorite_win,
            self.underdog_win,
            self.home_favorite_win,
            self.away_underdog_win,
            self.away_favorite_win,
            self.home_underdog_win,
            self.home_cover,
            self.away_cover,
            self.favorite_cover,
            self.underdog_cover,
            self.home_favorite_cover,
            self.away_underdog_cover,
            self.away_favorite_cover,
            self.home_underdog_cover,
            self.over_hit,
            self.under_hit
        )
        return values

    def __str__(self):
        """
        Generates a string representation of the game object.

        Returns:
            str: A string representation of the game object.
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
    