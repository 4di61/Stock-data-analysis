import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
print(px.data.stocks)
df_stock = pd.read_csv(
    'D:\Documents\College docs\Sem III\Mini project\code\ADANIPORTS.csv', encoding='utf-8')

data = df_stock['Date'], ((df_stock['Close'] -
                          df_stock['Open'])/df_stock['Open']*100)

data_frame = pd.DataFrame(data)
fig = px.line(data)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=data)
])

if __name__ == '__main__':
    app.run_server(debug=True)
