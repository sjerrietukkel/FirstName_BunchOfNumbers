import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

df = pd.read_json("data/tweets_hash.json")
sentiment = df["sentiment"]
fol = df["followers"]
app = dash.Dash(__name__)
fig = px.density_heatmap(df, x=sentiment, y=fol)

print(df["sentiment"])
app.layout = html.Div(
    children=[
        dcc.Input(
            id="search_input".format("search"),
            type="search",
            placeholder="e.g. coronapas".format("search")
        ),
        html.Button(id='my-button', n_clicks=0, children="Search"),
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