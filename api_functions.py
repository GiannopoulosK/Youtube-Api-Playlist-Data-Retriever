import pandas as pd

def get_playlist_videos(api, playlist_id, max_results=50):
    """
    Get videos from a YouTube playlist.

    Args:
    - api: YouTube Data API service object.
    - playlist_id: ID of the playlist from which to get videos.
    - max_results: Maximum number of results to get per page.(max 50)

    Returns:
    - A list of dictionaries, each representing a video in the playlist.
    
    API calls -> Tokens Used: 1 per 50 videos
    """
    playlist_videos = []

    # Initial playlist request
    pl_request = api.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=max_results
    )

    # Retrieve all pages of videos
    while pl_request:
        pl_snippet = pl_request.execute()  # Execute the request
        playlist_videos.extend(pl_snippet['items'])  # Add videos to the list
        pl_request = api.playlistItems().list_next(pl_request, pl_snippet)  # Check for more pages until all videos are pulled

    return playlist_videos


"""
Below functions take in the playlist videos retrieved with the get_playlist_videos function
and extract relevant information(see function names for details)
"""


def extract_publish_dates(playlist_videos):
    publish_dates = []
    for video_info in playlist_videos:
        if 'snippet' in video_info and video_info['snippet'].get('title') != 'Private video':
            publish_dates.append(video_info['snippet'].get('publishedAt'))
    return publish_dates

def extract_video_ids(playlist_videos):
    video_ids = []
    for video_info in playlist_videos:
        if 'snippet' in video_info and video_info['snippet'].get('title') != 'Private video':
            video_ids.append(video_info['snippet'].get('resourceId', {}).get('videoId'))
    return video_ids

def extract_titles(playlist_videos):
    titles = []
    for video_info in playlist_videos:
        if 'snippet' in video_info and video_info['snippet'].get('title') != 'Private video':
            titles.append(video_info['snippet']['title'])
    return titles

def extract_descriptions(playlist_videos):
    descriptions = []
    for video_info in playlist_videos:
        if 'snippet' in video_info and video_info['snippet'].get('title') != 'Private video':
            descriptions.append(video_info['snippet'].get('description'))
    return descriptions

# This is just a helper function
def split_list(lst, batch_size):
    """Function to split a list into batches.(Helper Function for other API calls)"""
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]


"""
Below functions take in the playlist video IDs retrieved with the extract_video_ids function
and extract relevant information(see function names for details)
""" 


def get_video_statistics(api, video_ids):
    """
    Function to get statistics for a list of video IDs.
    API calls -> Tokens Used: 1 per 50 videos
    """
    batch_size = 50  # Adjust batch size based on API limits
    all_videos_stats = []

    for batch in split_list(video_ids, batch_size):
        video_ids_str = ','.join(batch)
        stat_request = api.videos().list(part='statistics', id=video_ids_str)

        try:
            response = stat_request.execute()
            all_videos_stats.extend(response['items'])
        except Exception as e:
            print(f"Error getting statistics for batch {batch}: {e}")

    return all_videos_stats

def get_video_topic_details(api, video_ids):
    """
    Function to get topic details for a list of video IDs.
    API calls -> Tokens Used: 1 per 50 videos
    """
    batch_size = 50  # Adjust batch size based on API limits
    all_video_topic_details = []

    for batch in split_list(video_ids, batch_size):
        video_ids_str = ','.join(batch)
        topic_request = api.videos().list(part='topicDetails', id=video_ids_str)

        try:
            response = topic_request.execute()
            all_video_topic_details.extend(response['items'])
        except Exception as e:
            print(f"Error getting topic details for batch {batch}: {e}")

    return all_video_topic_details

def get_video_content_details(api, video_ids):
    """
    Function to get content details for a list of video IDs.
    API calls -> Tokens Used: 1 per 50 videos
    """
    batch_size = 50  # Adjust batch size based on API limits
    all_video_content_details = []

    for batch in split_list(video_ids, batch_size):
        video_ids_str = ','.join(batch)
        content_request = api.videos().list(part='contentDetails', id=video_ids_str)

        try:
            response = content_request.execute()
            all_video_content_details.extend(response['items'])
        except Exception as e:
            print(f"Error getting content details for batch {batch}: {e}")

    return all_video_content_details



"""
Below functions take in the playlist video IDs retrieved with the api calls
and extract relevant information(see function names for details)
""" 


def extract_video_duration(video_content_details_responses):
    """Function to extract video durations from video content details response."""
    durations = []
    for item in video_content_details_responses:
        durations.append(item['contentDetails'].get('duration'))
    return durations


def extract_video_definition(video_content_details_responses):
    """Function to extract video definitions from video content details response."""
    definitions = []
    for item in video_content_details_responses:
        definitions.append(item['contentDetails'].get('definition'))
    return definitions


def extract_view_count(video_statistics_response):
    """Function to extract view counts from video statistics response."""
    view_counts = []
    for item in video_statistics_response:
        view_counts.append(item['statistics'].get('viewCount'))
    return view_counts

def extract_like_count(video_statistics_responses):
    """Function to extract like counts from video statistics response."""
    like_counts = []
    for item in video_statistics_responses:
        like_counts.append(item['statistics'].get('likeCount'))
    return like_counts

def extract_favorite_count(video_statistics_response):
    """Function to extract favorite counts from video statistics response."""
    favorite_counts = []
    for item in video_statistics_response:
        favorite_counts.append(item['statistics'].get('favoriteCount'))
    return favorite_counts

def extract_comment_count(video_statistics_response):
    """Function to extract comment counts from video statistics response."""
    comment_counts = []
    for item in video_statistics_response:
        comment_counts.append(item['statistics'].get('commentCount'))
    return comment_counts

def extract_topic_categories(video_topic_response):
    """Function to extract topic categories from video topic response."""
    topic_categories = []
    for item in video_topic_response:
        try:
            topic_categories.append(item['topicDetails'].get('topicCategories'))
        except Exception as e:
            topic_categories.append(None)
        
    return topic_categories



def get_playlist_df(api, playlist_id):
    """
    This is the function used for fast access to the dataframe. 
    It uses all the above functions and creates the final DataFrame.
    API calls -> Tokens Used: 4 per 50 videos
    """
    
    # Get Playlist Videos
    playlist_videos = get_playlist_videos(api, playlist_id)

    # Get Video Info
    publish_dates = extract_publish_dates(playlist_videos)
    video_ids = extract_video_ids(playlist_videos)
    titles = extract_titles(playlist_videos)
    descriptions = extract_descriptions(playlist_videos)

    # Get Video Content Details
    content_details = get_video_content_details(api, video_ids)

    video_durations = extract_video_duration(content_details)
    video_hd = extract_video_definition(content_details)

    # Get Video Stats
    stats = get_video_statistics(api, video_ids)

    video_views = extract_view_count(stats)
    video_likes = extract_like_count(stats)
    video_favorites = extract_favorite_count(stats)
    video_comments = extract_comment_count(stats)

    # Get Topic Details
    topic_details = get_video_topic_details(api, video_ids)

    topic_categories = extract_topic_categories(topic_details)
    
    
    # Create DataFrame
    df = pd.DataFrame({
        'PublishDate': publish_dates,
        'VideoId': video_ids,
        'Title': titles,
        'Description': descriptions,
        'Duration': video_durations,
        'HD': video_hd,
        'Views': video_views,
        'Likes': video_likes,
        'Favorites': video_favorites,
        'Comments': video_comments,
        'TopicCategories': topic_categories
    })
    
    return df    