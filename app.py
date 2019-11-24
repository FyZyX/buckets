import os
from datetime import datetime

from flask import Flask, render_template, request

from nba_api import NBA

app = Flask(__name__)

# TODO: Change DEBUG default to false
DEBUG = os.environ.get('DEBUG', True)
API_KEY = os.environ.get('API_KEY')

NBA_API = NBA(API_KEY)


@app.route('/games')
def games():
    date = request.args.get('date')

    if date:
        # TODO: Handle parsing error
        date = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        # TODO: Deal with timezones
        date = datetime.utcnow().date()

    data = NBA_API.games_by_date(date)
    return render_template('games.html', games=data)


if __name__ == '__main__':
    app.run(debug=DEBUG)
