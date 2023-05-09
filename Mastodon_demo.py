from mastodon import Mastodon, StreamListener
import json, os, couchdb

#from dotenv import load_dotenv

#load_dotenv()

# authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'mastodon'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# optional, better not hardcode here
token = ''
m = Mastodon(
    # your server here
    api_base_url=f'https://mastodon.au',
    access_token="5Pw5eEN3nQqPtxFZ1BmazMSgKPO5H63zKGsC5P-zPJk"
)


# listen on the timeline
class Listener(StreamListener):
    # called when receiving new post or status update
    def on_update(self, status):
        # do sth
        json_str = json.dumps(status, indent=2, sort_keys=True, default=str)
        doc_id, doc_rev = db.save(json.loads(json_str))
        print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')


# make it better with try-catch and error-handling
m.stream_public(Listener())
