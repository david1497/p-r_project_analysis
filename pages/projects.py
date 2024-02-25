#%%
import dash
import plotly.graph_objs as go

dash.register_page(__name__, path='/', name='Projects')

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from helpers.table_builder import generate_metric_list_header, generate_metric_row_helper, generate_metric_row

costs_payments_df = pd.read_excel("/home/vadim/P&R data/04. Cost V Payments S4, S5, FR to end Sept '23.xlsx")
costs_per_project = costs_payments_df.groupby('Site').agg(
    total_materials=('Materials ','sum'),
    total_labour=('Labout Tot', 'sum'),
    total_plant=('Plant', 'sum')
).reset_index()

cost_types = {
    'total_materials':'Materials', 
    'total_labour':'Labour', 
    'total_plant':'Plant'
}

custom_colors = ['#f087b8f3',  # Red
              '#5fe6c8f3',  # Green
              '#078cdaf3'   # Blue
             ]

pie_charts = []
for k, v in cost_types.items():
    # Create the pie chart
    trace = go.Pie(
        labels=costs_per_project['Site'], 
        values=costs_per_project[k],
        marker=dict(colors=custom_colors, line=dict(color='#FFFFFF', width=2)))

    # Create pie chart layout
    layout = go.Layout(title=f'Cost of {v}')
    # Create figure
    pie_chart = go.Figure(data=[trace], layout=layout)
    pie_charts.append(pie_chart)
#-------------------- Done with piecharts



layout = html.Div(children=[
    html.Br(),
    dbc.Row(children=[
        dbc.Col(children=[
            dcc.Slider(
                id='my-slider',
                min=0,
                max=10,
                step=1,
                value=5,  # Initial value
                marks={i: str(i) for i in range(11)}  # Marks for slider values
            ),
            html.Div(id='slider-output')  # Display selected value
        ],
        width=5),
        dbc.Col(children=[
            dcc.Slider(
                id='my-slider',
                min=0,
                max=10,
                step=1,
                value=5,  # Initial value
                marks={i: str(i) for i in range(11)}  # Marks for slider values
            ),
            html.Div(id='slider-output')  # Display selected value
        ],
        width=7)
    ]),
    html.Br(),
	dbc.Row([
        dbc.Col(width=1),
        dbc.Col(id='one_row_metrics',
            children=[html.Div(
                id="metric-div",
                children=[
                    generate_metric_list_header(),
                    html.Div(
                        id="metric-rows",
                        children=[
                            generate_metric_row_helper(0),
                            generate_metric_row_helper(1),
                            generate_metric_row_helper(2),
                        ]
                    )
                ]
            )],
            width=10
        ),
        dbc.Col(width=1)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='pie-chart_0',
                figure=pie_charts[0]
            )
        ], width=4),
        dbc.Col([
            dcc.Graph(
                id='pie-chart_1',
                figure=pie_charts[1]
            )
        ], width=4),
        dbc.Col([
            dcc.Graph(
                id='pie-chart_2',
                figure=pie_charts[2]
            )
        ], width=4)
    ])
])
# %%
