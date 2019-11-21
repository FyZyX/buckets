from datetime import datetime

from flask import Flask, render_template

import nba_api

app = Flask(__name__)


@app.route('/games')
def games():
    today = datetime.today().date()
    data = nba_api.games_by_date(str(today))
    return render_template('games.html', games=data)


if __name__ == '__main__':
    # TODO: Use a DEBUG environment variable
    app.run(debug=True)
