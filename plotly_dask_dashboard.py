import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dask.dataframe as dd
from datetime import datetime

app = dash.Dash(__name__)
app.title = "Employee Analytics Dashboard"

colors = {
    'background': '#1e1e1e',
    'card': '#2d2d2d',
    'text': '#ffffff',
    'primary': '#3b82f6',
    'secondary': '#8b5cf6',
    'border': '#404040'
}

def load_data():
    ddf = dd.read_csv('../data/employee_extended_50.csv')
    df = ddf.compute()
    df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
    df['Joining_Year'] = df['Joining_Date'].dt.year
    df['Tenure'] = (datetime.now() - df['Joining_Date']).dt.days / 365.25
    return df

df = load_data()

app.layout = html.Div(style={'backgroundColor': colors['background'], 'minHeight': '100vh', 'fontFamily': 'Arial'}, children=[
    html.Div([
        html.H1('👥 Employee Analytics Dashboard', 
                style={'textAlign': 'center', 'color': colors['text'], 'padding': '30px', 
                       'margin': '0', 'background': f'linear-gradient(135deg, {colors["primary"]}, {colors["secondary"]})',
                       'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'}),
    ]),
    
    html.Div([
        html.Div([
            html.H3('🔍 Filters', style={'color': colors['text'], 'marginBottom': '20px'}),
            html.Div([
                html.Label('Department:', style={'fontWeight': 'bold', 'marginTop': '10px', 'color': colors['text'], 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(id='dept-filter',
                            options=[{'label': 'All', 'value': 'All'}] + 
                                   [{'label': d, 'value': d} for d in sorted(df['Dept'].unique())],
                            value='All', style={'marginBottom': '15px'}),
                
                html.Label('City:', style={'fontWeight': 'bold', 'color': colors['text'], 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(id='city-filter',
                            options=[{'label': 'All', 'value': 'All'}] + 
                                   [{'label': c, 'value': c} for c in sorted(df['City'].unique())],
                            value='All', style={'marginBottom': '15px'}),
                
                html.Label('Age Range:', style={'fontWeight': 'bold', 'color': colors['text'], 'display': 'block', 'marginBottom': '5px'}),
                dcc.RangeSlider(id='age-slider', min=int(df['Age'].min()), max=int(df['Age'].max()),
                               value=[int(df['Age'].min()), int(df['Age'].max())],
                               marks={i: {'label': str(i), 'style': {'color': colors['text']}} for i in range(int(df['Age'].min()), int(df['Age'].max())+1, 5)},
                               tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label('Salary Range:', style={'fontWeight': 'bold', 'marginTop': '20px', 'color': colors['text'], 'display': 'block', 'marginBottom': '5px'}),
                dcc.RangeSlider(id='salary-slider', min=int(df['Sal'].min()), max=int(df['Sal'].max()),
                               value=[int(df['Sal'].min()), int(df['Sal'].max())],
                               marks={i: {'label': f'{i//1000}K', 'style': {'color': colors['text']}} for i in range(int(df['Sal'].min()), int(df['Sal'].max())+1, 10000)},
                               tooltip={"placement": "bottom", "always_visible": True}),
            ], style={'padding': '25px', 'backgroundColor': colors['card'], 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)', 'border': f'1px solid {colors["border"]}'}),
        ], style={'width': '22%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        
        html.Div([
            html.Div(id='kpi-cards', style={'marginBottom': '20px'}),
            
            html.Div([
                html.Div([
                    html.H4('📊 Distribution Analysis', style={'color': colors['text'], 'margin': '0 0 15px 15px', 'fontSize': '16px'}),
                    html.Div([
                        html.Div([dcc.Graph(id='dept-pie-chart', style={'height': '350px'})], 
                                style={'width': '33.33%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                        html.Div([dcc.Graph(id='city-bar-chart', style={'height': '350px'})], 
                                style={'width': '33.33%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                        html.Div([dcc.Graph(id='age-box-plot', style={'height': '350px'})], 
                                style={'width': '33.33%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                    ]),
                ], style={'backgroundColor': colors['card'], 'borderRadius': '10px', 'padding': '15px 10px', 
                         'marginBottom': '20px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'}),
            ]),
            
            html.Div([
                html.Div([
                    html.H4('💰 Salary Insights', style={'color': colors['text'], 'margin': '0 0 15px 15px', 'fontSize': '16px'}),
                    html.Div([
                        html.Div([dcc.Graph(id='salary-dept-chart', style={'height': '350px'})], 
                                style={'width': '50%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                        html.Div([dcc.Graph(id='salary-exp-scatter', style={'height': '350px'})], 
                                style={'width': '50%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                    ]),
                ], style={'backgroundColor': colors['card'], 'borderRadius': '10px', 'padding': '15px 10px', 
                         'marginBottom': '20px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'}),
            ]),
            
            html.Div([
                html.Div([
                    html.H4('📈 Performance & Trends', style={'color': colors['text'], 'margin': '0 0 15px 15px', 'fontSize': '16px'}),
                    html.Div([
                        html.Div([dcc.Graph(id='performance-hist', style={'height': '320px'})], 
                                style={'width': '33.33%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                        html.Div([dcc.Graph(id='hiring-trend', style={'height': '320px'})], 
                                style={'width': '33.33%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                        html.Div([dcc.Graph(id='dept-hiring-trend', style={'height': '320px'})], 
                                style={'width': '33.33%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                    ]),
                ], style={'backgroundColor': colors['card'], 'borderRadius': '10px', 'padding': '15px 10px', 
                         'marginBottom': '20px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'}),
            ]),
            
            html.Div([
                html.Div([
                    html.H4('🗺️ Geographic Distribution', style={'color': colors['text'], 'margin': '0 0 15px 15px', 'fontSize': '16px'}),
                    dcc.Graph(id='geo-map', style={'height': '450px'}),
                ], style={'backgroundColor': colors['card'], 'borderRadius': '10px', 'padding': '15px 10px', 
                         'marginBottom': '20px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'}),
            ]),
            
            html.Div([
                html.Div([
                    html.H4('📉 Analytics', style={'color': colors['text'], 'margin': '0 0 15px 15px', 'fontSize': '16px'}),
                    html.Div([
                        html.Div([dcc.Graph(id='correlation-heatmap', style={'height': '400px'})], 
                                style={'width': '50%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                        html.Div([dcc.Graph(id='tenure-chart', style={'height': '400px'})], 
                                style={'width': '50%', 'display': 'inline-block', 'padding': '5px', 'verticalAlign': 'top'}),
                    ]),
                ], style={'backgroundColor': colors['card'], 'borderRadius': '10px', 'padding': '15px 10px', 
                         'marginBottom': '20px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'}),
            ]),
            
            html.Div([
                html.H3('📋 Employee Data', style={'padding': '15px 15px 10px 15px', 'color': colors['text'], 'margin': '0', 'fontSize': '16px'}),
                html.Div(id='data-table-container', style={'padding': '10px 15px 15px 15px'}),
            ], style={'backgroundColor': colors['card'], 'borderRadius': '10px', 'margin': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'}),
        ], style={'width': '78%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ]),
])

@app.callback(
    [Output('kpi-cards', 'children'), Output('dept-pie-chart', 'figure'), Output('city-bar-chart', 'figure'),
     Output('salary-dept-chart', 'figure'), Output('salary-exp-scatter', 'figure'), Output('performance-hist', 'figure'),
     Output('age-box-plot', 'figure'), Output('geo-map', 'figure'), Output('hiring-trend', 'figure'),
     Output('dept-hiring-trend', 'figure'), Output('correlation-heatmap', 'figure'), Output('tenure-chart', 'figure'),
     Output('data-table-container', 'children')],
    [Input('dept-filter', 'value'), Input('city-filter', 'value'), 
     Input('age-slider', 'value'), Input('salary-slider', 'value')]
)
def update_dashboard(selected_dept, selected_city, age_range, salary_range):
    filtered_df = df.copy()
    
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Dept'] == selected_dept]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1]) &
                              (filtered_df['Sal'] >= salary_range[0]) & (filtered_df['Sal'] <= salary_range[1])]
    
    kpi_cards = html.Div([
        html.Div([html.Div([html.H4('Total Employees', style={'fontSize': '13px', 'color': '#94a3b8', 'margin': '0 0 10px 0'}), 
                           html.H2(f"{len(filtered_df)}", style={'margin': '0', 'color': colors['text'], 'fontSize': '32px', 'fontWeight': 'bold'})],
                          style={'backgroundColor': colors['card'], 'padding': '25px', 'borderRadius': '10px', 'textAlign': 'center', 
                                 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)', 'border': f'1px solid {colors["border"]}'})
                 ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
        html.Div([html.Div([html.H4('Avg Salary', style={'fontSize': '13px', 'color': '#94a3b8', 'margin': '0 0 10px 0'}), 
                           html.H2(f"₹{filtered_df['Sal'].mean():,.0f}", style={'margin': '0', 'color': '#10b981', 'fontSize': '32px', 'fontWeight': 'bold'})],
                          style={'backgroundColor': colors['card'], 'padding': '25px', 'borderRadius': '10px', 'textAlign': 'center', 
                                 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)', 'border': f'1px solid {colors["border"]}'})
                 ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
        html.Div([html.Div([html.H4('Avg Experience', style={'fontSize': '13px', 'color': '#94a3b8', 'margin': '0 0 10px 0'}), 
                           html.H2(f"{filtered_df['Experience'].mean():.1f} yrs", style={'margin': '0', 'color': colors['text'], 'fontSize': '32px', 'fontWeight': 'bold'})],
                          style={'backgroundColor': colors['card'], 'padding': '25px', 'borderRadius': '10px', 'textAlign': 'center', 
                                 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)', 'border': f'1px solid {colors["border"]}'})
                 ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
        html.Div([html.Div([html.H4('Avg Performance', style={'fontSize': '13px', 'color': '#94a3b8', 'margin': '0 0 10px 0'}), 
                           html.H2(f"{filtered_df['Per_score'].mean():.1f}%", style={'margin': '0', 'color': '#f59e0b', 'fontSize': '32px', 'fontWeight': 'bold'})],
                          style={'backgroundColor': colors['card'], 'padding': '25px', 'borderRadius': '10px', 'textAlign': 'center', 
                                 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)', 'border': f'1px solid {colors["border"]}'})
                 ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
        html.Div([html.Div([html.H4('Departments', style={'fontSize': '13px', 'color': '#94a3b8', 'margin': '0 0 10px 0'}), 
                           html.H2(f"{filtered_df['Dept'].nunique()}", style={'margin': '0', 'color': colors['text'], 'fontSize': '32px', 'fontWeight': 'bold'})],
                          style={'backgroundColor': colors['card'], 'padding': '25px', 'borderRadius': '10px', 'textAlign': 'center', 
                                 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)', 'border': f'1px solid {colors["border"]}'})
                 ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
    ])
    
    template = 'plotly_dark'
    
    dept_counts = filtered_df['Dept'].value_counts()
    fig1 = px.pie(values=dept_counts.values, names=dept_counts.index, title="By Department", hole=0.4)
    fig1.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=20))
    
    city_counts = filtered_df['City'].value_counts().head(10)
    fig2 = px.bar(x=city_counts.values, y=city_counts.index, orientation='h', title="Top 10 Cities")
    fig2.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=20))
    
    dept_salary = filtered_df.groupby('Dept')['Sal'].agg(['mean', 'max']).reset_index()
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name='Average', x=dept_salary['Dept'], y=dept_salary['mean']))
    fig3.add_trace(go.Bar(name='Maximum', x=dept_salary['Dept'], y=dept_salary['max']))
    fig3.update_layout(title="By Department", barmode='group', template=template, 
                      paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=60))
    
    fig4 = px.scatter(filtered_df, x='Experience', y='Sal', color='Dept', size='Per_score',
                     hover_data=['Name', 'Age'], title="Salary vs Experience")
    fig4.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=40))
    
    fig5 = px.histogram(filtered_df, x='Per_score', nbins=20, title="Performance Distribution")
    fig5.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=40))
    
    fig6 = px.box(filtered_df, x='Dept', y='Age', color='Dept', title="Age by Department")
    fig6.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=60))
    
    fig7 = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', color='Dept', size='Sal',
                             hover_data=['Name', 'City'], zoom=3.5)
    fig7.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=0, r=0, t=0, b=0), showlegend=True)
    
    hiring_trend = filtered_df.groupby('Joining_Year').size().reset_index(name='Count')
    fig8 = px.line(hiring_trend, x='Joining_Year', y='Count', title="Yearly Hiring", markers=True)
    fig8.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=40))
    
    dept_year = filtered_df.groupby(['Joining_Year', 'Dept']).size().reset_index(name='Count')
    fig9 = px.bar(dept_year, x='Joining_Year', y='Count', color='Dept', title="Hiring by Department")
    fig9.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=40))
    
    corr_matrix = filtered_df[['Age', 'Sal', 'Experience', 'Per_score']].corr()
    fig10 = px.imshow(corr_matrix, text_auto='.2f', title="Correlation Matrix", color_continuous_scale='RdBu_r')
    fig10.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=20))
    
    tenure_dept = filtered_df.groupby('Dept')['Tenure'].mean().sort_values(ascending=False)
    fig11 = px.bar(x=tenure_dept.values, y=tenure_dept.index, orientation='h', title="Avg Tenure by Department")
    fig11.update_layout(template=template, paper_bgcolor=colors['card'], plot_bgcolor=colors['card'], 
                      font_color=colors['text'], margin=dict(l=20, r=20, t=50, b=20))
    
    data_table = dash_table.DataTable(
        data=filtered_df.head(20).to_dict('records'),
        columns=[{'name': col, 'id': col} for col in filtered_df.columns if col not in ['Latitude', 'Longitude', 'Joining_Date']],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '12px', 'backgroundColor': colors['card'], 
                   'color': colors['text'], 'border': f'1px solid {colors["border"]}'},
        style_header={'backgroundColor': colors['primary'], 'color': 'white', 'fontWeight': 'bold', 
                     'border': f'1px solid {colors["border"]}', 'padding': '12px'},
        style_data={'border': f'1px solid {colors["border"]}'},
        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#252525'}],
        page_size=20, sort_action='native', filter_action='native'
    )
    
    return kpi_cards, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, data_table

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
