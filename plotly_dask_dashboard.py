import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dask.dataframe as dd

app = dash.Dash(__name__)
app.title = "Employee Analytics Dashboard"

def load_data():
    ddf = dd.read_csv('../data/employee_extended_50.csv')
    df = ddf.compute()
    df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
    df['Joining_Year'] = df['Joining_Date'].dt.year
    return df

df = load_data()

app.layout = html.Div(style={'backgroundColor': '#1e1e1e', 'minHeight': '100vh', 'padding': '20px'}, children=[
    html.H1('Employee Analytics Dashboard', 
            style={'textAlign': 'center', 'color': 'white', 'marginBottom': '30px'}),
    
    html.Div([
        html.Label('Department:', style={'color': 'white', 'marginBottom': '5px'}),
        dcc.Dropdown(id='dept-filter',
                    options=[{'label': 'All', 'value': 'All'}] + 
                           [{'label': d, 'value': d} for d in sorted(df['Dept'].unique())],
                    value='All', style={'marginBottom': '20px', 'width': '300px'}),
    ]),
    
    html.Div(id='kpi-cards', style={'marginBottom': '30px'}),
    
    html.Div([
        html.Div([dcc.Graph(id='dept-pie-chart')], 
                style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='salary-exp-scatter')], 
                style={'width': '50%', 'display': 'inline-block'}),
    ]),
    
    html.Div([
        html.Div([dcc.Graph(id='performance-hist')], 
                style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='hiring-trend')], 
                style={'width': '50%', 'display': 'inline-block'}),
    ]),
])

@app.callback(
    [Output('kpi-cards', 'children'), Output('dept-pie-chart', 'figure'),
     Output('salary-exp-scatter', 'figure'), Output('performance-hist', 'figure'),
     Output('hiring-trend', 'figure')],
    [Input('dept-filter', 'value')]
)
def update_dashboard(selected_dept):
    filtered_df = df.copy()
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Dept'] == selected_dept]
    
    kpi_style = {'backgroundColor': '#2d2d2d', 'padding': '20px', 'borderRadius': '10px', 
                 'textAlign': 'center', 'color': 'white', 'margin': '10px'}
    
    kpi_cards = html.Div([
        html.Div([
            html.H4('Total Employees'),
            html.H2(f"{len(filtered_df)}")
        ], style={**kpi_style, 'width': '22%', 'display': 'inline-block'}),
        html.Div([
            html.H4('Avg Salary'),
            html.H2(f"₹{filtered_df['Sal'].mean():,.0f}")
        ], style={**kpi_style, 'width': '22%', 'display': 'inline-block'}),
        html.Div([
            html.H4('Avg Experience'),
            html.H2(f"{filtered_df['Experience'].mean():.1f} yrs")
        ], style={**kpi_style, 'width': '22%', 'display': 'inline-block'}),
        html.Div([
            html.H4('Departments'),
            html.H2(f"{filtered_df['Dept'].nunique()}")
        ], style={**kpi_style, 'width': '22%', 'display': 'inline-block'}),
    ])
    
    dept_counts = filtered_df['Dept'].value_counts()
    fig1 = px.pie(values=dept_counts.values, names=dept_counts.index, 
                  title="Employee Distribution by Department")
    fig1.update_layout(template='plotly_dark')
    
    fig2 = px.scatter(filtered_df, x='Experience', y='Sal', color='Dept',
                     hover_data=['Name'], title="Salary vs Experience")
    fig2.update_layout(template='plotly_dark')
    
    fig3 = px.histogram(filtered_df, x='Per_score', nbins=20, 
                       title="Performance Score Distribution")
    fig3.update_layout(template='plotly_dark')
    
    hiring_trend = filtered_df.groupby('Joining_Year').size().reset_index(name='Count')
    fig4 = px.line(hiring_trend, x='Joining_Year', y='Count', 
                  title="Hiring Trends", markers=True)
    fig4.update_layout(template='plotly_dark')
    
    return kpi_cards, fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)