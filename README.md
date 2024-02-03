# NFL Trends Analyzer

## Overview

The NFL Trends Analyzer is a Python tool designed to analyze historical data from every NFL game since 2006. It generates trends related to both game information and betting information, providing insights into home/away and favorite/underdog trends for moneylines, spreads, and totals.

## Installation

To use the NFL Trends Analyzer, follow these steps:

1. Clone the repository:
```bash
   git clone https://github.com/andyboulle/NFLTrendsAnalyzer.git
   cd NFLTrendsAnalyzer
```
2. Create a virtual environment:
```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv/Scripts/activate      # Windows
``` 
3. Install requirements:
```bash
   pip install -r requirements.txt
```
## Usage
1. Run `data_generator.py` to generate necessary datafiles:
```bash
   python scripts/data_generation/data_generator.py
```
2. Run `playground.py` to write trends:
```bash
   python scripts/playground.py
```
All customization will be done in the `playground.py` file. This is where you give the details of the game you want to analyze as well as set what trends you want to write. It will write the created trends to the `output.txt` file.
## Game Class

The `Game` class is a fundamental component of the NFL Trends Analyzer, serving as the primary means to input information for analysis. Instances of this class represent individual NFL games and encapsulate various parameters associated with those games.

### Parameters

- **Season (str):** The season in the format 'YYYY-YYYY', e.g., '2023-2024'.
- **Date (str):** The date of the game in the format 'YYYY-MM-DD', e.g., '2023-10-29'.
- **Home Team (str):** The name of the home team.
- **Away Team (str):** The name of the away team.
- **Home Moneyline (int):** Moneyline odds for the home team.
- **Away Moneyline (int):** Moneyline odds for the away team.
- **Home Spread (float):** Point spread for the home team.
- **Away Spread (float):** Point spread for the away team.
- **Total (float):** The total points for the game.

### Example Usage

```python
from src.analysis.objects.Game import Game

# Example Game
game = Game('2023-2024', '2023-10-29', 'Washington Commanders', 'Philadelphia Eagles', 265, -330, 7, -7, 43.5)
```
Instances of the Game class serve as the foundation for generating trends related to both game information and betting information within the NFL Trends Analyzer.
## Basic Trends

Basic Trends in the NFL trends analyzer are all the most basic categories of trends with no more specific filter applied to the search criteria. These trends are as follows:
### Moneyline Trends
- Home Team Record Straight Up
- Away Team Record Straight Up
- Favorite Record Straight Up
- Underdog Record Straight Up
- Home Favorite/Away Favorite Record Straight Up
- Home Underdog/Away Underdog Record Straight Up

### Spread Trends
- Home team Record ATS (Against the Spread)
- Away Team Record ATS
- Favored Record ATS
- Not Favored Record ATS
- Home Favored/Away Favored Record ATS
- Home Not Favored/Away Not Favored Record ATS

### Total Trends
- Overs Record
- Unders Record

These Basic Trends are the foundation of all the more complicated, specific, and filtered trends that will be discussed later. The given Game object will be used as the filter. For each unique aspect of the game (month, day, divisions, spread, moneyline, total, etc) the NFL Trend Analyzer will tell you the record for every single one of these basic trends with the filtered specifics attached (see examples below). The Game object passed will also determine things like whether the basic trends will use Home Favorite/Away Underdog or Away Favorite/Home Underdog, as well as Home Favored/Away Not Favored or Away Favored/Home Not Favored. 

**Note:** The words "favorite" and "underdog" are used when talking about moneylines and the words "favored" and "not favored" are used when talking about spreads.

## Option Trends

Option Trends in the NFL Trends Analyzer refer to comprehensive analyses that consider various combinations of options, providing valuable insights into team performance based on different criteria. These trends are instrumental in understanding patterns, tendencies, and statistical outcomes across a spectrum of factors. The major categories of Option Trends include:

### ```GameOptionTrends.py```: Game Information Trends

This section provides insights into trends based on various game information parameters. The trends include:

- **Day of the Week:** Analyzes team performance on specific days.

- **Regular Season or Post Season:** Compares team performance during regular and post seasons.

- **Divisional Matchup:** Explores trends related to divisional games.

- **Month of the Year:** Examines performance trends based on the month.

**Examples:**
```
- Away Favored Record ATS in games where the month is 10 and it is a divisional game: 55-54-3 (49.11%)

- Overs Record in games where the month is 10 and it is the regular season and it is a divisional game: 149-167-4 (46.56%)

- Favored Record ATS in games where the day of the week is Sunday : 1905-2049-99 (47.0%)
```

### ```BettingOptionTrends.py```: Betting Information Trends

This section provides insights into trends based on betting information parameters. The trends include:

- **Moneyline:** Analyzes team performance based on moneyline odds.

- **Spread:** Explores trends related to team performance against the spread.

- **Total:** Examines performance trends related to total points.

**Examples:**
```
- Favorite Record Straight Up in games where the underdog moneyline is +265: 24-10-0 (70.59%)

- Home Not Favored Record ATS in games where the moneyline for the underdog is -100 or higher: 767-755-37 (49.2%)

- Unders Record in games where the spread is 7 and the total is 35.0 or higher : 93-97-8 (46.97%)
```

### ```IntegratedOptionTrends.py```: Integrated Trends

This section integrates trends from both game and betting information. It explores every possible combination of trends to provide comprehensive insights.

**Examples:**
```
- Home Team Record ATS in games where the spread is 7.0 or more and the total is 49.0 or lower and the day of the week is Sunday and the month is 10 and it is a divisional game: 17-15-1 (51.52%)

- Overs Record in games where the spread is 2.0 or more and the total is 37.5 or higher and the month is 10: 335-355-10 (47.86%)

- Away Team Record ATS in games where the moneyline for the favorite is -300 or lower and the total is 43.5 and it is a divisional game: 16-15-0 (51.61%)
```

### ```YearlyOptionTrends.py```: Yearly Trends

This section provides trends for every year since 2006. It combines game and betting information trends for each season.

**Examples:**
```
- Home Team Record ATS in games where the moneyline for the underdog is -100 or higher and the total is 61.5 or lower and the day of the week is Sunday and the month is 10 and it is the regular season since the 2010-2011 season: 341-384-20 (45.77%)

- Home Team Record Straight Up in games where the spread is 7 and the total is 41.0 or higher and it is the regular season and it is a divisional game since the 2021-2022 season: 7-2-0 (77.78%)

- Unders Record in games where the underdog moneyline is +265 and the total is 57.0 or lower and the day of the week is Sunday and the month is 10 since the 2023-2024 season: 1-0-0 (100.0%)
```
---
Plug any ```Game``` object into any of these option trend objects and discover any trends you could possibly imagine for that game. You can also plug a ```Game``` object into an ```AllOptionTrends``` object to get all of these other option trends in one.


## Contributions

Contributions are welcome! If you have any suggestions, bug reports, or enhancements, please open an issue or submit a pull request.
