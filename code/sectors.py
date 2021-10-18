import plotly.express as px
import dash
from datetime import date
from dash import html
from dash import dcc
import dash_daq as daq
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
from app import app
from data import all_stock_df

sectors_layout = html.Div(
    [
        # Dropdown row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Sectors"),
                        dcc.Dropdown(
                            id="dd-sector-multi",
                            multi=True,
                            value="",
                            options=[
                                {"label": stock, "value": stock}
                                for stock in all_stock_df["Symbol"].unique()
                            ],
                            clearable=False,
                        ),
                    ],
                    width=5,
                ),
                dbc.Col(
                    [
                        html.Label("Select Date Range"),
                        dcc.DatePickerRange(
                            id='date-picker-range-sector',
                            min_date_allowed=all_stock_df["Date"].min(),
                            max_date_allowed=all_stock_df["Date"].max(),
                            initial_visible_month=date.today(),
                            start_date=all_stock_df["Date"].min(),
                            end_date=all_stock_df["Date"].max()
                        )
                    ],
                    width=4,
                ),
                dbc.Button("Apply changes", color="info",
                           className="mr-1", id="btn-stock-run", style={"margin": "2rem"}),
            ],
            className="mt-4",

        ),
        # Candlestick graph row
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="graph-sector", figure={}),

                    ],
                    width=7),


                dbc.Col(
                    [
                        daq.Gauge(
                            style={"marginTop": "6rem"},
                            id='gauge-sector',
                            scale={"custom": {1: {"label": "Bearish"},
                                              3: {"label": "Bullish"}}},
                            label="Market Indicator",
                            value=0,
                            max=4,
                            min=0,
                            color={"gradient": True, "ranges": {
                                "red": [0, 1.33], "yellow":[1.33, 2.66], "green":[2.66, 4]}},
                        ),
                    ],
                    width=5),
            ]
        ),
        # radar chart row
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="funnel-sector", figure={})
                    ],
                    width=6),


                dbc.Col(
                    [
                        dcc.Graph(id="indicator-sector", figure={})
                    ],
                    width=6),
            ]
        ),
    ]
)
