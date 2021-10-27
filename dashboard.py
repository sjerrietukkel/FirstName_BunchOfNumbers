import math
from numpy import average
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

df = pd.read_json("data/tweets_hash.json")
print(df)
sentiment = df["sentiment"]
fol = df["followers"]
app = dash.Dash(__name__)
fig = px.density_heatmap(df, x=sentiment, y=fol)

count = df["text"].count()
total_count = (count/1000) * 100
retweet_count = df["retweet"].mean()
retweet_count = math.ceil(retweet_count * 100)
male_count = df['gender'].value_counts(normalize=True).mul(100)
male_perc = math.ceil(male_count["male"])
average_followers = math.ceil((df["followers"].sum()) / count)


print(df["sentiment"])
app.layout = html.Div(
    children=[
        html.H1("Hi, my name is Firstname Bunchofnumbers, nice to meet you!"),
        html.H2("Select a #hashtag and I’ll tell you all about it. "),
        dcc.Input(
            id="search_input".format("search"),
            type="search",
            placeholder="e.g. coronapas".format("search")
        ),
        html.Div(className="flex-bar", children=[
            html.Div(className="flex-bar", children=[
                html.H3(str(total_count) + "%", className="red percentage"),
                html.H4("all retrieved tweets", className="percentage_expl"),
            ]),
            html.Div(className="flex-bar" ,children=[
                html.H3(str(retweet_count) + "%", className="red percentage"),
                html.H4("consists of retweets", className="percentage_expl"),
            ]),
            html.Div(className="flex-bar", children=[
                html.H3(str(male_perc) + "%", className="red percentage"),
                html.H4("is male", className="percentage_expl"),
            ]),
            html.Div(className="flex-bar", children=[
                html.H3(average_followers, className="red percentage"),
                html.H4("average followers", className="percentage_expl"),
            ]),
        ]),
        # html.Button(id='my-button', n_clicks=0, children="Search"),
        # dcc.Graph(id='graph-output', figure={}),
        dcc.Graph(id="heatmap", figure=fig)
    ]
)

@app.callback(
    Output(component_id='graph-output', component_property='figure'),
    # [Input(component_id='search_input', component_property='value')],
    [Input(component_id='my-button', component_property='n_clicks')],
    [State(component_id='search_input', component_property='value')],
    prevent_initial_call=True
)
def update_my_graph(n, val_chosen):
    if len(val_chosen) > 0:
        # print(n)
        print(f"value user chose: {val_chosen}")
        print(type(val_chosen))
        dff = df[df["fund_extended_name"].isin(val_chosen)]
        fig = px.pie(dff, values="ytd_return", names="fund_extended_name", title="Year-to-Date Returns")
        fig.update_traces(textinfo="value+percent").update_layout(title_x=0.5)
        return fig
    elif len(val_chosen) == 0:
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)