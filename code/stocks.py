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

stocks_layout = html.Div(
    [
        # Dropdown row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select sector"),
                        dcc.Dropdown(
                            id="dd-sector",
                            multi=False,
                            value="",
                            options=[
                                {"label": industry, "value": industry}
                                for industry in all_stock_df["Industry"].unique()
                            ],
                            clearable=False,
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.Label("Select stocks"),
                        dcc.Dropdown(
                            id="dd-stock",
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
                            id='date-picker-range',
                            min_date_allowed=all_stock_df["Date"].min(),
                            max_date_allowed=all_stock_df["Date"].max(),
                            initial_visible_month=date.today(),
                            start_date=all_stock_df["Date"].min(),
                            end_date=all_stock_df["Date"].max()
                        )
                    ],
                    width=4,
                ),
            ],
            className="mt-4",
        ),
        # Candlestick graph row
        dbc.Row(
            [

                dbc.Col(
                    [
                        dcc.Graph(id="stock_graph", figure={}),
                        dcc.Slider(
                            id='slider_moving_average',
                            min=1,
                            max=100,
                            step=1,
                            value=1,
                        ),
                        html.Div(id='slider-output-container',
                                 children="1", style={'textAlign': 'center'}),

                    ],
                    width=7),
                dbc.Col(
                    [
                        daq.ToggleSwitch(
                            label='Candle stick',
                            labelPosition='bottom'
                        ),
                        daq.ToggleSwitch(
                            label='Percent change',
                            labelPosition='bottom'
                        ),
                    ], width=1, style={'marginTop': '8rem'}),

                dbc.Col(
                    [
                        dcc.Graph(id="stock_graph", figure={})
                    ],
                    width=4),
            ]
        ),
        # Word chart row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            id="notification",
                            children="blwch",
                            style={"textAlign": "center"},
                        )
                    ],
                    width=12,
                )
            ]
        ),
    ]
)


# # pull data from twitter and create the figures
# @app.callback(
#     Output(component_id="myscatter", component_property="figure"),
#     Output(component_id="myscatter2", component_property="figure"),
#     Output(component_id="notification", component_property="children"),
#     Input(component_id="hit-button", component_property="n_clicks"),
#     State(component_id="count-mentions", component_property="value"),
#     State(component_id="input-handle", component_property="value"),
# )
# def display_value(nclicks, num, acnt_handle):
#     results = api.GetSearch(
#         raw_query=f"q=%40{acnt_handle}&src=typed_query&count={num}"
#     )       #       q=%40MoveTheWorld%20until%3A2021-08-05%20since%3A2021-01-01&src=typed_query

#     twt_followers, twt_likes, twt_count, twt_friends, twt_name = [], [], [], [], []
#     for line in results:
#         twt_likes.append(line.user.favourites_count)
#         twt_followers.append(line.user.followers_count)
#         twt_count.append(line.user.statuses_count)
#         twt_friends.append(line.user.friends_count)
#         twt_name.append(line.user.screen_name)

#         print(line)

#     d = {
#         "followers": twt_followers,
#         "likes": twt_likes,
#         "tweets": twt_count,
#         "friends": twt_friends,
#         "name": twt_name,
#     }
#     df = pd.DataFrame(d)
#     print(df.head())

#     most_followers = df.followers.max()
#     most_folwrs_account_name = df["name"][df.followers == most_followers].values[0]

#     scatter_fig = px.scatter(
#         df, x="followers", y="likes", trendline="ols", hover_data={"name": True}
#     )
#     scatter_fig2 = px.scatter(
#         df, x="friends", y="likes", trendline="ols", hover_data={"name": True}
#     )
#     message = f"The Twitter account that mentioned @{acnt_handle} from Jan-Aug of 2021 is called {most_folwrs_account_name} and it has the highest followers count: {most_followers} followers."

#     return scatter_fig, scatter_fig2, message
