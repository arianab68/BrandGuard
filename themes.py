from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from virality_model import subset_df

# Vectorize the tweets using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(subset_df['tweets'])

# Choose the number of clusters/themes
number_of_clusters = 8
km = KMeans(n_clusters=number_of_clusters, random_state=42)

# Fit the K-Means model to the data
km.fit(tfidf_matrix)

# Predict the cluster for each tweet
predicted_clusters = km.predict(tfidf_matrix)

# Ensure the length matches the DataFrame's length
assert len(predicted_clusters) == len(subset_df)

# Assign the cluster labels to the DataFrame
subset_df['theme'] = predicted_clusters

# Optionally, look at the top terms for each cluster
#print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = tfidf_vectorizer.get_feature_names_out()
for i in range(number_of_clusters):
    top_terms = [terms[ind] for ind in order_centroids[i, :10]]
    #print(f"Cluster {i}: {top_terms}")

# Create a mapping from cluster label to descriptive names based on the top terms
cluster_to_theme = {
    0: 'Controversy & Backlash',
    1: 'Brand Preference',
    2: 'Celebrity Endorsements',
    3: 'Ad Reactions & Sentiments',
    4: 'Consumer Opinions',
    5: 'Commercial Offense',
    6: 'Social Commentary',
    7: 'General Confusion'
}

# Use 'apply' with the mapping to replace numerical labels with descriptive names
subset_df['theme'] = subset_df['theme'].apply(lambda x: cluster_to_theme[x])

# Your DataFrame will now have a 'predicted_theme' column with descriptive names
subset_df['brand'] = 'Pepsi'
subset_df['industry'] = 'Food and Beverage'