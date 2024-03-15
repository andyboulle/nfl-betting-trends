from flask import Flask, render_template, request
import psycopg2
from models.upcoming_game import UpcomingGame
from models.trend import Trend
import time

app = Flask(__name__)

db_host = 'postgres'
db_port = "5432"
db_name = 'postgres'
db_user = 'postgres'
db_password = 'bangarang19'

@app.route('/', methods=['GET'])
def index():
    # Connect to database
    conn = psycopg2.connect(database=db_name, 
                            user=db_user, 
                            password=db_password, 
                            host="localhost", port=db_port)
    cur = conn.cursor()

    # Get all upcoming games and pass to index
    games = {}
    cur.execute("SELECT * FROM upcoming_games")
    rows = cur.fetchall()
    for row in rows:
        games[row[0]] = UpcomingGame(row[2], row[8], row[11], row[16], row[17], row[19], row[20], row[21], row[23], row[24], row[26])
    
    cur.close()
    conn.close()

    return render_template('index.html', games=games)

@app.route('/<id>', methods=['GET', 'POST'])
def single_game(id):

    # Connect to database
    conn = psycopg2.connect(database=db_name, 
                            user=db_user, 
                            password=db_password, 
                            host="localhost", port=db_port)
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM upcoming_games WHERE id='{id}'")
    game_row = cur.fetchone()
    game = UpcomingGame(game_row[2], game_row[8], game_row[11], game_row[16], game_row[17], game_row[19], game_row[20], game_row[21], game_row[23], game_row[24], game_row[26], True)

    # Get all trends for game and pass to single game trends page
    trend_ids = [trend.id for trend in game.trends]
    trend_ids_with_quotes = [f"'{trend_id}'" for trend_id in trend_ids]
    placeholders = ','.join(trend_ids_with_quotes)

    sql_query = f"SELECT * FROM trends WHERE id IN ({placeholders})"

    filters = {}

    if request.method == 'POST':
        #
        # Trend Category Filters
        #
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

        sql_query += ' AND ((('
        for filter, value in filters.items():
            if value == 'true':
                if (filter == 'home' or filter == 'away' or filter == 'favorite' or filter == 'underdog'):
                    sql_query += f" category LIKE '{filter} o%' OR category LIKE '{filter} a%' OR"
                else:
                    sql_query += f" category LIKE '%{filter}%' OR"
        sql_query += ' FALSE)'

        #
        # Betting Category Filters
        #
        filters['ats'] = request.form['ats']
        filters['outright'] = request.form['outright']

        sql_query += ' AND ('
        for filter, value in filters.items():
            if (filter == 'ats' or filter == 'outright') and value == 'true':
                sql_query += f" category LIKE '%{filter}%' OR"
        sql_query += ' FALSE))'

        #
        # Over/Under Filters
        #
        filters['over'] = request.form['over']
        filters['under'] = request.form['under']

        sql_query += ' OR ('
        if filters['over'] == 'true':
            sql_query += f" category = 'over' OR"
        if filters['under'] == 'true':
            sql_query += f" category = 'under' OR"
        sql_query += ' FALSE))'

        #
        # Game Info Filters
        #
        filters['month'] = request.form['month']
        filters['day'] = request.form['day']
        filters['type'] = request.form['type']

        if filters['month'] == 'game_month':
            sql_query += f" AND month='{game.month}'"
            filters['game_month'] = 'true'
            filters['any_month'] = 'false'
        else:
            filters['any_month'] = 'true'
            filters['game_month'] = 'false'
            sql_query += ' AND month IS NULL'

        if filters['day'] == 'game_day':
            sql_query += f" AND day_of_week='{game.day_of_week}'"
            filters['game_day'] = 'true'
            filters['any_day'] = 'false'
        else:
            filters['any_day'] = 'true'
            filters['game_day'] = 'false'
            sql_query += ' AND day_of_week IS NULL'

        if filters['type'] == 'divisional':
            if game.divisional == True:
                sql_query += f" AND divisional=TRUE"
                filters['divisional'] = 'true'
                filters['any_type'] = 'false'
            else:
                sql_query += f" AND divisional=FALSE"
                filters['divisional'] = 'true'
                filters['any_type'] = 'false'
        else:
            filters['any_type'] = 'true'
            filters['divisional'] = 'false'
            sql_query += ' AND divisional IS NULL'

        #
        # Betting Info Filters
        #
        filters['spread'] = request.form['spread']
        for key, value in request.form.items():
            if 'spread' in key:
                filters[key] = request.form[key]

        if filters['spread'] == 'true':
            sql_query += ' AND ('
            for key, value in filters.items():
                if 'spread ' in key and value == 'true':
                    sql_query += f" spread='{key[7:]}' OR "
            sql_query += ' FALSE)'
        else:
            sql_query += ' AND spread IS NULL'

        filters['total'] = request.form['total']
        for key, value in request.form.items():
            if 'total' in key:
                filters[key] = request.form[key]

        if filters['total'] == 'true':
            sql_query += ' AND ('
            for key, value in filters.items():
                if 'total ' in key and value == 'true':
                    sql_query += f" total='{key[6:]}' OR "
            sql_query += ' FALSE)'
        else:
            sql_query += ' AND total IS NULL'

        # TODO: Figure out why when "less than 4" is selected, nothing shows up, but when "less than 3" is selected, stuff shows up
        # TODO: Figure out a better and/or system. Should add an option for game details: "any month, september, any month or just september", should also give option for combination of criteria selected, not just automatically all criteria selected has to be applied

        #
        # Season Info Filters
        #
        filters['seasons'] = request.form['seasons']
        if filters['seasons'] != 'since 2006-2007':
            seasons_included = []
            season_selected = filters['seasons'][6:]
            for i in range(int(season_selected[:4]), 2024):
                seasons_included.append(f"'since {i}-{i + 1}'")
            sql_query += f" AND seasons IN ({','.join(seasons_included)})"

        #
        # Total Games Filters
        #
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

        #
        # Win Percentage Filters
        #
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

        #
        # Category Sorting Filters
        #
        filters['first_sort_category'] = request.form['first-sort-category']
        filters['first_sort_order'] = request.form['first-sort-order']
        filters['second_sort_category'] = request.form['second-sort-category']
        filters['second_sort_order'] = request.form['second-sort-order']

        #
        # Max Results Filter
        #
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

        filters['any_month'] = 'true'
        filters['game_month'] = 'false'
        filters['any_day'] = 'true'
        filters['game_day'] = 'false'
        filters['any_type'] = 'true'
        filters['divisional'] = 'false'

        filters['spread'] = 'true'
        for i in range(1, 21):
            filters[f'spread {i} or more'] = 'true'
            filters[f'spread {i} or less'] = 'true'
            filters[f'spread {i}.0'] = 'true'
            filters[f'spread {i}.5'] = 'true'

        filters['total'] = 'true'
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

    sql_query += f" ORDER BY {filters['first_sort_category']} {filters['first_sort_order']}, {filters['second_sort_category']} {filters['second_sort_order']}"
    sql_query += f" LIMIT {filters['max_results']}"

    cur.execute(sql_query)
    trend_rows = cur.fetchall()

    trends = []
    trends_descriptions = []
    for row in trend_rows:
        trends.append(Trend(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
    
    for trend in trends:
        trends_descriptions.append(trend.get_description())
    
    cur.close()
    conn.close()

    return render_template('single_game_trend_page.html', game=game, trends=trends, trends_descriptions=trends_descriptions, filters=filters)


if __name__ == '__main__':
    app.run(debug=True)