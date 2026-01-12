import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Employee Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('../data/employee_extended_50.csv')
    df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
    df['Joining_Year'] = df['Joining_Date'].dt.year
    return df

st.title("Employee Analytics Dashboard")
st.markdown("---")
df = load_data()

st.sidebar.header("Filters")
departments = ['All'] + sorted(df['Dept'].unique().tolist())
selected_dept = st.sidebar.selectbox("Department", departments)

filtered_df = df.copy()
if selected_dept != 'All':
    filtered_df = filtered_df[filtered_df['Dept'] == selected_dept]

st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Employees", len(filtered_df))
with col2:
    st.metric("Avg Salary", f"₹{filtered_df['Sal'].mean():,.0f}")
with col3:
    st.metric("Avg Experience", f"{filtered_df['Experience'].mean():.1f} yrs")
with col4:
    st.metric("Departments", filtered_df['Dept'].nunique())

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    dept_counts = filtered_df['Dept'].value_counts()
    fig1 = px.pie(values=dept_counts.values, names=dept_counts.index, 
                  title="Employee Distribution by Department")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.scatter(filtered_df, x='Experience', y='Sal', color='Dept',
                     hover_data=['Name'], title="Salary vs Experience")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig3 = px.histogram(filtered_df, x='Per_score', nbins=20, 
                       title="Performance Score Distribution")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    hiring_trend = filtered_df.groupby('Joining_Year').size().reset_index(name='Count')
    fig4 = px.line(hiring_trend, x='Joining_Year', y='Count', 
                  title="Hiring Trends", markers=True)
    st.plotly_chart(fig4, use_container_width=True)