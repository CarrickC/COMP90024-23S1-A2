from flask import Flask, render_template, request
from flask_restful import Api, Resource
import couchdb

# authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'twitterv5'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

app = Flask(__name__)
api = Api(app)

res1 = {'code': 200, 'msg': 'OK', 'data': {}}
res2 = {'code': 200, 'msg': 'OK', 'data': {'array': ['data1', 'data2', 'data3'], 'str': 'string'}}


@app.route('/')
def root():
    return render_template('Index.html')


# default GET
@app.route('/api_0/<param>')
def api_0(param):
    # Mango Queries
    query = {
        'selector': {
            'language': param
        }
    }
    # Execute the query
    results = []
    for row in db.find(query):
        results.append(row)
    # Return the results as JSON
    return {'data': results}


@app.route('/api_1', methods=['GET', 'POST', 'DELETE'])
def api_1():
    if request.method == 'POST':
        # using an existing view
        view = db.view('languages/judge', group_level=1)
        # Retrieve the view results
        results = {}
        for row in view:
            results[row.key] = row.value
        # Return the results as JSON
        return {'data': results}
    else:
        view = db.view('languages/langAvg', group_level=1)
        # Retrieve the view results
        results = {}
        print(view)
        for row in view:
            results[row.key] = row.value
        # Return the results as JSON
        return {'data': results}


class api_2(Resource):

    def get(self):
        # do sth
        # using an existing view
        view = db.view('author_count/by_author', group_level=1)
        # Retrieve the view results
        results = {}
        print(view)
        for row in view:
            results[row.key] = row.value
        # Return the results as JSON
        return {'data': results}





    def post(self):
        # do sth
        # using an existing view
        view = db.view('author_count/by_author', group_level=1)
        # Retrieve the view results
        results = {}
        print(view)
        for row in view:
            results[row.key] = row.value
        # Return the results as JSON
        return {'data': results}

    def delete(self, id=None):
        if not id:
            # do sth
            return "no id"
        else:
            doc = db.get(id)
            if doc:
                db.delete(doc)
                return 'Document deleted successfully'
            else:
                return 'Document not found'


api.add_resource(api_2, '/api_2', '/api_2/<id>')


from flask_cors import CORS




api = Api()
app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:8080', 'http://localhost:8081'])

api.add_resource(api_2, '/api_2', '/api_2/<id>')
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)


