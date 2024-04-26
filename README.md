### This project utilizes the YouTube API to retrieve data from any YouTube playlist and return the results as a Pandas DataFrame.

## Installation
### To use this project, you'll need to install the required dependencies. You can install them using pip:

``` pip install -r requirements.txt ```

## Usage
1. **First, obtain your YouTube API key from the Google Cloud Console.**

2. **Clone this repository to your local machine:**

``` git clone https://github.com/GiannopoulosK/Youtube-Api-Playlist-Data-Retriever ```

3. **Navigate to the project directory:**

``` cd Youtube-Api-Playlist-Data-Retriever ```

4. **Replace "YOUR_API_KEY" in main.py with your actual YouTube API key.**

5. **Replace "YOUR_PLAYLIST_ID" in main.py with the Playlist ID you want the data from.**

6. **Run the main.py script:**

``` python main.py ```

7. **The script will fetch the data and store it as a csv_file.(Optinally, change the last line of code to store it as you like.)**

## Requirements
- Python 3.x
- pandas
- google-api-python-client

## Helper

### To get your playlist ID, all you need to do is go into the playlist and, on the url, copy and paste the part after 'list='. It always starts with PL.

### For example, in the following url, the playlist ID is PLfoNZDHitwjX-oU5YVAkfuXkALZqempRS: 
#### https://www.youtube.com/watch?v=f9j8nhMNYO4&list=PLfoNZDHitwjX-oU5YVAkfuXkALZqempRS