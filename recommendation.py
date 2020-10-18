import requests
import json
from constants import tmdb_posterpathURI, movie_externalIdURI, tmdb_posterNAURI
from werkzeug.wrappers import Request, Response
from tmdbv3api import TMDb, Movie


class recommendation:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def getRecommendation(self, movieid):
        data_URL = 'https://api.themoviedb.org/3/movie/' + \
            movieid+'/recommendations?api_key='+self.apiKey
        response = requests.get(data_URL).json()
        result = []
        for res in response['results']:
            temp = {}
            if 'id' and 'title' and 'poster_path' in res:
                temp['tmdb_id'] = res['id']
                temp['title'] = res['title']
                if res['poster_path'] != 'null' and res['poster_path']:
                    print(res['poster_path'])
                    temp['poster_path'] = tmdb_posterpathURI + \
                        res['poster_path']
                else:
                    temp['poster_path'] = tmdb_posterNAURI
                external_id = requests.get(
                    movie_externalIdURI+str(res['id'])+'/external_ids?api_key='+self.apiKey).json()
                if external_id:
                    temp['external_id'] = external_id['imdb_id']
                result.append(temp)
        return result
