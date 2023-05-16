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
CORS(app, origins=['http://127.0.0.1:8080', 'http://localhost:8081'])




# Load the shapefile
gdf = gpd.read_file('SA2_2021_AUST_GDA2020.shp')

# Filter for Melbourne
gdf_melbourne = gdf[gdf['GCC_NAME21'] == 'Greater Melbourne']
gdf_melbourne.reset_index(drop=True, inplace=True)


# Simplify your dataframe
simp = gdf_melbourne[["SA2_NAME21", "geometry"]]



class AverageToxicity(Resource):
    def get(self):
        # using an existing view
        view = db.view('exp1/suburbtoxicity', group=True)
        
        # Convert the GeoDataFrame to GeoJSON
        geojson = simp.to_json()

        # Parse the GeoJSON to a dictionary
        geojson_dict = json.loads(geojson)

        # Retrieve the view results
        results = {}
        print("View: ", view)
        for row in view:
            print("Key: ", row.key)
            print("Value: ", row.value)
            
            # calculate the average from the sum and count values
            avg = row.value[0] / row.value[1] if row.value[1] > 0 else 0

            # Get the geometry for the suburb from the GeoJSON
            geometry = None
            for feature in geojson_dict['features']:
                if feature['properties']['SA2_NAME21'] == row.key:
                    geometry = feature['geometry']
                    break

            results[row.key] = {
                'average_toxicity': avg,
                'geometry': geometry
            }
        
        # Return the results as JSON
        return {'data': results}

api.add_resource(AverageToxicity, '/average_toxicity', '/average_toxicity/<id>')



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
        return {'I': moran.I, 'Expected I': moran.EI, 'p-value': moran.p_sim}

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

        # Convert the GeoDataFrame to GeoJSON
        geojson = simp.to_json()

        # Parse the GeoJSON to a dictionary
        geojson_dict = json.loads(geojson)

        # Prepare the results
        results = {}
        for i, row in gdf_melbourne.iterrows():
            suburb = row['SA2_NAME21']
            lisa = moran_loc.Is[i]
            EI = moran_loc.EI_sim[i]
            VI = moran_loc.VI_sim[i]
            ZI = moran_loc.z_sim[i]
            p_value = moran_loc.p_sim[i]

            # Get the geometry for the suburb from the GeoJSON
            geometry = None
            for feature in geojson_dict['features']:
                if feature['properties']['SA2_NAME21'] == suburb:
                    geometry = feature['geometry']
                    break

            results[suburb] = {
                'LISA': lisa,
                'EI': EI,
                'VI': VI,
                'ZI': ZI,
                'p_value': p_value,
                'geometry': geometry
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

        # Convert the GeoDataFrame to GeoJSON
        geojson = simp.to_json()

        # Parse the GeoJSON to a dictionary
        geojson_dict = json.loads(geojson)

        # Prepare the results
        results = {}
        for i, row in gdf_melbourne.iterrows():
            suburb = row['SA2_NAME21']
            is_significant = int(significant[i])

            # Get the geometry for the suburb from the GeoJSON
            geometry = None
            for feature in geojson_dict['features']:
                if feature['properties']['SA2_NAME21'] == suburb:
                    geometry = feature['geometry']
                    break

            results[suburb] = {
                'is_significant': is_significant,
                'geometry': geometry
            }

        # Return the results as JSON
        return {'data': results}

api.add_resource(SignificantLocalAutocorrelation, '/significant_local_autocorrelation')






api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)


