from flask import Flask, render_template

app = Flask(__name__)


@app.route('/games')
def games():
    # TODO: This should come from a data collection package
    data = [
        {'home_team': 'Bucks',
         'away_team': 'Celtics'},
        {'home_team': 'Clippers',
         'away_team': 'Bitches'},
        {'home_team': 'Hawks',
         'away_team': 'Lakers'},
    ]
    return render_template('games.html', games=data)


if __name__ == '__main__':
    # TODO: Use a DEBUG environment variable
    app.run(debug=True)
