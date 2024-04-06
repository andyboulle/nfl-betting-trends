"""
Module: trend.py

This module defines a class representing trends in sports betting. Trends capture patterns 
in game outcomes based on various factors such as category, month, day of the week, spread, 
total, and seasons.

Classes:
- Trend: Represents a trend in sports betting.

Attributes:
- trend_id: Unique identifier for the trend.
- category: Category of the trend, e.g., 'home outright', 'away ats'.
- month: Month of the trend.
- day_of_week: Day of the week of the trend.
- divisional: Indicates if the trend applies to divisional games.
- spread: Spread associated with the trend.
- total: Total associated with the trend.
- seasons: Seasons associated with the trend.
- conditions: Conditions associated with the trend.
- wins: Number of wins for the trend.
- losses: Number of losses for the trend.
- pushes: Number of pushes for the trend.
- total_games: Total number of games for the trend.
- win_pct: Win percentage for the trend.
- applicable_games: Games to which the trend applies.

Methods:
- __init__: Initializes a Trend object with the given attributes.
- update_record: Updates the trend record based on game outcomes.
- get_description: Returns a description of the trend.
- get_category_description: Returns a description of the trend category.
- get_month_description: Returns a description of the trend month.
- to_dict: Converts the trend object to a dictionary.
- to_tuple: Converts the trend object to a tuple.
- __str__: Returns a string representation of the trend.
"""

import hashlib

class Trend:
    """
    Class representing a trend in sports betting.

    Attributes:
    - trend_id (str): Unique identifier for the trend.
    - category (str): Category of the trend, e.g., 'home outright', 'away ats'.
    - month (str): Month of the trend.
    - day_of_week (str): Day of the week of the trend.
    - divisional (bool): Indicates if the trend applies to divisional games.
    - spread (float): Spread associated with the trend.
    - total (float): Total associated with the trend.
    - seasons (str): Seasons associated with the trend.
    - conditions (str): Conditions associated with the trend.
    - wins (int): Number of wins for the trend.
    - losses (int): Number of losses for the trend.
    - pushes (int): Number of pushes for the trend.
    - total_games (int): Total number of games for the trend.
    - win_pct (float): Win percentage for the trend.
    - applicable_games (list): Games to which the trend applies.

    Methods:
    - __init__: Initializes a Trend object with the given attributes.
    - update_record: Updates the trend record based on game outcomes.
    - get_description: Returns a description of the trend.
    - get_category_description: Returns a description of the trend category.
    - to_dict: Converts the trend object to a dictionary.
    - to_tuple: Converts the trend object to a tuple.
    - __str__: Returns a string representation of the trend.
    """

    trend_id = None

    category = None
    month = None
    day_of_week = None
    divisional = None
    spread = None
    total = None
    seasons = None
    conditions = None

    wins = None
    losses = None
    pushes = None
    total_games = None
    win_pct = None

    applicable_games = None

    def __init__(self, category, month, day_of_week, divisional, spread, total,
                  seasons, wins=0, losses=0, pushes=0, total_games=0, win_pct=0,
                    applicable_games=None):
        """
        Initializes a Trend object with the given attributes.

        Args:
        - category (str): Category of the trend.
        - month (str): Month of the trend.
        - day_of_week (str): Day of the week of the trend.
        - divisional (bool): Indicates if the trend applies to divisional games.
        - spread (float): Spread associated with the trend.
        - total (float): Total associated with the trend.
        - seasons (str): Seasons associated with the trend.
        - wins (int): Number of wins for the trend (default: 0).
        - losses (int): Number of losses for the trend (default: 0).
        - pushes (int): Number of pushes for the trend (default: 0).
        - total_games (int): Total number of games for the trend (default: 0).
        - win_pct (float): Win percentage for the trend (default: 0).
        - applicable_games (list): Games to which the trend applies (default: None).
        """

        self.category = category
        self.month = month
        self.day_of_week = day_of_week
        self.divisional = divisional
        self.spread = spread
        self.total = total
        self.seasons = seasons

        self.id_string = ','.join(map(str, [category, month, day_of_week,
                                             divisional, spread, total, seasons]))
        self.trend_id = hashlib.sha256(self.id_string.encode()).hexdigest()

        self.wins = wins
        self.losses = losses
        self.pushes = pushes
        self.total_games = total_games
        self.win_pct = win_pct

        self.applicable_games = applicable_games

    def update_record(self, game):
        """
        Updates the trend record based on game outcomes.

        Args:
        - game (Game): Game object representing the outcome of a game.

        Returns:
        - None
        """

        if self.category in ['home outright', 'away outright']:
            if game.tie:
                self.pushes += 1
            elif (self.category == 'home outright' and game.home_win) \
                  or (self.category == 'away outright' and game.away_win):
                self.wins += 1
            else:
                self.losses += 1
        elif self.category in ['favorite outright', 'underdog outright']:
            if not game.pickem:
                if game.tie:
                    self.pushes += 1
                elif (self.category == 'favorite outright' and game.favorite_win) \
                      or (self.category == 'underdog outright' and game.underdog_win):
                    self.wins += 1
                else:
                    self.losses += 1
        elif self.category in ['home favorite outright', 'away underdog outright']:
            if not game.pickem:
                if game.home_favorite:
                    if game.tie:
                        self.pushes += 1
                    elif (self.category == 'home favorite outright' and game.home_favorite_win) \
                          or (self.category == 'away underdog outright' and game.away_underdog_win):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['away favorite outright', 'home underdog outright']:
            if not game.pickem:
                if game.away_favorite:
                    if game.tie:
                        self.pushes += 1
                    elif (self.category == 'away favorite outright' and game.away_favorite_win) \
                          or (self.category == 'home underdog outright' and game.home_underdog_win):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['home ats', 'away ats']:
            if game.spread_push:
                self.pushes += 1
            elif (self.category == 'home ats' and game.home_cover) \
                  or (self.category == 'away ats' and game.away_cover):
                self.wins += 1
            else:
                self.losses += 1
        elif self.category in ['favorite ats', 'underdog ats']:
            if not game.pickem:
                if game.spread_push:
                    self.pushes += 1
                elif (self.category == 'favorite ats' and game.favorite_cover) \
                      or (self.category == 'underdog ats' and game.underdog_cover):
                    self.wins += 1
                else:
                    self.losses += 1
        elif self.category in ['home favorite ats', 'away underdog ats']:
            if not game.pickem:
                if game.home_favorite:
                    if game.spread_push:
                        self.pushes += 1
                    elif (self.category == 'home favorite ats' and game.home_favorite_cover) \
                          or (self.category == 'away underdog ats' and game.away_underdog_cover):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['away favorite ats', 'home underdog ats']:
            if not game.pickem:
                if game.away_favorite:
                    if game.spread_push:
                        self.pushes += 1
                    elif (self.category == 'away favorite ats' and game.away_favorite_cover) \
                          or (self.category == 'home underdog ats' and game.home_underdog_cover):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['over', 'under']:
            if game.total_push:
                self.pushes += 1
            elif (self.category == 'over' and game.over_hit) \
                  or (self.category == 'under' and game.under_hit):
                self.wins += 1
            else:
                self.losses += 1

        self.total_games = self.wins+self.losses+self.pushes
        win_pct_games = self.wins + self.losses + (self.pushes / 2)
        self.win_pct = 0 if win_pct_games == 0 \
              else round(self.wins / (self.wins + self.losses + (self.pushes / 2)) * 100, 2)

    def get_description(self):
        """
        Returns a description of the trend.

        Returns:
        - str: Description of the trend.
        """

        returner = ''
        returner += self.get_category_description(self.category)
        if self.day_of_week is not None:
            returner += f' on {self.day_of_week}s'
        if self.month is not None:
            returner += f' in {self.month}'
        if self.divisional is not None:
            returner += ' in divisional games' if self.divisional else ' in non-divisional games'
        if self.spread is not None:
            returner += f' when the spread is {self.spread}'
        if self.total is not None:
            returner += f' and the total is {self.total}' \
                  if self.spread is not None else f' when the total is {self.total}'
        if self.seasons is not None:
            returner += f' {self.seasons}'

        return returner

    def get_category_description(self, category):
        """
        Returns a description of the trend category.

        Args:
        - category (str): Category of the trend.

        Returns:
        - str: Description of the trend category.
        """

        returner = ''
        if category == 'home outright':
            returner += 'Home teams outright'
        elif category == 'away outright':
            returner += 'Away teams outright'
        elif category == 'favorite outright':
            returner += 'Favorites outright'
        elif category == 'underdog outright':
            returner += 'Underdogs outright'
        elif category == 'home favorite outright':
            returner += 'Home Favorites outright'
        elif category == 'away underdog outright':
            returner += 'Away Underdogs outright'
        elif category == 'away favorite outright':
            returner += 'Away Favorites outright'
        elif category == 'home underog outright':
            returner += 'Home Underdogs outright'
        elif category == 'home ats':
            returner += 'Home teams against the spread'
        elif category == 'away ats':
            returner += 'Away teams against the spread'
        elif category == 'favorite ats':
            returner += 'Favorites against the spread'
        elif category == 'underdog ats':
            returner += 'Underdogs against the spread'
        elif category == 'home favorite ats':
            returner += 'Home Favorites against the spread'
        elif category == 'away underdog ats':
            returner += 'Away Underdogs against the spread'
        elif category == 'away favorite ats':
            returner += 'Away Favorites against the spread'
        elif category == 'home underdog ats':
            returner += 'Home Underdogs against the spread'
        elif category == 'over':
            returner += 'Overs'
        elif category == 'under':
            returner += 'Unders'
        return returner

    def to_dict(self):
        """
        Converts the trend object to a dictionary.

        Returns:
        - dict: Dictionary representation of the trend.
        """

        return vars(self)

    def to_tuple(self):
        """
        Converts the trend object to a tuple.

        Returns:
        - tuple: Tuple representation of the trend.
        """

        if self.applicable_games is None:
            values = (
                self.trend_id,
                self.id_string,
                self.category,
                self.month,
                self.day_of_week,
                self.divisional,
                self.spread,
                self.total,
                self.seasons,
                int(self.wins),
                int(self.losses),
                int(self.pushes),
                int(self.total_games),
                float(self.win_pct)
            )
            return values

        values = (
            self.trend_id,
            self.id_string,
            self.category,
            self.month,
            self.day_of_week,
            self.divisional,
            self.spread,
            self.total,
            self.seasons,
            int(self.wins),
            int(self.losses),
            int(self.pushes),
            int(self.total_games),
            float(self.win_pct),
            self.applicable_games
        )
        return values

    def __str__(self):
        """
        Returns a string representation of the trend.

        Returns:
        - str: String representation of the trend.
        """

        return f'{self.id_string}: {self.wins}-{self.losses}-{self.pushes} ({self.win_pct}%)'
