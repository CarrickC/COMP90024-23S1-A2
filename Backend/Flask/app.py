from flask import Flask, render_template, request
from flask_restful import Api, Resource
import couchdb
import geopandas as gpd
import json
from flask_cors import CORS
from pysal.explore import esda
from pysal.lib import weights
from esda.moran import Moran_Local

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from bs4 import BeautifulSoup
import re
from datetime import datetime
from nltk.stem import WordNetLemmatizer
import string
import emoji


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


# authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'twittersegeov11'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]
    



app = Flask(__name__)
api = Api(app)
stop_words = set(stopwords.words('english'))
#CORS(app, origins=['http://127.0.0.1:8080', 'http://localhost:8081'])
CORS(app, origins=['*'])

############
############
#Loading the map information
############
############


# Load the shapefile
gdf = gpd.read_file('SA2_2021_AUST_GDA2020.shp')

# Filter for Melbourne
gdf_melbourne = gdf[gdf['GCC_NAME21'] == 'Greater Melbourne']
gdf_melbourne.reset_index(drop=True, inplace=True)


# Simplify your dataframe
simp = gdf_melbourne[["SA2_NAME21", "geometry"]]



############
############
#API for getting GeoJsonData
############
############


class GeoJsonData(Resource):
    def get(self):
        # Assuming that `gdf_melbourne` is a GeoDataFrame with a "geometry" column
        # Convert the GeoDataFrame to GeoJSON
        geojson = gdf_melbourne.to_json()

        # Parse the GeoJSON to a dictionary
        geojson_dict = json.loads(geojson)

        # Return the GeoJSON data
        return geojson_dict

api.add_resource(GeoJsonData, '/geojson')



############
############
#API for toxicity
############
############


class AverageToxicity(Resource):
    def get(self):
        # using an existing view
        view = db.view('exp1/suburbtoxicity', group=True)

        # Retrieve the view results
        results = {}
        for row in view:
            # calculate the average from the sum and count values
            avg = row.value[0] / row.value[1] if row.value[1] > 0 else 0

            results[row.key] = {
                'average_toxicity': avg,
            }
        
        # Return the results as JSON
        return {'data': results}

api.add_resource(AverageToxicity, '/average_toxicity')




class GlobalAutocorrelation(Resource):
    def get(self):
        # Get the rule parameter from the request
        rule = request.args.get('rule', 'queen')

        # Get the average toxicity for each suburb
        view = db.view('exp1/suburbtoxicity', group=True)
        toxicity_avgs = {row.key: row.value[0] / row.value[1] if row.value[1] > 0 else 0 for row in view}

        # Merge the average toxicity back to the geospatial data
        gdf_melbourne['avg_toxicity'] = gdf_melbourne['SA2_NAME21'].map(toxicity_avgs)

        # Fill NA values with 0 (assuming no data is equivalent to 0 toxicity)
        gdf_melbourne['avg_toxicity'] = gdf_melbourne['avg_toxicity'].fillna(0)

        # Create a spatial weights matrix
        if rule.lower() == 'rook':
            w = weights.contiguity.Rook.from_dataframe(gdf_melbourne)
        else:  # Default to 'queen'
            w = weights.contiguity.Queen.from_dataframe(gdf_melbourne)

        # Conduct Moran's I test
        moran = esda.moran.Moran(gdf_melbourne['avg_toxicity'], w)

        # Return the results as JSON
        return {
            'I': moran.I,
            'Expected I': moran.EI,
            'p-value': moran.p_sim
        }

api.add_resource(GlobalAutocorrelation, '/global_autocorrelation')





class LocalAutocorrelation(Resource):
    def get(self):
        # Get the rule parameter from the request
        rule = request.args.get('rule', 'queen')

        # Get the average toxicity for each suburb
        view = db.view('exp1/suburbtoxicity', group=True)
        toxicity_avgs = {row.key: row.value[0] / row.value[1] if row.value[1] > 0 else 0 for row in view}

        # Merge the average toxicity back to the geospatial data
        gdf_melbourne['avg_toxicity'] = gdf_melbourne['SA2_NAME21'].map(toxicity_avgs)

        # Fill NA values with 0 (assuming no data is equivalent to 0 toxicity)
        gdf_melbourne['avg_toxicity'] = gdf_melbourne['avg_toxicity'].fillna(0)

        # Create a spatial weights matrix
        if rule.lower() == 'rook':
            w = weights.contiguity.Rook.from_dataframe(gdf_melbourne)
        else:  # Default to 'queen'
            w = weights.contiguity.Queen.from_dataframe(gdf_melbourne)

        # Calculate Local Moran's I
        moran_loc = Moran_Local(gdf_melbourne['avg_toxicity'], w)

        # Prepare the results
        results = {}
        for i, row in gdf_melbourne.iterrows():
            suburb = row['SA2_NAME21']
            lisa = moran_loc.Is[i]
            EI = moran_loc.EI_sim[i]
            VI = moran_loc.VI_sim[i]
            ZI = moran_loc.z_sim[i]
            p_value = moran_loc.p_sim[i]

            results[suburb] = {
                'LISA': lisa,
                'EI': EI,
                'VI': VI,
                'ZI': ZI,
                'p_value': p_value,
            }

        # Return the results as JSON
        return {'data': results}

api.add_resource(LocalAutocorrelation, '/local_autocorrelation')



class SignificantLocalAutocorrelation(Resource):
    def get(self):
        # Get the significance level parameter from the request
        alpha = float(request.args.get('alpha', 0.05))

        # Get the rule parameter from the request
        rule = request.args.get('rule', 'queen')

        # Get the average toxicity for each suburb
        view = db.view('exp1/suburbtoxicity', group=True)
        toxicity_avgs = {row.key: row.value[0] / row.value[1] if row.value[1] > 0 else 0 for row in view}

        # Merge the average toxicity back to the geospatial data
        gdf_melbourne['avg_toxicity'] = gdf_melbourne['SA2_NAME21'].map(toxicity_avgs)

        # Fill NA values with 0 (assuming no data is equivalent to 0 toxicity)
        gdf_melbourne['avg_toxicity'] = gdf_melbourne['avg_toxicity'].fillna(0)

        # Create a spatial weights matrix
        if rule.lower() == 'rook':
            w = weights.contiguity.Rook.from_dataframe(gdf_melbourne)
        else:  # Default to 'queen'
            w = weights.contiguity.Queen.from_dataframe(gdf_melbourne)

        # Calculate Local Moran's I
        moran_loc = Moran_Local(gdf_melbourne['avg_toxicity'], w)

        # Create a boolean mask for significant local spatial autocorrelation
        significant = moran_loc.p_sim < alpha

        # Prepare the results
        results = {}
        for i, row in gdf_melbourne.iterrows():
            suburb = row['SA2_NAME21']
            is_significant = int(significant[i])

            results[suburb] = {
                'is_significant': is_significant,
            }

        # Return the results as JSON
        return {'data': results}

api.add_resource(SignificantLocalAutocorrelation, '/significant_local_autocorrelation')




##################
##################
#API for sentiment
##################
##################




class AverageSent(Resource):
    def get(self, label='positive'):
        # using an existing view
        view = db.view('exp1/suburbsent', group_level=2)

        response = []

        for row in view:
            if row.key[1] == label:

                response.append({
                    "suburb": row.key[0], 
                    "label": row.key[1], 
                    "value": row.value,
                })

            
        return response, 200  # Return with HTTP status 200 (OK)


api.add_resource(AverageSent, '/average_sent', '/average_sent/<label>')





class GlobalAutocorrelationSentiment(Resource):
    def get(self, label='positive'):
        # Get the rule parameter from the request
        rule = request.args.get('rule', 'queen')

        # Get the average sentiment for each suburb and the specific label
        view = db.view('exp1/suburbsent', group_level=2)
        sentiment_avgs = {row.key[0]: row.value["average"] for row in view if row.key[1] == label}
        

        # Merge the average sentiment back to the geospatial data
        gdf_melbourne['avg_sentiment'] = gdf_melbourne['SA2_NAME21'].map(sentiment_avgs)
        
        
        print(gdf_melbourne['avg_sentiment'])


        # Fill NA values with 0 (assuming no data is equivalent to 0 sentiment)
        gdf_melbourne['avg_sentiment'] = gdf_melbourne['avg_sentiment'].fillna(0)

        # Create a spatial weights matrix
        if rule.lower() == 'rook':
            w = weights.contiguity.Rook.from_dataframe(gdf_melbourne)
        else:  # Default to 'queen'
            w = weights.contiguity.Queen.from_dataframe(gdf_melbourne)

        # Conduct Moran's I test
        moran = esda.moran.Moran(gdf_melbourne['avg_sentiment'], w)

        # Return the results as JSON
        return {
            'I': moran.I,
            'Expected I': moran.EI,
            'p-value': moran.p_sim
        }

api.add_resource(GlobalAutocorrelationSentiment, '/global_autocorrelation_sentiment', '/global_autocorrelation_sentiment/<label>')



class LocalAutocorrelationSentiment(Resource):
    def get(self, label='positive'):
        # Get the rule parameter from the request
        rule = request.args.get('rule', 'queen')

        # Get the average sentiment for each suburb
        view = db.view('exp1/suburbsent', group_level=2)
        sentiment_avgs = {row.key[0]: row.value["average"] for row in view if row.key[1] == label}

        # Merge the average sentiment back to the geospatial data
        gdf_melbourne['avg_sentiment'] = gdf_melbourne['SA2_NAME21'].map(sentiment_avgs)

        # Fill NA values with 0 (assuming no data is equivalent to 0 sentiment)
        gdf_melbourne['avg_sentiment'] = gdf_melbourne['avg_sentiment'].fillna(0)

        # Create a spatial weights matrix
        if rule.lower() == 'rook':
            w = weights.contiguity.Rook.from_dataframe(gdf_melbourne)
        else:  # Default to 'queen'
            w = weights.contiguity.Queen.from_dataframe(gdf_melbourne)

        # Calculate Local Moran's I
        moran_loc = Moran_Local(gdf_melbourne['avg_sentiment'], w)

        # Prepare the results
        results = {}
        for i, row in gdf_melbourne.iterrows():
            suburb = row['SA2_NAME21']
            lisa = moran_loc.Is[i]
            EI = moran_loc.EI_sim[i]
            VI = moran_loc.VI_sim[i]
            ZI = moran_loc.z_sim[i]
            p_value = moran_loc.p_sim[i]

            results[suburb] = {
                'LISA': lisa,
                'EI': EI,
                'VI': VI,
                'ZI': ZI,
                'p_value': p_value,
            }

        # Return the results as JSON
        return {'data': results}

api.add_resource(LocalAutocorrelationSentiment, '/local_autocorrelation_sentiment', '/local_autocorrelation_sentiment/<label>')





class SignificantLocalAutocorrelationSentiment(Resource):
    def get(self, label='positive'):
        # Get the significance level parameter from the request
        alpha = float(request.args.get('alpha', 0.05))

        # Get the rule parameter from the request
        rule = request.args.get('rule', 'queen')

        # Get the average sentiment for each suburb
        view = db.view('exp1/suburbsent', group_level=2)
        sentiment_avgs = {row.key[0]: row.value["average"] for row in view if row.key[1] == label}

        # Merge the average sentiment back to the geospatial data
        gdf_melbourne['avg_sentiment'] = gdf_melbourne['SA2_NAME21'].map(sentiment_avgs)

        # Fill NA values with 0 (assuming no data is equivalent to 0 sentiment)
        gdf_melbourne['avg_sentiment'] = gdf_melbourne['avg_sentiment'].fillna(0)

        # Create a spatial weights matrix
        if rule.lower() == 'rook':
            w = weights.contiguity.Rook.from_dataframe(gdf_melbourne)
        else:  # Default to 'queen'
            w = weights.contiguity.Queen.from_dataframe(gdf_melbourne)

        # Calculate Local Moran's I
        moran_loc = Moran_Local(gdf_melbourne['avg_sentiment'], w)

        # Create a boolean mask for significant local spatial autocorrelation
        significant = moran_loc.p_sim < alpha

        # Prepare the results
        results = {}
        for i, row in gdf_melbourne.iterrows():
            suburb = row['SA2_NAME21']
            is_significant = int(significant[i])

            results[suburb] = {
                'is_significant': is_significant,
            }

        # Return the results as JSON
        return {'data': results}

api.add_resource(SignificantLocalAutocorrelationSentiment, '/significant_local_autocorrelation_sentiment', '/significant_local_autocorrelation_sentiment/<label>')




############
############
#API for text analysis
############
############




class TopWordCounts(Resource):
    def get(self):
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        # retrieve all docs
        view_results = db.view('WordCounts/RawText', include_docs=True, startkey=[start_date, None], endkey=[end_date, {}])

        # get all the tweet texts
        tweet_texts = [row.value for row in view_results]

        # remove HTML tags
        tweet_texts = [BeautifulSoup(text, features="lxml").get_text() for text in tweet_texts]

        # remove URLs
        tweet_texts = [re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE) for text in tweet_texts]

        # remove emojis
        tweet_texts = [re.sub(':.*?:', '', emoji.demojize(text)) for text in tweet_texts]

        # tokenize and remove stop words, punctuation, apply lemmatization, and filter for alphabetical words only
        words = [lemmatizer.lemmatize(word.lower()) for text in tweet_texts for word in word_tokenize(text) 
                 if word.lower() not in stop_words and word.isalpha() and word not in string.punctuation]


        # count occurrences of each word
        word_counts = Counter(words)

        return {'data': dict(word_counts)}


api.add_resource(TopWordCounts, '/top_word_counts')



class TopWordCountsByAllSuburbs(Resource):
    def get(self):
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        # A list of all suburbs
        suburbs = list(simp["SA2_NAME21"])  # replace this with the list of suburbs you have

        data = {}

        for suburb in suburbs:
            view_results = db.view('WordCounts/RawText', include_docs=True, startkey=[start_date, suburb], endkey=[end_date, suburb])

            # get all the tweet texts for the specific suburb
            tweet_texts = [row.value for row in view_results if row.key[1] == suburb]

            # remove HTML tags
            tweet_texts = [BeautifulSoup(text, features="lxml").get_text() for text in tweet_texts]

            # remove URLs
            tweet_texts = [re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE) for text in tweet_texts]

            # remove emojis
            tweet_texts = [re.sub(':.*?:', '', emoji.demojize(text)) for text in tweet_texts]

            # tokenize and remove stop words, punctuation, and apply lemmatization
            words = [lemmatizer.lemmatize(word.lower()) for text in tweet_texts for word in word_tokenize(text) if word.lower() not in stop_words and word not in string.punctuation]

            # count occurrences of each word
            word_counts = Counter(words)

            data[suburb] = dict(word_counts)

        return {'data': data}


api.add_resource(TopWordCountsByAllSuburbs, '/top_word_counts_by_all_suburbs')



class TopWordCountsBySuburb(Resource):
    def get(self):
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        suburb = request.args.get('suburb', None)

        # retrieve all docs
        view_results = db.view('WordCounts/RawText', include_docs=True, startkey=[start_date, suburb], endkey=[end_date, suburb])

        # get all the tweet texts for the specific suburb
        tweet_texts = [row.value for row in view_results if row.key[1] == suburb]

        # remove HTML tags
        tweet_texts = [BeautifulSoup(text, features="lxml").get_text() for text in tweet_texts]

        # remove URLs
        tweet_texts = [re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE) for text in tweet_texts]

        # remove emojis
        tweet_texts = [re.sub(':.*?:', '', emoji.demojize(text)) for text in tweet_texts]

        # tokenize and remove stop words, punctuation, and apply lemmatization
        words = [lemmatizer.lemmatize(word.lower()) for text in tweet_texts for word in word_tokenize(text) if word.lower() not in stop_words and word not in string.punctuation]

        # count occurrences of each word
        word_counts = Counter(words)

        return {'data': dict(word_counts)}


api.add_resource(TopWordCountsBySuburb, '/top_word_counts_by_suburb')



###############
###############
#SUDO Data
###############
###############


db_crime = couch['sudocrime']
db_rent = couch['sudorent']
db_population = couch['sudopopulation']
db_bars = couch['sudobars']
db_jobsforecasts = couch['sudojobsforecasts']
db_sudocarpark = couch['sudocarpark']



class CrimeData(Resource):
    def get(self):
        crime_data = {doc["id"]: doc['doc'] for doc in db_crime.view('_all_docs', include_docs=True)}
        return {'crime_data': crime_data}


class RentData(Resource):
    def get(self):
        all_docs = {doc['id']: doc['doc'] for doc in db_rent.view('_all_docs', include_docs=True)}
        rent_data = {}
        for id, data in all_docs.items():
            rent_ranges = {
                ' r_0_74_tot': 74,
                ' r_75_99_tot': 99,
                ' r_100_149_tot': 149,
                ' r_150_199_tot': 199,
                ' r_200_224_tot': 224,
                ' r_225_274_tot': 274,
                ' r_275_349_tot': 349,
                ' r_350_449_tot': 449,
                ' r_450_549_tot': 549,
                ' r_550_649_tot': 649,
                ' r_650_749_tot': 749,
                ' r_750_849_tot': 849,
                ' r_850_949_tot': 949,
                ' r_950_over_tot': 950  # Consider adjusting this as needed
            }

            weighted_sum = 0
            total_rentals = 0
            for range, max_value in rent_ranges.items():
                count = data.get(range, 0)
                weighted_sum += max_value * count
                total_rentals += count

            if total_rentals != 0:
                average_rent = weighted_sum / total_rentals
            else:
                average_rent = 0

            rent_data[id] = {"SA2_NAME21": data.get("SA2_NAME21"), "average_rent": average_rent}

        return {'rent_data': rent_data}


    
    
    
class TotalValueByAge(Resource):
    def get(self):

        view = db_population.view('sum/geoage', group=True)

        results = {}
        for row in view:
            geography, age = row.key
            total_value = row.value
            if geography not in results:
                results[geography] = {}
            results[geography][age] = total_value

        return {'data': results}


    
class TotalValueByGender(Resource):
    def get(self):

        view = db_population.view('sum/geogender', group=True)

        results = {}
        for row in view:
            geography, gender = row.key
            total_value = row.value
            if geography not in results:
                results[geography] = {}
            results[geography][gender] = total_value

        return {'data': results}



class TotalPatronsByArea(Resource):
    def get(self):

        view = db_bars.view('sum/sum', group=True)

        results = {}
        for row in view:
            results[row.key] = row.value

        return {'data': results}




class TotalValueByJobsForecasts(Resource):
    def get(self):

        view = db_jobsforecasts.view('sum/sum', group=True)

        results = {}
        for row in view:
            results[row.key] = row.value

        return {'data': results}


    
    
    
    
class TotalSpacesByAreaAndType(Resource):
    def get(self):
        
        view = db_sudocarpark.view('sum/sum', group=True)

        results = {}
        for row in view:
            area, parking_type = row.key
            total_spaces = row.value
            if area not in results:
                results[area] = {}
            results[area][parking_type] = total_spaces

        return {'data': results}




    
    
    
    
    

    
api.add_resource(TotalSpacesByAreaAndType, '/total_spaces_by_area_and_type')
api.add_resource(TotalValueByJobsForecasts, '/total_value_by_jobsforecasts')
api.add_resource(TotalPatronsByArea, '/total_patrons_by_area')
api.add_resource(TotalValueByGender, '/total_value_by_gender')
api.add_resource(TotalValueByAge, '/total_value_by_age')
api.add_resource(CrimeData, '/crime_data')
api.add_resource(RentData, '/rent_data')


###############
###############
#Mastodon Data
###############
###############



db_M = couch['mastodon_comb']


class SentimentDistribution(Resource):
    def get(self):
        
        db_type = request.args.get('db', "mastodon")
        
        if db_type == 'mastodon':
            # using the created view
            view = db_M.view('sentiment/sentiment_distribution', group=True)
            
        else:
            view = db.view('sentiment/sentiment_distribution', group=True)

        # Retrieve the view results
        results = {}
        for row in view:
            results[row.key] = row.value
        
        # Return the results as JSON
        return {'data': results}

api.add_resource(SentimentDistribution, '/sentiment_distribution')





class FollowersScatter(Resource):
    def get(self):
        # using the created view
        view = db_M.view('user_interaction_analysis/followers_sentiment_toxicity')

        # Retrieve the view results
        results = { 'followers_count': [], 'toxicity': [] }
        for row in view:
            results['followers_count'].append(row.key)
            results['toxicity'].append(row.value['toxicity'])

        # Return the results as JSON
        return {'data': results}

api.add_resource(FollowersScatter, '/followers_scatter')


class FollowingScatter(Resource):
    def get(self):
        # using the created view
        view = db_M.view('user_interaction_analysis/following_sentiment_toxicity')

        # Retrieve the view results
        results = { 'following_count': [], 'toxicity': [] }
        for row in view:
            results['following_count'].append(row.key)
            results['toxicity'].append(row.value['toxicity'])

        # Return the results as JSON
        return {'data': results}

api.add_resource(FollowingScatter, '/following_scatter')





class TopWordCountsMastodon(Resource):
    def get(self):
        # Retrieve all docs
        num_words = int(request.args.get('num_words', 100))
        
        view_results = db_M.view('_all_docs', include_docs=True)

        # Get all the texts
        texts = [row.doc['text'] for row in view_results if 'text' in row.doc]

        # Tokenize and remove stop words, punctuation, apply lemmatization, and filter for alphabetical words only
        words = [lemmatizer.lemmatize(word.lower()) for text in texts for word in word_tokenize(text) 
                 if word.lower() not in stop_words and word.isalpha()]

        # Count occurrences of each word
        word_counts = Counter(words)

        # Return the 10 most common words
        return {'data': dict(word_counts.most_common(num_words))}

api.add_resource(TopWordCountsMastodon, '/top_word_counts_mastodon')










api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)


