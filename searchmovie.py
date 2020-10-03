import json
from random import random
from constants import genres, movie_externalIdURI, movie_getDirectorURI, omdbApiURI, tmdb_posterpathURI, tmdb_posterNAURI, empty_movieResult, languages
from werkzeug.wrappers import Request, Response
from collections import OrderedDict


class searchmovie:
    def __init__(self, movie, tmdb, api, http, apiKey):
        self.movie = movie
        self.tmdb = tmdb
        self.tmdb.api_key = api
        self.http = http
        self.apiKey = apiKey

    def searchMovies(self, id, requestID):
        try:
            resp = []
            external_ids = []

            search = self.movie.search(id)
            for p in search:
                if p:
                    temp = {}
                    url = movie_externalIdURI + \
                        str(p.id)+'/external_ids?api_key=' + \
                        str(self.tmdb.api_key)
                    external_id = json.loads(
                        (self.http.request('GET', url)).data.decode('utf-8'))
                    temp['tmdb_id'] = p.id
                    if 'imdb_id' in external_id.keys():
                        if external_id['imdb_id']:
                            # print(external_id)
                            external_ids.append(external_id['imdb_id'])
                            temp["ratings"] = self.omdbAPI(
                                external_id['imdb_id'])
                            director_name = self.getDirector(external_id)
                            temp["director"] = director_name
                            temp["external_id"] = external_id['imdb_id']
                            temp["external_id_boolean"] = True
                        else:
                            temp["external_id_boolean"] = False
                    try:
                        if p.genre_ids:
                            temp["genre"] = ""
                            for genre_id in p.genre_ids:
                                temp["genre"] = temp["genre"] + \
                                    " / " + genres[str(genre_id)]
                        else:
                            temp["genre"] = "NA"
                    except:
                        temp["genre"] = "NA"

                    temp["title"] = p.title
                    # print(p.title)
                    try:
                        if p.release_date:
                            temp["release_date"] = p.release_date.split(
                                '-')[0]
                            # print(temp["release_date"])
                        else:
                            temp["release_date"] = "NIL"
                    except:
                        temp["release_date"] = "NIL"
                    try:
                        if p.original_language:
                            if p.original_language in languages:
                                temp["original_language"] = languages[str(
                                    p.original_language)]
                            else:
                                temp["original_language"] = "NA"
                        else:
                            temp["original_language"] = "NIL"
                    except:
                        temp["original_language"] = "NIL"
                    try:
                        if p.overview:
                            temp["overview"] = p.overview
                        else:
                            temp["overview"] = "NIL"
                    except:
                        temp["overview"] = "NIL"
                    try:
                        if p.poster_path:
                            _poster_path = tmdb_posterpathURI + \
                                str(p.poster_path)
                        else:
                            _poster_path = tmdb_posterNAURI
                        temp["poster_path"] = _poster_path
                    except:
                        temp["poster_path"] = tmdb_posterNAURI
                    try:
                        if p.popularity:
                            temp["popularity"] = p.popularity

                            # array.append(p.popularity)
                            # print(p.popularity)
                        else:
                            temp["popularity"] = "NA"
                    except:
                        temp["popularity"] = "NA"

                        # print("No such popularity")
                    resp.append(temp)
            if requestID:
                resp.append({"requestID": requestID})

            return resp

        except Exception as e:
            print("Exception arised", e)
            if not resp:
                return empty_movieResult
            else:
                return resp

    def getDirector(self, id):
        dir_name = ""
        url = movie_getDirectorURI + \
            id['imdb_id']+'/casts?api_key=' + self.tmdb.api_key.format(id)
        resp = json.loads((self.http.request('GET', url)).data.decode('utf-8'))
        if 'crew' in resp.keys():
            for cast in resp['crew']:
                if cast['job'] == "Director":
                    dir_name = cast['name']

        if dir_name == "":
            dir_name = "NA"
        return dir_name

    def omdbAPI(self, external_id):
        url = omdbApiURI+external_id + "&plot=short&r=json&&apikey="+self.apiKey
        resp = json.loads((self.http.request('GET', url)).data.decode('utf-8'))
        if 'Ratings' in resp:
            for i in resp['Ratings']:
                return(i['Value'].replace("/10", ""))
