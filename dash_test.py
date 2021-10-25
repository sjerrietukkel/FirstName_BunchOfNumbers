import dash
from dash.html.Title import Title
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import numpy as np

np.random.seed(50)
x_rand = np.random.randint(1,61,60)
y_rand = np.random.randint(1,61,60)


app = dash.Dash()
# app.layout = html.Div([
#     html.H1("Hello World!"),
#     html.Div("Dash - a Data product development framework."),

#     dcc.Graph(
#         id = 'samplechart',
#         figure = {
#             'data' : [
#                 {'x' : [4,6,8], 'y' :[12,14,16], 'type': 'bar', 'name': 'first char'},
#                 {'x' : [4,6,8], 'y' :[20,22,6], 'type': 'bar', 'name': 'second char'}
#             ],
#             'layout' : {
#                 'title' : 'simple bar chart',
#             }
#         }
#     )
# ])


# app.layout = html.Div([
#     dcc.Graph(
#         id="scatter_chart",
#         figure = {
#             'data' : [
#                 go.Scatter(
#                     x = x_rand,
#                     y = y_rand,
#                     mode = 'markers'
#                 )
#             ],
#             'layout' : go.Layout(
#                 title = "Scatterplot "
#             )
#         }
#     )
# ])


app.layout = html.Div([
    html.Label('Choose a city : '),
    dcc.Dropdown(
        id = 'first-dropdown',
        options = [
            {'label' : 'San Francisco', 'value' : 'sf'},
            {'label' : 'New York City', 'value' : 'nyc'},
            {'label' : 'Spakenburg', 'value' : 'spa'},
        ],
        value= 'spa',
        multi = True,
    )
])

app.run_server(port = 4050)