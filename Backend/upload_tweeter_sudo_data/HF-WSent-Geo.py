"""
Author:      Edward Liu
Student id:  913500
Date:        2023-5-26 08:36:06
Description: main function
"""

import json, os, couchdb
import pandas as pd
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

# Authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# Get CouchDB instance
couch = couchdb.Server(url)

# Indicate the db name
db_name = 'twittersegeov11'

# If not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]


# In[ ]:


import re
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

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
        inputs = self.tokenizer(text, return_tensors='pt')

        # Get the model's predictions
        outputs = self.model(**inputs)

        # Use softmax to get probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Convert the probabilities tensor to a list
        probabilities_list = probabilities.squeeze().tolist()

        # Return only the probability of the text being toxic
        return probabilities_list[1]  # Assumes 'toxic' is the second class

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


# In[ ]:


import geopandas as gpd
from shapely.geometry import Point
from langdetect import detect
import time

# Initialize the classifiers
toxic_comment_classifier = ToxicCommentClassifier("martin-ha/toxic-comment-model")


# Load the shapefile
gdf = gpd.read_file('SA2_2021_AUST_GDA2020.shp')
gdf_melbourne = gdf[gdf['GCC_NAME21'] == 'Greater Melbourne']


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
    
batch_data = []
batch_texts = []
batch_size = 50

with open('twitter-huge.json', 'r') as file:
    start = 0
    while True:
        
        line = file.readline()
        
        
        try:
            if start == 0:
                start += 1
                continue
            else:
                if not line or line[:2] == ']}':
                    break
                data = safe_json_loads(line[:-2])

                created_at = data.get('doc', {}).get('data', {}).get('created_at', '')
                text = data.get('doc', {}).get('data', {}).get('text', '')
                coordinates = data.get('doc', {}).get('data', {}).get('geo', {}).get('coordinates', {}).get('coordinates', '')

                if created_at != '' and text != '' and coordinates != '' and isinstance(text, str) and is_english(text):            

                    # Separate the coordinates into two columns
                    lon, lat = coordinates

                    # Create a new GeoDataFrame
                    geometry = [Point(lon, lat)]
                    geo_df = gpd.GeoDataFrame([data], geometry=geometry)  # Note the change here: [data] instead of data

                    # Make sure the GeoDataFrame has the same CRS as your Melbourne data
                    geo_df.set_crs(gdf_melbourne.crs, inplace=True)

                    # Perform the spatial join
                    points_in_melbourne = gpd.sjoin(geo_df, gdf_melbourne, how="inner", op='within')

                    # If the point is in Melbourne, add the suburb to the data and save to CouchDB
                    if not points_in_melbourne.empty:
                        
                        batch_texts.append(re.sub(r'[^a-zA-Z0-9 `~!@#$%^&*()_+-={}\[\]|\\:;"\'<>,.?/]', "", text))
                        # Add toxicity to data
                        data['toxicity'] = toxic_comment_classifier.predict(text)
                        data['suburb'] = points_in_melbourne.iloc[0]['SA2_NAME21']
                        batch_data.append(data)
                        
                    
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for line: {line}")
            continue
            
            
        if len(batch_data) == batch_size:
            
            
            assert(len(batch_data) == len(batch_texts))
            
            
            
            while True:
                sentiment_output = query({"inputs": batch_texts})

                if type(sentiment_output) != list:
                    print("Error occurred. Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    break
        
                
                
            
            for bd, so in zip(batch_data, sentiment_output):
                
                bd['sentiment'] = so
                
                doc_id, doc_rev = db.save(bd)
            
            batch_data = []
            batch_texts = []
            
            print("finished a batch")


# In[ ]:





# In[ ]:




