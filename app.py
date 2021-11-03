import math
import pandas as pd
import plotly.express as px
import dash
from dash.exceptions import PreventUpdate
import json 
import glob
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
app = dash.Dash(__name__)
server = app.server


def merge_JsonFiles():
    total_tweet_count = 0
    result = list()
    for filename in glob.iglob('data/*.json', recursive=True):
        total_tweet_count = total_tweet_count + 1000
        with open(filename, 'r') as infile:
            result.extend(json.load(infile))
    with open('all_tweets.json', 'w') as output_file:
        json.dump(result, output_file)
    return total_tweet_count
totaltweets = merge_JsonFiles()

df = pd.read_json("all_tweets.json")

# remove follower outliers
cols = ['followers'] # one or more

Q1 = df[cols].quantile(0)
Q3 = df[cols].quantile(0.9)
IQR = Q3 - Q1

df_fol = df[~((df[cols] < (Q1 - 1.5 * IQR)) |(df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# print(df_fol["followers"])
# print(df)
sentiment = df_fol["sentiment"]
fol = df_fol["followers"]

df_sen_avg = df
# df_temp = df.groupby('query').size().to_frame('count')
# df_temp = df_temp.iloc[1:, :]
# print(df_temp)
df_sen_avg = df_sen_avg.groupby(["query", "gender"],)["sentiment"].agg(["mean", "count"]).reset_index()
# df_sen_avg["count"] = df_temp["count"]


# s = df_temp['item_id'].map(df_item.set_index('item_id')['item_name'])
# df = df_bill.drop('item_id', 1).assign(item_name = s)


# print(df_sen_avg)
# print(df_gen_avg)
# print("hierboven")

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
            html.P("This project is meant to give an insight into the phenomenon FirstName BunchOfNumbers on Twitter. When creating an account this will be the default username generated, making it the prime choice for people with negative outings and bots alike. "),
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
        html.H2("Information about all retreived tweets :", className="information-bar"),
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
        # html.Button(id='my-button', n_clicks=0, children="Search"),
        # dcc.Graph(id='graph-output', figure={}),
        html.Div(className="flex-bar1", children=([
            html.Div(className="w50", children=([
                html.H2("Sentiment compared with amount of followers."),
                html.Div(className="white", children=([
                    dcc.Graph(
                        id="heatmap",
                        className="graph",
                        figure=fig,
                    ),
                    html.P("** Taken from complete sample size"),
                ])),
            ])),
            html.Div(className="w50", children=([
                html.H2("Select a #hashtag and I’ll tell you all about it. "),
                html.Div(className="white", children=[
                    dcc.Dropdown(
                        id="search_input",
                        options= [{'label': option, 'value': option}
                        for option in QUERY],
                    ),
                    html.P("Sentiment ranges from: -1 <-> -.5 = very negative, -.5 <-> -.2 = negative, -.2 <-> .2 = neutral, .2 <-> .5 = positive, .5 <-> 1 = very positive."),
                    dcc.Graph(
                        id="fig_hist",
                        figure=fig_hist,
                        className="graph"
                    ),
                    html.P(" ** For generating data based on hashtags of your choice please check out the README.md file over on https://github.com/sjerrietukkel/FirstName_BunchOfNumbers"),
                ]),
            ])),
        ])),
    ]
)

@app.callback(
    Output("fig_hist", "figure"),
    [Input("search_input", "value")]
)
def updateFigure(value):
    df_query = df[df["query"] == value]
    print(df_query)
    df_q_count = df_query.groupby("query").count().reset_index()
    print(df_q_count)
    df_sen_avg = df_query.groupby(["query", "gender"])["sentiment"].agg([ "count"]).reset_index()
    # print(df_sen_avg)
    fig_hist = px.histogram(df_query, x='sentiment', color='gender', range_x=[-1, 1], nbins=20, pattern_shape="retweet",color_discrete_sequence=["#2cfcc4", "#FD5445"])
    fig_hist.update_layout(
        plot_bgcolor='rgba(4,161,137, .2)',
        paper_bgcolor='white',
        xaxis = {'showgrid': False},
        yaxis = {'showgrid': False},
    )
    return fig_hist

 
if __name__ == '__main__':
    app.run_server()