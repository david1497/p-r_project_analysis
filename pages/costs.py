#%%
import dash
import plotly.graph_objs as go

dash.register_page(__name__, path='/costs', name='Costs')

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

costs_file = "/home/vadim/P&R data/04. Cost V Payments S4, S5, FR to end Sept '23.xlsx"
costs_df = pd.read_excel(costs_file)
grouped_by_ys = costs_df.groupby(['Year', 'Site']).agg(TotalMaterials=('Materials ', 'sum')).reset_index()
#%%

bar_chart_groups_ys = go.Figure()

# Iterate over unique years and sites to add bars
for year in grouped_by_ys['Year'].unique():
    df_year = grouped_by_ys[grouped_by_ys['Year'] == year]
    for site in grouped_by_ys['Site'].unique():
        df_site = df_year[df_year['Site'] == site]
        bar_chart_groups_ys.add_trace(go.Bar(x=[f'{year} - {site}'], y=[df_site['TotalMaterials'].sum()]))

# Update layout
bar_chart_groups_ys.update_layout(
    title='Total Materials by Year and Site',
    xaxis_title='Year - Site',
    yaxis_title='Total Materials'
)



layout = dbc.Container([
	dbc.Row([
        dbc.Col([
            dcc.Graph(figure=bar_chart_groups_ys)
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=bar_chart_groups_ys)
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=bar_chart_groups_ys)
        ], width=4),
        dbc.Col([
            dcc.Graph(figure=bar_chart_groups_ys)
        ], width=8)
    ])
])

# %%
