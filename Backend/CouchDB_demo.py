import couchdb
import json

# authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@127.0.0.1:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'testdemo'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# data to be stored
json_str = '{"key1": "xxx", "key2": "yyy"}'
data = json.loads(json_str)

# save to db
doc_id, doc_rev = db.save(data)
print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')

# define the _id
my_id = 'my_id'
print(db.get(my_id))
if db.get(my_id):
    rev = db.get(my_id).rev
    data['_id'] = my_id
    data['_rev'] = rev
else:
    data['_id'] = my_id

# save to db
doc_id, doc_rev = db.save(data)
print(f"Document saved with ID: {doc_id} and revision: {doc_rev}")

# basic query all the docs
for _id in db:
    doc = db.get(_id)
    # filter and do sth
    print(f"ID: {_id}, Rev: {doc['_rev']}")
