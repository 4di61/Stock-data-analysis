import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
from app import app

# Connect to the layout and callbacks of each tab
from stocks import stocks_layout
from sectors import sectors_layout


app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Stocks", tab_id="tab-stocks",
                        labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Sectors", tab_id="tab-sectors",
                        labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-stocks",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Sectorwise Stock Trends",
                            style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])

])


@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-stocks":
        return stocks_layout
    elif tab_chosen == "tab-sectors":
        return sectors_layout
    return html.P("Welcome")


if __name__ == '__main__':
    app.run_server(debug=True)
