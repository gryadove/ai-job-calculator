import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Custom CSS for table formatting
st.markdown("""
    <style>
    .stDataFrame [data-testid="stDataFrameDataCell"] {
        text-align: right;
    }
    .stDataFrame [data-testid="stHeaderCell"] {
        height: 80px;
        white-space: normal;
        text-align: center;
        vertical-align: middle;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("AI Job Impact Calculator")

# Create columns for inputs across the top
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("% of Jobs Lost in 2025: Tier-1 Jobs")
    high_initial = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        key="high_initial",
        help="Enter your assumption regarding % of total 1st Tier Content/Admin jobs that will be lost due to AI in 2025"
    ) / 100.0

    st.write("% Change in the Job Loss Rate Post 2025: Tier-1 Jobs")
    high_change = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        key="high_change",
        help="Enter the % increase in the initial 1st Tier Content/Admin job loss rate post 2025."
    ) / 100.0

with col2:
    st.write("% of Jobs Lost in 2025: Tier-2 Jobs")
    moderate_initial = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.1,
        key="moderate_initial",
        help="Enter your assumption regarding % of total 2nd Tier Content/Admin jobs that will be lost due to AI in 2025."
    ) / 100.0

    st.write("Change in the Job Loss Rate Post 2025: Tier-2 Jobs")
    moderate_change = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        key="moderate_change",
        help="Enter the % increase in the initial 2nd Tier Content/Admin job loss rate post 2025."
    ) / 100.0

with col3:
    st.write("Labor Force Growth (in millions)")
    labor_growth = st.number_input(
        "",
        min_value=0.0,
        max_value=5.0,
        value=0.620,
        step=0.001,
        format="%.3f",
        key="labor_growth",
        help="Per Bureau of Labor Statistics the expected change in U.S. labor force due to demographics and migration is forecasted to be 620,000 workers/year till 2033. If you believe that the annual labor force growth will be different, please enter the number of new workers expected to enter the labor force annually (in millions)."
    )

with col4:
    st.write("New Jobs Per Year (in millions)")
    new_jobs = st.number_input(
        "",
        min_value=0.0,
        max_value=10.0,
        value=1.084,
        step=0.001,
        format="%.3f",
        key="new_jobs",
        help="The 25-year historical average of Net Job Creation in the U.S. is 1.084 million jobs per year. The calculator assumes that the non-AI economy job formation will continue at this annual pace till 2033. If you believe that the annual job creation will be different, please enter the new jobs you expect annually (in millions)."
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
    base_labor_force = 169.2  # millions
    base_employed = 162.7    # millions
    high_impact_jobs = 22.74  # millions
    moderate_impact_jobs = 5.08  # millions
    
    years = range(2025, 2034)
    data = []
    
    for year in years:
        if year == 2025:
            high_rate = high_impact_initial_rate
            moderate_rate = moderate_impact_initial_rate
            labor_force = base_labor_force
            total_employed = base_employed
            prev_ai_job_loss = 0
            # Reset jobs to initial values for 2025
            current_high_impact_jobs = high_impact_jobs
            current_moderate_impact_jobs = moderate_impact_jobs
        else:
            high_rate = min(1.0, prev_high_rate * (1 + high_impact_rate_change))
            moderate_rate = min(1.0, prev_moderate_rate * (1 + moderate_impact_rate_change))
            labor_force = prev_labor_force + labor_force_growth
            total_employed = prev_employed + new_jobs_per_year - prev_ai_job_loss
            current_high_impact_jobs = prev_high_impact_jobs
            current_moderate_impact_jobs = prev_moderate_impact_jobs
        
        # Calculate job losses
        high_impact_loss = current_high_impact_jobs * high_rate
        moderate_impact_loss = current_moderate_impact_jobs * moderate_rate
        total_ai_job_loss = high_impact_loss + moderate_impact_loss
        
        # Update remaining impact jobs for next iteration
        next_high_impact_jobs = current_high_impact_jobs - high_impact_loss
        next_moderate_impact_jobs = current_moderate_impact_jobs - moderate_impact_loss
        
        # Calculate unemployment
        unemployed = labor_force - total_employed + total_ai_job_loss
        unemployment_rate = (unemployed / labor_force)
        
        # Store current values for next iteration
        prev_high_rate = high_rate
        prev_moderate_rate = moderate_rate
        prev_employed = total_employed
        prev_labor_force = labor_force
        prev_ai_job_loss = total_ai_job_loss
        prev_high_impact_jobs = next_high_impact_jobs
        prev_moderate_impact_jobs = next_moderate_impact_jobs
        
        data.append({
            'Year': year,
            'Total Labor Force (M)': round(labor_force, 2),
            'Total Civilians Employed (M)': round(total_employed, 2),
            '% Rate of Job Loss Tier 1 Jobs': f"{high_rate:.1%}",
            'Total # of Tier 1 Jobs (M)': round(current_high_impact_jobs, 2),
            '# of Tier 1 Jobs Lost (M)': round(high_impact_loss, 2),
            '% Rate of Job Loss Tier 2 Jobs': f"{moderate_rate:.1%}",
            'Total # of Tier 2 Jobs (M)': round(current_moderate_impact_jobs, 2),
            '# of Tier 2 Jobs Lost (M)': round(moderate_impact_loss, 2),
            'Total Number of Jobs Lost due to AI (M)': round(total_ai_job_loss, 2),
            'Total Number of Unemployed (M)': round(unemployed, 2),
            'Unemployment Rate (%)': f"{unemployment_rate:.1%}"
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
        "Year": st.column_config.NumberColumn(format="%d", width="small"),
        "Total Labor Force (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "Total Civilians Employed (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "% Rate of Job Loss Tier 1 Jobs": st.column_config.TextColumn(width="small"),
        "Total # of Tier 1 Jobs (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "# of Tier 1 Jobs Lost (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "% Rate of Job Loss Tier 2 Jobs": st.column_config.TextColumn(width="small"),
        "Total # of Tier 2 Jobs (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "# of Tier 2 Jobs Lost (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "Total Number of Jobs Lost due to AI (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "Total Number of Unemployed (M)": st.column_config.NumberColumn(format="%.2f", width="small"),
        "Unemployment Rate (%)": st.column_config.TextColumn(width="small")
    },
    use_container_width=True
)

# Create visualizations
st.subheader("Visualizations")

# Employment and Labor Force Trends
fig1 = px.line(df, x='Year', y=['Total Labor Force (M)', 'Total Civilians Employed (M)'],
               title='Employment and Labor Force Trends')
st.plotly_chart(fig1)

# Job Losses
fig2 = px.line(df, x='Year', 
               y=['# of Tier 1 Jobs Lost (M)', '# of Tier 2 Jobs Lost (M)', 'Total Number of Jobs Lost due to AI (M)'],
               title='AI-Related Job Losses')
st.plotly_chart(fig2)

# Unemployment Rate
fig3 = px.line(df, x='Year', y='Unemployment Rate (%)',
               title='Unemployment Rate Projection')
st.plotly_chart(fig3)