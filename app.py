import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# Font Awesome CDN
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Sidebar
sidebar = html.Div(
    [
        html.A([html.I(className="fas fa-home"), html.Span(" Home")], href="#"),
        html.A([html.I(className="fas fa-map-marker-alt"), html.Span(" Maps/Hot")], href="#"),
        html.A([html.I(className="fas fa-chart-line"), html.Span(" Trends & Analysis")], href="#"),
        html.A([html.I(className="fas fa-lightbulb"), html.Span(" Recommendation")], href="#"),
    ],
    className="sidebar"
)

# Load dataset
# For Phase 1, you can use dummy numbers if dataset not ready
high_risk_districts = 12
avg_stunting_rate = 32.5  # %
predicted_risk = 28.0     # %
total_children_affected = 250000

# Cards
cards = html.Div(
    [
        html.Div([html.I(className="fas fa-exclamation-triangle"),
                  html.Div(f"{high_risk_districts}", className="metric"),
                  html.Div("High-Risk Districts", className="description")], className="card"),
        html.Div([html.I(className="fas fa-chart-bar"),
                  html.Div(f"{avg_stunting_rate}%", className="metric"),
                  html.Div("Average Stunting Rate", className="description")], className="card"),
        html.Div([html.I(className="fas fa-bolt"),
                  html.Div(f"{predicted_risk}%", className="metric"),
                  html.Div("Predicted Risk (2-3 Years)", className="description")], className="card"),
        html.Div([html.I(className="fas fa-users"),
                  html.Div(f"{total_children_affected}", className="metric"),
                  html.Div("Children Affected", className="description")], className="card")
    ],
    className="cards-container"
)

# Quick insights
quick_insights = html.Div(
    [
        html.H3("Quick Insights"),
        html.Ul([
            html.Li("Eastern and Southern districts show highest risk of hidden hunger."),
            html.Li("Poverty and low crop yields are main contributing factors.")
        ])
    ],
    className="quick-insights"
)

# Main content
main_content = html.Div(
    [
        html.Div([html.H1("NutriMap Rwanda – Fighting Hidden Hunger"),
                  html.P("Mapping and Predicting Malnutrition Across Rwanda")], className="header"),
        cards,
        quick_insights,
        html.P("Click cards to navigate to Map / Trends / Recommendation pages.")
    ],
    className="main-content"
)

# Layout
app.layout = html.Div([sidebar, main_content])

if __name__ == "__main__":
    app.run(debug=True)
