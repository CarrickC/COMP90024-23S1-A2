"""
Author:      Edward Liu
Student id:  913500
Date:        2023-5-26 08:36:06
Description: main function
"""


from mastodon import Mastodon, StreamListener
import json, os, couchdb
import time
from dotenv import load_dotenv

import re
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from langdetect import detect

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from bs4 import BeautifulSoup
import re
from datetime import datetime
from nltk.stem import WordNetLemmatizer
import string
import emoji

load_dotenv()

# authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'mastodon_comb'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# optional, better not hardcode here
token = ''
m = Mastodon(
    # your server here
    api_base_url=f'https://aus.social',
    access_token="QvzGanPOh_FT0LtFwZOWIegId-1KY5CpAzb97h_3M_g"
)

##############
##############
#NLP Cleaning
##############
##############


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

class ToxicCommentClassifier:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def clean_text(self, text):
        cleaned_text = re.sub(r'[^a-zA-Z0-9 `~!@#$%^&*()_+-={}\[\]|\\:;"\'<>,.?/]', "", text)
        return cleaned_text

    def predict(self, text):
        # Clean the text
        text = self.clean_text(text)
        
        # Tokenize the text
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)

        # Get the model's predictions
        outputs = self.model(**inputs)

        # Use softmax to get probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Convert the probabilities tensor to a list
        probabilities_list = probabilities.squeeze().tolist()

        # Return only the probability of the text being toxic
        return probabilities_list[1]  # Assumes 'toxic' is the second class
    
class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.labels = ['negative', 'neutral', 'positive']

    def analyze(self, texts):
        results = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
            outputs = self.model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1).tolist()[0]
            result = [{"label": self.labels[i], "score": probabilities[i]} for i in range(len(self.labels))]
            results.append(result)
        return results

def safe_json_loads(json_string):
    try:
        # Attempt to parse the JSON
        return json.loads(json_string)
    except json.JSONDecodeError:
        # If there is an error, try cleaning up the string
        json_string = json_string.strip()  # Remove leading/trailing whitespace
        json_string = json_string.rstrip(',')  # Remove trailing commas
        json_string = json_string.rstrip('.')  # Remove trailing periods
        # Attempt to parse the JSON again
        return json.loads(json_string)
    
    
#Set up API for Huggingface sentiment classifier:
import requests
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()



# Function to check if a text is in English
def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False
    
    
# Initialize the classifiers
toxic_comment_classifier = ToxicCommentClassifier("martin-ha/toxic-comment-model")
    
    
sentiment_classifier = SentimentAnalyzer()
    
    
    
##############
##############
#NLP Cleaning
##############
##############


# listen on the timeline
class Listener(StreamListener):
    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.tweets_buffer = []
        self.followers_count_buffer = []
        self.following_count_buffer = []
        self.buffer_size = 50  # adjustable batch size

    # called when receiving new post or status update
    def on_update(self, status):
        json_str = json.dumps(status, indent=2, sort_keys=True, default=str)
        
        
        try:
        
            obj = json.loads(json_str)
            is_bot = obj["account"]["bot"]
            followers_count = obj["account"]["followers_count"]
            following_count = obj["account"]["following_count"]
            text = obj["content"]
            
        except:
            
            print("Invalid json_str")
            
            return

        # get all the tweet texts
        self.tweets_buffer.append(text)
        self.followers_count_buffer.append(followers_count)
        self.following_count_buffer.append(following_count)
        if len(self.tweets_buffer) < self.buffer_size:
            return

        # process batch of tweets
        tweet_texts = self.tweets_buffer

        # remove HTML tags
        tweet_texts = [BeautifulSoup(text, features="lxml").get_text() for text in tweet_texts]

        # remove URLs
        tweet_texts = [re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE) for text in tweet_texts]

        # remove emojis
        tweet_texts = [re.sub(':.*?:', '', emoji.demojize(text)) for text in tweet_texts]

        tweet_texts = [re.sub(r'[^a-zA-Z0-9 `~!@#$%^&*()_+-={}\[\]|\\:;"\'<>,.?/]', "", text) for text in tweet_texts]


        # process each tweet text independently
        tweet_word_lists = []

        for text in tweet_texts:
            # tokenize and remove stop words, punctuation, and apply lemmatization
            words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text) if word.lower() not in stop_words and word not in string.punctuation]
            tweet_word_lists.append(words)



        # calculate toxicity
        toxicities = [toxic_comment_classifier.predict(text) for text in tweet_texts]

        # using API to calculate sentiment
        while True:  # retry up to n times
            
            sentiment_outputs = sentiment_classifier.analyze(tweet_texts)
            if type(sentiment_outputs) != list:
                print("Error occured. Retrying in 5 seconds.")
                time.sleep(5)
            else:
                break




            

        # save all processed tweets to database
        for i in range(self.buffer_size):
            
            if is_english(tweet_texts[i]) == True:
            
                to_save = {
                    "text": tweet_texts[i],
                    "words": tweet_word_lists[i],
                    "toxicity": toxicities[i],
                    "sentiment": sentiment_outputs[i],
                    "followers_count": self.followers_count_buffer[i],
                    "following_count": self.following_count_buffer[i]
                    
                }
                doc_id, doc_rev = db.save(to_save)
                print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')
                
            else:
                continue
        
        # reset the buffer
        self.tweets_buffer = []







# make it better with try-catch and error-handling
m.stream_public(Listener())
