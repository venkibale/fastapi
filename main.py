from fastapi import FastAPI, Header
#from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from pyrogram import Client
import time
#from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
from tmdbv3api import TMDb, Movie, Discover, TV, Person, Collection, Company, Configuration, Genre, Season, List, Certification
from users import users
from searchmovie import searchmovie
from getRottenDetails import getRottenDetails
from getOTT import getOttDetails
import os
from os import path, environ
import urllib3
#import db
import urllib.parse
from recommendation import recommendation
import fastapiconfig
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from telegramapi import telegramapi

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


tmdb = TMDb()
if environ.get('ENV') and os.environ['ENV'] == 'production':
    apiKey = os.environ['API_KEY']
    app.secret_key = os.environ['SECRET_KEY']
    tmdb.api_key = os.environ['TMDB_API_KEY']
    mongoID = os.environ['MONGO_USERNAME']
    mongoPwd = os.environ['MONGO_PASSWORD']
    mongoClusterId = os.environ['MONGO_CLUSTERID']
    mongoDB = os.environ['MONGO_DBNAME']
    api_id = os.environ['TELEGRAM_API_ID']
    api_hash = os.environ['TELEGRAM_API_HASH']
    chat_id = os.environ['CHAT_ID']

else:
    try:
        apiKey = fastapiconfig.settings.API_KEY
        app.secret_key = fastapiconfig.settings.SECRET_KEY
        tmdb.api_key = fastapiconfig.settings.TMDB_API_KEY
        mongoID = fastapiconfig.settings.MONGO_USERNAME
        mongoPwd = fastapiconfig.settings.MONGO_PASSWORD
        mongoClusterId = fastapiconfig.settings.MONGO_CLUSTERID
        mongoDB = fastapiconfig.settings.MONGO_DBNAME
        api_id = fastapiconfig.settings.TELEGRAM_API_ID
        api_hash = fastapiconfig.settings.TELEGRAM_API_HASH
        chat_id = fastapiconfig.settings.CHAT_ID
    except Exception as e:
        print("Issue with config details", e)


tmdb.language = 'en'
tmdb.debug = True
movie = Movie()
http = urllib3.PoolManager()

searchmovie_obj = searchmovie(movie, tmdb, tmdb.api_key, http, apiKey)
getfulldetails_obj = getRottenDetails(apiKey)
getrecommendations = recommendation(tmdb.api_key)


@cross_origin
@app.get("/searchMovie/{movie}")
async def searchMovies(movie, requestID: int = None):
    print("Processing...", id, requestID)
    return JSONResponse(searchmovie_obj.searchMovies(movie, requestID))


@cross_origin
@app.get("/getlinks/{movie}")
async def getlinks(movie):
    telegramobj = telegramapi(api_id, api_hash, chat_id)
    await telegramobj.sendMessage(movie)
    time.sleep(8)
    return await telegramobj.getmessages()


# @app.post('/adduser')
# def adduser():
#     return adduser_obj.addUser(db, request)


# @app.get('/getusers')
# def getUsers():
#     users = db.db.collection.find()
#     return dumps(users)


# @app.get('/getuser/{id}')
# def getUser(id):
#     user = db.db.collection.find_one({'_id': ObjectId(id)})
#     return dumps(user)


# @app.delete('/deleteuser/{id}')
# def deleteuser(id):
#     if db.db.collection.find_one({'_id': ObjectId(id)}):
#         db.db.collection.delete_one({'_id': ObjectId(id)})
#         return "User got deleted successfully"
#     else:
#         return "No such User found."


# @app.put('/updateuser/{id}')
# def updateuser(id):
#     return adduser_obj.updateuser(id, ObjectId)


# @cross_origin
# @app.post('/validateuser', response_model=usermodel)
# def validateUser(request):
#     print(request.get('email'), request.get('password'))
#     adduser_obj = users(db, request.get())
#     print(request.get())
#     return adduser_obj.validateUser()


@cross_origin
@app.get('/getFullDetails/{id}')
def getFullDetails(id):
    return getfulldetails_obj.getRottenDetails(id)


@cross_origin
@app.get('/getOTTDetails/{movie}')
def getOTTDetails(movie, external_id: str = None):
    getOtt_obj = getOttDetails(apiKey, external_id, movie)
    res = getOtt_obj.getOTT()
    return JSONResponse(res)


@cross_origin
@app.get('/getrecommendations/{id}')
def getmovierecommendations(id):
    return JSONResponse(getrecommendations.getRecommendation(id))


@cross_origin
@app.get("/")
async def root():
    return {"message": "Hello World"}
