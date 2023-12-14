import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from flask import Flask
from themes import subset_df

#DROPDOWNS
date_options = [{'label': date, 'value': date} for date in subset_df['timestamp'].dropna().unique()]
industry_options = [{'label': industry, 'value': industry} for industry in subset_df['industry'].dropna().unique()]
brand_options = [{'label': brand, 'value': brand} for brand in subset_df['brand'].dropna().unique()]

#STAT CARDS
average_sentiment_score = subset_df['score'].mean()
percentage_viral_tweets = (subset_df['is_viral'].sum() / len(subset_df)) * 100

card_style = {
    'border': '1px solid #ddd',
    'borderRadius': '5px',  # Rounded corners
    'padding': '20px',
    'margin': '10px 0',  # Margin for top and bottom
    'textAlign': 'center',
    'backgroundColor': 'black',
    'boxShadow': '2px 2px 2px lightgrey',  # Simple shadow
    'color': 'white'
}

#SCORE BARS
max_sentiment_score = subset_df['score'].max()
max_virality_score = subset_df['virality_score'].max()

# Generate a horizontal bar chart for average sentiment score
fig_sentiment_score_bar = go.Figure(go.Indicator(
    mode="gauge+number",
    value=average_sentiment_score,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Sentiment"},
    gauge={
        'axis': {'range': [None, max_sentiment_score]},
        'bar': {'color': 'green' if average_sentiment_score > 0 else 'red'},
    }
))

# Generate a horizontal bar chart for percentage of viral tweets
fig_virality_score_bar = go.Figure(go.Indicator(
    mode="gauge+number",
    value=percentage_viral_tweets,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Virality"},
    gauge={
        'axis': {'range': [None, 100]},  # Assuming the virality is a percentage
        'bar': {'color': 'green' if percentage_viral_tweets > 0 else 'red'},
    }
))

#GUAGE CHART
average_virality_score = subset_df['virality_score'].mean()

#TWEET FEED
dff = subset_df.copy()
# Define sentiment colors
sentiment_colors = {
    'POSITIVE': 'green',
    'NEGATIVE': 'red'
}
fig_tweet_feed = px.scatter(
    subset_df,
    x='timestamp',
    y='tweets',
    color='sentiment',
    color_discrete_map= sentiment_colors,  # Use the defined sentiment colors
    size='score',
    title='Tweet Feed',
    height=300  # Set the height of the scatter plot
)

# Update the layout of the bar chart
fig_tweet_feed.update_layout(
    title='Tweet Feed',
    xaxis_title='Date',
    yaxis_title='Tweets',
    plot_bgcolor='white',  # Set the background color to white
    showlegend=False,  # Hide the legend if not required
    xaxis=dict(showgrid=False),  # Hide the x-axis grid lines
    yaxis=dict(showgrid=False)  # Hide the y-axis grid lines
)

#THEMES
# Assuming 'theme' is a column in subset_df
#theme_counts = subset_df['theme'].value_counts()

theme_colors = subset_df['sentiment'].map({'POSITIVE': 'green', 'NEGATIVE': 'red'}).tolist()

fig_theme_bar = go.Figure(data=[
    go.Bar(
        x=subset_df['theme'].value_counts().index,
        y=subset_df['theme'].value_counts().values,
        marker_color=theme_colors  # Set the color of the bars based on sentiment
    )
])

# Update the layout of the bar chart
fig_theme_bar.update_layout(
    title='Distribution of Themes',
    xaxis_title='Theme',
    yaxis_title='Count',
    plot_bgcolor='white',  # Set the background color to white
    showlegend=False,  # Hide the legend if not required
    xaxis=dict(showgrid=False),  # Hide the x-axis grid lines
    yaxis=dict(showgrid=False)  # Hide the y-axis grid lines
)

# Create a Dash application
external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    # Header
    html.Header(style={'backgroundColor': 'black', 'padding': '10px'}, children=[
        # Logo and title
        html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
            # Regression line icon (using a placeholder image as an example)
            html.Img(src='assets/logo.png', style={'height': '30px', 'marginRight': '10px'}),
            # Title
            html.H1('BrandGuard', style={'color': 'white', 'fontSize': '36px', 'margin': '0'})
        ]),
    ]),
    # Dropdowns row
    html.Div(className='top-dropdown', children=[
        # Industry dropdown with label
        html.Div(className='top-dropdown-inner', children=[
            html.Label('Select Industry', style={'color': 'black'}),
            dcc.Dropdown(
                id='industry-dropdown',
                options=industry_options,
                value=industry_options[0]['value'] if industry_options else None,
                placeholder="Industry",
                style={'color': 'white'}
            ),
        ]),
        # Brand dropdown with label
        html.Div(className='top-dropdown-inner', children=[
            html.Label('Select Brand', style={'color': 'black'}),
            dcc.Dropdown(
                id='brand-dropdown',
                options=brand_options,
                value=brand_options[0]['value'] if industry_options else None,
                placeholder="Brand",
                style={'color': 'white'}
            ),
        ]),
        # Date dropdown with label
        html.Div(className='top-dropdown-inner', children=[
            html.Label('Select Date', style={'color': 'black'}),
            dcc.Dropdown(
                id='date-dropdown',
                options=date_options,
                value=date_options[0]['value'] if date_options else None,
                placeholder="Date",
                style={'color': 'white'}
            ),
        ]),
    ]),
    # Graph section
    html.Div([
        dcc.Graph(
            id='sentiment-trend-chart',
            figure={
                'data': [
                    # Positive sentiment bars
                    go.Bar(
                        x=subset_df.timestamp,
                        y=subset_df[subset_df['sentiment'] == "POSITIVE"]['score'],
                        name='Positive',
                        marker=dict(color='green')
                    ),
                    # Negative sentiment bars
                    go.Bar(
                        x=subset_df.timestamp,
                        y=-subset_df[subset_df['sentiment'] == "NEGATIVE"]['score'],
                        name='Negative',
                        marker=dict(color='red')
                    ),
                ],
                'layout': go.Layout(
                    title='Sentiment Analysis Trend',
                    xaxis=dict(title='Date'),
                    yaxis=dict(title='Level of Sentiment', range=[-1, 1]),
                    hovermode='closest'
                ), 
                
            }
        ),
         # Row for pie chart and stat cards
        html.Div(style={'display': 'flex'}, children=[
        dcc.Graph(
            id='sentiment-pie-chart',
            style={'width': '50%'}, 
            figure={
                'data': [
                    go.Pie(
                        labels=['Positive', 'Negative'],
                        values=[
                            subset_df[subset_df['sentiment'] == "POSITIVE"]['score'].count(),
                            subset_df[subset_df['sentiment'] == "NEGATIVE"]['score'].count()
                        ],
                        marker=dict(colors=['green', 'red']),
                        hoverinfo='label+percent',
                        textinfo='value'
                    )
                ],
                'layout': go.Layout(
                    title='Sentiment Distribution'
                )
            }
        ),
        # Gauge chart for Virality Score
            dcc.Graph(
                id='virality-gauge-chart',
                style={'width': '50%'}, 
                figure={
                    'data': [
                        go.Indicator(
                            mode='gauge+number',
                            value=average_virality_score,
                            title={'text': 'Virality Score'},
                            gauge={
                                'axis': {'range': [None, subset_df['virality_score'].max()]},
                                'steps': [
                                    {'range': [0, subset_df['virality_score'].quantile(0.25)], 'color': 'lightgray'},
                                    {'range': [subset_df['virality_score'].quantile(0.25), subset_df['virality_score'].quantile(0.5)], 'color': 'gray'},
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': average_virality_score}
                            }
                        )
                    ]
                }
            )
        ]),
       html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}, children=[
    # Container for score cards and bar chart side by side
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'width': '100%'}, children=[
        # Container for the Average Sentiment Score card and bar
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            html.Div([
                html.H3('Average Sentiment Score'),
                html.P(f'{average_sentiment_score:.2f}', style={'color': 'green' if average_sentiment_score > 0 else 'red'}),
            ], style=card_style),
            dcc.Graph(figure=fig_sentiment_score_bar, config={'displayModeBar': False})  # Hide the modebar of the plot
        ]),
        # Container for the Percentage of Viral Tweets card and bar
        html.Div(style={'width': '50%', 'padding': '10px'}, children=[
            html.Div([
                html.H3('Percentage of Viral Tweets'),
                html.P(f'{percentage_viral_tweets:.2f}%', style={'color': 'green' if percentage_viral_tweets > 0 else 'red'}),
            ], style=card_style),
            dcc.Graph(figure=fig_virality_score_bar, config={'displayModeBar': False})  # Hide the modebar of the plot
        ]),
    ]),
     html.Div(style={'width': '100%', 'padding': '10px'}, children=[
                dcc.Graph(
                    id='theme-bar-chart',
                    figure=fig_theme_bar
                )
            ]),
        ]),
        # Container for the Tweet feed plot underneath the score cards and bar chart
        html.Div(style={'width': '100%', 'padding': '10px'}, children=[
            dcc.Graph(
                id='tweet-feed-plot',
                figure=fig_tweet_feed
            )
        ])
    ])
])



if __name__ == '__main__':
    app.run_server(debug=True)
