# sentiment_model.py
from transformers import pipeline
from tweet_processor import subset_df
import torch

# Load the DistilBERT model for sentiment analysis
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = pipeline("sentiment-analysis", model=model_name, device=0 if torch.cuda.is_available() else -1)

# Function to process tweets in batches and append results to DataFrame
def process_tweets(subset_df, batch_size=64):
    sentiments = []
    scores = []
    for i in range(0, len(subset_df), batch_size):
        batch = subset_df.iloc[i:i + batch_size]['tweets'].tolist()
        batch_results = model(batch)
        for result in batch_results:
            sentiments.append(result['label'])
            scores.append(result['score'])
    return sentiments, scores

# Process tweets and add results to DataFrame
subset_df['sentiment'],subset_df['score'] = process_tweets(subset_df)
