# tweet_processor.py
import data
import re
import pandas as pd

def clean_tweet(tweet):
    """Clean the tweet by removing URLs, special characters, and converting to lowercase."""
    tweet = re.sub(r'http\S+', '', tweet)  # Remove URLs
    tweet = re.sub(r'[^A-Za-z0-9\s]', '', tweet)  # Remove special characters
    tweet = tweet.lower()  # Convert to lowercase
    return tweet.strip()

def preprocess_tweets(df):
    """Apply preprocessing to the 'text' column of the DataFrame."""
    df['text'] = df['text'].astype(str)
    df['tweets'] = df['text'].apply(clean_tweet)
    return df

def replace_nulls(df):
    """Replace null values in the DataFrame. Use '-' for text and '0' for numeric columns."""
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('-')
        else:
            df[col] = df[col].fillna(0)
    return df

# Preprocess the DataFrame
df = preprocess_tweets(data.df)

# Replace null values
df = replace_nulls(df)

#Drop unprocessed text column
df.drop('text', axis = 1, inplace = True)


# Check if the DataFrame has at least 10,000 rows
if len(df) >= 10000:
    subset_df = df.sample(n=5000, random_state=42)  # Randomly select 10,000 rows
else:
    print("DataFrame contains fewer than 10,000 rows.")
    subset_df = df  # If less than 10k rows, use the entire DataFrame
