def games_by_date(date):
    """
    Get a list of games on a specified date.

    :param str date: Date formatted as YYYY-MM--DD
    :return: List of game records
    """
    # TODO: This should return dynamic data depending on the date
    data = [
        {'home_team': 'Bucks',
         'away_team': 'Celtics'},
        {'home_team': 'Clippers',
         'away_team': 'Bitches'},
        {'home_team': 'Hawks',
         'away_team': 'Lakers'},
    ]
    return data
