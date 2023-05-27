#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request
from flask_restful import Api, Resource
import couchdb
import geopandas as gpd
import pandas as pd
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

# Load the shapefile
gdf = gpd.read_file('SA2_2021_AUST_GDA2020.shp')

# Filter for Melbourne
gdf_melbourne = gdf[gdf['GCC_NAME21'] == 'Greater Melbourne']
gdf_melbourne.reset_index(drop=True, inplace=True)


# Simplify your dataframe
simp = gdf_melbourne[["SA2_NAME21", "geometry"]]


# In[ ]:


import pandas as pd

start = 2021
end = 2022
# Read the Excel file
df = pd.read_excel('SUDO_Data/Data_Tables_LGA_Recorded_Offences_Year_Ending_December_2022.xlsx', sheet_name=4)  # sheet_name is 0-indexed
df[['Suburb/Town Name', 'Offence Count']]
df = df[df["Year"].isin(list(range(start, end + 1)))]
grouped_df = df.groupby('Suburb/Town Name')['Offence Count'].sum().reset_index()
merged_df = pd.merge(simp, grouped_df, how='inner', left_on='SA2_NAME21', right_on='Suburb/Town Name')
final_df = merged_df[["Suburb/Town Name", "Offence Count"]]


# In[ ]:


import json, os, couchdb
import pandas as pd


# Authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# Get CouchDB instance
couch = couchdb.Server(url)

# Indicate the db name
db_name = 'sudocrime'

# If not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# Convert the DataFrame to a list of dictionaries
data_list = final_df.to_dict(orient='records')

# Save each dictionary (row) as a separate document in CouchDB

    
for i, data in enumerate(data_list):
    data['_id'] = f'row_{i}'
    doc_id, doc_rev = db.save(data)
    print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')


# In[ ]:


df = pd.read_excel('SUDO_Data/sa2_g36_weekly_rent_by_landlord_type_census_2016-314532625477305047.xlsx', sheet_name=0)
merged_df = pd.merge(simp, df, how='inner', left_on='SA2_NAME21', right_on=' sa2_name16')
final_df = merged_df[['SA2_NAME21', ' r_0_74_tot', ' r_75_99_tot', ' r_100_149_tot', 
                      ' r_150_199_tot', ' r_200_224_tot', ' r_225_274_tot', 
                      ' r_275_349_tot', ' r_350_449_tot', ' r_450_549_tot', 
                      ' r_550_649_tot', ' r_650_749_tot', ' r_750_849_tot', 
                      ' r_850_949_tot', ' r_950_over_tot']]


# In[ ]:


final_df = final_df.fillna(0)


# In[ ]:


import json, os, couchdb
import pandas as pd


# Authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# Get CouchDB instance
couch = couchdb.Server(url)

# Indicate the db name
db_name = 'sudorent'

# If not exist, create one
if db_name not in couch:
    db2 = couch.create(db_name)
else:
    db2 = couch[db_name]

# Convert the DataFrame to a list of dictionaries
data_list = final_df.to_dict(orient='records')

# Save each dictionary (row) as a separate document in CouchDB

    
for i, data in enumerate(data_list):
    data['_id'] = f'row_{i}'
    doc_id, doc_rev = db2.save(data)
    print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')


# In[ ]:





# In[ ]:





# In[ ]:


df = pd.read_csv('SUDO_Data/off-street-car-parks-with-capacity-and-type.csv')
df = df.groupby(['CLUE small area', 'Parking type'])['Parking spaces'].sum().reset_index()


# In[ ]:


import json, os, couchdb
import pandas as pd


# Authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# Get CouchDB instance
couch = couchdb.Server(url)

# Indicate the db name
db_name = 'sudocarpark'

# If not exist, create one
if db_name not in couch:
    db3 = couch.create(db_name)
else:
    db3 = couch[db_name]

# Convert the DataFrame to a list of dictionaries
data_list = df.to_dict(orient='records')

# Save each dictionary (row) as a separate document in CouchDB

    
for i, data in enumerate(data_list):
    data['_id'] = f'row_{i}'
    doc_id, doc_rev = db3.save(data)
    print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')


# In[ ]:


df = pd.read_csv('SUDO_Data/city-of-melbourne-jobs-forecasts-by-small-area-2020-2040.csv')
df = df[df["Industry Space Use"] != 'Total jobs']
df = df.groupby('Geography')['Value'].sum().reset_index()


# In[ ]:


import json, os, couchdb
import pandas as pd


# Authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# Get CouchDB instance
couch = couchdb.Server(url)

# Indicate the db name
db_name = 'sudojobsforecasts'

# If not exist, create one
if db_name not in couch:
    db4 = couch.create(db_name)
else:
    db4 = couch[db_name]

# Convert the DataFrame to a list of dictionaries
data_list = df.to_dict(orient='records')

# Save each dictionary (row) as a separate document in CouchDB

    
for i, data in enumerate(data_list):
    data['_id'] = f'row_{i}'
    doc_id, doc_rev = db4.save(data)
    print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')


# In[ ]:


df = pd.read_csv('SUDO_Data/bars-and-pubs-with-patron-capacity.csv')
df = df.groupby('CLUE small area')['Number of patrons'].sum().reset_index()


# In[ ]:


import json, os, couchdb
import pandas as pd


# Authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# Get CouchDB instance
couch = couchdb.Server(url)

# Indicate the db name
db_name = 'sudobars'

# If not exist, create one
if db_name not in couch:
    db5 = couch.create(db_name)
else:
    db5 = couch[db_name]

# Convert the DataFrame to a list of dictionaries
data_list = df.to_dict(orient='records')

# Save each dictionary (row) as a separate document in CouchDB

    
for i, data in enumerate(data_list):
    data['_id'] = f'row_{i}'
    doc_id, doc_rev = db5.save(data)
    print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')


# In[ ]:





# In[ ]:





# In[ ]:


allowed_age = ['Age 15-19', 'Age 85+', 'Age 75-79', 'Age 40-44', 
               'Age 60-64', 'Age 65-69', 'Age 70-74', 'Age 10-14', 
               'Age 35-39', 'Age 0-4', 'Age 45-49', 
               'Age 30-34', 'Age 55-59', 'Age 50-54', 'Age 5-9', 
               'Age 80-84', 'Age 20-24', 'Age 25-29']

allowed_gender = ['Male', 'Female']


# In[ ]:


import pandas as pd
df = pd.read_csv('SUDO_Data/city-of-melbourne-population-forecasts-by-small-area-2020-2040.csv')
df = df.dropna()
df = df[df['Age'].isin(allowed_age)]
df = df[df['Gender'].isin(allowed_gender)]


# In[ ]:


import json, os, couchdb
import pandas as pd


# Authentication
admin = 'admin'
password = 'password'
url = f'http://{admin}:{password}@172.26.131.185:5984/'

# Get CouchDB instance
couch = couchdb.Server(url)

# Indicate the db name
db_name = 'sudopopulation'

# If not exist, create one
if db_name not in couch:
    db6 = couch.create(db_name)
else:
    db6 = couch[db_name]

# Convert the DataFrame to a list of dictionaries
data_list = df.to_dict(orient='records')

# Save each dictionary (row) as a separate document in CouchDB

    
for i, data in enumerate(data_list):
    data['_id'] = f'row_{i}'
    doc_id, doc_rev = db6.save(data)
    print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')


# In[ ]:





# In[ ]:





# In[ ]:




