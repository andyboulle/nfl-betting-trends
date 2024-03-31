from flask import Flask, render_template, request
import psycopg2
from models.upcoming_game import UpcomingGame
from models.trend import Trend
import config.weekly_config as weekly_config
import config.all_time_config as all_time_config

app = Flask(__name__)

DB_HOST = 'postgres'
DB_PORT = "5432"
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'bangarang19'

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host="localhost", port=DB_PORT)
    cur = conn.cursor()

    games = get_upcoming_games(cur)
    filters = {
        'config': request.form.get('config', 'weekly')
    }

    if request.method == 'GET':
        filters = get_default_filters(games)
    table = 'trends' if filters['config'] == 'all_time' else 'weekly_trends'
    sql_query = get_sql_query(table, filters, request)

    cur.execute(sql_query)
    trend_rows = cur.fetchall()

    trends = get_trends(trend_rows, filters)
    trends_descriptions = get_trend_descriptions(trends)

    cur.close()
    conn.close()

    configs = {
        'weekly_config': weekly_config,
        'all_time_config': all_time_config
    }

    return render_template('index.html',
                            games=games, trends=trends,
                            trends_descriptions=trends_descriptions,
                            filters=filters, configs=configs)

@app.route('/<game_id_string>', methods=['GET', 'POST'])
def single_game(game_id_string):
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host="localhost", port=DB_PORT)
    cur = conn.cursor()
    
    game = get_selected_game(cur, game_id_string)
    filters = {
        'config': request.form.get('config', 'game')
    }

    if request.method == 'GET':
        filters = get_default_filters()
        filters['config'] = 'game'
    sql_query = get_sql_query(game_id_string, filters, request)

    cur.execute(sql_query)
    trend_rows = cur.fetchall()

    trends = get_trends(trend_rows, filters)
    trends_descriptions = get_trend_descriptions(trends)

    cur.close()
    conn.close()

    return render_template('single_game_page.html', game=game, trends=trends,
                            trends_descriptions=trends_descriptions, filters=filters)

def get_upcoming_games(cur):
    """
    Get all upcoming games from the database.

    Args:
        cur: The cursor object for the database connection.

    Returns:
        dict: A dictionary containing all upcoming games.
    """

    games = {}
    cur.execute("SELECT * FROM upcoming_games")
    rows = cur.fetchall()
    for row in rows:
        games[row[0]] = UpcomingGame(
            row[2], row[8], row[11], row[16], row[17], row[19],
            row[20], row[21], row[23], row[24], row[26]
        )

    return games

def get_selected_game(cur, game_id_string):
    cur.execute(f"SELECT * FROM upcoming_games WHERE id_string ='{game_id_string}'")
    game_row = cur.fetchone()
    game = UpcomingGame(game_row[2], game_row[8], game_row[11], game_row[16], game_row[17],
                         game_row[19], game_row[20], game_row[21], game_row[23], game_row[24],
                           game_row[26], True)
    
    return game

def get_sql_query(table, filters, req):
    """
    Construct the SQL query based on the provided filters and request data.

    Args:
        start_query (str): The initial part of the SQL query.
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query.
    """

    sql_query = f'SELECT * FROM {table} WHERE id IS NOT NULL'
    sql_query += get_trend_category_query(filters, req)
    sql_query += get_betting_category_query(filters, req)
    sql_query += get_over_under_query(filters, req)
    sql_query += get_month_query(filters, req)
    sql_query += get_day_query(filters, req)
    sql_query += get_type_query(filters, req)
    sql_query += get_spread_query(filters, req)
    sql_query += get_total_query(filters, req)
    sql_query += get_season_query(filters, req)
    sql_query += get_total_games_query(filters, req)
    sql_query += get_games_to_include_query(filters, req)
    sql_query += get_win_pct_query(filters, req)
    sql_query += get_sort_query(filters, req)
    sql_query += get_max_results_query(filters, req)

    return sql_query

def get_default_filters(games=None):
    """
    Generate default filter options.

    Returns:
        dict: A dictionary containing default filter options.
    """

    filters = {}

    filters['config'] = 'weekly'

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
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
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
    for i in range(0, 28):
        filters[f'spread {i}.0'] = 'true'
        filters[f'spread {i}.5'] = 'true'
        if i < 15:
            filters[f'spread {i} or more'] = 'true'
            filters[f'spread {i} or less'] = 'true'

    filters['no_total'] = 'true'
    for i in range(30, 61, 5):
        filters[f'total {i} or more'] = 'true'
        filters[f'total {i} or less'] = 'true'

    if games is not None:
        for game in games.values():
            filters[f'include_{game.home_abbreviation}vs{game.away_abbreviation}'] = 'true'

    filters['seasons'] = 'since 2006-2007'
    filters['season_type'] = 'seasons_after'

    filters['gle_total_games'] = 'gt'
    filters['total_games'] = '0'
    filters['gle_win_pct'] = 'gt'
    filters['win_pct'] = '0'

    filters['first_sort_category'] = 'win_percentage'
    filters['first_sort_order'] = 'desc'
    filters['second_sort_category'] = 'total_games'
    filters['second_sort_order'] = 'desc'

    filters['max_results'] = '50'

    return filters

def get_trend_category_query(filters, req):
    """
    Construct the SQL query for trend category filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for trend category filtering.
    """
    sql_query = ''

    # Extract trend categories from POST form
    filters['home'] = req.form.get('home', 'true')
    filters['away'] = req.form.get('away', 'true')
    filters['favorite'] = req.form.get('favorite', 'true')
    filters['underdog'] = req.form.get('underdog', 'true')
    filters['home favorite'] = req.form.get('home_favorite', 'true')
    filters['away underdog'] = req.form.get('away_underdog', 'true')
    filters['away favorite'] = req.form.get('away_favorite', 'true')
    filters['home underdog'] = req.form.get('home_underdog', 'true')

    # Add trend categories to SQL query
    sql_query += ' AND ((('
    for custom_filter, value in filters.items():
        if value == 'true':
            if custom_filter in ('home', 'away', 'favorite', 'underdog'):
                sql_query += f" category LIKE '{custom_filter} o%' OR category LIKE \
                      '{custom_filter} a%' OR"
            else:
                sql_query += f" category LIKE '%{custom_filter}%' OR"
    sql_query += ' FALSE)'

    return sql_query

def get_betting_category_query(filters, req):
    """
    Construct the SQL query for betting category filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for betting category filtering.
    """

    sql_query = ''

    # Extract betting categories from POST form
    filters['ats'] = req.form.get('ats', 'true')
    filters['outright'] = req.form.get('outright', 'true')

    # Add betting categories to SQL query
    sql_query += ' AND ('
    for custom_filter, value in filters.items():
        if custom_filter in ('ats', 'outright') and value == 'true':
            sql_query += f" category LIKE '%{custom_filter}%' OR"
    sql_query += ' FALSE))'

    return sql_query

def get_over_under_query(filters, req):
    """
    Construct the SQL query for over/under category filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for over/under category filtering.
    """

    sql_query = ''

    # Extract over/under categories from POST form
    filters['over'] = req.form.get('over', 'true')
    filters['under'] = req.form.get('under', 'true')

    # Add over/under categories to SQL query
    sql_query += ' OR ('
    if filters['over'] == 'true':
        sql_query += " category = 'over' OR"
    if filters['under'] == 'true':
        sql_query += " category = 'under' OR"
    sql_query += ' FALSE))'

    return sql_query

def get_month_query(filters, req):
    """
    Construct the SQL query for month filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for month filtering.
    """

    sql_query = ''

    # Extract month categories and add them to SQL query
    filters['no_month'] = req.form.get('no_month', 'true')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    selected_months = []
    for month in months:
        filters[month.lower()] = req.form.get(month.lower(), 'false' if req.method == 'POST' else 'true')
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

    return sql_query

def get_day_query(filters, req):
    """
    Construct the SQL query for day filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for day filtering.
    """

    sql_query = ''

    # Extract day categories and add them to SQL query
    filters['no_day'] = req.form.get('no_day', 'true')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    selected_days = []
    for day in days:
        filters[day.lower()] = req.form.get(day.lower(), 'false' if req.method == 'POST' else 'true')
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

    return sql_query

def get_type_query(filters, req):
    """
    Construct the SQL query for type filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for type filtering.
    """

    sql_query = ''

    # Extract type categories and add them to SQL query
    filters['no_type'] = req.form.get('no_type', 'true')
    filters['divisional'] = req.form.get('divisional', 'false' if req.method == 'POST' else 'true')
    filters['non_divisional'] = req.form.get('non_divisional', 'false' if req.method == 'POST' else 'true')
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

    return sql_query

def get_spread_query(filters, req):
    """
    Construct the SQL query for spread filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for spread filtering.
    """

    sql_query = ''

    # Extract spread categories and add them to SQL query
    filters['no_spread'] = req.form.get('no_spread', 'true')
    spreads = []
    for i in range(0, 28):
        spreads.append(f'spread {i}.0')
        spreads.append(f'spread {i}.5')
        if i < 15:
            spreads.append(f'spread {i} or more')
            spreads.append(f'spread {i} or less')

    selected_spreads = []
    for spread in spreads:
        filters[spread] = req.form.get(spread, 'false' if req.method == 'POST' else 'true')
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

    return sql_query

def get_total_query(filters, req):
    """
    Construct the SQL query for total filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for total filtering.
    """

    sql_query = ''

    # Extract total categories and add them to SQL query
    filters['no_total'] = req.form.get('no_total', 'true')
    totals = []
    for i in range(30, 61, 5):
        totals.append(f'total {i} or more')
        totals.append(f'total {i} or less')

    selected_totals = []
    for total in totals:
        filters[total] = req.form.get(total, 'false' if req.method == 'POST' else 'true')
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

    return sql_query

def get_games_to_include_query(filters, req):
    sql_query = ''

    # Get the games that are not checked and add them to the SQL query
    # It will get all games not like the ones that are unchecked
    games_to_exclude = []
    included_values = {key: value for key, value in req.form.items() if 'include' in key}
    for key, value in included_values.items():
        filters[key] = req.form.get(key, 'true')
        if filters[key] == 'false':
            games_to_exclude.append(key[8:])

    if len(games_to_exclude) > 0:
        sql_query += ' AND ('
        for game in games_to_exclude:
            sql_query += f" games_applicable NOT LIKE '%{game}%' AND"
        sql_query += ' TRUE)'

    return sql_query        

def get_season_query(filters, req):
    """
    Construct the SQL query for season filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for season filtering.
    """

    sql_query = ''

    # Extract seasons and add them to SQL query
    filters['seasons'] = req.form.get('seasons', 'since 2006-2007')
    filters['season_type'] = req.form.get('season_type', 'seasons_after')
    seasons_included = []
    season_selected = filters['seasons'][6:]
    if filters['season_type'] == 'only_season':
        seasons_included.append(f"'{filters['seasons']}'")
    else:
        if filters['season_type'] == 'seasons_after':
            for i in range(int(season_selected[:4]), 2024):
                seasons_included.append(f"'since {i}-{i + 1}'")
        elif filters['season_type'] == 'seasons_before':
            for i in range(2006, int(season_selected[:4]) + 1):
                seasons_included.append(f"'since {i}-{i + 1}'")
    sql_query += f" AND seasons IN ({','.join(seasons_included)})"

    return sql_query

def get_total_games_query(filters, req):
    """
    Construct the SQL query for total games filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for total games filtering.
    """

    sql_query = ''

    # Extract total games filtering method and add it to SQL query
    filters['gle_total_games'] = req.form.get('gle-total-games', 'gt')
    filters['total_games'] = req.form.get('total-games', '0')
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

    return sql_query

def get_win_pct_query(filters, req):
    """
    Construct the SQL query for win percentage filtering.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for win percentage filtering.
    """

    sql_query = ''

    # Extract win pct filtering method and add it to SQL query
    filters['gle_win_pct'] = req.form.get('gle-win-pct', 'gt')
    filters['win_pct'] = req.form.get('win-pct', '0')
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

    return sql_query

def get_sort_query(filters, req):
    """
    Construct the SQL query for sorting.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for sorting.
    """

    # Extract sorting category and order and add them to SQL query
    filters['first_sort_category'] = req.form.get('first-sort-category', 'win_percentage')
    filters['first_sort_order'] = req.form.get('first-sort-order', 'desc')
    filters['second_sort_category'] = req.form.get('second-sort-category', 'total_games')
    filters['second_sort_order'] = req.form.get('second-sort-order', 'desc')

    return f" ORDER BY {filters['first_sort_category']} \
                    {filters['first_sort_order']}, \
                    {filters['second_sort_category']} \
                    {filters['second_sort_order']}"

def get_max_results_query(filters, req):
    """
    Construct the SQL query for limiting maximum results.

    Args:
        filters (dict): A dictionary containing the filter options.
        req: The request object containing form data.

    Returns:
        str: The constructed SQL query for limiting maximum results.
    """

    # Extract max results and add it to SQL query
    filters['max_results'] = req.form.get('max_results', '50')

    return f" LIMIT {filters['max_results']}"

def get_trends(trend_rows, filters):
    trends = []
    for row in trend_rows:
        if filters['config'] != 'weekly':
            trends.append(Trend(row[2], row[3], row[4], row[5], row[6], row[7],
                             row[8], row[9], row[10], row[11], row[12], row[13]))
        else:
            trends.append(Trend(row[2], row[3], row[4], row[5], row[6], row[7],
                             row[8], row[9], row[10], row[11], row[12], row[13], row[14]))
            
    return trends

def get_trend_descriptions(trends):
    trends_descriptions = []
    for trend in trends:
        trends_descriptions.append(trend.get_description())
    
    return trends_descriptions

if __name__ == '__main__':
    app.run(debug=True)
