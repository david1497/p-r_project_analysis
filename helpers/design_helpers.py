from dash import dcc

def generate_tab(tab_name, tab_label, tab_id, pg):
	tab = dcc.Tab(label=tab_label, value=tab_name, id=tab_id, children=[
				dcc.Link(pg['name'], href=f'{pg["relative_path"]}', className="btn btn-dark m-2 fs-5")
			])
	return tab