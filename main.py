import os
from googleapiclient.discovery import build
from api_functions import *
from preprocessing_functions import *

# First, get your API key and store it here
api_key = YOUR_API_KEY

# Then initialize the API with this convenient way
api = build('youtube', 'v3', developerKey = api_key)

# Then get the data
playlist_id = YOUR_PLAYLIST_ID # Provide the playlist ID you want the data from.
df = get_playlist_df(api=api, playlist_id=playlist_id)

# Apply Preprocessing steps(optional)
df = preprocess_df(df)

# Finally, store the data in a csv file(optional)
df.to_csv("Youtube_Data.csv", index=False)