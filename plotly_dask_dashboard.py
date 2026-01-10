"""
Employee Data Analysis Dashboard using Plotly Dash and Dask
This dashboard provides interactive analysis with high-performance data processing
using Dask for handling large datasets efficiently.
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dask.dataframe as dd
from datetime import datetime
import numpy as np

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Employee Analytics Dashboard"

# Load data with Dask for efficient processing
def load_data_with_dask():
    """Load data using Dask for efficient processing"""
    # Read with Dask
    ddf = dd.read_csv('../data/employee_extended_50.csv')
    
    # Convert to pandas for visualization (suitable for this dataset size)
    # For larger datasets, keep as Dask dataframe and process in chunks
    df = ddf.compute()
    
    # Data preprocessing
    df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
    df['Joining_Year'] = df['Joining_Date'].dt.year
    df['Tenure'] = (datetime.now() - df['Joining_Date']).dt.days / 365.25
    
    return df

# Load data
df = load_data_with_dask()

# Define color scheme
colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#0d6efd',
    'secondary': '#6c757d',
    'success': '#198754',
    'danger': '#dc3545',
    'card_bg': '#ffffff'
}

# App Layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    # Header
    html.Div([
        html.H1(
            '👥 Employee Analytics Dashboard',
            style={
                'textAlign': 'center',
                'color': colors['primary'],
                'padding': '20px',
                'backgroundColor': colors['card_bg'],
                'marginBottom': '0px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }
        ),
        html.P(
            'Interactive Analytics powered by Plotly Dash & Dask',
            style={
                'textAlign': 'center',
                'color': colors['secondary'],
                'backgroundColor': colors['card_bg'],
                'paddingBottom': '20px',
                'marginTop': '0px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }
        ),
    ]),
    
    # Filters Section
    html.Div([
        html.Div([
            html.H3('🔍 Filters', style={'color': colors['primary']}),
            
            html.Div([
                html.Label('Department:', style={'fontWeight': 'bold', 'marginTop': '10px'}),
                dcc.Dropdown(
                    id='dept-filter',
                    options=[{'label': 'All Departments', 'value': 'All'}] + 
                            [{'label': dept, 'value': dept} for dept in sorted(df['Dept'].unique())],
                    value='All',
                    style={'marginBottom': '15px'}
                ),
                
                html.Label('City:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='city-filter',
                    options=[{'label': 'All Cities', 'value': 'All'}] + 
                            [{'label': city, 'value': city} for city in sorted(df['City'].unique())],
                    value='All',
                    style={'marginBottom': '15px'}
                ),
                
                html.Label('Age Range:', style={'fontWeight': 'bold'}),
                dcc.RangeSlider(
                    id='age-slider',
                    min=int(df['Age'].min()),
                    max=int(df['Age'].max()),
                    value=[int(df['Age'].min()), int(df['Age'].max())],
                    marks={i: str(i) for i in range(int(df['Age'].min()), int(df['Age'].max())+1, 5)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.Label('Salary Range (₹):', style={'fontWeight': 'bold', 'marginTop': '20px'}),
                dcc.RangeSlider(
                    id='salary-slider',
                    min=int(df['Sal'].min()),
                    max=int(df['Sal'].max()),
                    value=[int(df['Sal'].min()), int(df['Sal'].max())],
                    marks={i: f'{i//1000}K' for i in range(int(df['Sal'].min()), int(df['Sal'].max())+1, 10000)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'padding': '20px', 'backgroundColor': colors['card_bg'], 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        
        # Main Content
        html.Div([
            # KPI Cards
            html.Div(id='kpi-cards', style={'marginBottom': '20px'}),
            
            # Charts Row 1
            html.Div([
                html.Div([
                    dcc.Graph(id='dept-pie-chart')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    dcc.Graph(id='city-bar-chart')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            ]),
            
            # Charts Row 2
            html.Div([
                html.Div([
                    dcc.Graph(id='salary-dept-chart')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    dcc.Graph(id='salary-exp-scatter')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            ]),
            
            # Charts Row 3
            html.Div([
                html.Div([
                    dcc.Graph(id='performance-hist')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    dcc.Graph(id='age-box-plot')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            ]),
            
            # Map
            html.Div([
                dcc.Graph(id='geo-map')
            ], style={'padding': '10px'}),
            
            # Charts Row 4
            html.Div([
                html.Div([
                    dcc.Graph(id='hiring-trend')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    dcc.Graph(id='dept-hiring-trend')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            ]),
            
            # Charts Row 5
            html.Div([
                html.Div([
                    dcc.Graph(id='correlation-heatmap')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    dcc.Graph(id='tenure-chart')
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            ]),
            
            # Data Table
            html.Div([
                html.H3('📋 Employee Data Table', style={'color': colors['primary'], 'padding': '20px 10px 10px 10px'}),
                html.Div(id='data-table-container', style={'padding': '10px'}),
            ]),
            
        ], style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ]),
    
    # Footer
    html.Div([
        html.P('Employee Analytics Dashboard | Built with Plotly Dash & Dask',
               style={'textAlign': 'center', 'color': colors['secondary'], 'padding': '20px'})
    ], style={'backgroundColor': colors['card_bg'], 'marginTop': '20px'})
])

# Callbacks for interactivity
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('dept-pie-chart', 'figure'),
     Output('city-bar-chart', 'figure'),
     Output('salary-dept-chart', 'figure'),
     Output('salary-exp-scatter', 'figure'),
     Output('performance-hist', 'figure'),
     Output('age-box-plot', 'figure'),
     Output('geo-map', 'figure'),
     Output('hiring-trend', 'figure'),
     Output('dept-hiring-trend', 'figure'),
     Output('correlation-heatmap', 'figure'),
     Output('tenure-chart', 'figure'),
     Output('data-table-container', 'children')],
    [Input('dept-filter', 'value'),
     Input('city-filter', 'value'),
     Input('age-slider', 'value'),
     Input('salary-slider', 'value')]
)
def update_dashboard(selected_dept, selected_city, age_range, salary_range):
    # Filter data using Dask-like operations (can be optimized for larger datasets)
    filtered_df = df.copy()
    
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Dept'] == selected_dept]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    
    filtered_df = filtered_df[
        (filtered_df['Age'] >= age_range[0]) &
        (filtered_df['Age'] <= age_range[1]) &
        (filtered_df['Sal'] >= salary_range[0]) &
        (filtered_df['Sal'] <= salary_range[1])
    ]
    
    # KPI Cards
    kpi_cards = html.Div([
        html.Div([
            html.Div([
                html.H4('Total Employees', style={'color': colors['secondary'], 'fontSize': '14px'}),
                html.H2(f"{len(filtered_df)}", style={'color': colors['primary'], 'margin': '0'})
            ], style={'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px', 
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Div([
                html.H4('Avg Salary', style={'color': colors['secondary'], 'fontSize': '14px'}),
                html.H2(f"₹{filtered_df['Sal'].mean():,.0f}", style={'color': colors['success'], 'margin': '0'})
            ], style={'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Div([
                html.H4('Avg Experience', style={'color': colors['secondary'], 'fontSize': '14px'}),
                html.H2(f"{filtered_df['Experience'].mean():.1f} yrs", style={'color': colors['primary'], 'margin': '0'})
            ], style={'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Div([
                html.H4('Avg Performance', style={'color': colors['secondary'], 'fontSize': '14px'}),
                html.H2(f"{filtered_df['Per_score'].mean():.1f}%", style={'color': colors['success'], 'margin': '0'})
            ], style={'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Div([
                html.H4('Departments', style={'color': colors['secondary'], 'fontSize': '14px'}),
                html.H2(f"{filtered_df['Dept'].nunique()}", style={'color': colors['primary'], 'margin': '0'})
            ], style={'backgroundColor': colors['card_bg'], 'padding': '20px', 'borderRadius': '5px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px'}),
    ])
    
    # 1. Department Pie Chart
    dept_counts = filtered_df['Dept'].value_counts()
    fig1 = px.pie(
        values=dept_counts.values,
        names=dept_counts.index,
        title="Employee Distribution by Department",
        hole=0.4
    )
    
    # 2. City Bar Chart
    city_counts = filtered_df['City'].value_counts().head(10)
    fig2 = px.bar(
        x=city_counts.values,
        y=city_counts.index,
        orientation='h',
        title="Top 10 Cities",
        labels={'x': 'Employees', 'y': 'City'}
    )
    
    # 3. Salary by Department
    dept_salary = filtered_df.groupby('Dept')['Sal'].agg(['mean', 'max']).reset_index()
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name='Average', x=dept_salary['Dept'], y=dept_salary['mean']))
    fig3.add_trace(go.Bar(name='Maximum', x=dept_salary['Dept'], y=dept_salary['max']))
    fig3.update_layout(title="Salary by Department", barmode='group')
    
    # 4. Salary vs Experience
    fig4 = px.scatter(
        filtered_df,
        x='Experience',
        y='Sal',
        color='Dept',
        size='Per_score',
        hover_data=['Name', 'Age'],
        title="Salary vs Experience"
    )
    
    # 5. Performance Distribution
    fig5 = px.histogram(
        filtered_df,
        x='Per_score',
        nbins=20,
        title="Performance Score Distribution"
    )
    
    # 6. Age Box Plot
    fig6 = px.box(
        filtered_df,
        x='Dept',
        y='Age',
        color='Dept',
        title="Age Distribution by Department"
    )
    
    # 7. Geographical Map
    fig7 = px.scatter_mapbox(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        color='Dept',
        size='Sal',
        hover_data=['Name', 'City'],
        title="Employee Distribution Map",
        zoom=3.5,
        height=500
    )
    fig7.update_layout(mapbox_style="open-street-map")
    
    # 8. Hiring Trend
    hiring_trend = filtered_df.groupby('Joining_Year').size().reset_index(name='Count')
    fig8 = px.line(
        hiring_trend,
        x='Joining_Year',
        y='Count',
        title="Hiring Trends",
        markers=True
    )
    
    # 9. Department Hiring
    dept_year = filtered_df.groupby(['Joining_Year', 'Dept']).size().reset_index(name='Count')
    fig9 = px.bar(
        dept_year,
        x='Joining_Year',
        y='Count',
        color='Dept',
        title="Department-wise Hiring"
    )
    
    # 10. Correlation Heatmap
    corr_cols = ['Age', 'Sal', 'Experience', 'Per_score']
    corr_matrix = filtered_df[corr_cols].corr()
    fig10 = px.imshow(
        corr_matrix,
        text_auto='.2f',
        title="Correlation Matrix",
        color_continuous_scale='RdBu_r'
    )
    
    # 11. Tenure Chart
    tenure_dept = filtered_df.groupby('Dept')['Tenure'].mean().sort_values(ascending=False)
    fig11 = px.bar(
        x=tenure_dept.values,
        y=tenure_dept.index,
        orientation='h',
        title="Average Tenure by Department"
    )
    
    # 12. Data Table
    data_table = dash_table.DataTable(
        data=filtered_df.head(20).to_dict('records'),
        columns=[{'name': col, 'id': col} for col in filtered_df.columns if col not in ['Latitude', 'Longitude']],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'backgroundColor': colors['card_bg']
        },
        style_header={
            'backgroundColor': colors['primary'],
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            }
        ],
        page_size=20,
        sort_action='native',
        filter_action='native'
    )
    
    return kpi_cards, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, data_table

# Run the app
if __name__ == '__main__':
    print("🚀 Starting Employee Analytics Dashboard...")
    print("📊 Dashboard running at: http://127.0.0.1:8050/")
    app.run_server(debug=True, port=8050)
