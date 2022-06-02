from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)

mongo_client = MongoClient(host='localhost', port=27017, username='mongoadmin', password='secret')
db = mongo_client['orbit']
collection = db['metrics_7']




