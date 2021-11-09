import math
import pandas as pd
import plotly.express as px
import dash
from dash.exceptions import PreventUpdate
import json 
import glob
from dash import dcc
import plotly.graph_objects as go
from dash import html
from dash.dependencies import Input, Output, State
app = dash.Dash(__name__)
server = app.server


def merge_JsonFiles(): # Merge all data files in to one
    total_tweet_count = 0
    result = list()
    for filename in glob.iglob('data/*.json', recursive=True):
        total_tweet_count = total_tweet_count + 1000
        with open(filename, 'r') as infile:
            result.extend(json.load(infile))
    with open('combined_data/combined_tweets.json', 'w') as output_file:
        json.dump(result, output_file)
    return total_tweet_count
totaltweets = merge_JsonFiles()

df = pd.read_json("combined_data/combined_tweets.json")


def merge_JsonFiles_all(): # Merge all data files in to one
    total_tweet_count = 0
    result = list()
    for filename in glob.iglob('data_all/*.json', recursive=True):
        total_tweet_count = total_tweet_count + 1000
        with open(filename, 'r') as infile:
            result.extend(json.load(infile))
    with open('combined_data/combined_full_tweets_all.json', 'w') as output_file:
        json.dump(result, output_file)
    return total_tweet_count
totaltweets_all = merge_JsonFiles_all()

df_all = pd.read_json('combined_data/combined_full_tweets_all.json')

print(df_all["sentiment"].agg('mean'))
print(df["sentiment"].agg('mean'))

# remove follower outliers https://stackoverflow.com/questions/35827863/remove-outliers-in-pandas-dataframe-using-percentiles
cols = ['followers']
Q1 = df[cols].quantile(0)
Q3 = df[cols].quantile(0.9)
IQR = Q3 - Q1
df_fol = df[~((df[cols] < (Q1 - 1.5 * IQR)) |(df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

sentiment = df_fol["sentiment"]
fol = df_fol["followers"]

df_sen_avg = df.groupby(["query", "gender"],)["sentiment"].agg(["mean", "count"]).reset_index()

fig = px.density_heatmap(
            df,
            x=sentiment,
            y=fol,
            nbinsx= 20,
            nbinsy= 20,
            marginal_x="box",   
            marginal_y="violin",
            color_continuous_scale= ["#1d2330", "#4aa189",  "#298f71","#2cfcc4"]
)

fig_pie = px.pie(df, values = "sentiment", names="query")
fig_hist = px.histogram(df_sen_avg, x="mean", y="count", color="gender", color_discrete_sequence=["#2cfcc4", "#FD5445"])
fig_ding = px.histogram(df_sen_avg, x="mean", y="count", color="gender", color_discrete_sequence=["#2cfcc4", "#FD5445"])

fig.update_layout(
    plot_bgcolor='rgba(4,161,137, .2)',
    paper_bgcolor='white',
    xaxis =  {'showgrid': False },
    yaxis = {'showgrid': False}
)


# Create QUERY list for populating dcc.Dropdown()
QUERY = []
for o in df["query"]:
    QUERY.append(o)
QUERY = list(dict.fromkeys(QUERY))


# Create list for populating comparison chart
QUERY_COMPARISON = []
for o in df_all["query"]:
    QUERY_COMPARISON.append(o)
QUERY_COMPARISON = list(dict.fromkeys(QUERY_COMPARISON))


# top bar information about the entire dataset
count = df["screen_name"].count()
total_count = round((count/totaltweets) * 100, 1)
retweet_count = df["retweet"].mean()
retweet_count = math.ceil(retweet_count * 100)
male_count = df['gender'].value_counts(normalize=True).mul(100)
male_perc = math.ceil(male_count["male"])
average_followers = math.ceil((df["followers"].sum()) / count)


app.layout = html.Div(
    className="main",
    children=[
        html.Div(className="white-1", children=[
            html.H1("Hi, my name is Firstname Bunchofnumbers, nice to meet you!"),
            html.P("This project is meant to give an insight into the phenomenon FirstName BunchOfNumbers (FB's) on Twitter. When creating an account this will be the default username generated, making it the prime choice for people with negative outings and bots alike. "),
            html.P("Caveats to take into consideration: The data is retrieved from Dutch Twitters users and the script will only detect Dutch first names scraped from http://www.naamkunde.net/. The sample data below was gathered amidst the Covid-19 pandemic during October 2021."),
            html.H3("Stack used:", className="tech"),
            html.Div(className="flexbar", children=([
                html.P("Python", className="tag"),
                html.P("Pandas.py", className="tag"),
                html.P("Plotly", className="tag"),
                html.P("Dash", className="tag"),
                html.P("Twitter API", className="tag"),
                html.P("Google Natural Languages API", className="tag"),
                html.P("Heroku", className="tag"),
            ])),
        ]),
        html.H2("Information about all retreived tweets:", className="information-bar"),
        html.Div(className="flex-bar", children=[
            html.Div(className="flex-bar perc-back", children=[
                html.H3(str(total_count) + "%", className="red percentage"),
                html.H4("all retrieved tweets", className="percentage_expl"),
            ]),
            html.Div(className="flex-bar perc-back" ,children=[
                html.H3(str(retweet_count) + "%", className="red percentage"),
                html.H4("consists of retweets", className="percentage_expl"),
            ]),
            html.Div(className="flex-bar perc-back", children=[
                html.H3(str(male_perc) + "%", className="red percentage"),
                html.H4("first name is male", className="percentage_expl"),
            ]),
            html.Div(className="flex-bar perc-back", children=[
                html.H3(average_followers, className="red percentage"),
                html.H4("average followers", className="percentage_expl"),
            ]),
            html.Div(className="flex-bar perc-back", children=[
                html.H3(totaltweets, className="red percentage"),
                html.H4("tweets scanned", className="percentage_expl"),
            ]),
        ]),
        html.Div(className="flex-bar1", children=([
            html.Div(className="w50", children=([
                    html.H2("Detailed information about a #hashtag"),
            html.Div(className="white", children=[
                html.H2("Select a hashtag:"),
                dcc.Dropdown(
                    id="indiv",
                    options= [{'label': option, 'value': option} # loop over QUERY list for population
                    for option in QUERY],
                ),
                html.P("Sentiment ranges from: -1 <-> -.5 = very negative, -.5 <-> -.2 = negative, -.2 <-> .2 = neutral, .2 <-> .5 = positive, .5 <-> 1 = very positive."),
                dcc.Graph(
                    id="fig_ding",
                    figure=fig_ding,
                    className="graph"
                ),
                html.P(" ** For generating data based on hashtags of your choice please check out the README.md file over on https://github.com/sjerrietukkel/FirstName_BunchOfNumbers"),
        ]),    
            ])),
            html.Div(className="w50", children=([
                html.H2("Compare hashtag with all results"),
                html.Div(className="white", children=[
                    html.Div(className="flex-bar-between", children=[
                        html.Div(className="w50x", children=[
                            html.H2("Select a hashtag:"),
                            dcc.Dropdown( 
                                id="search_input",
                                options= [{'label': option, 'value': option} # loop over QUERY list for population
                                for option in QUERY_COMPARISON],
                            ),
                        ]),
                    ]),
                    html.P("Sentiment ranges from: -1 <-> -.5 = very negative, -.5 <-> -.2 = negative, -.2 <-> .2 = neutral, .2 <-> .5 = positive, .5 <-> 1 = very positive."),
                    dcc.Graph(
                        id="fig_hist",
                        figure=fig_hist,
                        className="graph"
                    ),
                    html.P(" ** Comparison not available for all retrieved hashtags, due to technical issues. Values are shown in percentages, 50 tweets retrieved from all."),
                ]),
            ])),
        ])),
        html.Div(className="w100", children=[
                html.H2("Sentiment compared with amount of followers."),
                html.Div(className="white", children=([
                    dcc.Graph(
                        id="heatmap",
                        className="graph",
                        figure=fig,
                    ),
                    html.P("** Taken from complete sample size"),
                ])),
        ]),
        html.Footer(className="footert", children=[
            html.P("Daniel van der Schuur, 1811230", className="center")
        ]),
    ]
)

@app.callback(
    Output("fig_hist", "figure"),
    Input("search_input", "value"), 
)

def updateFigure(value):
    ctx = dash.callback_context
    if not ctx.triggered:
        print("")
    df_query = df[df["query"] == value]
    df_query1 = df_all[df_all["query"] == value]
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=df_query["sentiment"],
        histnorm='percent',
        name="FB's", # name used in legend and hover labels
        xbins=dict( # bins used for histogram
            start=-1.0,
            end=1.0,
            size=0.1
        ),
        marker_color='#FD5445',
        opacity=0.75
    ))
    fig_hist.add_trace(go.Histogram(
        x=df_query1["sentiment"],
        histnorm='percent',
        name="All Tweets", # name used in legend and hover labels
        xbins=dict( # bins used for histogram
            start=-1.0,
            end=1.0,
            size=0.1
        ),
        marker_color='#2cfcc4',
        opacity=0.75
    ))
    fig_hist.update_layout(
        plot_bgcolor='rgba(4,161,137, .2)',
    )
    return fig_hist

@app.callback(
    Output("fig_ding", "figure"),
    Input("indiv", "value")
)


def update_graphding(value):
    df_query = df[df["query"] == value]
    graph_ding = px.histogram(df_query, x='sentiment', color='gender', range_x=[-1, 1], nbins=20, pattern_shape="retweet",color_discrete_sequence=["#2cfcc4", "#FD5445"],)
    graph_ding.update_layout(
        plot_bgcolor='rgba(4,161,137, .2)',
        paper_bgcolor='white',
        xaxis = {'showgrid': False},
        yaxis = {'showgrid': False},
    )
    return graph_ding


if __name__ == '__main__':
    app.run_server(debug=True)

