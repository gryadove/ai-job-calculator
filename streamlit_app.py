import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page title and description
st.title('AI Job Impact Calculator')

# Sidebar with explanatory text and inputs
st.sidebar.markdown("""
    ### About the Assumptions
    * **Labor Force Growth:** Default is 620,000/year (U.S. Bureau of Labor Forecast)
    * **Historical Job Creation:** Default is 1,084,000/year (based on historical average)
    * Adjust other values to see different scenarios
""")

with st.sidebar:
    st.header('Input Parameters')
    high_initial = st.number_input('Initial High Impact Job Loss Rate (2025)', 
                                 value=0.05, min_value=0.0, max_value=1.0, format="%.3f")
    moderate_initial = st.number_input('Initial Moderate Impact Job Loss Rate (2025)', 
                                    value=0.025, min_value=0.0, max_value=1.0, format="%.3f")
    high_change = st.number_input('High Impact Rate Annual Change', 
                               value=0.30, min_value=0.0, max_value=5.0, format="%.3f")
    moderate_change = st.number_input('Moderate Impact Rate Annual Change', 
                                  value=0.20, min_value=0.0, max_value=5.0, format="%.3f")
    # Pre-filled values for these two inputs
    labor_growth = st.number_input('Annual Labor Force Growth (millions)', 
                                value=0.62, format="%.2f")
    new_jobs = st.number_input('New Jobs Created Annually', 
                            value=1084000, format="%d")

def calculate_projections(
    high_impact_initial_rate,
    moderate_impact_initial_rate,
    high_impact_rate_change,
    moderate_impact_rate_change,
    labor_force_growth,
    new_jobs_per_year
):
    # Initial values for 2024
    base_labor_force = 168.5
    base_employed = 161.7
    high_impact_jobs = 22.74
    moderate_impact_jobs = 5.08
    
    years = range(2025, 2034)
    data = []
    
    for year in years:
        # Calculate rates (ensuring they don't exceed 100%)
        if year == 2025:
            high_rate = high_impact_initial_rate
            moderate_rate = moderate_impact_initial_rate
        else:
            high_rate = min(1.0, prev_high_rate * (1 + high_impact_rate_change))
            moderate_rate = min(1.0, prev_moderate_rate * (1 + moderate_impact_rate_change))
            
        # Calculate labor force and employment
        labor_force = base_labor_force + (labor_force_growth * (year - 2024))
        
        # Calculate job losses
        high_impact_loss = high_impact_jobs * high_rate
        moderate_impact_loss = moderate_impact_jobs * moderate_rate
        total_ai_job_loss = high_impact_loss + moderate_impact_loss
        
        # Update remaining impact jobs
        high_impact_jobs -= high_impact_loss
        moderate_impact_jobs -= moderate_impact_loss
        
        # Calculate total employment
        if year == 2025:
            total_employed = base_employed + new_jobs_per_year/1000000 - total_ai_job_loss
        else:
            total_employed = prev_employed + new_jobs_per_year/1000000 - total_ai_job_loss
            
        # Calculate unemployment
        unemployed = labor_force - total_employed
        unemployment_rate = (unemployed / labor_force) * 100
        
        # Store current values for next iteration
        prev_high_rate = high_rate
        prev_moderate_rate = moderate_rate
        prev_employed = total_employed
        
        # Add to results
        data.append({
            'Year': year,
            'Civilian_Labor_Force': round(labor_force, 1),
            'Total_Employed': round(total_employed, 1),
            'High_Impact_Rate': f"{high_rate:.1%}",
            'High_Impact_Jobs_Lost': round(high_impact_loss, 2),
            'Moderate_Impact_Rate': f"{moderate_rate:.1%}",
            'Moderate_Impact_Jobs_Lost': round(moderate_impact_loss, 2),
            'Total_AI_Job_Loss': round(total_ai_job_loss, 2),
            'Unemployed': round(unemployed, 2),
            'Unemployment_Rate': f"{unemployment_rate:.1%}"
        })
    
    return pd.DataFrame(data)

# Calculate and display results
df = calculate_projections(
    high_initial,
    moderate_initial,
    high_change,
    moderate_change,
    labor_growth,
    new_jobs
)

st.dataframe(df)

# Visualizations
# Employment Impact Chart
fig1 = px.line(df, x='Year', 
               y=['Civilian_Labor_Force', 'Total_Employed'],
               title='Labor Force and Employment Projections')
st.plotly_chart(fig1)

# Job Loss Chart
fig2 = px.line(df, x='Year', 
               y=['High_Impact_Jobs_Lost', 'Moderate_Impact_Jobs_Lost', 'Total_AI_Job_Loss'],
               title='AI-Related Job Losses Over Time')
st.plotly_chart(fig2)

# Unemployment Rate Chart
fig3 = px.line(df, x='Year', y='Unemployment_Rate',
               title='Projected Unemployment Rate')
st.plotly_chart(fig3)