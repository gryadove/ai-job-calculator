import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Read historical data and clean column names
historical_df = pd.read_csv('Historical Labor Data.csv')
historical_df.columns = historical_df.columns.str.strip()

# Custom CSS for table formatting
st.markdown("""
    <style>
    .stDataFrame [data-testid="stDataFrameDataCell"] {
        text-align: right;
    }
    div[data-testid="stDataFrame"] div[data-testid="stDataFrameContainer"] div[role="columnheader"] {
        min-height: 150px !important;
        height: 200px !important;
        max-height: 200px !important;
        line-height: 1.2 !important;
        padding: 10px !important;
        white-space: normal;
        text-align: center;
        vertical-align: middle;
    }
    div[data-testid="stDataFrame"] div[data-testid="stDataFrameContainer"] div[role="columnheader"] div {
        text-align: center !important;
        justify-content: center !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Future of Jobs: AI Impact Calculator")

st.markdown("""
    Explore how artificial intelligence could reshape employment over the next decade. This interactive calculator 
    lets you simulate potential job market changes through 2033, focusing on:
    * Tier 1 Jobs - Most vulnerable to AI automation
    * Tier 2 Jobs - Moderately vulnerable to AI automation
    
    For Tier definitions and additional analysis read Substack (https://aiforstarters.substack.com/p/unemployment-in-the-age-of-ai.
    <br/>Adjust the parameters below to create different scenarios and see possible employment outcomes. Click on question mark icons for parameter definitions.  

    """)

# Optional: Add a visual separator
st.markdown("---")

# Create columns for inputs across the top
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("% of Jobs Lost in 2025: Tier-1 Jobs")
    high_initial = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        key="high_initial",
        help="Enter your assumption regarding % of total 1st Tier Content/Admin jobs that will be lost due to AI in 2025"
    ) 
#Addvertical space between inputs within col1
st.markdown("<div style='margin: 30px 0;'></div>",unsafe_allow_html=True)

    st.write("% Change in the Job Loss Rate Post 2025: Tier-1 Jobs")
    high_change = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=30.0,
        step=0.1,
        key="high_change",
        help="Enter the % increase in the initial 1st Tier Content/Admin job loss rate post 2025."
    ) 
with col2:
    st.write("% of Jobs Lost in 2025: Tier-2 Jobs")
    moderate_initial = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        key="moderate_initial",
        help="Enter your assumption regarding % of total 2nd Tier Content/Admin jobs that will be lost due to AI in 2025."
    ) 
#Addvertical space between inputs within col1
st.markdown("<div style='margin: 30px 0;'></div>",unsafe_allow_html=True)

    st.write("% Change in the Job Loss Rate Post 2025: Tier-2 Jobs")
    moderate_change = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=0.1,
        key="moderate_change",
        help="Enter the % increase in the initial 2nd Tier Content/Admin job loss rate post 2025."
    ) 

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
   # Convert input percentages to decimals for calculations
    high_impact_initial_rate = high_impact_initial_rate / 100
    moderate_impact_initial_rate = moderate_impact_initial_rate / 100
    high_impact_rate_change = high_impact_rate_change / 100
    moderate_impact_rate_change = moderate_impact_rate_change / 100

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
            '% Rate of Job Loss Tier 1 Jobs': round(high_rate * 100, 1),
            'Total # of Tier 1 Jobs (M)': round(current_high_impact_jobs, 2),
            '# of Tier 1 Jobs Lost (M)': round(high_impact_loss, 2),
            '% Rate of Job Loss Tier 2 Jobs': round(moderate_rate * 100, 1),
            'Total # of Tier 2 Jobs (M)': round(current_moderate_impact_jobs, 2),
            '# of Tier 2 Jobs Lost (M)': round(moderate_impact_loss, 2),
            'Total Number of Jobs Lost due to AI (M)': round(total_ai_job_loss, 2),
            'Total Number of Unemployed (M)': round(unemployed, 2),
              'Unemployment Rate (%)': round(unemployment_rate * 100, 1)
        })
    
    return pd.DataFrame(data)

# Add some space before the results
st.markdown("<div style='margin: 50px 0;'></div>", unsafe_allow_html=True)

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
        "Year": st.column_config.NumberColumn(format="%d", width="40px"),
        "Total Labor Force (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="Labor Force (M)"),
        "Total Civilians Employed (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="Employed (M)"),
        "% Rate of Job Loss Tier 1 Jobs": st.column_config.NumberColumn(format="%.1f%%", width="70px", label="T1 Job Loss Rate (%)"),
        "Total # of Tier 1 Jobs (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="T1 Jobs (M)"),
        "# of Tier 1 Jobs Lost (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="T1 Jobs Lost (M)"),
        "% Rate of Job Loss Tier 2 Jobs": st.column_config.NumberColumn(format="%.1f%%", width="70px", label="T2 Job Loss Rate (%)"),
        "Total # of Tier 2 Jobs (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="T2 Jobs (M)"),
        "# of Tier 2 Jobs Lost (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="T2 Jobs Lost (M)"),
        "Total Number of Jobs Lost due to AI (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="Total AI Job Loss (M)"),
        "Total Number of Unemployed (M)": st.column_config.NumberColumn(format="%.2f", width="small", label="Unemployed (M)"),
        "Unemployment Rate (%)": st.column_config.NumberColumn(format="%.1f%%", width="small", label="Unemp. Rate (%)")
    },
    use_container_width=True
)
# Add source citation with link right after the table
st.markdown("""
    <div style="font-size: 0.9em; color: #666; margin: 10px 0 30px 0;">
        Source: Initial values based on U.S. Bureau of Labor Statistics Current Population Survey (CPS), annual averages. 
        <a href="https://www.census.gov/programs-surveys/cps.html" target="_blank">CPS Details</a>
    </div>
""", unsafe_allow_html=True)

# Add space before visualizations
st.markdown("<div style='margin: 50px 0;'></div>", unsafe_allow_html=True)

# Create visualizations
st.subheader("Employement Trends in Age of AI")

# Create the combined dataframe
combined_df = pd.concat([
    historical_df[['Year', 'Total Labor Force (M)', 'Total Civilians Employed (M)', 'Unemployment Rate (%)']],
    df[['Year', 'Total Labor Force (M)', 'Total Civilians Employed (M)', 'Unemployment Rate (%)']]
], ignore_index=True)

# Create the first visualization
fig1 = px.line(combined_df, x='Year', y=['Total Labor Force (M)', 'Total Civilians Employed (M)'],
               title='Employment, Labor Force, and Unemployment Rate Trends (2000-2033)')

# Add Unemployment Rate on secondary y-axis
fig1.add_scatter(x=combined_df['Year'], 
                y=combined_df['Unemployment Rate (%)'],  # removed the str.rstrip('%') part
                name='Unemployment Rate (%)',
                yaxis='y2')

# Enhanced graph layout
fig1.update_layout(
    yaxis=dict(
        title='Millions of Workers',
        range=[100, 200],
        showgrid=True,
        zeroline=True,
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    yaxis2=dict(
        title='Unemployment Rate (%)',
        overlaying='y',
        side='right',
        range=[2, 25],
        showgrid=False,
        zeroline=True,
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    xaxis=dict(
        showgrid=True,
        zeroline=True,
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    legend=dict(
        x=0.7,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0.8)'
    ),
    margin=dict(t=50, b=50)
)

# Display the plot
st.plotly_chart(fig1, use_container_width=True)

# Add source citation for the graph
st.markdown("""
    <div style="font-size: 0.9em; color: #666; margin: 10px 0;">
        Source for 2020–2024: U.S. Bureau of Labor Statistics Current Population Survey (CPS), annual averages. 
        <a href="https://www.census.gov/programs-surveys/cps.html" target="_blank">CPS Details</a>. 2025-2033: Projected values based on input parameters
    </div>
""", unsafe_allow_html=True)
# Add final spacing
st.markdown("<div style='margin: 50px 0;'></div>", unsafe_allow_html=True)