from flask import Flask, render_template, request
from flask_restful import Api, Resource
import couchdb
import geopandas as gpd
import json
from flask_cors import CORS
from pysal.explore import esda
from pysal.lib import weights
from esda.moran import Moran_Local

# authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'twittersegeov3'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

app = Flask(__name__)
api = Api(app)
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
    def get(self, label='LABEL_0'):
        # using an existing view
        view = db.view('exp1/suburbsent', group_level=2, limit=10)

        response = []

        for row in view:
            if row.key[1] == label:

                response.append({
                    "suburb": row.key[0], 
                    "label": row.key[1], 
                    "value": row.value,
                })

                # Limit to the first 10 records for debug purpose
                if len(response) >= 10:
                    break
            
        return response, 200  # Return with HTTP status 200 (OK)


api.add_resource(AverageSent, '/average_sent', '/average_sent/<label>')





class GlobalAutocorrelationSentiment(Resource):
    def get(self, label='LABEL_0'):
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
    def get(self, label='LABEL_0'):
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
    def get(self, label='LABEL_0'):
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








api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)


