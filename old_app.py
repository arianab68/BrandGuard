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


"""Simulated Data"""
data = {
    'date': pd.date_range(start='1/1/2021', periods=30, freq='D'),
    'positive': np.random.rand(30),
    'negative': np.random.rand(30) * -1  # Negative sentiment is represented as negative values
}

df = pd.DataFrame(data)

data2 = [
    {'Rank': 1, 'Keywords/Hashtags': 'sustainability', 'Virality Rate': '90%', 'Companies Affected': 'General Motors', 'Alert': True},
    {'Rank': 2, 'Keywords/Hashtags': 'plastic', 'Virality Rate': '75%', 'Companies Affected': 'Nestle, Unilever', 'Alert': True},
    {'Rank': 3, 'Keywords/Hashtags': 'lowwages', 'Virality Rate': '72%', 'Companies Affected': 'NIKE', 'Alert': False},
    {'Rank': 4, 'Keywords/Hashtags': 'diversity', 'Virality Rate': '71%', 'Companies Affected': 'Pepsi', 'Alert': False},
    {'Rank': 5, 'Keywords/Hashtags': 'equalpay', 'Virality Rate': '65%', 'Companies Affected': 'Amazon, Tesla', 'Alert': False},
]

# Calculate trend lines - Trend Graph
positive_trend = np.poly1d(np.polyfit(range(len(df.date)), df.positive, 1))(range(len(df.date)))
negative_trend = np.poly1d(np.polyfit(range(len(df.date)), df.negative, 1))(range(len(df.date)))

# Calculate the sum of positive and negative sentiments for the pie chart - Pie Chart
total_positive = df.positive.sum()
total_negative = df.negative.sum()
total_negative = abs(total_negative)

# Placeholder stats data
num_comments = 1780
num_users = 5000
comments_percentage_change = 5  # Placeholder percentage change
users_percentage_change = -3    # Placeholder percentage change

overall_sentiment_score = 3.8
industry_base_score = 4.0

"""Simulated Data"""

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
            #html.Img(src='flask/images.png', style={'height': '30px', 'marginRight': '10px'}),
            # Title
            html.H1('BrandGuard', style={'color': 'white', 'fontSize': '36px', 'margin': '0'})
        ])
    ]),
   # Dropdowns row
    html.Div(className='top-dropdown', children=[
        # Industry dropdown with label
        html.Div(className='top-dropdown-inner', children=[
            html.Label('Select Industry', style={'color': 'black'}),
            dcc.Dropdown(
                id='industry-dropdown',
                options=[
                    {'label': 'Food & Beverages', 'value': 'FB'},
                    # ... other industry options
                ],
                value='FB',  # Default value
                placeholder="Industry",
                className='top-dropdown-inner-inner'
            ),
        ]),
        # Brand dropdown with label
        html.Div(className='top-dropdown-inner', children=[
            html.Label('Select Brand', style={'color': 'black'}),
            dcc.Dropdown(
                id='brand-dropdown',
                options=[
                    {'label': 'Pepsi', 'value': 'PE'},
                    # ... other brand options
                ],
                value='PE',  # Default value
                placeholder="Brand",
                style={'color': 'black'}
            ),
        ]),
        # Date dropdown with label
        html.Div(className='top-dropdown-inner', children=[
            html.Label('Select Date', style={'color': 'black'}),
            dcc.Dropdown(
                id='date-dropdown',
                options=[
                    {'label': '2021', 'value': '2021'},
                    # ... other date options
                ],
                value='2021',  # Default value
                placeholder="Date",
                style={'color': 'blue'}
            ),
        ]),
    ]),
    html.Div([
    dcc.Graph(
        id='sentiment-trend-chart',
        figure={
            'data': [
                # Positive sentiment bars
                go.Bar(
                    x=df.date,
                    y=df.positive,
                    name='Positive',
                    marker=dict(color='green')
                ),
                # Negative sentiment bars
                go.Bar(
                    x=df.date,
                    y=df.negative,
                    name='Negative',
                    marker=dict(color='red')
                ),
                # Positive sentiment trend line
                go.Scatter(
                    x=df.date,
                    y=positive_trend,
                    mode='lines',
                    name='Positive Trend',
                    line=dict(color='green', width=2)
                ),
                # Negative sentiment trend line
                go.Scatter(
                    x=df.date,
                    y=negative_trend,
                    mode='lines',
                    name='Negative Trend',
                    line=dict(color='red', width=2)
                )
            ],
            'layout': go.Layout(
                title='Sentiment Analysis Trend',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Level of Sentiment', range=[-1, 1]),
                hovermode='closest'
            ),
            
        }
    )
]),
html.Div([
    # Parent container for the pie chart and any other content
    html.Div(style={'display': 'flex', 'flexDirection': 'row'}, children=[
        # Container for the pie chart
        html.Div(style={'width': '50%'}, children=[
            dcc.Graph(
                id='sentiment-pie-chart',
                figure={
                    'data': [
                        go.Pie(
                            labels=['Positive', 'Negative'],
                            values=[total_positive, total_negative],
                            marker=dict(colors=['green', 'red']),
                            hoverinfo='label+percent',
                            textinfo='value'
                        )
                    ],
                    'layout': go.Layout(
                        title='Sentiment Distribution',
                        showlegend=True
                    )
                }
            ),
        ]),
        # Container for stat cards
        html.Div(style={'width': '50%', 'display': 'flex', 'flexDirection': 'column'}, children=[
            # Stat card for comments
            html.Div(style={'border': '1px solid #ddd', 'padding': '10px', 'margin': '5px', 'textAlign': 'center', 'backgroundColor': 'white'}, children=[
                html.P('Comments Mentioning the Brand'),
                html.H3(f'{num_comments}'),
                html.P(f'{comments_percentage_change:+}%', style={'color': 'green' if comments_percentage_change > 0 else 'red'}),
            ]),
            # Stat card for users
            html.Div(style={'border': '1px solid #ddd', 'padding': '10px', 'margin': '5px', 'textAlign': 'center', 'backgroundColor': 'white'}, children=[
                html.P('Users Mentioning the Brand'),
                html.H3(f'{num_users}'),
                html.P(f'{users_percentage_change:+}%', style={'color': 'green' if users_percentage_change > 0 else 'red'}),
    ]),
    # Sentiment score bar with numbers
    html.Div(style={'marginBottom': '20px'}, children=[
        html.P('Overall Sentiment Score'),
        html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
            html.Span('0', style={'marginRight': '5px'}),
            html.Div(style={'border': '1px solid #000', 'width': '100%', 'height': '30px', 'position': 'relative'}, children=[
                html.Div(style={
                    'width': f'{(overall_sentiment_score / 5) * 100}%',
                    'backgroundColor': 'red',
                    'height': '100%',
                    'color': 'black',
                    'textAlign': 'center',
                    'lineHeight': '30px',
                    'backgroundImage': 'repeating-linear-gradient(-45deg, white, white 10px, gray 10px, gray 20px)'  # striped effect
                }, children=str(overall_sentiment_score))
            ]),
            html.Span('5', style={'marginLeft': '5px'}),
        ])
    ]),

    # Industry base score bar with numbers
    html.Div(style={'marginBottom': '20px'}, children=[
        html.P('Industry Base'),
        html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
            html.Span('0', style={'marginRight': '5px'}),
            html.Div(style={'border': '1px solid #000', 'width': '100%', 'height': '30px', 'position': 'relative'}, children=[
                html.Div(style={
                    'width': f'{(industry_base_score / 5) * 100}%',
                    'backgroundColor': 'red',
                    'height': '100%',
                    'color': 'black',
                    'textAlign': 'center',
                    'lineHeight': '30px',
                    'backgroundImage': 'repeating-linear-gradient(-45deg, white, white 10px, gray 10px, gray 20px)'  # striped effect
                }, children=str(industry_base_score))
            ]),
            html.Span('5', style={'marginLeft': '5px'}),
        ])
            ]),
        html.Div([
            html.Div(style={'flex': '3', 'flexDirection': 'column'}, children=[
                # Left-aligned table
                html.Div(style={'flex': '1'}, children=[
                    html.Span('5', style={'marginLeft': '5px'}),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in subset_df.columns],
                        data= subset_df.to_dict('records'),
                        style_cell={'textAlign': 'center', 'padding': '10px'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                        filter_action='native',
                        sort_action='native',
                        page_size=10
                    ), 
                    # Place other components here
                ]),
            ]),

    ])
    ])
    ])
    ])
    ])


# @app.callback(
#     Output( 'sentiment_', 'data2'),
#     Input('table', 'data')
# )

def display_click_data(clickData):
    if clickData is None:
        return 'Click on a bar to see details'
    else:
        # You can extract and use click data as needed here
        sentiment = clickData['points'][0]['y']
        return f'You clicked a bar with sentiment level: {sentiment}'
    
def update_output(timestamp, rows):
    if timestamp is None:
        raise PreventUpdate
    # Add logic to handle alert changes if necessary
    return rows


if __name__ == '__main__':
    app.run_server(debug=True)
