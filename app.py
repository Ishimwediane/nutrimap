# app.py
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Dummy data for testing frontend
df = pd.DataFrame({
    "Year": [2015, 2016, 2017, 2018, 2019],
    "Value": [10, 20, 15, 25, 30]
})

# Create Dash app
app = dash.Dash(__name__)

# Layout: what the user sees
app.layout = html.Div([
    html.H1("My First Dashboard", style={"textAlign": "center"}),

    # Graph
    dcc.Graph(
        id="test-graph",
        figure=px.line(df, x="Year", y="Value", title="Dummy Data Trend")
    )
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
