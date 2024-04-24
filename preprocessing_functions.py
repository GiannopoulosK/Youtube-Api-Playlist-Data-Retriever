import re
import pandas as pd

"""
Below functions apply preprocessing to the DataFrame returned which contains data
from a Youtube Playlist's videos.
"""

def parse_date(df):
    df[['Date', 'Time']] = df['PublishDate'].str.split('T', expand=True)
    df['Time'] = df['Time'].str.rstrip('Z')
    df.drop(columns=['PublishDate'], inplace=True)
    return df


def parse_duration(df):
    def parse_duration(duration):
        hours = 0
        minutes = 0
        seconds = 0

        hours_match = re.search(r'(\d+)H', duration)
        minutes_match = re.search(r'(\d+)M', duration)
        seconds_match = re.search(r'(\d+)S', duration)

        if hours_match:
            hours = int(hours_match.group(1))
        if minutes_match:
            minutes = int(minutes_match.group(1))
        if seconds_match:
            seconds = int(seconds_match.group(1))

        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds

    new_df = df.copy()
    new_df['TotalSeconds'] = df['Duration'].apply(parse_duration)
    new_df.drop(columns=['Duration'], inplace=True)
    return new_df


def parse_topic_categories(df):
    df['TopicCategories'] = df['TopicCategories'].apply(lambda x: [url.replace('https://en.wikipedia.org/wiki/', '') if url is not None else None for url in x] if isinstance(x, list) else None)
    return df


def preprocess_df(df):
    """
    Combines all preprocessing steps
    """
    df_temp = df.copy()
    df_temp = parse_date(df_temp)
    df_temp = parse_duration(df_temp)
    df_temp = parse_topic_categories(df_temp)
    
    return df_temp