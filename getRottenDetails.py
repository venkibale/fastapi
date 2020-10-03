import requests
from pprint import PrettyPrinter


class getRottenDetails:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def getRottenDetails(self, external_id):

        data_URL = 'http://www.omdbapi.com/?apikey='+self.apiKey
        params = {
            'i': external_id
        }
        response = requests.get(data_URL, params=params).json()
        return response
