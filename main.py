import os
from googleapiclient.discovery import build
from api_functions import *
from preprocessing_functions import *

# First, get your API key and store it here
api_key = os.environ.get('YOUTUBE-API-KEY')

# Then initialize the API with this convenient way
api = build('youtube', 'v3', developerKey = api_key)

# Then get the data
your_playlist_id = "" # Provide the playlist ID you want the data from.
df = get_playlist_df(api, playlist_id=your_playlist_id)

# Apply Preprocessing steps(optional)
df = preprocess_df(df)

# Finally, store the data in a csv file(optional)
df.to_csv("Youtube_Data.csv", index=False)