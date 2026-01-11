import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

st.set_page_config(page_title="Employee Analytics Dashboard", page_icon="👥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('../data/employee_extended_50.csv')
    df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
    df['Joining_Year'] = df['Joining_Date'].dt.year
    df['Tenure'] = (datetime.now() - df['Joining_Date']).dt.days / 365.25
    df['Joining_Date_Display'] = df['Joining_Date'].dt.strftime('%Y-%m-%d')
    return df

st.title("👥 Employee Analytics Dashboard")
st.markdown("---")

try:
    df = load_data()
    
    st.sidebar.header("🔍 Filters")
    
    departments = ['All'] + sorted(df['Dept'].unique().tolist())
    selected_dept = st.sidebar.selectbox("Department", departments)
    
    cities = ['All'] + sorted(df['City'].unique().tolist())
    selected_city = st.sidebar.selectbox("City", cities)
    
    age_range = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), 
                                   (int(df['Age'].min()), int(df['Age'].max())))
    
    salary_range = st.sidebar.slider("Salary Range", int(df['Sal'].min()), int(df['Sal'].max()), 
                                      (int(df['Sal'].min()), int(df['Sal'].max())), step=1000)
    
    filtered_df = df.copy()
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Dept'] == selected_dept]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1]) &
                              (filtered_df['Sal'] >= salary_range[0]) & (filtered_df['Sal'] <= salary_range[1])]
    
    st.header("📊 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Employees", len(filtered_df))
    with col2:
        st.metric("Avg Salary", f"₹{filtered_df['Sal'].mean():,.0f}")
    with col3:
        st.metric("Avg Experience", f"{filtered_df['Experience'].mean():.1f} yrs")
    with col4:
        st.metric("Avg Performance", f"{filtered_df['Per_score'].mean():.1f}%")
    with col5:
        st.metric("Departments", filtered_df['Dept'].nunique())
    
    st.markdown("---")
    
    st.header("🏢 Department & Location Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        dept_counts = filtered_df['Dept'].value_counts()
        fig1 = px.pie(values=dept_counts.values, names=dept_counts.index, 
                      title="Employee Distribution by Department", hole=0.4)
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        city_counts = filtered_df['City'].value_counts().head(10)
        fig2 = px.bar(x=city_counts.values, y=city_counts.index, orientation='h',
                      title="Top 10 Cities", labels={'x': 'Employees', 'y': 'City'})
        st.plotly_chart(fig2, use_container_width=True)
    
    st.header("💰 Salary Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        dept_salary = filtered_df.groupby('Dept')['Sal'].agg(['mean', 'max']).reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Average', x=dept_salary['Dept'], y=dept_salary['mean']))
        fig3.add_trace(go.Bar(name='Maximum', x=dept_salary['Dept'], y=dept_salary['max']))
        fig3.update_layout(title="Salary by Department", barmode='group')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = px.scatter(filtered_df, x='Experience', y='Sal', color='Dept', size='Per_score',
                         hover_data=['Name', 'Age'], title="Salary vs Experience")
        st.plotly_chart(fig4, use_container_width=True)
    
    st.header("📈 Performance & Demographics")
    col1, col2 = st.columns(2)
    
    with col1:
        fig5 = px.histogram(filtered_df, x='Per_score', nbins=20, title="Performance Score Distribution")
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        fig6 = px.box(filtered_df, x='Dept', y='Age', color='Dept', title="Age Distribution by Department")
        st.plotly_chart(fig6, use_container_width=True)
    
    st.header("🗺️ Geographical Distribution")
    
    fig7 = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', color='Dept', size='Sal',
                             hover_data=['Name', 'City'], title="Employee Distribution Map", zoom=3.5, height=500)
    fig7.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig7, use_container_width=True)
    
    st.header("📅 Hiring Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        hiring_trend = filtered_df.groupby('Joining_Year').size().reset_index(name='Count')
        fig8 = px.line(hiring_trend, x='Joining_Year', y='Count', title="Hiring Trends", markers=True)
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        dept_year = filtered_df.groupby(['Joining_Year', 'Dept']).size().reset_index(name='Count')
        fig9 = px.bar(dept_year, x='Joining_Year', y='Count', color='Dept', title="Department-wise Hiring")
        st.plotly_chart(fig9, use_container_width=True)
    
    st.header("🔬 Advanced Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        corr_matrix = filtered_df[['Age', 'Sal', 'Experience', 'Per_score']].corr()
        fig10 = px.imshow(corr_matrix, text_auto='.2f', title="Correlation Matrix")
        st.plotly_chart(fig10, use_container_width=True)
    
    with col2:
        tenure_dept = filtered_df.groupby('Dept')['Tenure'].mean().sort_values(ascending=False)
        fig11 = px.bar(x=tenure_dept.values, y=tenure_dept.index, orientation='h', title="Average Tenure by Department")
        st.plotly_chart(fig11, use_container_width=True)
    
    st.header("📋 Employee Data")
    
    search_term = st.text_input("Search by Name", "")
    display_df = filtered_df[filtered_df['Name'].str.contains(search_term, case=False, na=False)] if search_term else filtered_df
    
    display_table = display_df.copy()
    display_table['Joining_Date'] = display_table['Joining_Date_Display']
    display_table = display_table.drop(columns=['Joining_Date_Display'])
    
    max_rows = len(display_table)
    default_rows = min(10, max_rows)
    rows_to_show = st.number_input("Rows to display", min_value=1, max_value=max(1, max_rows), value=default_rows)
    st.dataframe(display_table.head(rows_to_show), use_container_width=True)
    
    csv = display_table.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", csv, f'employee_data_{datetime.now().strftime("%Y%m%d")}.csv', 'text/csv')
    
    st.header("📊 Summary Statistics")
    st.dataframe(filtered_df.select_dtypes(include=[np.number]).describe(), use_container_width=True)
    
except FileNotFoundError:
    st.error("Data file not found! Ensure 'employee_extended_50.csv' is in '../data/' directory.")
except Exception as e:
    st.error(f"Error: {str(e)}")
