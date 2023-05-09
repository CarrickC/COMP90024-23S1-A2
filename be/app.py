from flask import Flask, request
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

DB_URL = "http://172.26.131.185:5984"
AUTH = ("admin", "password")

class CRUDResource(Resource):
    def get(self, database, doc_id=None):
        if doc_id is None:
            response = requests.get(f"{DB_URL}/{database}/_all_docs", auth=AUTH)
        else:
            response = requests.get(f"{DB_URL}/{database}/{doc_id}", auth=AUTH)
        return response.json()

    def post(self, database):
        data = request.get_json()
        response = requests.post(f"{DB_URL}/{database}", json=data, auth=AUTH)
        return response.json()

    def put(self, database, doc_id):
        data = request.get_json()
        response = requests.put(f"{DB_URL}/{database}/{doc_id}", json=data, auth=AUTH)
        return response.json()

    def delete(self, database, doc_id):
        response = requests.get(f"{DB_URL}/{database}/{doc_id}", auth=AUTH)
        doc = response.json()
        response = requests.delete(f"{DB_URL}/{database}/{doc_id}?rev={doc['_rev']}", auth=AUTH)
        return response.json()

api.add_resource(CRUDResource, "/api/<string:database>", "/api/<string:database>/<string:doc_id>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9999)
