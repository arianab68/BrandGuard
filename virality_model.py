from sentiment_model import subset_df
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# Assuming columns 'likes', 'replies', 'retweets', and 'sentiment_score' exist in df
scaler = MinMaxScaler()
subset_df[['likes', 'replies', 'retweets']] = scaler.fit_transform(subset_df[['likes', 'replies', 'retweets']])

# Calculate the average (mean) for each column
average_likes = subset_df['likes'].mean()
average_retweets = subset_df['retweets'].mean()
average_replies = subset_df['replies'].mean()
average_sentiment = subset_df['score'].mean()

# Print the results
# print(f"Average Likes: {average_likes}")
# print(f"Average Retweets: {average_retweets}")
# print(f"Average Reply: {average_replies}")
# print(f"Average Score: {average_sentiment}")

def calculate_virality_score(row):
    like_weight = 10
    reply_weight = 20
    retweet_weight = 200
    sentiment_weight = 5  # Weight for sentiment score

    # Adjust the sentiment score
    adjusted_sentiment_score = abs(row['score'] - 0.5) * 2

    score = (row['likes'] * like_weight +
             row['replies'] * reply_weight +
             row['retweets'] * retweet_weight +
             adjusted_sentiment_score * sentiment_weight)

    return score

subset_df['virality_score'] = subset_df.apply(calculate_virality_score, axis=1)

VIRAL_THRESHOLD = 10 # Example threshold
subset_df['is_viral'] = subset_df['virality_score'] > VIRAL_THRESHOLD

from sklearn.ensemble import GradientBoostingClassifier

# Define features and the target
X = subset_df[['likes', 'replies', 'retweets', 'score', 'virality_score']]  # Features
y = subset_df['is_viral']  # Target

# Train the Gradient Boosting Classifier
model = GradientBoostingClassifier()
model.fit(X, y)

# Predict virality
subset_df['predicted_viral'] = model.predict(X)