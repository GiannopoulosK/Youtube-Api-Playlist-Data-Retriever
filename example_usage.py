from googleapiclient.discovery import build
from api_functions import *
from preprocessing_functions import *

# Initialize API KEY
import os
api_key = os.environ.get('YOUTUBE-API-KEY')

# Convenient way to create the API functionality
api = build('youtube', 'v3', developerKey = api_key)

# Call the API and get the data
playlist_id = 'PLfoNZDHitwjX-oU5YVAkfuXkALZqempRS'
df = get_playlist_df(api, playlist_id=playlist_id)  

# Apply Preprocessing steps(optional)
df = preprocess_df(df)

df.to_csv('Youtube_Data.csv', index=False)