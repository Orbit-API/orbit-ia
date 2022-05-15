from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)

mongo_client = MongoClient(host='20.84.71.186', port=27017, username='mongoadmin', password='secret')





