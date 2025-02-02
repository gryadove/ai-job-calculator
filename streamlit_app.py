import streamlit as st
import pandas as pd
import plotly.express as px

st.title("AI Job Impact Calculator")

# Create columns for inputs across the top
col1, col2, col3, col4 = st.columns(4)

with col1:
    high_initial = st.number_input(
        "Initial High Impact Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        help="Enter the initial rate of job displacement for high-impact jobs"
    ) / 100.0

    high_change = st.number_input(
        "High Impact Rate Change (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        help="Enter the annual change in high-impact displacement rate"
    ) / 100.0

with col2:
    moderate_initial = st.number_input(
        "Initial Moderate Impact Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.1,
        help="Enter the initial rate of job displacement for moderate-impact jobs"
    ) / 100.0

    moderate_change = st.number_input(
        "Moderate Impact Rate Change (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        help="Enter the annual change in moderate-impact displacement rate"
    ) / 100.0

with col3:
    labor_growth = st.number_input(
        "Labor Force Growth (in millions)",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Enter the expected annual growth in labor force (in millions)"
    )

with col4:
    new_jobs = st.number_input(
        "New Jobs per Year (in millions)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1,
        help="Enter the number of new jobs expected to be created annually (in millions)"
    )

def calculate_projections(
    high_impact_initial_rate,
    moderate_impact_initial_rate,
    high_impact_rate_change,
    moderate_impact_rate_change,
    labor_force_growth,
    new_jobs_per_year
):
    # Initial values for 2024
    base_labor_force = 168.5  # millions
    base_employed = 161.7    # millions
    high_impact_jobs = 22.74  # millions
    moderate_impact_jobs = 5.08  # millions
    
    years = range(2025, 2034)
    data = []
    
    for year in years:
        # Calculate rates (ensuring they don't exceed 100%)
        if year == 2025:
            high_rate = high_impact_initial_rate
            moderate_rate = moderate_impact_initial_rate
            labor_force = base_labor_force
            total_employed = base_employed
            prev_ai_job_loss = 0  # Initialize for first year
        else:
            high_rate = min(1.0, prev_high_rate * (1 + high_impact_rate_change))
            moderate_rate = min(1.0, prev_moderate_rate * (1 + moderate_impact_rate_change))
            labor_force = prev_labor_force + labor_force_growth
            total_employed = prev_employed + new_jobs_per_year - prev_ai_job_loss  # Use previous year's job loss
            
        # Calculate job losses
        high_impact_loss = high_impact_jobs * high_rate
        moderate_impact_loss = moderate_impact_jobs * moderate_rate
        total_ai_job_loss = high_impact_loss + moderate_impact_loss
        
        # Update remaining impact jobs
        high_impact_jobs -= high_impact_loss
        moderate_impact_jobs -= moderate_impact_loss
        
        # Calculate unemployment (modified formula)
        unemployed = labor_force - total_employed + total_ai_job_loss
        unemployment_rate = (unemployed / labor_force)
        
        # Store current values for next iteration
        prev_high_rate = high_rate
        prev_moderate_rate = moderate_rate
        prev_employed = total_employed
        prev_labor_force = labor_force
        prev_ai_job_loss = total_ai_job_loss  # Store for next iteration
        
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

# Add some space before the results
st.markdown("---")

# Calculate and display results
df = calculate_projections(
    high_initial,
    moderate_initial,
    high_change,
    moderate_change,
    labor_growth,
    new_jobs
)

# Display results
st.subheader("Projected Impact of AI on Employment")
st.dataframe(
    df,
    hide_index=True,
    column_config={
        "Year": st.column_config.NumberColumn(format="%d"),
    },
    use_container_width=True
)

# Create visualizations
st.subheader("Visualizations")

# Employment and Labor Force Trends
fig1 = px.line(df, x='Year', y=['Civilian_Labor_Force', 'Total_Employed'],
               title='Employment and Labor Force Trends')
st.plotly_chart(fig1)

# Job Losses
fig2 = px.line(df, x='Year', y=['High_Impact_Jobs_Lost', 'Moderate_Impact_Jobs_Lost', 'Total_AI_Job_Loss'],
               title='AI-Related Job Losses')
st.plotly_chart(fig2)

# Unemployment Rate
fig3 = px.line(df, x='Year', y='Unemployment_Rate',
               title='Unemployment Rate Projection')
st.plotly_chart(fig3)