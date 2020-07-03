import dash  
import dash_core_components as dcc 
import dash_html_components as html  
from dash.dependencies import Input, Output
import yfinance 
import plotly.graph_objects as go 
from dash.exceptions import PreventUpdate


df = yfinance.download("MSFT", "2020-01-01", "2020-06-26")
df.reset_index(inplace=True)

def get_graph(v=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode="lines", x=df["Date"], y=df["Close"], name="Price"))

    if v=="mva10":
        df["SMA10"] = df["Close"].rolling(window=10, min_periods=1).mean()
        fig.add_trace(go.Scatter(mode="lines", x=df["Date"], y=df["SMA10"], name="SMA10"))
    elif v=="mva30":
        df["SMA30"] = df["Close"].rolling(window=30, min_periods=1).mean()
        fig.add_trace(go.Scatter(mode="lines", x=df["Date"], y=df["SMA30"], name="SMA30"))

    fig.update_layout(title={
        "text":"MSFT Close Price",
        "y":0.9,
        "x":0.5,
    })

    return fig


app = dash.Dash(external_stylesheets=["https://fonts.googleapis.com/css2?family=Notable&display=swap"])

app.layout = html.Div([
             html.H2(["Welcome to our dynamic dashboard !!"], className="title"), 
             html.Div([
                 dcc.Graph(figure=get_graph(), className="graph-01", id="graph"),
                 dcc.RadioItems(options=[
                     {"label":"Moving Average 10", "value":"mva10"},
                     {"label":"Moving Average 30", "value":"mva30"},
                 ], className="radio", id="radio-items")
             ], className="container")
])


@app.callback([Output("graph", "figure")],
              [Input("radio-items", "value")])
def on_radio_click(v):
    if v==None:
        raise PreventUpdate
    return [get_graph(v)]

app.run_server(debug=True)


