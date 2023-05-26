# Melbourne GeoSpatial Social Media Analysis ProjectCancel changes

This comprehensive project utilizes Flask RESTful API to analyze geo-tagged social media posts, focusing on sentiment and toxicity distribution in both Tweets and Mastodon posts within the Greater Melbourne area. The API also interacts with various databases to extract information about rent, population, crime, bars, jobs forecasts, and car parking in the area.

## Dependencies

The project requires the following libraries:

- Flask
- Flask_restful
- CouchDB
- configparser
- geopandas
- json
- flask_cors
- nltk
- collections
- bs4
- re
- datetime
- string
- emoji
- PySAL

You can install these libraries using pip:


```sh
pip install flask flask_restful couchdb configparser geopandas json flask_cors nltk collections bs4 re datetime string emoji pysal
```

Running the Server
To start the server, run the python script from your terminal:

```sh
python script_name.py
```

## API Endpoints
The project provides a wide array of endpoints:

Twitter Endpoints
- **geojson**: Returns GeoJSON data representing the Greater Melbourne area.
- **average_toxicity**: Returns a JSON object with the average toxicity of tweets for each suburb in Greater Melbourne.
- **global_autocorrelation**: Returns the global Moran's I, an indicator of spatial autocorrelation, based on the average tweet toxicity. It can take two optional parameters - 'rule' to choose the contiguity rule ('queen' or 'rook') and 'alpha' for the significance level.
- **local_autocorrelation**: Returns a JSON object with Local Moran's I, an indicator of local spatial autocorrelation, based on the average tweet toxicity for each suburb in Greater Melbourne. It can take two optional parameters - 'rule' to choose the contiguity rule ('queen' or 'rook') and 'alpha' for the significance level.
- **significant_local_autocorrelation**: Returns a JSON object indicating whether each suburb in Greater Melbourne shows significant local spatial autocorrelation of tweet toxicity, based on the provided significance level ('alpha') and contiguity rule ('rule').
SUDO Data Endpoints
- **crime_data**: Returns all documents from the 'sudocrime' database. Each document presumably contains information about a specific crime.
- **rent_data**: Calculates the average rent for different areas by aggregating data from the 'sudorent' database. The calculation is based on ranges of rent prices and the number of rentals in each range.
- **total_value_by_age**: Returns the total population for different geographical areas by age group, based on data from the 'sudopopulation' database.
- **total_value_by_gender**: Aggregates population data by gender.
- **total_patrons_by_area**: Retrieves the total number of bar patrons by area, based on data from the 'sudobars' database.
- **total_value_by_jobsforecasts**: Fetches the total job forecasts by area, based on data from the 'sudojobsforecasts' database.
- **total_spaces_by_area_and_type**: Retrieves the total number of parking spaces by area and type, based on data from the 'sudocarpark' database.
Mastodon Data Endpoints
- **sentiment_distribution**: Fetches the distribution of sentiment values from the Mastodon social media posts stored in the 'mastodon_comb' database.
- **followers_scatter, /following_scatter**: Retrieve data for creating scatter plots of the number of followers/followings against the toxicity of posts for users in the 'mastodon_comb' database.
- **top_word_counts_mastodon**: Retrieves the most common words in the text of the Mastodon posts stored in the 'mastodon_comb' database.

All these endpoints return data in the JSON format. Each resource is defined as a class that inherits from Resource, a class provided by the Flask-RESTful library.

## Configuration
The CouchDB configuration is contained in a configuration file couchdb_config.ini which needs to be created and should look like this:

```ini
[couchdb]
nodes = node1,node2,node3
Replace node1,node2,node3 with your CouchDB nodes.
```

Database Authentication
For authentication, the script uses admin and password. Change these to your CouchDB credentials.

CORS
Cross-Origin Resource Sharing (CORS) is enabled on all origins for all routes. Adjust the origins parameter as needed for your setup.

Geospatial Data
The geospatial data is contained in a shapefile under the path Australia_shapefiles/SA2_2021_AUST_GDA2020.shp. Make sure the file is present in the mentioned path before running the script.

Contact
For any questions or issues, please raise an issue in the GitHub repository.

License
This project is licensed under the terms of the MIT license.
