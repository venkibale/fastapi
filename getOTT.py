from justwatchapi import JustWatch
import pprint
import json
from werkzeug.wrappers import Request, Response
import requests
from justwatch import JustWatch, justwatchapi
justwatchapi.__dict__["HEADER"] = {
    "User-Agent": "JustWatch client (github.com/dawoudt/JustWatchAPI)"
}
just_watch = JustWatch(country="IN")


class getOttDetails:
    def __init__(self, apiKey, external_id, movie_name):
        self.just_watch = JustWatch(country='IN')
        self.apiKey = apiKey
        self.external_id = external_id
        self.name = movie_name
        print("Processing.....OTT Details")

    def getOTT(self):
        url = {'subscriptions': {}}
        # print(self.name)
        results = just_watch.search_for_item(
            query=self.name)
        # print(results)
        if results['items'] != None:
            for value in results['items']:
                if self.name.lower() == value['title'].lower() and value['object_type'] == "movie" and "offers" in value:
                    # print(value)
                    for i in value['offers']:
                        print(i['monetization_type'],
                              i['presentation_type'], i['urls']['standard_web'], i)
                        if i['monetization_type'] == 'flatrate' or i['monetization_type'] == 'ads' or i['monetization_type'] == 'free' and i['presentation_type'] == 'sd':
                            first_part = i['urls']['standard_web'].split('.com')[
                                0]
                            # print(first_part)
                            if 'www.' in first_part:
                                key = first_part.split('www.')[1]
                            elif 'https://' in first_part:
                                key = first_part.split('https://')[1]
                            #url['subscriptions'][key] = []
                            url['subscriptions'][key] = i['urls']['standard_web']
                            url['ifSubscription'] = True
                            # print(url)
                elif "offers" not in value and self.name == value['title']:
                    print("Oops...we couldnt find any streaming options")
                # print(url)
                # print((json.dumps(url)))
            # print(self.external_id)
            resp = self.getRottenDetails(self.external_id)
            # print(resp)
            if resp:
                url['rated'] = []
                url['actors'] = []
                url['rotten_rating'] = []
                url['awards'] = []
                url['poster_path'] = []
                url['director'] = []
                url['rating'] = []
                url['overview'] = []
                if resp['Rated']:
                    url['rated'] = resp['Rated']
                else:
                    url['rated'] = "NA"
                if resp['Actors']:
                    url['actors'] = resp['Actors']
                else:
                    url['actors'] = "NA"
                if resp['Ratings']:
                    for rating in resp['Ratings']:
                        if rating['Source'] == 'Rotten Tomatoes':
                            # print(rating['Value'])
                            url['rotten_rating'] = rating['Value']
                            rt_rating = int(rating['Value'].replace('%', ''))
                            if rt_rating >= 60:
                                url['rt_value'] = "fresh"
                            else:
                                url['rt_value'] = "rotten"

                else:
                    url['rotten_rating'] = "NA"
                if not url['rotten_rating']:
                    url['rotten_rating'] = "NA"
                if resp['Awards']:
                    url['awards'] = resp['Awards']
                else:
                    url['awards'] = "NA"
                if resp['Poster']:
                    url['poster_path'] = resp['Poster']
                else:
                    url['poster_path'] = "NA"
                if resp['Title']:
                    url['title'] = resp['Title']
                else:
                    url['title'] = "NA"
                if resp['Director']:
                    url['director'] = resp['Director']
                else:
                    url['director'] = "NA"
                if resp['imdbRating']:
                    url['rating'] = resp['imdbRating']
                else:
                    url['rating'] = "NA"
                if resp['Plot']:
                    url['overview'] = resp['Plot']
                else:
                    url['overview'] = "NA"

                # print(url)
        return url

    def getRottenDetails(self, external_id):

        data_URL = 'http://www.omdbapi.com/?apikey='+self.apiKey
        params = {
            'i': external_id
        }
        response = requests.get(data_URL, params=params).json()
        # print(response)
        return response
