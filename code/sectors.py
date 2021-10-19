import plotly.express as px
from datetime import date
from dash import html
from dash import dcc
import dash_daq as daq
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from data import all_stock_df, industries
from app import app

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
                            value=list(industries.keys()),
                            options=[
                                {"label": stock, "value": stock}
                                for stock in all_stock_df["Industry"].unique()
                            ],
                            clearable=False,
                        ),
                    ],
                    width=6,
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
                dbc.Col([
                    dbc.Button("Apply changes", color="info",
                               className="mr-1", id="btn-stock-run", style={"margin": "2rem"}
                               )
                ], width=2)
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
                    width=8),


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
                    width=4),
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


@app.callback(
    Output(component_id="graph-sector", component_property="figure"),
    # Output(component_id="gauge-sector", component_property="value"),
    # Output(component_id="funnel-sector", component_property="figure"),
    # Output(component_id="indicator-sector",
    #        component_property="figure"),
    Input(component_id="btn-stock-run",
          component_property="n_clicks"),
    State(component_id="dd-sector-multi", component_property="value"),
    State(component_id="date-picker-range-sector",
          component_property="start_date"),

    State(component_id="date-picker-range-sector",
          component_property="end_date"),
    prevent_initial_call=True
)
def on_apply_changes(n_clicks, industries, start_date, end_date):
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)
    # Sector Graph
    selected_industry_df = all_stock_df.loc[all_stock_df["Industry"].isin(
        industries)]
    selected_industry_df = selected_industry_df.loc[(selected_industry_df["Date"] >= start_datetime) & (
        selected_industry_df["Date"] <= end_datetime)]
    sector_df = all_stock_df.groupby(["Industry", "Date"]).mean()
    sector_fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Sectors"), shapes=[dict(
            x0=date, x1=date, y0=0, y1=1, xref='x', yref='paper',
            line_width=2) for date in selected_industry_df.drop_duplicates('Prime minister', keep="first")["Date"]],
        annotations=[dict(
            x=data[1]["Date"], y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text=data[1]["Prime minister"]) for data in selected_industry_df.drop_duplicates('Prime minister', keep="first").iterrows()]
    ))
    for industry in industries:
        data = sector_df.loc[industry].reset_index()
        data["Date"] = data["Date"].dt.strftime('%Y-%m-%d')
        sector_fig.add_trace(go.Scatter(x=data["Date"], y=data["Percent change"],
                                        mode='lines',
                                        name=industry))
    sector_fig.update_xaxes(rangeslider_visible=True)
    # sector_fig = px.line(sector_df, title="Sectors", x="Date", y="Close", color="Symbol",
    #                      line_group="Industry", hover_name="Industry", line_shape="spline", render_mode="svg")
    # for data in date_wise_mean_df.drop_duplicates('Prime minister', keep="first").iterrows():
    #     sector_fig.add_annotation(x=data[1]["Date"], y=0.05,
    #                               text=data[1]["Prime minister"],)
    # sector_fig.update_xaxes(rangeslider_visible=True)

    # # Gauge chart
    # perc_change_start = date_wise_mean_df.loc[date_wise_mean_df["Date"] ==
    #                                           start_datetime, "Percent change"]
    # perc_change_end = date_wise_mean_df.loc[date_wise_mean_df["Date"] ==
    #                                         end_datetime, "Percent change"]
    # gauge_value = 3 if perc_change_end > perc_change_start else 1
    # Radar chart
    # radar_fig = go.Figure()
    # radar_categories = selected_industry_df["Finance minister"].unique()
    # for stock in stocks:
    #     radar_fig.add_trace(go.Scatterpolar(
    #         r=selected_industry_df.loc[selected_industry_df["Symbol"]
    #                                    == stock].groupby(by="Finance minister").mean()["Percent change"],
    #         theta=radar_categories,
    #         fill='toself',
    #         name=stock
    #     ))
    # Indicators

    # data_dict = {"Symbol": [], "Initial close": [], "Final close": []}

    # for stock in stocks:
    #     data_dict["Symbol"].append(stock)
    #     stock_df = selected_industry_df.loc[selected_industry_df["Symbol"] == stock]
    #     data_dict["Initial close"].append(stock_df.iloc[0]["Close"])
    #     data_dict["Final close"].append(stock_df.iloc[-1]["Close"])
    # data_df = pd.DataFrame.from_dict(data_dict)
    # data_df["Diff"] = data_df["Final close"] - data_df["Initial close"]
    # data_df = data_df.sort_values(by=["Diff"])

    # indicator_fig = go.Figure()
    # indicator_fig.add_trace(go.Indicator(
    #     mode="number+delta",
    #     value=data_df.iloc[-1]["Final close"],
    #     title={"text": "{}<br><span style='font-size:0.8em;color:gray'>Best performing Stock</span>".format(
    #         data_df.iloc[-1]["Symbol"])},
    #     delta={'reference': data_df.iloc[-1]
    #            ["Initial close"], 'relative': True},
    #     domain={'x': [0.5, 1], 'y': [0, 0.5]},))

    # indicator_fig.add_trace(go.Indicator(
    #     mode="number+delta",
    #     value=data_df.iloc[0]["Final close"],
    #     title={"text": "{}<br><span style='font-size:0.8em;color:gray'>Worst performing Stock</span>".format(
    #         data_df.iloc[0]["Symbol"])},

    #     delta={'reference': data_df.iloc[0]
    #            ["Initial close"], 'relative': True},
    #     domain={'x': [0.5, 1], 'y': [0.5, 1]},))

    return sector_fig
    # , gauge_value
    # radar_fig, indicator_fig
