# BrandGuard

## Overview
This project focuses on analyzing social media sentiment and predicting virality, particularly in the context of brand campaigns. Our case study revolves around Pepsi's Kendall Jenner campaign of April 2017. We scraped 30,000 tweets from this period using APIFY and analyzed them to understand sentiment dynamics and virality factors.
### Prototype:

<img width="569" alt="Screenshot 2023-12-05 at 3 11 22 PM" src="https://github.com/arianab68/BrandGuard/assets/70418227/796d8b37-fb78-4c16-adbd-4d9a28fb97c1">
<br>

## Demo

### UI
https://github.com/arianab68/BrandGuard/assets/70418227/19349d2e-04f5-4308-9c86-2a5cb1d8d63a

### Alerting System

https://github.com/arianab68/BrandGuard/assets/70418227/6b8f6ec2-8465-49bb-9777-0f4327a35b48

## Features

### Data Collection

**Source:** Twitter, via APIFY

**Period:** April 4th to 6th, 2017

**Scope:** Tweets related to Pepsi's campaign

**Format:** Raw JSON data

### Data Cleaning and Preprocessing
**Conversion:** Raw JSON to DataFrame via Pandas

**Feature Selection:** Dropped irrelevant columns, retained essential features

**Null Handling:** Created replace_nulls function for imputation

**Preprocessing for Model Training:** Removal of URLs, special characters, case normalization

### Sentiment Model Pipeline
Our goal is to predict the sentiment of these tweets within the timeframe of a “negative” brand campaign. We want to use these sentiments to pipeline into our virality model to predict the potential of negative tweets going viral in a specific time period. For sentiment analysis, sophisticated deep learning models like BERT (Bidirectional Encoder Representations from Transformers) are highly effective because they can understand the context of a word in a sentence, which is great for sentiment analysis. 

**Objective:** Predict tweet sentiments during a negative campaign

**BERT Model:** Used for deep sentiment analysis

**Tweet Embedding and Clustering:** Utilized BERT for embeddings, clustered with K-means

**Sentiment Analysis on Clusters:** VADER for sentiment scores

### Virality Model
For our virality model, the goal is to understand what are the factors that make tweets go viral. For example, engagement metrics such as retweets, likes and comments, all play a factor on a tweet's visibility, thus increasing the opportunity for the tweet to go viral. Using our dataset of 30k tweets, we created an algorithm that took assigned scores for the weights of retweets, likes, comments, and computed a virality score based on that. 

We looked at the averages of likes, retweets, comments, and assigned a weighted scoring system based on how impactful the feature is in correlation with engagement. We determined the scores for each of these features by creating a correlation matrix between tweets that had a “negative” sentiment prediction and each feature. From this, we analyzed which features represented an indicator of higher engagement and assigned those features a higher score.  We then used all these weights to calculate a ‘Virality Score’ threshold based on our understanding of what constitutes 'virality' within our dataset. Lastly, we created a function that takes in our algorithm and model. 

**Aim:** Identify factors contributing to tweet virality

**Features:** Engagement metrics

**Model:** Gradient Boosting Classifier

**Algorithm:** Weighed scoring system based on engagement metrics 

### UI
Our goal is to create some sort of UI (like a dashboard) that can allow for near real-time monitoring of tweets that are flagged to go viral. In our version of this tool, we are not ingesting data in real time, instead we are using a curated dataset. But, ultimately for a future iteration that would be the goal.

**Framework:** Flask with Dash for interactive visualizations

**Deployment:** Hosted on Heroku

### Alerting System
A crucial component of the UI is an integrated monitoring system that sends email alerts to stakeholders regarding tweets that go above a certain threshold of virality. Using our virality algorithm and the thresholds and scores we defined earlier that constitutes ‘virality’, we wrote a script to send automated alerts to stakeholders whenever we see something that has the potential to blow up. The goal of doing this is to ensure the effectiveness of our product, because quite frankly no stakeholder is going to constantly monitor this dashboard and look for anomalies. This is why incorporating an alerting system plays in the foundation of our tool.

**Functionality:** Automated email alerts for high virality potential tweets

**Implementation:** Python script using SMTP for email dispatch

## Interpretation and Analysis
In evaluating our project aimed at predicting and preventing negative viral social media campaigns against brands, several aspects of our approach come into play. Firstly, our data collection and analysis centered on a large dataset of 30,000 tweets from the Pepsi Kendall Jenner campaign, providing a solid foundation to understand campaign dynamics. However, for predictive accuracy, a more diverse dataset encompassing various brands and campaign types would be advantageous.

Our use of BERT for sentiment analysis was an industry recommended choice, ensuring precise interpretation of public sentiments. The virality model, with its focus on engagement metrics and user profiles, is crucial in understanding how tweets gain momentum based off of engagement metric. However, for proactive prediction, we will need more than historical data analysis,  we will need to incorporate real-time monitoring and early warning indicators  for more robustness (which was not technically or economically feasible at this stage).

The process of combining sentiment data with engagement metrics in our feature engineering and model training was vital. However, to effectively prevent negative campaigns we would need to explore beyond Twitter. Looking at predictive indicators or signs of a campaign turning negative through other outlets would enhance our model's preventative capabilities.

Our decision to develop a real-time, interactive dashboard using Flask and Dash was instrumental for ongoing campaign monitoring. This platform would be key in early detection, but it requires real-time data ingestion and automated alert systems for real prevention.

Deploying this tool on Heroku and maintaining a feedback loop ensures continuous improvement. However, integrating the tool with a brand's social media monitoring systems and including a rapid response mechanism would make it more effective in preventing negative campaigns.

In conclusion, while our project successfully tackles the analysis of negative social media campaigns and offers insights into public sentiment and virality, there is room for enhancement. Specifically, incorporating a broader dataset, real-time monitoring, and integrated response mechanisms would significantly boost our tool's ability to predict and prevent negative viral campaigns against brands.



