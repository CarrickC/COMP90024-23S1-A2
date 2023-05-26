# Upload Tweeter & SUDO Data

This repository contains scripts to upload Twitter and SUDO data to CouchDB.

## Getting Started
### Prerequisites
- Python 3.7+
- CouchDB 3.1.1

### Dependencies
- pandas
- couchdb
- flask
- flask_restful
- geopandas
- json
- flask_cors
- nltk
- BeautifulSoup
- emoji
- 
You can install any missing dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage
This project includes two main scripts: upload_twitter_data.py and upload_sudo_data.py.

Upload Twitter Data
To upload Twitter data to CouchDB, run:

```bash
python HF-WSent-Geo.py
```

### Upload SUDO Data
To upload SUDO data to CouchDB, run:

```bash
python HF_SUDO.py
```

### Code Overview
The HF-WSent-Geo.py script contains functions for connecting to Twitter's API, fetching tweets based on predefined search criteria, processing those tweets (including cleaning the text and extracting useful information), and uploading the data to CouchDB.

The HF_SUDO.py script contains functions for reading in data from various sources (including Excel files and shapefiles), preprocessing and cleaning that data, and uploading it to CouchDB. It includes data on a range of features, such as crime rates, rent prices, parking spaces, job forecasts, bar patron capacities, and population forecasts.
