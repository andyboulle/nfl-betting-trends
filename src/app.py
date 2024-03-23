"""
Flask Application: TrendAnalyzer

This Flask application provides a web interface for analyzing upcoming games and their trends.

Routes:
- '/' (GET, POST): Displays the index page with upcoming games and allows filtering trends.
- '/<id>' (GET, POST): Displays a single game with its associated trends.

Functions:
- index(): Renders the index page with upcoming games and allows filtering trends.
- single_game(id): Renders a single game page with its associated trends.

Execution:
The application can be executed directly, running the Flask web server in debug mode.

Example:
    if __name__ == '__main__':
        app.run(debug=True)
"""

from flask import Flask, render_template, request
import psycopg2
from models.upcoming_game import UpcomingGame
from models.trend import Trend

app = Flask(__name__)

DB_HOST = 'postgres'
DB_PORT = "5432"
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'pass'

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render the index page with upcoming games and allows filtering trends.

    This function handles both GET and POST requests for the index page. For GET requests,
    it retrieves all upcoming games from the database and renders the index page with
    default filter options. For POST requests, it processes the form data submitted by
    the user to filter the trends and renders the index page accordingly.

    Returns:
        render_template: HTML template for the index page.
    """

    # Connect to database
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host="localhost", port=DB_PORT)
    cur = conn.cursor()

    # Get all upcoming games and pass to index
    games = {}
    cur.execute("SELECT * FROM upcoming_games")
    rows = cur.fetchall()
    for row in rows:
        games[row[0]] = UpcomingGame(
            row[2], row[8], row[11], row[16], row[17], row[19],
            row[20], row[21], row[23], row[24], row[26]
        )

    sql_query = 'SELECT * FROM trends WHERE id IS NOT NULL'

    filters = {}

    if request.method == 'POST':
        # Extract trend categories from POST form
        filters['home'] = request.form['home']
        filters['away'] = request.form['away']
        filters['favorite'] = request.form['favorite']
        filters['underdog'] = request.form['underdog']
        filters['home favorite'] = request.form['home_favorite']
        filters['away underdog'] = request.form['away_underdog']
        filters['away favorite'] = request.form['away_favorite']
        filters['home underdog'] = request.form['home_underdog']

        # Add trend categories to SQL query
        sql_query += ' AND ((('
        for filter, value in filters.items():
            if value == 'true':
                if filter in ('home', 'away', 'favorite', 'underdog'):
                    sql_query += f" category LIKE '{filter} o%' OR category LIKE '{filter} a%' OR"
                else:
                    sql_query += f" category LIKE '%{filter}%' OR"
        sql_query += ' FALSE)'

        # Extract betting categories from POST form
        filters['ats'] = request.form['ats']
        filters['outright'] = request.form['outright']

        # Add betting categories to SQL query
        sql_query += ' AND ('
        for filter, value in filters.items():
            if filter in ('ats', 'outright') and value == 'true':
                sql_query += f" category LIKE '%{filter}%' OR"
        sql_query += ' FALSE))'

        # Extract over/under categories from POST form
        filters['over'] = request.form['over']
        filters['under'] = request.form['under']

        # Add over/under categories to SQL query
        sql_query += ' OR ('
        if filters['over'] == 'true':
            sql_query += " category = 'over' OR"
        if filters['under'] == 'true':
            sql_query += " category = 'under' OR"
        sql_query += ' FALSE))'

        # Extract month categories and add them to SQL query
        filters['no_month'] = request.form['no_month']
        months = ['January', 'February', 'September', 'October', 'November', 'December']
        selected_months = []
        for month in months:
            filters[month.lower()] = request.form[month.lower()]
            if filters[month.lower()] == 'true':
                selected_months.append(f"'{month}'")
        sql_query += ' AND ('

        month_list = ','.join(selected_months)

        # Filter by selected month categories
        if filters['no_month'] == 'true':
            sql_query += ' month IS NULL'
        if filters['no_month'] == 'true' and len(selected_months) > 0:
            sql_query += ' OR'
        if len(selected_months) > 0:
            sql_query += f" (month IN ({month_list}))"
        sql_query += ')'

        # Extract day categories and add them to SQL query
        filters['no_day'] = request.form['no_day']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        selected_days = []
        for day in days:
            filters[day.lower()] = request.form[day.lower()]
            if filters[day.lower()] == 'true':
                selected_days.append(f"'{day}'")
        sql_query += ' AND ('

        day_list = ','.join(selected_days)

        # Filter by selected day categories
        if filters['no_day'] == 'true':
            sql_query += ' day_of_week IS NULL'
        if filters['no_day'] == 'true' and len(selected_days) > 0:
            sql_query += ' OR'
        if len(selected_days) > 0:
            sql_query += f" (day_of_week IN ({day_list}))"
        sql_query += ')'

        # Extract type categories and add them to SQL query
        filters['no_type'] = request.form['no_type']
        filters['divisional'] = request.form['divisional']
        filters['non_divisional'] = request.form['non_divisional']
        sql_query += ' AND ('

        # Filter by selected type categories
        if filters['no_type'] == 'true':
            sql_query += ' divisional IS NULL'
        if filters['no_type'] == 'true' and filters['divisional'] == 'true':
            sql_query += ' OR'
        if filters['divisional'] == 'true':
            sql_query += ' divisional=TRUE'
        if filters['no_type'] == 'true' and filters['non_divisional'] == 'true':
            sql_query += ' OR'
        if filters['non_divisional'] == 'true':
            sql_query += ' divisional=FALSE'
        sql_query += ')'

        # Extract spread categories and add them to SQL query
        filters['no_spread'] = request.form['no_spread']
        spreads = []
        for i in range(1, 15):
            spreads.append(f'spread {i} or more')
            spreads.append(f'spread {i} or less')
            spreads.append(f'spread {i}.0')
            spreads.append(f'spread {i}.5')

        selected_spreads = []
        for spread in spreads:
            filters[spread] = request.form[spread]
            if filters[spread] == 'true':
                selected_spreads.append(f"'{spread[7:]}'")
        sql_query += ' AND ('

        spread_list = ','.join(selected_spreads)

        # Filter by selected spread categories
        if filters['no_spread'] == 'true':
            sql_query += ' spread IS NULL'
        if filters['no_spread'] == 'true' and len(selected_spreads) > 0:
            sql_query += ' OR'
        if len(selected_spreads) > 0:
            sql_query += f" (spread IN ({spread_list}))"
        sql_query += ')'

        # Extract total categories and add them to SQL query
        filters['no_total'] = request.form['no_total']
        totals = []
        for i in range(30, 61, 5):
            totals.append(f'total {i} or more')
            totals.append(f'total {i} or less')

        selected_totals = []
        for total in totals:
            filters[total] = request.form[total]
            if filters[total] == 'true':
                selected_totals.append(f"'{total[6:]}'")
        sql_query += ' AND ('

        total_list = ','.join(selected_totals)

        # Filter by selected total categories
        if filters['no_total'] == 'true':
            sql_query += ' total IS NULL'
        if filters['no_total'] == 'true' and len(selected_totals) > 0:
            sql_query += ' OR'
        if len(selected_totals) > 0:
            sql_query += f" (total IN ({total_list}))"
        sql_query += ')'

        # Extract seasons and add them to SQL query
        filters['seasons'] = request.form['seasons']
        if filters['seasons'] != 'since 2006-2007':
            seasons_included = []
            season_selected = filters['seasons'][6:]
            for i in range(int(season_selected[:4]), 2024):
                seasons_included.append(f"'since {i}-{i + 1}'")
            sql_query += f" AND seasons IN ({','.join(seasons_included)})"

        # Extract total games filtering method and add it to SQL query
        filters['gle_total_games'] = request.form['gle-total-games']
        filters['total_games'] = request.form['total-games']
        sql_query += ' AND total_games'
        if filters['gle_total_games'] == 'gt':
            sql_query += ' >'
        elif filters['gle_total_games'] == 'gte':
            sql_query += ' >='
        elif filters['gle_total_games'] == 'eq':
            sql_query += ' ='
        elif filters['gle_total_games'] == 'lte':
            sql_query += ' <='
        elif filters['gle_total_games'] == 'lt':
            sql_query += ' <'
        sql_query += f" {filters['total_games']}"

        # Extract win pct filtering method and add it to SQL query
        filters['gle_win_pct'] = request.form['gle-win-pct']
        filters['win_pct'] = request.form['win-pct']
        sql_query += ' AND win_percentage'
        if filters['gle_win_pct'] == 'gt':
            sql_query += ' >'
        elif filters['gle_win_pct'] == 'gte':
            sql_query += ' >='
        elif filters['gle_win_pct'] == 'eq':
            sql_query += ' ='
        elif filters['gle_win_pct'] == 'lte':
            sql_query += ' <='
        elif filters['gle_win_pct'] == 'lt':
            sql_query += ' <'
        sql_query += f" {filters['win_pct']}"

        filters['first_sort_category'] = request.form['first-sort-category']
        filters['first_sort_order'] = request.form['first-sort-order']
        filters['second_sort_category'] = request.form['second-sort-category']
        filters['second_sort_order'] = request.form['second-sort-order']

        filters['max_results'] = request.form['max_results']

    else:
        filters['home'] = 'true'
        filters['away'] = 'true'
        filters['favorite'] = 'true'
        filters['underdog'] = 'true'
        filters['home favorite'] = 'true'
        filters['away underdog'] = 'true'
        filters['away favorite'] = 'true'
        filters['home underdog'] = 'true'

        filters['ats'] = 'true'
        filters['outright'] = 'true'

        filters['over'] = 'true'
        filters['under'] = 'true'

        filters['no_month'] = 'true'
        months = ['January', 'February', 'September', 'October', 'November', 'December']
        for month in months:
            filters[month.lower()] = 'true'

        filters['no_day'] = 'true'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            filters[day.lower()] = 'true'

        filters['no_type'] = 'true'
        filters['divisional'] = 'true'
        filters['non_divisional'] = 'true'

        filters['no_spread'] = 'true'
        for i in range(1, 15):
            filters[f'spread {i} or more'] = 'true'
            filters[f'spread {i} or less'] = 'true'
            filters[f'spread {i}.0'] = 'true'
            filters[f'spread {i}.5'] = 'true'

        filters['no_total'] = 'true'
        for i in range(30, 61, 5):
            filters[f'total {i} or more'] = 'true'
            filters[f'total {i} or less'] = 'true'

        filters['seasons'] = 'since 2006-2007'

        filters['gle_total_games'] = 'gt'
        filters['total_games'] = '0'
        filters['gle_win_pct'] = 'gt'
        filters['win_pct'] = '0'

        filters['first_sort_category'] = 'win_percentage'
        filters['first_sort_order'] = 'desc'
        filters['second_sort_category'] = 'total_games'
        filters['second_sort_order'] = 'desc'

        filters['max_results'] = '50'

    # Add sorting methods and max results to SQL query
    sql_query += f" ORDER BY {filters['first_sort_category']} \
                    {filters['first_sort_order']}, \
                    {filters['second_sort_category']} \
                    {filters['second_sort_order']}"
    sql_query += f" LIMIT {filters['max_results']}"

    cur.execute(sql_query)
    trend_rows = cur.fetchall()

    trends = []
    trends_descriptions = []
    for row in trend_rows:
        trends.append(Trend(row[2], row[3], row[4], row[5], row[6], row[7],
                             row[8], row[9], row[10], row[11], row[12], row[13]))

    # Get descriptions for all trends for a game
    for trend in trends:
        trends_descriptions.append(trend.get_description())

    cur.close()
    conn.close()

    return render_template('index.html',
                            games=games, trends=trends,
                            trends_descriptions=trends_descriptions, filters=filters)

@app.route('/<id>', methods=['GET', 'POST'])
def single_game(id):
    """
    Render a single game page with its associated trends.

    This function handles both GET and POST requests for a single game page.
    For GET requests, it retrieves the game information and its associated trends
    from the database and renders the single game page. For POST requests, it
    processes the form data submitted by the user to filter the trends and renders
    the single game page accordingly.

    Args:
        id (str): The ID of the game to display.

    Returns:
        render_template: HTML template for the single game page.
    """

    # Connect to database
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host="localhost", port=DB_PORT)
    cur = conn.cursor()
    print(id)
    print(f"SELECT * FROM upcoming_games WHERE id='{id}'")
    cur.execute(f"SELECT * FROM upcoming_games WHERE id='{id}'")
    game_row = cur.fetchone()
    print(game_row)
    game = UpcomingGame(game_row[2], game_row[8], game_row[11], game_row[16], game_row[17],
                         game_row[19], game_row[20], game_row[21], game_row[23], game_row[24],
                           game_row[26], True)

    # Get all trends for game and pass to single game trends page
    trend_ids = [trend.id for trend in game.trends]
    trend_ids_with_quotes = [f"'{trend_id}'" for trend_id in trend_ids]
    placeholders = ','.join(trend_ids_with_quotes)

    sql_query = f"SELECT * FROM trends WHERE id IN ({placeholders})"

    filters = {}

    if request.method == 'POST':

        # Extract trend categories from POST form
        filters['home'] = request.form['home']
        filters['away'] = request.form['away']
        if game.spread != 0:
            filters['favorite'] = request.form['favorite']
            filters['underdog'] = request.form['underdog']
            if game.home_spread < 0:
                filters['home favorite'] = request.form['home_favorite']
                filters['away underdog'] = request.form['away_underdog']
            else:
                filters['away favorite'] = request.form['away_favorite']
                filters['home underdog'] = request.form['home_underdog']

        # Add trend categories to SQL query
        sql_query += ' AND ((('
        for filter, value in filters.items():
            if value == 'true':
                if filter in ('home', 'away', 'favorite', 'underdog'):
                    sql_query += f" category LIKE '{filter} o%' OR category LIKE '{filter} a%' OR"
                else:
                    sql_query += f" category LIKE '%{filter}%' OR"
        sql_query += ' FALSE)'

        # Extract betting categories from POST form
        filters['ats'] = request.form['ats']
        filters['outright'] = request.form['outright']

        # Add betting categories to SQL query
        sql_query += ' AND ('
        for filter, value in filters.items():
            if filter in ('ats', 'outright') and value == 'true':
                sql_query += f" category LIKE '%{filter}%' OR"
        sql_query += ' FALSE))'

        # Extract over/under categories from POST form
        filters['over'] = request.form['over']
        filters['under'] = request.form['under']

        # Add over/under categories to SQL query
        sql_query += ' OR ('
        if filters['over'] == 'true':
            sql_query += " category = 'over' OR"
        if filters['under'] == 'true':
            sql_query += " category = 'under' OR"
        sql_query += ' FALSE))'

        # Extract month category and add it to SQL query
        filters['no_month'] = request.form['no_month']
        filters['game_month'] = request.form['game_month']
        sql_query += ' AND('

        # Filter by selected month categories
        if filters['no_month'] == 'true':
            sql_query += ' month IS NULL'
        if filters['no_month'] == 'true' and filters['game_month'] == 'true':
            sql_query += ' OR'
        if filters['game_month'] == 'true':
            sql_query += f" month='{game.month}'"
        sql_query += ')'

        # Extract day category and add it to SQL query
        filters['no_day'] = request.form['no_day']
        filters['game_day'] = request.form['game_day']
        sql_query += ' AND('

        # Filter by selected day categories
        if filters['no_day'] == 'true':
            sql_query += ' day_of_week IS NULL'
        if filters['no_day'] == 'true' and filters['game_day'] == 'true':
            sql_query += ' OR'
        if filters['game_day'] == 'true':
            sql_query += f" day_of_week='{game.day_of_week}'"
        sql_query += ')'

        # Extract type category and add it to SQL query
        filters['no_type'] = request.form['no_type']
        filters['divisional'] = request.form['divisional']
        sql_query += ' AND('

        # Filter by selected type categories
        if filters['no_type'] == 'true':
            sql_query += ' divisional IS NULL'
        if filters['no_type'] == 'true' and filters['divisional'] == 'true':
            sql_query += ' OR'
        if filters['divisional'] == 'true':
            if game.divisional:
                sql_query += ' divisional=TRUE'
            else:
                sql_query += ' divisional=FALSE'
        sql_query += ')'

        # Extract spread filters from request form
        filters['no_spread'] = request.form['no_spread']
        for key, value in request.form.items():
            if 'spread ' in key:
                filters[key] = value

        # Add spread to SQL query
        sql_query += ' AND ('
        if filters['no_spread'] == 'true':
            sql_query += " spread IS NULL OR"
        for key, value in filters.items():
            if 'spread ' in key and value == 'true':
                sql_query += f" spread='{key[7:]}' OR "
        sql_query += ' FALSE)'

        # Extract total filters from request form
        filters['no_total'] = request.form['no_total']
        for key, value in request.form.items():
            if 'total ' in key:
                filters[key] = value

        # Add spread to SQL query
        sql_query += ' AND ('
        if filters['no_total'] == 'true':
            sql_query += " total IS NULL OR"
        for key, value in filters.items():
            if 'total ' in key and value == 'true':
                sql_query += f" total='{key[6:]}' OR "
        sql_query += ' FALSE)'

        # Extract seasons and add them to SQL query
        filters['seasons'] = request.form['seasons']
        if filters['seasons'] != 'since 2006-2007':
            seasons_included = []
            season_selected = filters['seasons'][6:]
            for i in range(int(season_selected[:4]), 2024):
                seasons_included.append(f"'since {i}-{i + 1}'")
            sql_query += f" AND seasons IN ({','.join(seasons_included)})"

        # Extract total games filtering method and add it to SQL query
        filters['gle_total_games'] = request.form['gle-total-games']
        filters['total_games'] = request.form['total-games']
        sql_query += ' AND total_games'
        if filters['gle_total_games'] == 'gt':
            sql_query += ' >'
        elif filters['gle_total_games'] == 'gte':
            sql_query += ' >='
        elif filters['gle_total_games'] == 'eq':
            sql_query += ' ='
        elif filters['gle_total_games'] == 'lte':
            sql_query += ' <='
        elif filters['gle_total_games'] == 'lt':
            sql_query += ' <'
        sql_query += f" {filters['total_games']}"

        # Extract win pct filtering method and add it to SQL query
        filters['gle_win_pct'] = request.form['gle-win-pct']
        filters['win_pct'] = request.form['win-pct']
        sql_query += ' AND win_percentage'
        if filters['gle_win_pct'] == 'gt':
            sql_query += ' >'
        elif filters['gle_win_pct'] == 'gte':
            sql_query += ' >='
        elif filters['gle_win_pct'] == 'eq':
            sql_query += ' ='
        elif filters['gle_win_pct'] == 'lte':
            sql_query += ' <='
        elif filters['gle_win_pct'] == 'lt':
            sql_query += ' <'
        sql_query += f" {filters['win_pct']}"

        filters['first_sort_category'] = request.form['first-sort-category']
        filters['first_sort_order'] = request.form['first-sort-order']
        filters['second_sort_category'] = request.form['second-sort-category']
        filters['second_sort_order'] = request.form['second-sort-order']

        filters['max_results'] = request.form['max_results']

    # Set default filters for when page is first loaded
    else:
        filters['home'] = 'true'
        filters['away'] = 'true'
        filters['favorite'] = 'true'
        filters['underdog'] = 'true'
        filters['home favorite'] = 'true'
        filters['away underdog'] = 'true'
        filters['away favorite'] = 'true'
        filters['home underdog'] = 'true'

        filters['ats'] = 'true'
        filters['outright'] = 'true'

        filters['over'] = 'true'
        filters['under'] = 'true'

        filters['no_month'] = 'true'
        filters['game_month'] = 'true'
        filters['no_day'] = 'true'
        filters['game_day'] = 'true'
        filters['no_type'] = 'true'
        filters['divisional'] = 'true'

        filters['no_spread'] = 'true'
        for i in range(1, 21):
            filters[f'spread {i} or more'] = 'true'
            filters[f'spread {i} or less'] = 'true'
            filters[f'spread {i}.0'] = 'true'
            filters[f'spread {i}.5'] = 'true'

        filters['no_total'] = 'true'
        for i in range(30, 61, 5):
            filters[f'total {i} or more'] = 'true'
            filters[f'total {i} or less'] = 'true'

        filters['seasons'] = 'since 2006-2007'

        filters['gle_total_games'] = 'gt'
        filters['total_games'] = '0'
        filters['gle_win_pct'] = 'gt'
        filters['win_pct'] = '0'

        filters['first_sort_category'] = 'win_percentage'
        filters['first_sort_order'] = 'desc'
        filters['second_sort_category'] = 'total_games'
        filters['second_sort_order'] = 'desc'

        filters['max_results'] = '50'

    # Add sorting methods and max results to SQL query
    sql_query += f" ORDER BY {filters['first_sort_category']} \
                    {filters['first_sort_order']}, \
                    {filters['second_sort_category']} \
                    {filters['second_sort_order']}"
    sql_query += f" LIMIT {filters['max_results']}"

    cur.execute(sql_query)
    trend_rows = cur.fetchall()

    trends = []
    trends_descriptions = []
    for row in trend_rows:
        trends.append(Trend(row[2], row[3], row[4], row[5], row[6],
                             row[7], row[8], row[9], row[10], row[11], row[12], row[13]))

    # Get descriptions for all trends for a game
    for trend in trends:
        trends_descriptions.append(trend.get_description())

    cur.close()
    conn.close()

    return render_template('single_game_trend_page.html', game=game, trends=trends,
                            trends_descriptions=trends_descriptions, filters=filters)

if __name__ == '__main__':
    app.run(debug=True)
