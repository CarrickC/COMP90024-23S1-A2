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


# 获取所有文档的数据


def get_top_10_word(top=10):
    docs = db.view('_all_docs', include_docs=True)

    # 存储所有文档中的 text 字段的字符串
    text_strings = []

    # 遍历每个文档
    for doc in docs:
        # 获取文档的数据
        data = doc['doc']
        # 提取 text 字段的字符串，并将其添加到 text_strings 列表中
        if 'doc' in data and 'text' in data['doc']['data']:
            text = data['doc']['data']['text']
            text_strings.extend(text.split())

    # 统计 text 字段字符串出现的次数
    counter = Counter(text_strings)

    # 找到出现次数最多的字符串
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
