from flask import Flask
from flask_pymongo import pymongo
import main
import urllib
from main import mongoPwd, mongoDB, mongoClusterId, mongoID

CONNECTION_STRING = "mongodb+srv://"+mongoID+":"+urllib.parse.quote(
    mongoPwd)+mongoClusterId
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database(mongoDB)
user_collection = pymongo.collection.Collection(db, 'collection')
