"""
Employee Data Analysis Dashboard using Streamlit
This dashboard provides comprehensive analysis of employee data including
salary trends, department distribution, experience analysis, and geographical insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Employee Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and prepare employee data"""
    df = pd.read_csv('../data/employee_extended_50.csv')
    df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
    df['Joining_Year'] = df['Joining_Date'].dt.year
    df['Tenure'] = (datetime.now() - df['Joining_Date']).dt.days / 365.25
    return df

# Main title
st.markdown('<div class="main-header">👥 Employee Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# Load data
try:
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Department filter
    departments = ['All'] + sorted(df['Dept'].unique().tolist())
    selected_dept = st.sidebar.selectbox("Select Department", departments)
    
    # City filter
    cities = ['All'] + sorted(df['City'].unique().tolist())
    selected_city = st.sidebar.selectbox("Select City", cities)
    
    # Age range filter
    age_range = st.sidebar.slider(
        "Age Range",
        int(df['Age'].min()),
        int(df['Age'].max()),
        (int(df['Age'].min()), int(df['Age'].max()))
    )
    
    # Salary range filter
    salary_range = st.sidebar.slider(
        "Salary Range",
        int(df['Sal'].min()),
        int(df['Sal'].max()),
        (int(df['Sal'].min()), int(df['Sal'].max())),
        step=1000
    )
    
    # Apply filters
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
    
    # Key Metrics
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
    
    # Row 1: Department and City Analysis
    st.header("🏢 Department & Location Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Department Distribution
        dept_counts = filtered_df['Dept'].value_counts()
        fig1 = px.pie(
            values=dept_counts.values,
            names=dept_counts.index,
            title="Employee Distribution by Department",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # City Distribution
        city_counts = filtered_df['City'].value_counts().head(10)
        fig2 = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation='h',
            title="Top 10 Cities by Employee Count",
            labels={'x': 'Number of Employees', 'y': 'City'},
            color=city_counts.values,
            color_continuous_scale='Viridis'
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Salary Analysis
    st.header("💰 Salary Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary by Department
        dept_salary = filtered_df.groupby('Dept')['Sal'].agg(['mean', 'min', 'max']).reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Average', x=dept_salary['Dept'], y=dept_salary['mean'], marker_color='lightblue'))
        fig3.add_trace(go.Bar(name='Maximum', x=dept_salary['Dept'], y=dept_salary['max'], marker_color='darkblue'))
        fig3.update_layout(
            title="Salary Distribution by Department",
            xaxis_title="Department",
            yaxis_title="Salary (₹)",
            barmode='group'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Salary vs Experience Scatter
        fig4 = px.scatter(
            filtered_df,
            x='Experience',
            y='Sal',
            color='Dept',
            size='Per_score',
            hover_data=['Name', 'Age', 'City'],
            title="Salary vs Experience (Size: Performance Score)",
            labels={'Sal': 'Salary (₹)', 'Experience': 'Years of Experience'}
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Row 3: Performance and Age Analysis
    st.header("📈 Performance & Demographics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance Score Distribution
        fig5 = px.histogram(
            filtered_df,
            x='Per_score',
            nbins=20,
            title="Performance Score Distribution",
            labels={'Per_score': 'Performance Score', 'count': 'Number of Employees'},
            color_discrete_sequence=['#636EFA']
        )
        fig5.update_layout(showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Age Distribution by Department
        fig6 = px.box(
            filtered_df,
            x='Dept',
            y='Age',
            color='Dept',
            title="Age Distribution by Department",
            labels={'Age': 'Age (years)', 'Dept': 'Department'}
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # Row 4: Geographical Analysis
    st.header("🗺️ Geographical Distribution")
    
    # Map visualization
    fig7 = px.scatter_mapbox(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        color='Dept',
        size='Sal',
        hover_data=['Name', 'City', 'Sal', 'Experience'],
        title="Employee Distribution Across India",
        zoom=3.5,
        height=500
    )
    fig7.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig7, use_container_width=True)
    
    # Row 5: Hiring Trends
    st.header("📅 Hiring Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        # Hiring by Year
        hiring_trend = filtered_df.groupby('Joining_Year').size().reset_index(name='Count')
        fig8 = px.line(
            hiring_trend,
            x='Joining_Year',
            y='Count',
            title="Hiring Trends Over Years",
            labels={'Joining_Year': 'Year', 'Count': 'Number of Employees'},
            markers=True
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        # Department-wise Hiring
        dept_year = filtered_df.groupby(['Joining_Year', 'Dept']).size().reset_index(name='Count')
        fig9 = px.bar(
            dept_year,
            x='Joining_Year',
            y='Count',
            color='Dept',
            title="Department-wise Hiring Trends",
            labels={'Joining_Year': 'Year', 'Count': 'Number of Employees'}
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    # Row 6: Advanced Analytics
    st.header("🔬 Advanced Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation Heatmap
        corr_cols = ['Age', 'Sal', 'Experience', 'Per_score']
        corr_matrix = filtered_df[corr_cols].corr()
        fig10 = px.imshow(
            corr_matrix,
            text_auto='.2f',
            title="Correlation Matrix",
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    with col2:
        # Tenure Analysis
        tenure_dept = filtered_df.groupby('Dept')['Tenure'].mean().sort_values(ascending=False)
        fig11 = px.bar(
            x=tenure_dept.values,
            y=tenure_dept.index,
            orientation='h',
            title="Average Tenure by Department",
            labels={'x': 'Average Tenure (years)', 'y': 'Department'},
            color=tenure_dept.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig11, use_container_width=True)
    
    # Data Table
    st.header("📋 Employee Data Table")
    
    # Search functionality
    search_term = st.text_input("🔍 Search by Name", "")
    if search_term:
        display_df = filtered_df[filtered_df['Name'].str.contains(search_term, case=False, na=False)]
    else:
        display_df = filtered_df
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col1:
        show_all = st.checkbox("Show all rows", False)
    with col2:
        rows_to_show = st.number_input("Rows to display", min_value=5, max_value=len(display_df), value=10)
    
    if show_all:
        st.dataframe(display_df, use_container_width=True)
    else:
        st.dataframe(display_df.head(rows_to_show), use_container_width=True)
    
    # Download option
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f'employee_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
    )
    
    # Summary Statistics
    st.header("📊 Summary Statistics")
    st.dataframe(filtered_df.describe(), use_container_width=True)
    
except FileNotFoundError:
    st.error("❌ Data file not found! Please ensure 'employee_extended_50.csv' is in the '../data/' directory.")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Employee Analytics Dashboard | Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
