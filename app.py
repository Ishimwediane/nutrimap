import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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

# Sample data for visualizations
provinces_data = pd.DataFrame({
    'Province': ['Eastern', 'Western', 'Southern', 'Northern', 'Kigali'],
    'Stunting_Rate': [38.2, 35.1, 36.8, 33.5, 28.9],
    'Poverty_Rate': [42.1, 38.5, 40.2, 35.8, 22.3],
    'Population': [2800000, 2600000, 2900000, 1900000, 1300000]
})

# Time series data
years = list(range(2015, 2026))
trend_data = pd.DataFrame({
    'Year': years,
    'Stunting_Rate': [42.5, 41.8, 40.2, 38.9, 37.5, 36.2, 35.0, 33.8, 32.5, 31.2, 30.0],
    'Predicted': [None]*6 + [35.0, 33.8, 32.5, 31.2, 30.0]
})

# District risk data
district_data = pd.DataFrame({
    'District': ['Bugesera', 'Nyagatare', 'Gatsibo', 'Kayonza', 'Ngoma', 
                 'Kirehe', 'Rwamagana', 'Huye', 'Gisagara', 'Nyaruguru',
                 'Kamonyi', 'Muhanga'],
    'Risk_Level': ['High', 'High', 'High', 'High', 'High', 
                   'High', 'Medium', 'High', 'High', 'High',
                   'High', 'High'],
    'Stunting_Rate': [41.2, 40.5, 39.8, 38.9, 38.5, 
                      37.9, 34.5, 37.2, 36.8, 39.1,
                      36.5, 37.8]
})

# Sidebar
sidebar = html.Div([
    html.Div([
        html.I(className="fas fa-leaf", style={'fontSize': '32px', 'color': '#4CAF50'}),
        html.H2("NutriMap", style={'margin': '10px 0 5px 0', 'fontSize': '22px'}),
        html.P("Rwanda", style={'margin': '0', 'fontSize': '14px', 'opacity': '0.8'})
    ], style={'textAlign': 'center', 'padding': '30px 20px', 'borderBottom': '1px solid rgba(255,255,255,0.1)'}),
    
    html.Div([
        html.A([
            html.I(className="fas fa-home", style={'marginRight': '12px', 'width': '20px'}),
            html.Span("Overview")
        ], href="#", className="nav-link active", id="nav-overview"),
        
        html.A([
            html.I(className="fas fa-map-marked-alt", style={'marginRight': '12px', 'width': '20px'}),
            html.Span("Hotspot Map")
        ], href="#", className="nav-link", id="nav-map"),
        
        html.A([
            html.I(className="fas fa-chart-line", style={'marginRight': '12px', 'width': '20px'}),
            html.Span("Trends & Analysis")
        ], href="#", className="nav-link", id="nav-trends"),
        
        html.A([
            html.I(className="fas fa-lightbulb", style={'marginRight': '12px', 'width': '20px'}),
            html.Span("Recommendations")
        ], href="#", className="nav-link", id="nav-recommendations"),
        
        html.A([
            html.I(className="fas fa-info-circle", style={'marginRight': '12px', 'width': '20px'}),
            html.Span("About")
        ], href="#", className="nav-link", id="nav-about"),
    ], style={'padding': '20px 0'})
], className="sidebar")

# Header with filters
header = html.Div([
    html.Div([
        html.Div([
            html.H1("Rwanda at a Glance", style={'margin': '0', 'fontSize': '28px', 'fontWeight': '600'}),
            html.P("Fighting Hidden Hunger - Where Rwanda Stands Today", 
                   style={'margin': '5px 0 0 0', 'color': '#718096', 'fontSize': '14px'})
        ]),
        html.Div([
            html.Div([
                html.Label("Time Period:", style={'marginRight': '10px', 'fontSize': '14px'}),
                dcc.Dropdown(
                    id='year-filter',
                    options=[{'label': str(y), 'value': y} for y in range(2015, 2026)],
                    value=2023,
                    clearable=False,
                    style={'width': '120px', 'marginRight': '15px'}
                ),
            ], style={'display': 'inline-block'}),
            html.Div([
                html.Label("Region:", style={'marginRight': '10px', 'fontSize': '14px'}),
                dcc.Dropdown(
                    id='region-filter',
                    options=[{'label': 'All Regions', 'value': 'all'}] + 
                            [{'label': p, 'value': p} for p in provinces_data['Province']],
                    value='all',
                    clearable=False,
                    style={'width': '150px'}
                ),
            ], style={'display': 'inline-block'})
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})
], className="header")

# KPI Cards
kpi_cards = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H3("32.5%", style={'margin': '0', 'fontSize': '32px', 'fontWeight': '700', 'color': '#2D3748'}),
                html.P("Stunting Rate Avg", style={'margin': '5px 0', 'fontSize': '13px', 'color': '#718096'}),
                html.Div([
                    html.I(className="fas fa-arrow-down", style={'fontSize': '10px', 'marginRight': '4px'}),
                    html.Span("4.8%", style={'fontSize': '12px', 'fontWeight': '600'})
                ], style={'color': '#48BB78', 'display': 'flex', 'alignItems': 'center'}),
                html.Span("Δ 2023 vs 2015", style={'fontSize': '11px', 'color': '#A0AEC0'})
            ], style={'flex': '1'}),
            html.Div([
                html.I(className="fas fa-child", style={'fontSize': '42px', 'color': '#E6F2FF', 'opacity': '0.6'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ], className="kpi-card"),
    
    html.Div([
        html.Div([
            html.Div([
                html.H3("6.8/10", style={'margin': '0', 'fontSize': '32px', 'fontWeight': '700', 'color': '#2D3748'}),
                html.P("Food Security Index", style={'margin': '5px 0', 'fontSize': '13px', 'color': '#718096'}),
                html.Div([
                    html.I(className="fas fa-arrow-up", style={'fontSize': '10px', 'marginRight': '4px'}),
                    html.Span("0.4%", style={'fontSize': '12px', 'fontWeight': '600'})
                ], style={'color': '#48BB78', 'display': 'flex', 'alignItems': 'center'}),
                html.Span("Δ 2024 vs 2018", style={'fontSize': '11px', 'color': '#A0AEC0'})
            ], style={'flex': '1'}),
            html.Div([
                html.I(className="fas fa-apple-alt", style={'fontSize': '42px', 'color': '#FFF5E6', 'opacity': '0.6'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ], className="kpi-card"),
    
    html.Div([
        html.Div([
            html.Div([
                html.H3("42.1%", style={'margin': '0', 'fontSize': '32px', 'fontWeight': '700', 'color': '#2D3748'}),
                html.P("Agricultural Participation", style={'margin': '5px 0', 'fontSize': '13px', 'color': '#718096'}),
                html.Div([
                    html.I(className="fas fa-arrow-down", style={'fontSize': '10px', 'marginRight': '4px'}),
                    html.Span("2.3%", style={'fontSize': '12px', 'fontWeight': '600'})
                ], style={'color': '#F56565', 'display': 'flex', 'alignItems': 'center'}),
                html.Span("Δ 2023 vs 2015", style={'fontSize': '11px', 'color': '#A0AEC0'})
            ], style={'flex': '1'}),
            html.Div([
                html.I(className="fas fa-tractor", style={'fontSize': '42px', 'color': '#E6FFE6', 'opacity': '0.6'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ], className="kpi-card"),
    
    html.Div([
        html.Div([
            html.Div([
                html.H3("12.9M", style={'margin': '0', 'fontSize': '32px', 'fontWeight': '700', 'color': '#2D3748'}),
                html.P("Total Population", style={'margin': '5px 0', 'fontSize': '13px', 'color': '#718096'}),
                html.Div([
                    html.I(className="fas fa-arrow-up", style={'fontSize': '10px', 'marginRight': '4px'}),
                    html.Span("0.9%", style={'fontSize': '12px', 'fontWeight': '600'})
                ], style={'color': '#4299E1', 'display': 'flex', 'alignItems': 'center'}),
                html.Span("Δ 2023 vs 2015", style={'fontSize': '11px', 'color': '#A0AEC0'})
            ], style={'flex': '1'}),
            html.Div([
                html.I(className="fas fa-users", style={'fontSize': '42px', 'color': '#F5E6FF', 'opacity': '0.6'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ], className="kpi-card"),
], className="kpi-container")

# Charts section
charts_section = html.Div([
    # Row 1
    html.Div([
        # Provincial comparison
        html.Div([
            html.Div([
                html.H3("Stunting Rate by Province", style={'margin': '0 0 15px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                html.P("Showing data for all provinces (% children under 5)", style={'fontSize': '13px', 'color': '#718096', 'margin': '0 0 20px 0'})
            ]),
            dcc.Graph(id='province-chart', config={'displayModeBar': False})
        ], className="chart-card", style={'flex': '1'}),
        
        # Trend over time
        html.Div([
            html.Div([
                html.H3("Has there been any significant change?", style={'margin': '0 0 15px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                html.P("Trend analysis with predictions", style={'fontSize': '13px', 'color': '#718096', 'margin': '0 0 20px 0'})
            ]),
            dcc.Graph(id='trend-chart', config={'displayModeBar': False})
        ], className="chart-card", style={'flex': '1'}),
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),
    
    # Row 2
    html.Div([
        # High risk districts
        html.Div([
            html.Div([
                html.H3("High-Risk Districts", style={'margin': '0 0 15px 0', 'fontSize': '16px', 'fontWeight': '600'}),
                html.P("Districts with stunting rates above 35%", style={'fontSize': '13px', 'color': '#718096', 'margin': '0 0 20px 0'})
            ]),
            dcc.Graph(id='districts-chart', config={'displayModeBar': False})
        ], className="chart-card", style={'flex': '2'}),
        
        # Key insights
        html.Div([
            html.H3("Key Insights", style={'margin': '0 0 20px 0', 'fontSize': '16px', 'fontWeight': '600'}),
            html.Div([
                html.Div([
                    html.I(className="fas fa-exclamation-triangle", 
                           style={'color': '#F56565', 'fontSize': '20px', 'marginRight': '12px'}),
                    html.Div([
                        html.P("12 districts", style={'margin': '0', 'fontWeight': '600', 'fontSize': '15px'}),
                        html.P("classified as high-risk for malnutrition", 
                               style={'margin': '0', 'fontSize': '13px', 'color': '#718096'})
                    ])
                ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                
                html.Div([
                    html.I(className="fas fa-chart-line", 
                           style={'color': '#48BB78', 'fontSize': '20px', 'marginRight': '12px'}),
                    html.Div([
                        html.P("28% improvement", style={'margin': '0', 'fontWeight': '600', 'fontSize': '15px'}),
                        html.P("in stunting rates since 2015, with continued decline predicted", 
                               style={'margin': '0', 'fontSize': '13px', 'color': '#718096'})
                    ])
                ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                
                html.Div([
                    html.I(className="fas fa-map-marker-alt", 
                           style={'color': '#4299E1', 'fontSize': '20px', 'marginRight': '12px'}),
                    html.Div([
                        html.P("Eastern Province", style={'margin': '0', 'fontWeight': '600', 'fontSize': '15px'}),
                        html.P("shows highest concentration of malnutrition hotspots", 
                               style={'margin': '0', 'fontSize': '13px', 'color': '#718096'})
                    ])
                ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                
                html.Div([
                    html.I(className="fas fa-seedling", 
                           style={'color': '#ED8936', 'fontSize': '20px', 'marginRight': '12px'}),
                    html.Div([
                        html.P("Agricultural factors", style={'margin': '0', 'fontWeight': '600', 'fontSize': '15px'}),
                        html.P("Poverty and low crop yields are primary drivers of malnutrition", 
                               style={'margin': '0', 'fontSize': '13px', 'color': '#718096'})
                    ])
                ], style={'display': 'flex', 'alignItems': 'flex-start'})
            ])
        ], className="chart-card", style={'flex': '1'})
    ], style={'display': 'flex', 'gap': '20px'})
], style={'marginTop': '20px'})

# Main content
main_content = html.Div([
    header,
    kpi_cards,
    charts_section
], className="main-content")

# Layout
app.layout = html.Div([sidebar, main_content], style={'display': 'flex'})

# Callbacks
@callback(
    Output('province-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_province_chart(region):
    df = provinces_data.copy()
    if region != 'all':
        df = df[df['Province'] == region]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Province'],
        y=df['Stunting_Rate'],
        marker_color=['#4299E1' if p == region or region == 'all' else '#CBD5E0' for p in df['Province']],
        text=df['Stunting_Rate'].apply(lambda x: f'{x}%'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Stunting Rate: %{y}%<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=40),
        height=280,
        showlegend=False,
        xaxis=dict(showgrid=False, showline=True, linecolor='#E2E8F0'),
        yaxis=dict(showgrid=True, gridcolor='#F7FAFC', range=[0, 45])
    )
    
    return fig

@callback(
    Output('trend-chart', 'figure'),
    Input('year-filter', 'value')
)
def update_trend_chart(selected_year):
    fig = go.Figure()
    
    # Historical data
    historical = trend_data[trend_data['Year'] <= 2023].copy()
    fig.add_trace(go.Scatter(
        x=historical['Year'],
        y=historical['Stunting_Rate'],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#4299E1', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Stunting Rate: %{y}%<extra></extra>'
    ))
    
    # Predicted data
    predicted = trend_data[trend_data['Year'] >= 2023].copy()
    fig.add_trace(go.Scatter(
        x=predicted['Year'],
        y=predicted['Predicted'],
        mode='lines+markers',
        name='Predicted',
        line=dict(color='#48BB78', width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond'),
        hovertemplate='<b>%{x}</b><br>Predicted: %{y}%<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=40),
        height=280,
        showlegend=True,
        legend=dict(orientation='h', yanchor='top', y=-0.15, xanchor='center', x=0.5),
        xaxis=dict(showgrid=False, showline=True, linecolor='#E2E8F0'),
        yaxis=dict(showgrid=True, gridcolor='#F7FAFC', range=[25, 45])
    )
    
    return fig

@callback(
    Output('districts-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_districts_chart(region):
    df = district_data[district_data['Risk_Level'] == 'High'].sort_values('Stunting_Rate', ascending=True)
    
    colors = ['#F56565' if rate > 39 else '#ED8936' if rate > 37 else '#ECC94B' for rate in df['Stunting_Rate']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['District'],
        x=df['Stunting_Rate'],
        orientation='h',
        marker_color=colors,
        text=df['Stunting_Rate'].apply(lambda x: f'{x}%'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Stunting Rate: %{x}%<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=120, r=20, t=20, b=40),
        height=400,
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='#F7FAFC', range=[0, 45]),
        yaxis=dict(showgrid=False, showline=False)
    )
    
    return fig

# CSS Styles
app.index_string = app.index_string.replace('</head>', '''
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #F7FAFC;
    color: #2D3748;
}

.sidebar {
    width: 70px;
    background: linear-gradient(180deg, #2C5282 0%, #2B6CB0 100%);
    color: white;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    overflow: hidden;
    box-shadow: 4px 0 12px rgba(0,0,0,0.1);
    transition: width 0.25s ease;
}

.sidebar:hover {
    width: 260px;
}

.nav-link {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 14px 18px;
    color: rgba(255,255,255,0.85);
    text-decoration: none;
    transition: all 0.25s ease;
    font-size: 14px;
    font-weight: 500;
    border-left: 3px solid transparent;
}

.nav-link i { width: 20px; text-align: center; margin-right: 0; }
.sidebar:hover .nav-link { justify-content: flex-start; padding: 14px 25px; }
.sidebar:hover .nav-link i { margin-right: 12px; }

.nav-link span { display: none; white-space: nowrap; }
.sidebar:hover .nav-link span { display: inline; }

.nav-link:hover {
    background: rgba(255,255,255,0.1);
    color: white;
    border-left-color: #4CAF50;
}

.nav-link.active {
    background: rgba(255,255,255,0.15);
    color: white;
    border-left-color: #4CAF50;
}

.main-content {
    margin-left: 70px;
    padding: 30px 40px;
    min-height: 100vh;
    transition: margin-left 0.25s ease;
}

.sidebar:hover ~ .main-content { margin-left: 260px; }

.header {
    background: white;
    padding: 25px 30px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

.kpi-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}

.kpi-card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.12);
}

.chart-card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

@media (max-width: 1400px) {
    .kpi-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .main-content { padding: 20px; }
    .kpi-container { grid-template-columns: 1fr; }
}
</style>
</head>''')

if __name__ == "__main__":
    app.run(debug=True)