import requests

from nba_api.cache import FileSystemCache


class NBA:
    host = 'api-nba-v1.p.rapidapi.com'

    def __init__(self, api_key, file_store='data'):
        self.headers = {
            'x-rapidapi-host': self.host,
            'x-rapidapi-key': api_key,
        }

        if file_store:
            self.cache = FileSystemCache(file_store)
        else:
            self.cache = None

    def games_by_date(self, date):
        """
        Get a list of games on a specified date.

        :param datetime.date date: Date on which games occurred
        :return: List of game records
        """
        key = f'games/{date}'
        if self.cache and key in self.cache:
            return self.cache[key]['api']['games']

        url = f"https://{self.host}/games/date/{date}"

        response = requests.request("GET", url, headers=self.headers)

        # TODO: Check error based on the status
        data = response.json()

        if self.cache:
            self.cache[key] = data

        # TODO: Create a list of Game objects from the raw data
        game_data = data['api']['games']

        return game_data
