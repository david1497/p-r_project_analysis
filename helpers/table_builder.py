#%%
import dash
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc


manpower_s4 = pd.read_excel('/home/vadim/P&R data/01.Manpower Data/1 S4 Manpower.xlsx')
manpower_s5 = pd.read_excel('/home/vadim/P&R data/01.Manpower Data/2 S5 Manpower.xlsx')
manpower_fr = pd.read_excel('/home/vadim/P&R data/01.Manpower Data/3 FR Manpower.xlsx')


manpower_df = pd.concat([manpower_s4, manpower_s5, manpower_fr], ignore_index=True)
number_of_people_by_day = manpower_df.groupby(['Site','Date']).agg(
    n_people=('Person Name', 'count')
).reset_index()


def pick_color(val):
    c = ''
    if val < 40:
        c = '#eee562'
    elif 40 <= val <= 80:
        c = '#99e436'
    else:
        c = '#36e49b'
    
    return c


progress_per_project = {
    'S5':[40, 5, 'fa-solid fa-square-check', pick_color(40), '935.86K'], 
    'S4':[25, 7, 'fa-regular fa-hourglass-half', pick_color(25), '1 115.15K'], 
    'FR':[85, 10, 'fa-regular fa-triangle-exclamation', pick_color(85), '2 859.32K']
    }

#%%

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"
params = list(set(manpower_df['Site']))


def generate_metric_list_header():
    return generate_metric_row(
        "metric_header",
        {"id": "m_header_1", "children": html.Div("Project")},
        {"id": "m_header_2", "children": html.Div("Workers")},
        {"id": "m_header_3", "children": html.Div("Subby")},
        {"id": "m_header_4", "children": html.Div("Completness")},
        {"id": "m_header_5", "children": html.Div("State")},
        {"id": "m_header_6", "children": html.Div("Cost")},
    )


def generate_metric_row_helper(index):
    item = params[index]
    count_id = item + suffix_count
    ooc_percentage_id = item + suffix_ooc_n

    return generate_metric_row(
        f'one_row_id_{item}',
        {
            "id": f'project_name_{item}',
            "className": "metric-row-button-text",
            "children": html.H3(
                id=f'project_button_{item}',
                className="metric-row-button",
                children=item,
                title="Click to visualize live SPC chart",
                n_clicks=0,
            ),
        },
        {
            "id": f"sparkline_loc{item}",
            "children": dcc.Graph(
                id=f"sparkline_{item}",
                config={
                    "staticPlot": False,
                    "editable": False,
                    "displayModeBar": False,
                },
                figure=go.Figure({
                    "data": [{
                        "x": number_of_people_by_day.loc[number_of_people_by_day['Site']==item, "Date"].tolist(),
                        "y": number_of_people_by_day.loc[number_of_people_by_day['Site']==item, "n_people"],
                        "mode": "lines+markers",
                        "name": item,
                        "line": {"color": "#1897e0"},
                    }],
                    "layout": {
                        "uirevision": True,
                        "margin": dict(l=0, r=0, t=4, b=4, pad=0),
                        "xaxis": dict(
                            showline=False,
                            showgrid=False,
                            zeroline=False,
                            showticklabels=False,
                        ),
                        "yaxis": dict(
                            showline=False,
                            showgrid=False,
                            zeroline=False,
                            showticklabels=False,
                        ),
                        "paper_bgcolor": "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                    },
                }),
            ),
        },
        {"id": count_id, "children": progress_per_project[item][1]},
        {
            "id": f'progress_loc_{item}',
            "children": [
                dbc.Progress(
                    className=f'progress_bar_chart_{item}',
                    label=f"{progress_per_project[item][0]}%",
                    value=progress_per_project[item][0],
                    color=progress_per_project[item][-2],
                    id="animated-progress", 
                    animated=False, 
                    striped=True
                )
            ]
        },
        {"id": ooc_percentage_id, "children": [html.I(className=f"{progress_per_project[item][2]}")]},
        {"id": f'status_icon_{item}', "children": f"{progress_per_project[item][-1]} GBP"}
    )


def generate_metric_row(given_id, col1, col2, col3, col4, col5, col6):
    return dbc.Row(html.Div(
        id=given_id,
        className="row metric-row",
        children=[
            html.Div(
                id=f"project_name_{given_id}",
                className="one column",
                children=col1["children"],
            ),
            html.Div(
                id=f"n_workers_{given_id}",
                style={},
                className="one column",
                children=col2["children"],
            ),
            html.Div(
                id=f"n_subby_{given_id}",
                className="four columns",
                children=col3["children"],
            ),
            html.Div(
                id=f"progress_col_{given_id}",
                className="one column",
                children=col4["children"],
            ),
            html.Div(
                id=f"status_icon_{given_id}",
                className="three columns",
                children=col5["children"],
            ),
            html.Div(
                id=f"total_cost_{given_id}",
                className="one column",
                children=col6["children"],
            ),
        ],
    ))