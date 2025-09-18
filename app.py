import dash
from dash import html

app = dash.Dash(__name__)
#font awesome
app.index_string = '''
<!DOCTYPE html>
<html>
 <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
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

sidebar = html.Div(
    [
        html.H2("dashboard",className="mb-4"),
        html.A([html.I(className="fas fa-home"),"Home"],href="#"),
        html.A([html.I(className="fas fa-chart-bar"),"Analytics"],href="#"),
        html.A([html.I(className="fas fa-cog"),"Settings"],href="#"),
        
    ],
    className="sidebar"
)
app.layout = html.Div([sidebar])
if __name__ == "__main__":
    app.run(debug=True)