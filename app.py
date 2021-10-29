import math
from numpy import average
import pandas as pd
import plotly.express as px
import dash
import json
import glob
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
colorscales = px.colors.named_colorscales()

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
Q3 = df[cols].quantile(0.8)
IQR = Q3 - Q1

df_fol = df[~((df[cols] < (Q1 - 1.5 * IQR)) |(df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

print(df_fol["followers"])
print(df)
sentiment = df_fol["sentiment"]
fol = df_fol["followers"]
app = dash.Dash(__name__)
fig = px.density_heatmap(
            df,
            title="Sentiment compared with amount of followers.",
            x=sentiment,
            y=fol,
            nbinsx= 20,
            nbinsy= 20,
            marginal_x="box",
            marginal_y="violin",
            color_continuous_scale= [ "#004369","#F4E683", "#FDA649",  "#FF8882","#fd5445"]
)

fig.update_layout(
    plot_bgcolor='ghostwhite',
)


# top bar information about the entire dataset
count = df["screen_name"].count()
total_count = round((count/totaltweets) * 100, 1)
retweet_count = df["retweet"].mean()
retweet_count = math.ceil(retweet_count * 100)
male_count = df['gender'].value_counts(normalize=True).mul(100)
male_perc = math.ceil(male_count["male"])
average_followers = math.ceil((df["followers"].sum()) / count)


print(df["sentiment"])
app.layout = html.Div(
    className="main",
    children=[
        html.H1("Hi, my name is Firstname Bunchofnumbers, nice to meet you!"),
        html.H2("Select a #hashtag and I’ll tell you all about it. "),
        dcc.Dropdown(
            id="search_input",
            options= [
                {'label': "Coronapas", 'value': 'coronapas'},
                {'label': "Onana", 'value': 'onana'},
                {'label': "Coronamaatregelen", 'value': 'coronamaatregelen'},
                {'label': "Nieuwsuur", 'value': 'nieuwsuur'},
            ],
            value="coronapas"
        ),
        html.H4("Information about all retreived tweets :", className="information-bar"),
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
        dcc.Graph(
            id="heatmap",
            className="graph-style",
            figure=fig,
        ),
    ]
)

@app.callback(
    Output("genre-graph", "figure"),
    [Input("search_input", "value")]
)
def updateFigure(value):
    df_platform = df[df["Platform"] == value]
    df_genres = df_platform.groupby("Genre").size().reset_index(name="Count")
    fig_genre = px.pie(df_genres, values = "Count", names="Genre", title="Fancy Title")
    return fig_genre


if __name__ == '__main__':
    app.run_server(debug=True)