#%%
import dash

dash.register_page(__name__, path='/subby', name='Subby')

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


layout = dbc.Container([
	dbc.Row([
        dbc.Col([
            html.H1("Plot Area1")
        ], width=6),
        dbc.Col([
            html.H1("Plot Area2")
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.H1("Plot Area3")
        ], width=4),
        dbc.Col([
            html.H1("Plot Area4")
        ], width=8)
    ])
])