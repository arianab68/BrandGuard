import json
import pandas as pd

# Replace these with the paths to your JSON files
file_paths = ['/Users/ariana/Downloads/dataset_tweet-flash-KendalJenner-1.json','/Users/ariana/Downloads/dataset_tweet-flash-KendalJenner-2.json' ,'/Users/ariana/Downloads/dataset_tweet-flash-KendalJenner-3.json']

# List to hold all the data
all_data = []

# Read and combine data from each file
for file_path in file_paths:
    with open(file_path, 'r') as file:
        data = json.load(file)
        all_data.append(data)

# Assuming each file contains a list of records
# Flatten the list of lists into a single list
combined_data = [item for sublist in all_data for item in sublist]

# Create a DataFrame
df = pd.DataFrame(combined_data)

#Drop unnecessary columns 
non_null_counts = df.count()
df = df.loc[:, non_null_counts > 0]
df.drop(['tweet_avatar', 'quotes','tweet_id','url','query','username','fullname', 'in_reply_to', 'images','tweet_links','tweet_hashtags','tweet_mentions'], axis=1, inplace=True)

df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date

# Now df is the DataFrame containing the combined data from the JSON files
df.head()
