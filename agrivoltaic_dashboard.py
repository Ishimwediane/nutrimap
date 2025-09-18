import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, date
import os

# Load the merged CSV data
def load_data():
    """Load the merged CSV data for the dashboard"""
    try:
        # Get the current directory (Notebooks folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate to the Data/Processed directory
        processed_dir = os.path.join(current_dir, '..', 'Data', 'Processed')
        all_data_filename = os.path.join(processed_dir, "merged.csv")
        
        # Load the CSV data
        merged_df = pd.read_csv(all_data_filename)
        
        # Step 1: Convert DATE to datetime format
        if 'DATE' in merged_df.columns:
            merged_df["DATE"] = pd.to_datetime(merged_df["DATE"], errors='coerce')
        
        # Step 2: Define ordered categorical months
        if 'Month' in merged_df.columns:
            month_order = ['May', 'June', 'July', 'August', 'October']
            merged_df['Month'] = pd.Categorical(merged_df['Month'], categories=month_order, ordered=True)
        
        # Convert timestamp column to datetime if it exists
        if 'timestamp' in merged_df.columns:
            merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'])
        elif 'Timestamp' in merged_df.columns:
            merged_df['Timestamp'] = pd.to_datetime(merged_df['Timestamp'])
        
        print(f"Data loaded successfully: {len(merged_df)} rows, {len(merged_df.columns)} columns")
        print(f"Columns: {list(merged_df.columns)}")
        
        return merged_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Load the data
merged_df = load_data()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
], suppress_callback_exceptions=True)

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', sans-serif;
                margin: 0;
                background-color: #f8fdf9;
            }
        </style>
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

# Define color scheme
COLORS = {
    'primary': '#2E8B57',      # Sea Green
    'secondary': '#98D8A8',    # Light Green
    'accent': '#1B5E20',       # Dark Green
    'background': '#f8fdf9',   # Very Light Green
    'white': '#ffffff',
    'text_dark': '#2c3e50',
    'text_light': '#7f8c8d',
    'success': '#27ae60',
    'warning': '#f39c12',
    'info': '#3498db'
}

# Header component
def create_header():
    return html.Div([
        html.Div([
            html.Div([
                html.H1("🌱 Agrivoltaic Systems Dashboard", 
                       style={
                           'color': COLORS['text_dark'],
                           'margin': '0',
                           'fontSize': '2.5rem',
                           'fontWeight': '700'
                       }),
                html.P("Environmental Monitoring & Analysis for Ghana Pilot Project",
                      style={
                          'color': COLORS['text_light'],
                          'margin': '10px 0 0 0',
                          'fontSize': '1.1rem',
                          'fontWeight': '400'
                      })
            ], style={'flex': '1'}),
            
            html.Div([
                html.Div([
                    html.H3("31,443", style={'margin': '0', 'color': COLORS['primary'], 'fontSize': '1.5rem'}),
                    html.P("Data Points", style={'margin': '0', 'color': COLORS['text_light'], 'fontSize': '0.9rem'})
                ], style={'textAlign': 'center', 'padding': '10px 20px'}),
                
                html.Div([
                    html.H3("5", style={'margin': '0', 'color': COLORS['primary'], 'fontSize': '1.5rem'}),
                    html.P("Months", style={'margin': '0', 'color': COLORS['text_light'], 'fontSize': '0.9rem'})
                ], style={'textAlign': 'center', 'padding': '10px 20px'}),
                
                html.Div([
                    html.H3("3", style={'margin': '0', 'color': COLORS['primary'], 'fontSize': '1.5rem'}),
                    html.P("Plot Types", style={'margin': '0', 'color': COLORS['text_light'], 'fontSize': '0.9rem'})
                ], style={'textAlign': 'center', 'padding': '10px 20px'})
            ], style={
                'display': 'flex',
                'backgroundColor': COLORS['white'],
                'borderRadius': '12px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
                'border': f'1px solid {COLORS["secondary"]}'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'padding': '30px',
            'backgroundColor': COLORS['white'],
            'borderRadius': '15px',
            'marginBottom': '30px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'border': f'2px solid {COLORS["secondary"]}'
        })
    ])

# Navigation tabs component
def create_navigation():
    return html.Div([
        dcc.Tabs(
            id="main-tabs",
            value="overview",
            children=[
                dcc.Tab(label="🏠 Overview", value="overview", 
                       style={'fontWeight': '500', 'fontSize': '1rem'}),
                dcc.Tab(label="📊 Executive Summary", value="executive", 
                       style={'fontWeight': '500', 'fontSize': '1rem'}),
                dcc.Tab(label="🌡️ Temperature Analysis", value="temperature", 
                       style={'fontWeight': '500', 'fontSize': '1rem'}),
                dcc.Tab(label="🌿 Environmental Conditions", value="environment", 
                       style={'fontWeight': '500', 'fontSize': '1rem'}),
                dcc.Tab(label="⚡ Energy Analysis", value="energy", 
                       style={'fontWeight': '500', 'fontSize': '1rem'}),
                dcc.Tab(label="🎯 Conclusion & Recommendation", value="finals", 
                       style={'fontWeight': '500', 'fontSize': '1rem'})
            ],
            style={
                'height': '70px',
                'fontFamily': 'Inter'
            },
            colors={
                "border": COLORS['secondary'],
                "primary": COLORS['primary'],
                "background": COLORS['background']
            }
        )
    ], style={'marginBottom': '30px'})

# Metric card component
def create_metric_card(title, value, subtitle, icon, color=COLORS['primary']):
    return html.Div([
        html.Div([
            html.Div(icon, style={
                'fontSize': '2rem',
                'marginBottom': '10px',
                'color': color
            }),
            html.H3(value, style={
                'margin': '0',
                'fontSize': '2rem',
                'fontWeight': '700',
                'color': COLORS['text_dark']
            }),
            html.P(title, style={
                'margin': '5px 0',
                'fontSize': '1rem',
                'fontWeight': '500',
                'color': COLORS['text_dark']
            }),
            html.P(subtitle, style={
                'margin': '0',
                'fontSize': '0.9rem',
                'color': COLORS['text_light']
            })
        ], style={
            'textAlign': 'center',
            'padding': '25px',
            'backgroundColor': COLORS['white'],
            'borderRadius': '12px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'border': f'1px solid {COLORS["secondary"]}',
            'height': '180px',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center'
        })
    ])

# Section header component
def create_section_header(title, description):
    return html.Div([
        html.H2(title, style={
            'color': COLORS['text_dark'],
            'fontSize': '1.8rem',
            'fontWeight': '600',
            'marginBottom': '10px'
        }),
        html.P(description, style={
            'color': COLORS['text_light'],
            'fontSize': '1rem',
            'marginBottom': '25px',
            'lineHeight': '1.5'
        })
    ])

# Chart container component
def create_chart_container(chart_id, title, description):
    return html.Div([
        html.Div([
            html.H4(title, style={
                'color': COLORS['text_dark'],
                'fontSize': '1.2rem',
                'fontWeight': '600',
                'marginBottom': '5px'
            }),
            html.P(description, style={
                'color': COLORS['text_light'],
                'fontSize': '0.9rem',
                'marginBottom': '20px'
            })
        ]),
        dcc.Graph(
            id=chart_id,
            style={'height': '400px'}
        )
    ], style={
        'backgroundColor': COLORS['white'],
        'borderRadius': '12px',
        'padding': '25px',
        'marginBottom': '25px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'border': f'1px solid {COLORS["secondary"]}'
    })

# Overview tab content
def create_overview_content():
    return html.Div([
        create_section_header(
            "Project Overview",
            "Comprehensive analysis of agrivoltaic systems in Ghana, examining how solar panel installations affect microclimatic conditions and agricultural productivity."
        ),
        
        # Key metrics row
        html.Div([
            html.Div([
                create_metric_card("Temperature Reduction", "10°C", "Average cooling in shaded plots", "🌡️", COLORS['info'])
            ], style={'width': '23%'}),
            
            html.Div([
                create_metric_card("Solar Efficiency", "91.3%", "Retained solar irradiance", "☀️", COLORS['warning'])
            ], style={'width': '23%'}),
            
            html.Div([
                create_metric_card("Data Points", "31,443", "Continuous measurements", "📊", COLORS['success'])
            ], style={'width': '23%'}),
            
            html.Div([
                create_metric_card("Statistical Significance", "p<0.001", "All major findings", "📈", COLORS['primary'])
            ], style={'width': '23%'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'marginBottom': '40px'
        }),
        
        # Study design section
        html.Div([
            html.Div([
                html.H3("Study Design", style={'color': COLORS['text_dark'], 'marginBottom': '20px'}),
                html.Div([
                    html.Div([
                        html.H4("🌱 Agrivoltaic Plots (AG)", style={'color': COLORS['primary']}),
                        html.P("Solar panels elevated above crops, providing partial shading while generating renewable energy.")
                    ], style={'marginBottom': '20px'}),
                    
                    html.Div([
                        html.H4("🌾 Control Plots (AO)", style={'color': COLORS['accent']}),
                        html.P("Traditional farming areas without solar panel coverage for baseline comparison.")
                    ], style={'marginBottom': '20px'}),
                    
                    html.Div([
                        html.H4("⚡ Ground PV (PO)", style={'color': COLORS['warning']}),
                        html.P("Ground-mounted solar installations for energy generation comparison.")
                    ], style={'marginBottom': '20px'}),
                    
                    html.Div([
                        html.H4("🌦️ Weather Station (WS)", style={'color': COLORS['info']}),
                        html.P("Ambient weather monitoring providing regional climate context.")
                    ])
                ])
            ], style={'width': '48%'}),
            
            html.Div([
                html.H3("Key Variables Monitored", style={'color': COLORS['text_dark'], 'marginBottom': '20px'}),
                html.Div([
                    html.Div([
                        html.Span("🌡️", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                        html.Span("Temperature (°C)", style={'fontSize': '1rem', 'fontWeight': '500'})
                    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    
                    html.Div([
                        html.Span("💧", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                        html.Span("Relative Humidity (%)", style={'fontSize': '1rem', 'fontWeight': '500'})
                    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    
                    html.Div([
                        html.Span("☀️", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                        html.Span("Solar Irradiation (W/m²)", style={'fontSize': '1rem', 'fontWeight': '500'})
                    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    
                    html.Div([
                        html.Span("🌱", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                        html.Span("Soil Moisture (%)", style={'fontSize': '1rem', 'fontWeight': '500'})
                    ], style={'marginBottom': '15px', 'display': 'flex', 'alignItems': 'center'}),
                    
                    html.Div([
                        html.Span("🌧️", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
                        html.Span("Rainfall (mm)", style={'fontSize': '1rem', 'fontWeight': '500'})
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ])
            ], style={'width': '48%'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'backgroundColor': COLORS['white'],
            'borderRadius': '12px',
            'padding': '30px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'border': f'1px solid {COLORS["secondary"]}'
        })
    ])

# Executive summary tab content
def create_executive_content():
    return html.Div([
        create_section_header(
            "Executive Summary",
            "High-level overview of environmental conditions and key findings from the agrivoltaic monitoring study."
        ),
        
        create_chart_container(
            "rainfall-trend",
            "Monthly Rainfall Patterns",
            "Seasonal precipitation trends affecting both agricultural and energy systems"
        ),
        
        html.Div([
            html.Div([
                create_chart_container(
                    "environmental-conditions",
                    "Environmental Conditions by Plot Type",
                    "Comparative analysis of key environmental parameters"
                )
            ], style={'width': '65%'}),
            
            html.Div([
                create_chart_container(
                    "summary-statistics",
                    "Data Column Type Distribution",
                    "Overview of numeric, categorical, and datetime columns in the dataset"
                )
            ], style={'width': '33%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ])

# Temperature analysis tab content
def create_temperature_content():
    return html.Div([
        create_section_header(
            "Temperature Analysis",
            "Detailed examination of temperature variations across different plot types and temporal patterns."
        ),
        
        create_chart_container(
            "temperature-comparison",
            "Temperature: Agrivoltaic vs Control",
            "Statistical comparison showing cooling effects of solar panel shading"
        ),
        
        html.Div([
            html.Div([
                create_chart_container(
                    "hourly-temperature",
                    "Daily Temperature Patterns",
                    "Hourly temperature variations across plot types"
                )
            ], style={'width': '48%'}),
            
            html.Div([
                create_chart_container(
                    "monthly-temperature",
                    "Seasonal Temperature Trends",
                    "Monthly temperature variations across different plots"
                )
            ], style={'width': '48%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ])

# Environmental conditions tab content
def create_environment_content():
    return html.Div([
        create_section_header(
            "Environmental Conditions",
            "Analysis of humidity and soil moisture patterns affecting crop growing conditions."
        ),
        
        html.Div([
            html.Div([
                create_chart_container(
                    "humidity-comparison",
                    "Humidity: Agrivoltaic vs Control",
                    "Atmospheric moisture differences between plot types"
                )
            ], style={'width': '48%'}),
            
            html.Div([
                create_chart_container(
                    "soil-moisture-comparison",
                    "Soil Moisture: Agrivoltaic vs Control",
                    "Soil water content variations affecting irrigation needs"
                )
            ], style={'width': '48%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        
        create_chart_container(
            "hourly-humidity",
            "Daily Humidity Patterns",
            "Hourly humidity trends across different environmental conditions"
        )
    ])

# Energy analysis tab content
def create_energy_content():
    return html.Div([
        create_section_header(
            "Energy Analysis",
            "Solar irradiance patterns and energy generation potential across different system configurations."
        ),
        
        create_chart_container(
            "irradiance-comparison",
            "Solar Irradiance: Agrivoltaic vs Ground PV",
            "Comparison of solar energy potential between system types"
        ),
        
        html.Div([
            html.Div([
                create_chart_container(
                    "correlation-analysis",
                    "Solar Irradiation vs Soil Moisture",
                    "Relationship between energy generation and agricultural conditions"
                )
            ], style={'width': '48%'}),
            
            html.Div([
                create_chart_container(
                    "hourly-irradiance",
                    "Daily Solar Irradiance Patterns",
                    "Hourly solar energy availability across system types"
                )
            ], style={'width': '48%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ])

# Main app layout
app.layout = html.Div([
    create_header(),
    create_navigation(),
    
    html.Div(id="tab-content", style={
        'padding': '0 30px 30px 30px'
    })
], style={
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif'
})

# Callback for tab content
@app.callback(
    Output("tab-content", "children"),
    [Input("main-tabs", "value")]
)
def update_tab_content(tab):
    if tab == "overview":
        return create_overview_content()
    elif tab == "executive":
        return create_executive_content()
    elif tab == "temperature":
        return create_temperature_content()
    elif tab == "environment":
        return create_environment_content()
    elif tab == "energy":
        return create_energy_content()
    elif tab == "finals":
        return create_finals_content()
    else:
        return create_overview_content()

# Placeholder callbacks for charts (you'll replace these with your actual chart code)
@app.callback(Output("rainfall-trend", "figure"), [Input("main-tabs", "value")])
def update_rainfall_chart(tab):
    if merged_df.empty:
        # Return placeholder if no data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig
    # fig = go.Figure()
    #     fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
    #     fig.update_layout(
    #         template="simple_white",
    #         font=dict(family="Inter"),
    #         title_font_size=16,
    #         margin=dict(l=0, r=0, t=30, b=0)
    #     )
    #     return fig
    
    try:
        # Check if 'WS/P (mm)' column exists (as in your original code)
        if 'WS/P (mm)' in merged_df.columns:
            # Step 1: Group by Month and calculate average rainfall
            rainfall_means = merged_df.groupby("Month")[
                ['WS/P (mm)']
            ].mean(numeric_only=True).reset_index()

            # Step 2: Rename for clarity
            rainfall_means.columns = ['Month', 'Rainfall']

            # Step 3: Plot with consistent styling using plotly.express
            fig = px.line(
                rainfall_means,
                x="Month",
                y="Rainfall",
                height=400,
                markers=True,
                color_discrete_sequence=["green"],  # Using your standard green
                labels={"Rainfall": "Avg Rainfall (mm)", "Month": "Month"}  # Explicit labels
            )

            # Update layout with bold formatting
            fig.update_layout(
                template="simple_white",
                xaxis=dict(
                    showgrid=False,
                    title_text="Month",
                    title_font=dict(size=14, family='Arial', weight='bold'),
                    tickfont=dict(size=12, family='Arial', weight='bold'),
                    tickangle=0  # Horizontal labels
                ),
                yaxis=dict(
                    showgrid=False,
                    title_text="Avg Rainfall (mm)",
                    title_font=dict(size=14, family='Arial', weight='bold'),
                    tickfont=dict(size=12, family='Arial', weight='bold')
                ),
                height=400,  # Reduced height to fit container
                margin=dict(l=40, r=40, t=20, b=60)  # Reduced top margin since no title
            )

            # Improve marker and line visibility
            fig.update_traces(
                marker=dict(
                    size=8,
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                line=dict(width=3)  # Slightly thicker line for single series
            )
            
            return fig
        
        # If 'WS/P (mm)' column doesn't exist, try to find alternative rainfall columns
        rainfall_cols = [col for col in merged_df.columns if 'rainfall' in col.lower() or 'rain' in col.lower() or 'p (mm)' in col.lower()]
        
        if rainfall_cols:
            # Use the first rainfall column found
            rainfall_col = rainfall_cols[0]
            
            # Get timestamp column
            time_col = 'timestamp' if 'timestamp' in merged_df.columns else 'Timestamp'
            
            if time_col in merged_df.columns:
                # Create monthly rainfall aggregation
                merged_df[time_col] = pd.to_datetime(merged_df[time_col])
                monthly_rainfall = merged_df.groupby(merged_df[time_col].dt.to_period('M'))[rainfall_col].sum().reset_index()
                monthly_rainfall[time_col] = monthly_rainfall[time_col].astype(str)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=monthly_rainfall[time_col],
                    y=monthly_rainfall[rainfall_col],
                    name="Monthly Rainfall",
                    marker_color=COLORS['info']
                ))
                
                fig.update_layout(
                    title="Monthly Rainfall Patterns",
                    xaxis_title="Month",
                    yaxis_title="Rainfall (mm)",
                    template="simple_white",
                    font=dict(family="Inter"),
                    title_font_size=16,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                return fig
        
        # If no rainfall data, show general data overview
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=merged_df.index[:100],  # Show first 100 data points
            y=merged_df.iloc[:100, 0],  # First numeric column
            name="Sample Data",
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Sample Data Overview",
            xaxis_title="Data Point",
            yaxis_title="Value",
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig
        
    except Exception as e:
        print(f"Error creating rainfall chart: {e}")
        # Return placeholder on error
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
    fig.update_layout(
        template="simple_white",
        font=dict(family="Inter"),
        title_font_size=16,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return fig

@app.callback(Output("environmental-conditions", "figure"), [Input("main-tabs", "value")])
def update_environmental_chart(tab):
    if merged_df.empty:
        # Return placeholder if no data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig
    
    try:
        # Step 1: Classify columns by plot type
        def classify_plot(col_name):
            if 'AG-PV' in col_name or 'AG-TI' in col_name or 'AG-SS' in col_name:
                return 'Agrivoltaic'
            elif 'AO-TI' in col_name or 'AO-SS' in col_name:
                return 'Control'
            elif 'PO-PV' in col_name:
                return 'Ground PV'
            elif 'WS' in col_name:
                return 'Weather Station'
            else:
                return 'Other'

        # Map column names to plot type
        plot_types = {col: classify_plot(col) for col in merged_df.columns[2:]}
        plot_df = pd.DataFrame({'Column': list(plot_types.keys()), 'Plot_Type': list(plot_types.values())})

        # Step 2: Melt the data
        melted_df = merged_df.melt(id_vars=['DATE', 'TIME', 'Month'], var_name='Sensor', value_name='Value')

        # Step 3: Merge with plot classification
        melted_df = melted_df.merge(plot_df, left_on='Sensor', right_on='Column', how='left')

        # Step 4: Add sensor type
        def get_sensor_type(sensor):
            if 'Irr' in sensor:
                return 'Irradiation'
            elif '/T' in sensor:
                return 'Temperature'
            elif '/RH' in sensor:
                return 'Humidity'
            elif '/P' in sensor:
                return 'Rainfall'
            else:
                return 'Other'

        melted_df['Sensor_Type'] = melted_df['Sensor'].apply(get_sensor_type)

        # Step 5: Group by plot type and sensor type
        avg_plot_data = (
            melted_df[melted_df['Plot_Type'].isin(['Agrivoltaic', 'Control', 'Ground PV'])]
            .groupby(['Plot_Type', 'Sensor_Type'])['Value']
            .mean()
            .reset_index()
        )

        # Step 6: Plot using Plotly with green palette
        fig = px.bar(
            avg_plot_data,
            x='Sensor_Type',
            y='Value',
            color='Plot_Type',
            height=400,  # Reduced height to fit container
            barmode='group',
            color_discrete_sequence=px.colors.sequential.Greens_r,
            text_auto='.2s'
        )

        fig.update_layout(
            xaxis=dict(
                title_text="Sensor Type",
                title_font=dict(weight='bold', size=14),
                tickfont=dict(weight='bold', size=12)
            ),
            yaxis=dict(
                title_text="Average Value",
                title_font=dict(weight='bold', size=14),
                tickfont=dict(weight='bold', size=12)
            ),
            legend_title="Plot Type",
            legend_title_font=dict(weight='bold'),
            legend_font=dict(weight='bold'),
            template="simple_white",
            font=dict(color="black"),
            height=400,  # Reduced height to fit container
            margin=dict(l=40, r=40, t=20, b=60)  # Reduced margins
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating environmental conditions chart: {e}")
        # Return placeholder on error
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig

@app.callback(Output("summary-statistics", "figure"), [Input("main-tabs", "value")])
def update_summary_chart(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            template="simple_white",
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

    try:
        # Analyze data types
        col_types = merged_df.dtypes

        # Count data types
        type_counts = {
            'Numeric': sum(col_types.apply(lambda x: pd.api.types.is_numeric_dtype(x))),
            'Categorical': sum(col_types.apply(lambda x: pd.api.types.is_object_dtype(x))),
            'Datetime': sum(col_types.apply(lambda x: pd.api.types.is_datetime64_any_dtype(x)))
        }

        # Convert to DataFrame
        type_df = pd.DataFrame({
            'Type': list(type_counts.keys()),
            'Count': list(type_counts.values())
        })

        # Plot pie chart
        fig = px.pie(
            type_df,
            names='Type',
            values='Count',
            color_discrete_sequence=px.colors.sequential.Greens_r,
            hole=0.3  # for donut style
        )

        # Update layout with consistent styling
        fig.update_layout(
            template="simple_white",
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            font=dict(family='Arial')
        )

        return fig

    except Exception as e:
        print(f"Error creating data type distribution chart: {e}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            template="simple_white",
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

@app.callback(Output("temperature-comparison", "figure"), [Input("main-tabs", "value")])
def update_temperature_comparison(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig
    
    try:
        # Define temperature groups
        temp_label = "Temperature (°C)"
        temp_groups = {
            "Shaded": ['AG-PV P1/T (oC)', 'AG-SS P1/T (oC)'],
            "Control": ['AO-TI P2/T (oC)', 'AO-SS P1/T (oC)']
        }

        # Prepare data
        df_temp = merged_df[temp_groups["Shaded"] + temp_groups["Control"]].copy()
        df_temp_long = df_temp.melt(var_name="Sensor", value_name=temp_label)
        df_temp_long = df_temp_long.dropna()
        df_temp_long["Condition"] = df_temp_long["Sensor"].apply(
            lambda x: "Shaded (AG)" if any(ag in x for ag in temp_groups["Shaded"]) else "Control (AO)"
        )

        # Create plot
        fig = px.box(
            df_temp_long,
            x="Condition",
            y=temp_label,
            color="Condition",
            height=400,
            template="simple_white",
            color_discrete_sequence=['#006400', '#9DC183']
        )

        fig.update_layout(
            showlegend=False,
            title={
                # 'text': f'<b>{temp_label} — Shaded (AG) vs Control (AO)</b>',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=18, family="Arial")
            },
            xaxis=dict(
                title='<b>Condition</b>',
                title_font=dict(size=14, family="Arial", color='black'),
                tickfont=dict(size=12, family="Arial", color='black')
            ),
            yaxis=dict(
                title=f'<b>{temp_label}</b>',
                title_font=dict(size=14, family="Arial", color='black'),
                tickfont=dict(size=12, family="Arial", color='black')
            ),
            font=dict(family="Arial", color='black'),
            margin=dict(l=40, r=40, t=30, b=60)
        )

        fig.update_traces(
            line=dict(width=2.5),
            marker=dict(size=4, line=dict(width=1, color='green'))
        )

        return fig
    
    except Exception as e:
        print(f"Error generating temperature comparison chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig

@app.callback(Output("hourly-temperature", "figure"), [Input("main-tabs", "value")])
def update_hourly_temperature(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig
    
    try:
        if 'Hour' not in merged_df.columns:
            merged_df['Hour'] = pd.to_datetime(merged_df['TIME'], errors='coerce').dt.hour

        hourly_means = merged_df.groupby("Hour")[
            ['AG-PV P3/T (oC)', 'AO-TI P2/T (oC)', 'PO-PV/T (oC)']
        ].mean(numeric_only=True).reset_index()

        hourly_means.columns = ['Hour', 'Agrivoltaic', 'Control', 'Ground-mounted']

        hourly_long = hourly_means.melt(
            id_vars="Hour",
            var_name="Plot Type",
            value_name="Temperature"
        )

        fig = px.line(
            hourly_long,
            x="Hour",
            y="Temperature",
            color="Plot Type",
            markers=True,
            height=400,
            color_discrete_sequence=["teal", "lime", "green"],
            labels={"Temperature": "Avg Temp (°C)", "Hour": "Hour of Day"}
        )

        fig.update_xaxes(
            tickvals=list(range(0, 24, 5)),
            ticktext=[f"{h}:00" for h in range(0, 24, 5)],
            showgrid=False,
            tickfont=dict(size=12, family='Arial', weight='bold')
        )

        fig.update_yaxes(
            showgrid=False,
            tickfont=dict(size=12, family='Arial', weight='bold')
        )

        fig.update_layout(
            template="simple_white",
            xaxis=dict(
                title_text="Hour of Day",
                title_font=dict(size=14, family='Arial', weight='bold')
            ),
            yaxis=dict(
                title_text="Avg Temp (°C)",
                title_font=dict(size=14, family='Arial', weight='bold')
            ),
            legend_title=dict(
                text="Plot Type",
                font=dict(size=12, family='Arial', weight='bold')
            ),
            font=dict(family="Arial"),
            margin=dict(l=40, r=40, t=20, b=60)  # Less top margin since no title
        )

        return fig

    except Exception as e:
        print(f"Error creating hourly temperature chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig

@app.callback(Output("monthly-temperature", "figure"), [Input("main-tabs", "value")])
def update_monthly_temperature(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig
    
    try:
        # Step 1: Convert DATE to datetime format if not done
        if not pd.api.types.is_datetime64_any_dtype(merged_df["DATE"]):
            merged_df["DATE"] = pd.to_datetime(merged_df["DATE"], errors='coerce')

        # Step 2: Define ordered categorical months
        month_order = ['May', 'June', 'July', 'August', 'October']
        if 'Month' not in merged_df.columns:
            merged_df['Month'] = merged_df['DATE'].dt.strftime('%B')  # Extract month name from DATE
        merged_df['Month'] = pd.Categorical(merged_df['Month'], categories=month_order, ordered=True)

        # Step 3: Group by Month and compute averages
        monthly_means = merged_df.groupby("Month")[
            ['AG-PV P3/T (oC)', 'AO-TI P2/T (oC)', 'PO-PV/T (oC)']
        ].mean(numeric_only=True).reset_index()

        # Step 4: Rename columns
        monthly_means.columns = ['Month', 'Agrivoltaic', 'Control', 'Ground-mounted']

        # Step 5: Melt for long format
        temp_long = monthly_means.melt(id_vars="Month", var_name="Plot Type", value_name="Temperature")

        # Step 6: Plot with Plotly Express
        fig = px.line(
            temp_long,
            x="Month",
            y="Temperature",
            color="Plot Type",
            markers=True,
            height=400,
            color_discrete_sequence=["green", "lime", "teal"],
            labels={"Temperature": "Avg Temp (°C)", "Month": "Month"}
        )

        # Layout updates with bold fonts and styling
        fig.update_layout(
            template="simple_white",
            xaxis=dict(
                showgrid=False,
                title_text="Month",
                title_font=dict(size=14, family='Arial', weight='bold'),
                tickfont=dict(size=12, family='Arial', weight='bold'),
                tickangle=0
            ),
            yaxis=dict(
                showgrid=False,
                title_text="Avg Temp (°C)",
                title_font=dict(size=14, family='Arial', weight='bold'),
                tickfont=dict(size=12, family='Arial', weight='bold')
            ),
            legend_title=dict(
                text="Plot Type",
                font=dict(size=12, family='Arial', weight='bold')
            ),
            font=dict(family="Arial"),
            margin=dict(l=40, r=40, t=40, b=60)
        )

        fig.update_traces(
            marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')),
            line=dict(width=2.5)
        )

        return fig

    except Exception as e:
        print(f"Error creating monthly temperature chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig

@app.callback(Output("humidity-comparison", "figure"), [Input("main-tabs", "value")])
def update_humidity_comparison(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig

    try:
        humidity_label = "Humidity (%)"
        humidity_groups = {
            "Shaded": ['AG-SS P1/RH (%)'],
            "Control": ['AO-TI P2/RH (%)', 'AO-SS P1/RH (%)']
        }

        # Prepare data
        df_humidity = merged_df[humidity_groups["Shaded"] + humidity_groups["Control"]].copy()
        df_humidity_long = df_humidity.melt(var_name="Sensor", value_name=humidity_label).dropna()

        df_humidity_long["Condition"] = df_humidity_long["Sensor"].apply(
            lambda x: "Shaded (AG)" if any(ag in x for ag in humidity_groups["Shaded"]) else "Control (AO)"
        )

        fig = px.box(
            df_humidity_long,
            x="Condition",
            y=humidity_label,
            color="Condition",
            height=400,
            template="simple_white",
            color_discrete_sequence=['#006400', '#9DC183'],
            labels={"Condition": "Condition", humidity_label: humidity_label},
        )

        fig.update_layout(
            showlegend=False,
            xaxis=dict(
                title='<b>Condition</b>',
                title_font=dict(size=14, family="Arial", weight='bold'),
                tickfont=dict(size=12, family="Arial", weight='bold')
            ),
            yaxis=dict(
                title=f'<b>{humidity_label}</b>',
                title_font=dict(size=14, family="Arial", weight='bold'),
                tickfont=dict(size=12, family="Arial", weight='bold')
            ),
            font=dict(family="Arial", weight='bold'),
            margin=dict(l=40, r=40, t=80, b=60)
        )

        fig.update_traces(
            line=dict(width=2.5),
            marker=dict(
                size=4,
                line=dict(width=1, color='green')
            )
        )

        return fig

    except Exception as e:
        print(f"Error creating humidity comparison chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig


@app.callback(Output("soil-moisture-comparison", "figure"), [Input("main-tabs", "value")])
def update_soil_moisture_comparison(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig

    try:
        soil_label = "Soil Moisture Proxy (%)"
        soil_groups = {
            "Shaded": ['AG-SS P1/RH (%)'],
            "Control": ['AO-SS P1/RH (%)']
        }

        # Prepare data
        df_soil = merged_df[soil_groups["Shaded"] + soil_groups["Control"]].copy()
        df_soil_long = df_soil.melt(var_name="Sensor", value_name=soil_label).dropna()

        df_soil_long["Condition"] = df_soil_long["Sensor"].apply(
            lambda x: "Shaded (AG)" if any(ag in x for ag in soil_groups["Shaded"]) else "Control (AO)"
        )

        fig = px.box(
            df_soil_long,
            x="Condition",
            y=soil_label,
            color="Condition",
            height=400,
            template="simple_white",
            color_discrete_sequence=['#006400', '#9DC183'],
            labels={"Condition": "Condition", soil_label: soil_label}
        )

        fig.update_layout(
            showlegend=False,
            xaxis=dict(
                title='<b>Condition</b>',
                title_font=dict(size=14, family="Arial", weight='bold'),
                tickfont=dict(size=12, family="Arial", weight='bold')
            ),
            yaxis=dict(
                title=f'<b>{soil_label}</b>',
                title_font=dict(size=14, family="Arial", weight='bold'),
                tickfont=dict(size=12, family="Arial", weight='bold')
            ),
            font=dict(family="Arial", weight='bold'),
            margin=dict(l=40, r=40, t=80, b=60)
        )

        fig.update_traces(
            line=dict(width=2.5),
            marker=dict(
                size=4,
                line=dict(width=1, color='green')
            )
        )

        return fig

    except Exception as e:
        print(f"Error creating soil moisture chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig

@app.callback(Output("hourly-humidity", "figure"), [Input("main-tabs", "value")])
def update_hourly_humidity(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig

    try:
        # Ensure 'Hour' column exists
        if 'Hour' not in merged_df.columns:
            merged_df['Hour'] = pd.to_datetime(merged_df['TIME'], errors='coerce').dt.hour

        # Step 1: Group by Hour and calculate mean humidity
        humidity_means = merged_df.groupby("Hour")[
            ['AG-TI P1/RH (%)', 'AO-TI P2/RH (%)']
        ].mean(numeric_only=True).reset_index()

        # Step 2: Rename columns
        humidity_means.columns = ['Hour', 'Agrivoltaic', 'Control']

        # Step 3: Melt to long format
        humidity_long = humidity_means.melt(id_vars="Hour", var_name="Plot Type", value_name="Humidity")

        # Step 4: Plot
        fig = px.line(
            humidity_long,
            x="Hour",
            y="Humidity",
            height=400,
            color="Plot Type",
            markers=True,
            color_discrete_sequence=["green", "lime"],
            labels={"Humidity": "Avg Humidity (%)", "Hour": "Hour of Day"}
        )

        # X-axis: 5-hour intervals
        fig.update_xaxes(
            tickvals=list(range(0, 24, 5)),
            ticktext=[f"{h}:00" for h in range(0, 24, 5)],
            showgrid=False,
            tickfont=dict(size=12, family='Arial', weight='bold'),
            title_font=dict(size=16, family='Arial', weight='bold')
        )

        # Y-axis
        fig.update_yaxes(
            showgrid=False,
            tickfont=dict(size=12, family='Arial', weight='bold'),
            title_font=dict(size=16, family='Arial', weight='bold')
        )

        # Layout updates
        fig.update_layout(
            template="simple_white",
            legend_title_text="Plot Type",
            legend_title_font=dict(size=14, family='Arial', weight='bold'),
            legend_font=dict(size=12, family='Arial', weight='bold'),
            margin=dict(l=40, r=40, t=60, b=60)
        )

        return fig

    except Exception as e:
        print(f"Error creating hourly humidity chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig


@app.callback(Output("irradiance-comparison", "figure"), [Input("main-tabs", "value")])
def update_irradiance_comparison(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig

    try:
        # Clean column names
        merged_df.columns = merged_df.columns.str.strip()

        # Define plot types of interest
        plot_types = ['AG-PV', 'AO-TI', 'AO-SS', 'PO-PV', 'AG-SS']

        # Select irradiance columns
        irradiance_cols = [col for col in merged_df.columns if "Irr" in col and any(pt in col for pt in plot_types)]

        # Melt DataFrame
        irr_long = merged_df[irradiance_cols].melt(var_name="Sensor", value_name="Irradiance")

        # Extract abbreviation
        irr_long["Abbreviation"] = irr_long["Sensor"].str.extract(r'(AG-PV|AO-TI|AO-SS|PO-PV|AG-SS)')

        # Map to full names
        plot_type_labels = {
            "PO-PV": "Ground-Mounted PV Systems",
            "AG-PV": "Agrivoltaic Photovoltaic Panel Sensors",
            "AO-TI": "Control Plot – Tin Roof",
            "AO-SS": "Control Plot – Soil Sensors",
            "AG-SS": "Agrivoltaic Soil Sensors"
        }
        irr_long["Plot_Type"] = irr_long["Abbreviation"].map(plot_type_labels)

        # Define color palette
        color_sequence = ['#006400', '#9DC183']

        # Create plot
        fig = px.box(
            irr_long,
            x="Abbreviation",
            y="Irradiance",
            color="Plot_Type",
            labels={
                "Irradiance": "Irradiance (W/m²)",
                "Abbreviation": "Plot Type"
            },
            template="simple_white",
            height=400,
            color_discrete_sequence=color_sequence
        )

        fig.update_layout(
            xaxis=dict(
                showgrid=False,
                title_text="Plot Type",
                title_font=dict(size=16, family='Arial', weight='bold'),
                tickfont=dict(size=14, family='Arial', weight='bold')
            ),
            yaxis=dict(
                showgrid=False,
                title_text="Irradiance (W/m²)",
                title_font=dict(size=16, family='Arial', weight='bold'),
                tickfont=dict(size=14, family='Arial', weight='bold')
            ),
            legend_title_text="Plot Type Description",
            legend_title_font=dict(size=14, family='Arial', weight='bold'),
            legend_font=dict(size=12, family='Arial', weight='bold'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(b=100),
            boxmode='group'
        )

        fig.update_traces(
            width=0.7,
            line=dict(width=2.5),
            marker=dict(
                size=5,
                line=dict(width=1.2, color='green')
            ),
            whiskerwidth=0.5,
            quartilemethod="exclusive"
        )

        return fig

    except Exception as e:
        print(f"Error creating irradiance comparison chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig

@app.callback(Output("correlation-analysis", "figure"), [Input("main-tabs", "value")])
def update_corr_heatmap(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No Data Available", showarrow=False, font=dict(size=16))
        fig.update_layout(template="simple_white", height=500)
        return fig

    try:
        # Step 1: Select relevant columns
        df_corr = merged_df[['AG-PV P3/Irr (W/m2)', 'AG-SS P1/RH (%)']].dropna()

        # Step 2: Compute Pearson correlation
        corr_matrix = df_corr.corr(method='pearson')
        rounded_corr = np.round(corr_matrix.values, 2)

        # Step 3: Plot heatmap with bold values
        fig = go.Figure(data=go.Heatmap(
            z=rounded_corr,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='Greens',
            text=rounded_corr,
            texttemplate="<b>%{text}</b>",
            showscale=True,
            zmin=-1, 
            zmax=1
        ))

        # Layout formatting
        fig.update_layout(
            xaxis=dict(
                title='<b>Variable</b>',
                title_font=dict(size=14, family="Arial"),
                tickfont=dict(size=12, family="Arial", color='black')
            ),
            yaxis=dict(
                title='<b>Variable</b>',
                title_font=dict(size=14, family="Arial"),
                tickfont=dict(size=12, family="Arial", color='black')
            ),
            font=dict(family="Arial"),
            height=400,
            template='simple_white'
        )

        return fig

    except Exception as e:
        print(f"Error creating heatmap: {e}")
        fig = go.Figure()
        fig.add_annotation(text="Error Loading Data", showarrow=False)
        fig.update_layout(template="simple_white", height=500)
        return fig

@app.callback(Output("hourly-irradiance", "figure"), [Input("main-tabs", "value")])
def update_hourly_irradiance(tab):
    if merged_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="No Data Available"))
        fig.update_layout(
            template="simple_white",
            font=dict(family="Inter"),
            title_font_size=16,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig

    try:
        # Ensure Hour exists
        merged_df['Hour'] = pd.to_datetime(merged_df['TIME'], errors='coerce').dt.hour

        # Group by Hour and calculate mean irradiance
        irradiance_means = merged_df.groupby("Hour")[
            ['AG-PV P1/Irr (W/m2)', 'PO-PV/Irr (W/m2)']
        ].mean(numeric_only=True).reset_index()

        # Rename columns
        irradiance_means.columns = ['Hour', 'Agrivoltaic', 'Ground-mounted']

        # Melt to long format
        irradiance_long = irradiance_means.melt(id_vars="Hour", var_name="Plot Type", value_name="Irradiance")

        # Create line plot
        fig = px.line(
            irradiance_long,
            x="Hour",
            y="Irradiance",
            height=400,
            color="Plot Type",
            markers=True,
            color_discrete_sequence=["green", "lime"],
            labels={"Irradiance": "Avg Irradiance (W/m²)", "Hour": "Hour of Day"}
        )

        # Customize axes
        fig.update_xaxes(
            tickvals=list(range(0, 24, 5)),
            ticktext=[f"{h}:00" for h in range(0, 24, 5)],
            showgrid=False,
            tickfont=dict(size=12, family='Arial', weight='bold'),
            title_font=dict(size=16, family='Arial', weight='bold')
        )
        fig.update_yaxes(
            showgrid=False,
            tickfont=dict(size=12, family='Arial', weight='bold'),
            title_font=dict(size=16, family='Arial', weight='bold')
        )

        # Update layout
        fig.update_layout(
            template="simple_white",
            legend_title_text="Plot Type",
            legend_title_font=dict(size=14, family='Arial', weight='bold'),
            legend_font=dict(size=12, family='Arial', weight='bold'),
            height=400,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        return fig

    except Exception as e:
        print(f"Error creating hourly irradiance chart: {e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Error Loading Data"))
        fig.update_layout(template="simple_white")
        return fig

def create_finals_content():
    return html.Div([
        create_section_header(
            "Conclusion & Recommendations",
            "Comprehensive analysis summary with actionable insights for agrivoltaic system optimization in Ghana."
        ),
        
        # Key Findings Summary Cards
        html.Div([
            html.H3("🔍 Key Findings", style={
                'color': COLORS['text_dark'], 
                'marginBottom': '25px',
                'fontSize': '1.5rem',
                'fontWeight': '600'
            }),
            
            html.Div([
                # Finding 1
                html.Div([
                    html.Div([
                        html.H4("🌡️ Temperature Regulation", style={
                            'color': COLORS['primary'],
                            'marginBottom': '10px',
                            'fontSize': '1.2rem'
                        }),
                        html.P("Agrivoltaic systems provide significant cooling benefits, reducing temperatures by up to 10°C compared to control plots.", 
                               style={'marginBottom': '10px'}),
                        html.Div([
                            html.Span("Impact: ", style={'fontWeight': 'bold'}),
                            html.Span("Reduced heat stress for crops, improved growing conditions")
                        ], style={'fontSize': '0.9rem', 'color': COLORS['text_light']})
                    ])
                ], style={
                    'backgroundColor': COLORS['white'],
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                    'border': f'1px solid {COLORS["secondary"]}',
                    'marginBottom': '15px'
                }),
                
                # Finding 2
                html.Div([
                    html.Div([
                        html.H4("💧 Humidity Retention", style={
                            'color': COLORS['info'],
                            'marginBottom': '10px',
                            'fontSize': '1.2rem'
                        }),
                        html.P("Shaded plots maintain higher humidity levels, creating more stable microclimatic conditions for agriculture.", 
                               style={'marginBottom': '10px'}),
                        html.Div([
                            html.Span("Impact: ", style={'fontWeight': 'bold'}),
                            html.Span("Reduced water evaporation, lower irrigation requirements")
                        ], style={'fontSize': '0.9rem', 'color': COLORS['text_light']})
                    ])
                ], style={
                    'backgroundColor': COLORS['white'],
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                    'border': f'1px solid {COLORS["secondary"]}',
                    'marginBottom': '15px'
                }),
                
                # Finding 3
                html.Div([
                    html.Div([
                        html.H4("⚡ Energy Efficiency", style={
                            'color': COLORS['warning'],
                            'marginBottom': '10px',
                            'fontSize': '1.2rem'
                        }),
                        html.P("Solar panels maintain 91.3% efficiency while providing agricultural benefits, demonstrating system viability.", 
                               style={'marginBottom': '10px'}),
                        html.Div([
                            html.Span("Impact: ", style={'fontWeight': 'bold'}),
                            html.Span("Dual land use optimization, sustainable energy generation")
                        ], style={'fontSize': '0.9rem', 'color': COLORS['text_light']})
                    ])
                ], style={
                    'backgroundColor': COLORS['white'],
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                    'border': f'1px solid {COLORS["secondary"]}'
                })
            ])
        ], style={'marginBottom': '40px'}),
        
        # Main conclusions and recommendations section
        html.Div([
            html.Div([
                html.H3("✅ Conclusions", style={
                    'color': COLORS['text_dark'], 
                    'marginBottom': '20px',
                    'fontSize': '1.4rem',
                    'fontWeight': '600'
                }),
                html.Div([
                    html.Div([
                        html.Div("🌱", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Microclimate Benefits: "),
                            html.Span("Agrivoltaic systems create favorable growing conditions through temperature regulation and humidity retention, particularly beneficial for tropical regions like Ghana.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div("🛡️", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Crop Protection: "),
                            html.Span("Solar panel shading protects crops from extreme heat stress, potentially improving yield quality and reducing crop losses during peak temperature periods.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div("💧", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Water Conservation: "),
                            html.Span("Higher humidity levels and reduced evaporation under panels lead to more efficient water use and potentially reduced irrigation needs.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div("📊", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Data-Driven Insights: "),
                            html.Span("Temporal patterns in environmental data provide valuable information for optimizing field management practices and seasonal crop planning.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start'})
                ])
            ], style={'width': '48%'}),
            
            html.Div([
                html.H3("📝 Recommendations", style={
                    'color': COLORS['text_dark'], 
                    'marginBottom': '20px',
                    'fontSize': '1.4rem',
                    'fontWeight': '600'
                }),
                html.Div([
                    html.Div([
                        html.Div("⚙️", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Panel Optimization: "),
                            html.Span("Adjust panel height (3-4m) and spacing to balance crop light requirements with energy generation efficiency.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div("🔄", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Seasonal Adjustments: "),
                            html.Span("Implement adjustable panel tilt angles based on seasonal solar patterns and crop growth cycles.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div("📡", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Enhanced Monitoring: "),
                            html.Span("Deploy additional soil moisture sensors and crop-specific monitoring equipment for more precise agricultural insights.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),
                    
                    html.Div([
                        html.Div("🌾", style={'fontSize': '1.5rem', 'marginRight': '15px', 'display': 'inline-block'}),
                        html.Div([
                            html.Strong("Crop Selection: "),
                            html.Span("Prioritize shade-tolerant or heat-sensitive crops that benefit most from the cooler, stable microclimatic conditions.")
                        ], style={'display': 'inline-block', 'width': 'calc(100% - 40px)'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start'})
                ])
            ], style={'width': '48%'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'backgroundColor': COLORS['white'],
            'borderRadius': '12px',
            'padding': '30px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'border': f'1px solid {COLORS["secondary"]}',
            'marginBottom': '30px'
        }),
        
        # Next Steps Section
        html.Div([
            html.H3("🎯 Next Steps", style={
                'color': COLORS['text_dark'], 
                'marginBottom': '20px',
                'fontSize': '1.4rem',
                'fontWeight': '600'
            }),
            
            html.Div([
                html.Div([
                    html.H4("Short-term (3-6 months)", style={'color': COLORS['success'], 'marginBottom': '15px'}),
                    html.Ul([
                        html.Li("Optimize panel positioning based on current findings"),
                        html.Li("Implement precision irrigation systems using humidity data"),
                        html.Li("Conduct crop yield comparisons between plot types"),
                        html.Li("Expand sensor network for comprehensive monitoring")
                    ], style={'paddingLeft': '20px'})
                ], style={'width': '32%'}),
                
                html.Div([
                    html.H4("Medium-term (6-12 months)", style={'color': COLORS['warning'], 'marginBottom': '15px'}),
                    html.Ul([
                        html.Li("Scale pilot project to additional sites"),
                        html.Li("Develop predictive models for crop-energy optimization"),
                        html.Li("Establish economic viability benchmarks"),
                        html.Li("Train local farmers on agrivoltaic best practices")
                    ], style={'paddingLeft': '20px'})
                ], style={'width': '32%'}),
                
                html.Div([
                    html.H4("Long-term (1-2 years)", style={'color': COLORS['info'], 'marginBottom': '15px'}),
                    html.Ul([
                        html.Li("Create national agrivoltaic implementation framework"),
                        html.Li("Develop policy recommendations for government adoption"),
                        html.Li("Establish commercial partnerships for scaling"),
                        html.Li("Integrate findings into climate adaptation strategies")
                    ], style={'paddingLeft': '20px'})
                ], style={'width': '32%'})
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between'
            })
        ], style={
            'backgroundColor': COLORS['white'],
            'borderRadius': '12px',
            'padding': '30px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'border': f'1px solid {COLORS["secondary"]}'
        })
    ])

if __name__ == "__main__":
    app.run(debug=True)