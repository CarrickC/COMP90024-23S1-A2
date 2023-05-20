# coding:utf-8

from collections import Counter
from flask import Flask
from flask_restful import Api, Resource
import couchdb
from flask_cors import CORS
import json

# authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'twitterv2'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]


# Get data for all documents


def get_top_10_word(top=10):
    docs = db.view('_all_docs', include_docs=True)

    # A string that stores text fields in all documents
    text_strings = []

    # Walk through each document
    for doc in docs:
        # Get the data for the document
        data = doc['doc']
        # Extract the string for the text field and add it to the text_strings list
        if 'doc' in data and 'text' in data['doc']['data']:
            text = data['doc']['data']['text']
            text_strings.extend(text.split())

    # Calculates the number of occurrences of the text field string
    counter = Counter(text_strings)

    # Find the string that appears the most times
    top_10 = counter.most_common(top)
    return top_10


app = Flask(__name__)
api = Api(app)
CORS(app, origins=['http://127.0.0.1:8080', 'http://localhost:8081'])


class TopWords(Resource):
    def get(self):
        return get_top_10_word()


api.add_resource(TopWords, '/top_words', '/top_words')

api.init_app(app)
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
