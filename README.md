# NFL Betting Trends Web Application

## Introduction
Welcome to the NFL Betting Trends web application! This application provides users with valuable insights into NFL betting trends, allowing them to make informed decisions when placing bets on upcoming games. Whether you're a seasoned bettor or just getting started, our platform offers a wealth of data and features to enhance your betting experience.

## Summary
The NFL Betting Trends web application aggregates and analyzes historical data to identify patterns and trends in NFL games. Users can explore trends related to team performance, point spreads, moneylines, over/under totals, and more. By applying customizable filters, users can narrow down trends to specific criteria, enabling them to make more strategic betting decisions.

## Filters
The NFL Betting Trends web application offers a wide range of filters to customize your analysis and refine your betting strategy. These filters allow users to focus on specific aspects of NFL games, such as team performance, game type, spread, total, and more. Here are some of the key filters available:

- **Specific Trend Categories:** Filter trends based on home/away teams, favorites/underdogs, and overs/unders.
- **Specific Betting Categories:** Filter trends based on betting types, such as against the spread (ATS) or outright wins.
- **Month and Day:** Narrow down trends based on the month or day of the week games are played.
- **Spread and Total Ranges:** Set ranges for point spreads and over/under totals to focus on specific scenarios.
- **Seasons Included:** Set trends to be calculated since any season dating back to the 2006-2007 season.
- **Total Games and Win Percentage:** Filter trends based on a minimum number of total games played and a minimum win percentage.

## Installation
To get started with the NFL Betting Trends web application, follow these simple steps:

1. Clone this repository to your local machine using the following command:
```bash
git clone https://github.com/your_username/nfl-betting-trends.git
```

2. Navigate to the project directory:
```bash
cd nfl-betting-trends
```

3. Create and activate a python virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

4. Install the required dependencies by running:
```bash
pip install -r requirements.txt
```

5. Adjust the settings for your postgres database in `config/db_config.py`
```python
DB_HOST = 'HOST'
DB_PORT = "PORT"
DB_NAME = 'DATABASE'
DB_USER = 'USERNAME'
DB_PASSWORD = 'PASSWORD'
```

6. Set up the database schema by executing (takes a long time. ~12 hours):
```bash
python src/db.py
```

7. Enter your API Key for "The Odds API" (https://the-odds-api.com/) on line 144 of `daily_jobs.py`
```python
body = {
        "apiKey": "APIKEY", <-- This Line
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "dateFormat": "iso",
        "oddsFormat": "american",
        "bookmakers": "fanduel",
        "commenceTimeFrom": all_time_config.WEEK_START,
        "commenceTimeTo": all_time_config.WEEK_END,
    }
```

8. Run `daily_jobs.py` to get the updated lines for this week's games and add the games to the database
```bash
python src/daily_jobs.py
```

9. Launch the Flask application:
```bash
python src/app.py
```
Access the web application through your preferred web browser at http://localhost:5000.

10. Continuously update the database using `weekly_jobs.py` and `daily_jobs.py`
  - Run `daily_jobs.py` every day to get updated lines
  - Run `weekly_jobs.py` every Tuesday/Wednesday to add the last weeks trends to the database

## Usage
Upon accessing the NFL Betting Trends web application, users will encounter the following key features:

- **Home Page:** Displays a list of upcoming NFL games along with basic information such as teams, dates, and odds.
- **Game Details:** Clicking on a specific game leads to a detailed page showing trends and statistics for that game.
- **Filtering Options:** Users can apply various filters to customize trend display based on specific criteria like team, spread, moneyline, total, and more.
- **Interactive Charts:** Visual representations of trends provide users with intuitive insights into betting patterns and outcomes.

## License
This project is licensed under the MIT License.

## Feedback and Support
We welcome any feedback or suggestions for improving the NFL Trends Analyzer web application. If you encounter any issues or have ideas for new features, please open an issue on GitHub or reach out to us directly.
