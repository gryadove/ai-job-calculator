import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Read historical data and clean column names
historical_df = pd.read_csv('Historical Labor Data.csv')
historical_df.columns = historical_df.columns.str.strip()

# Custom CSS for inputs and table formatting
st.markdown("""
    <style>
    .input-group {
        display: flex;
        margin-bottom: 20px;
    }
    .input-content {
        flex: 2;
    }
    .input-title {
        font-size: 1.1em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .input-description {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 10px;
    }
    .input-field {
        flex: 1;
        margin-left: 20px;
    }
    .stDataFrame [data-testid="stDataFrameDataCell"] {
        text-align: right;
    }
    .stDataFrame [data-testid="stHeaderCell"] {
        height: 100px;
        white-space: normal;
        text-align: center;
        vertical-align: middle;
        padding: 10px;
        font-size: 0.9em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("AI Job Impact Calculator")

# Create columns for inputs across the top
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="input-group">
            <div class="input-content">
                <div class="input-title">% of Jobs Lost in 2025: Tier-1 Jobs</div>
                <div class="input-description">Enter your assumption regarding % of total 1st Tier Content/Admin jobs that will be lost due to AI in 2025</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    high_initial = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        key="high_initial"
    ) / 100.0

    st.markdown("""
        <div class="input-group">
            <div class="input-content">
                <div class="input-title">% Change in the Job Loss Rate Post 2025: Tier-1 Jobs</div>
                <div class="input-description">Enter the % increase in the initial 1st Tier Content/Admin job loss rate post 2025.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    high_change = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        key="high_change"
    ) / 100.0

with col2:
    st.markdown("""
        <div class="input-group">
            <div class="input-content">
                <div class="input-title">% of Jobs Lost in 2025: Tier-2 Jobs</div>
                <div class="input-description">Enter your assumption regarding % of total 2nd Tier Content/Admin jobs that will be lost due to AI in 2025.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    moderate_initial = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.1,
        key="moderate_initial"
    ) / 100.0

    st.markdown("""
        <div class="input-group">
            <div class="input-content">
                <div class="input-title">Change in the Job Loss Rate Post 2025: Tier-2 Jobs</div>
                <div class="input-description">Enter the % increase in the initial 2nd Tier Content/Admin job loss rate post 2025.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    moderate_change = st.number_input(
        "",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        key="moderate_change"
    ) / 100.0

with col3:
    st.markdown("""
        <div class="input-group">
            <div class="input-content">
                <div class="input-title">Labor Force Growth (in millions)</div>
                <div class="input-description">Per Bureau of Labor Statistics the expected change in U.S. labor force due to demographics and migration is forecasted to be 620,000 workers/year till 2033.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    labor_growth = st.number_input(
        "",
        min_value=0.0,
        max_value=5.0,
        value=0.620,
        step=0.001,
        format="%.3f",
        key="labor_growth"
    )

with col4:
    st.markdown("""
        <div class="input-group">
            <div class="input-content">
                <div class="input-title">New Jobs Per Year (in millions)</div>
                <div class="input-description">The 25-year historical average of Net Job Creation in the U.S. is 1.084 million jobs per year.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    new_jobs = st.number_input(
        "",
        min_value=0.0,
        max_value=10.0,
        value=1.084,
        step=0.001,
        format="%.3f",
        key="new_jobs"
    )
  def calculate_projections(
    high_impact_initial_rate,
    moderate_impact_initial_rate,
    high_impact_rate_change,
    moderate_impact_rate_change,
    labor_force_growth,
    new_jobs_per_year
):
    # [Keep the existing calculation function as is - no changes needed]
    # Your original calculation code here...

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

# Add space before visualizations
st.markdown("<div style='margin: 50px 0;'></div>", unsafe_allow_html=True)

# Create visualizations
st.subheader("Visualizations")

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
                y=combined_df['Unemployment Rate (%)'].str.rstrip('%').astype(float), 
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

# Add final spacing
st.markdown("<div style='margin: 50px 0;'></div>", unsafe_allow_html=True)