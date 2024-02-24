#%%
import dash
from dash import Input, Output, State, html, dcc
import dash_labs as dl
import dash_bootstrap_components as dbc

from helpers.design_helpers import generate_tab
# %%


app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

navbar = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(children=
                    [html.A('Projects', href='/', id='a_main')],
                    id="tab_projects"
                ),
                dbc.Col(children=
                    [html.A('Costs', href='/costs', id='a_costs')],
                    id="tab_costs"
                ),
                dbc.Col(children=
                    [html.A('Employees', href='/employees', id='a_employees')],
                    id="tab_employees"
                ),
                dbc.Col(children=
                    [html.A('Subby', href='/subby', id='a_subby')],
                    id="tab_subby"
                ),
                dbc.Button(html.Span([
                        html.I(className="bi bi-slider", style=dict(display='inline-block')), '<'
                    ]),
                    n_clicks=0,
                    id="open-offcanvas"
                ),
                dbc.Offcanvas([
                    html.H1('Filter 1'),
                    html.H1('Filter 2'),
                    html.H1('Filter 3'),
                    html.H1('Filter 4'),
                    html.H1('Filter 5')
                ], 
                id='offcanvas',
                placement='end'
            )
            ]
        )
    ]
)



app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True
)


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open




if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.2")



