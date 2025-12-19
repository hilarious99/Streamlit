import streamlit as st
import plotly.express as px
from scripts.data_loader import (
    load_passenger_flow, 
    load_cargo_flow, 
    load_governance_flags,
    load_opportunity_scores
)
from scripts.metrics import calculate_total_passengers, calculate_total_cargo
from scripts.pipeline import run_scoring_pipeline

# Page configuration
st.set_page_config(
    page_title="AlgoEconomics – UK–Africa Aviation & Tourism (Beta)",
    layout="wide"
)

# Page title
st.title("AlgoEconomics – UK–Africa Aviation & Tourism (Beta)")

# Run scoring pipeline (with error handling)
scoring_success = False
try:
    governance_df_computed, opportunity_df_computed = run_scoring_pipeline()
    if governance_df_computed is not None and opportunity_df_computed is not None:
        scoring_success = True
except Exception as e:
    st.warning(f"Scoring pipeline encountered an issue: {str(e)}. Dashboard will continue with base data only.")

# Show info banner if scoring succeeded
if scoring_success:
    st.info("✅ Procurement readiness scores computed successfully")

# Load base data
passenger_df = load_passenger_flow()
cargo_df = load_cargo_flow()

# Load computed scores (with graceful fallback)
governance_df = load_governance_flags()
opportunity_df = load_opportunity_scores()

# Country filter (single select, default = All)
# Get countries from opportunity scores (primary source) or other data sources
all_countries = set()
if not opportunity_df.empty:
    all_countries.update(opportunity_df['country'].unique())
if not passenger_df.empty:
    all_countries.update(passenger_df['country'].unique())
if not cargo_df.empty:
    all_countries.update(cargo_df['country'].unique())
if not governance_df.empty:
    all_countries.update(governance_df['country'].unique())

country_list = ['All'] + sorted(list(all_countries))
selected_country = st.selectbox("Select Country", country_list, index=0)

# Filter data based on selected country
if selected_country != 'All':
    # Filter passenger data if not empty
    if not passenger_df.empty and 'country' in passenger_df.columns:
        passenger_df_filtered = passenger_df[passenger_df['country'] == selected_country].copy()
    else:
        passenger_df_filtered = passenger_df.copy()
    
    # Filter cargo data if not empty
    if not cargo_df.empty and 'country' in cargo_df.columns:
        cargo_df_filtered = cargo_df[cargo_df['country'] == selected_country].copy()
    else:
        cargo_df_filtered = cargo_df.copy()
    
    # Filter governance data if not empty
    if not governance_df.empty and 'country' in governance_df.columns:
        governance_df_filtered = governance_df[governance_df['country'] == selected_country].copy()
    else:
        governance_df_filtered = governance_df.copy()
    
    # Filter opportunity data if not empty
    if not opportunity_df.empty and 'country' in opportunity_df.columns:
        opportunity_df_filtered = opportunity_df[opportunity_df['country'] == selected_country].copy()
    else:
        opportunity_df_filtered = opportunity_df.copy()
else:
    passenger_df_filtered = passenger_df.copy()
    cargo_df_filtered = cargo_df.copy()
    governance_df_filtered = governance_df.copy()
    opportunity_df_filtered = opportunity_df.copy()

# Create tabs
tab1, tab2 = st.tabs(["Aviation", "Tourism & Hospitality"])

# Aviation Tab
with tab1:
    st.header("Aviation")
    
    # Passenger Volume Chart
    if not passenger_df_filtered.empty:
        st.subheader("Passenger Volume by Country")
        fig_passenger = px.bar(
            passenger_df_filtered,
            x='country',
            y='passenger_volume',
            labels={'country': 'Country', 'passenger_volume': 'Passenger Volume'},
            title="Passenger Volume by Country"
        )
        st.plotly_chart(fig_passenger, use_container_width=True, key="aviation_passenger_chart")
    
    # Cargo Tonnage Chart
    if not cargo_df_filtered.empty:
        st.subheader("Cargo Tonnage by Country")
        fig_cargo = px.bar(
            cargo_df_filtered,
            x='country',
            y='cargo_tonnage',
            labels={'country': 'Country', 'cargo_tonnage': 'Cargo Tonnage'},
            title="Cargo Tonnage by Country"
        )
        st.plotly_chart(fig_cargo, use_container_width=True, key="aviation_cargo_chart")
    
    # Summary Metrics
    st.subheader("Summary Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        total_passengers = calculate_total_passengers(passenger_df_filtered)
        st.metric("Total Passengers", f"{total_passengers:,}")
    
    with col2:
        total_cargo = calculate_total_cargo(cargo_df_filtered)
        st.metric("Total Cargo (Tonnage)", f"{total_cargo:,}")
    
    # Computed Scores Section
    if not opportunity_df_filtered.empty:
        st.subheader("Procurement Readiness Scores")
        
        # Check if new structure (with sector) or old structure
        has_sector = 'sector' in opportunity_df_filtered.columns and 'procurement_readiness_score' in opportunity_df_filtered.columns
        
        if has_sector:
            # New structure: Filter for Aviation sector
            aviation_scores = opportunity_df_filtered[opportunity_df_filtered['sector'] == 'Aviation'].copy()
            
            if not aviation_scores.empty:
                fig_opportunity = px.bar(
                    aviation_scores,
                    x='country',
                    y='procurement_readiness_score',
                    labels={'country': 'Country', 'procurement_readiness_score': 'Procurement Readiness Score'},
                    title="Aviation Procurement Readiness Score by Country"
                )
                st.plotly_chart(fig_opportunity, use_container_width=True, key="aviation_opportunity_chart")
            
            # Score Metrics
            col1, col2 = st.columns(2)
            with col1:
                aviation_scores = opportunity_df_filtered[opportunity_df_filtered['sector'] == 'Aviation']
                if not aviation_scores.empty:
                    avg_aviation = aviation_scores['procurement_readiness_score'].mean()
                    st.metric("Avg Aviation Procurement Score", f"{avg_aviation:.1f}")
            with col2:
                tourism_scores = opportunity_df_filtered[opportunity_df_filtered['sector'] == 'Tourism & Hospitality']
                if not tourism_scores.empty:
                    avg_tourism = tourism_scores['procurement_readiness_score'].mean()
                    st.metric("Avg Tourism Procurement Score", f"{avg_tourism:.1f}")
        else:
            # Old structure: backward compatibility
            if 'combined_opportunity_score' in opportunity_df_filtered.columns:
                fig_opportunity = px.bar(
                    opportunity_df_filtered,
                    x='country',
                    y='combined_opportunity_score',
                    labels={'country': 'Country', 'combined_opportunity_score': 'Combined Opportunity Score'},
                    title="Combined Opportunity Score by Country"
                )
                st.plotly_chart(fig_opportunity, use_container_width=True, key="aviation_combined_opportunity_chart")
            
            # Score Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'aviation_score' in opportunity_df_filtered.columns:
                    avg_aviation = opportunity_df_filtered['aviation_score'].mean()
                    st.metric("Avg Aviation Score", f"{avg_aviation:.2f}")
            with col2:
                if 'tourism_score' in opportunity_df_filtered.columns:
                    avg_tourism = opportunity_df_filtered['tourism_score'].mean()
                    st.metric("Avg Tourism Score", f"{avg_tourism:.2f}")
            with col3:
                if 'combined_opportunity_score' in opportunity_df_filtered.columns:
                    avg_combined = opportunity_df_filtered['combined_opportunity_score'].mean()
                    st.metric("Avg Combined Score", f"{avg_combined:.2f}")
    
    # Governance Flags Section
    if not governance_df_filtered.empty:
        st.subheader("Governance Flags")
        
        # Governance Flags - Create count for visualization
        governance_counts = governance_df_filtered['governance_flag'].value_counts().reset_index()
        governance_counts.columns = ['governance_flag', 'count']
        
        if not governance_counts.empty:
            fig_governance_aviation = px.bar(
                governance_counts,
                x='governance_flag',
                y='count',
                labels={'governance_flag': 'Governance Flag', 'count': 'Number of Countries'},
                title="Governance Flags Distribution",
                color='governance_flag',
                color_discrete_map={'HIGH': '#2ecc71', 'LOW': '#e74c3c'}
            )
            st.plotly_chart(fig_governance_aviation, use_container_width=True, key="aviation_governance_chart")
    
    # Data Table Preview
    st.subheader("Data Preview")
    
    if not passenger_df_filtered.empty:
        st.write("**Passenger Flow Data**")
        st.dataframe(passenger_df_filtered, use_container_width=True)
    
    if not cargo_df_filtered.empty:
        st.write("**Cargo Flow Data**")
        st.dataframe(cargo_df_filtered, use_container_width=True)
    
    if not opportunity_df_filtered.empty:
        st.write("**Opportunity Scores**")
        st.dataframe(opportunity_df_filtered, use_container_width=True)
    
    if not governance_df_filtered.empty:
        st.write("**Governance Flags**")
        st.dataframe(governance_df_filtered, use_container_width=True)

# Tourism Tab
with tab2:
    st.header("Tourism & Hospitality")
    
    # Computed Scores Section
    if not opportunity_df_filtered.empty:
        st.subheader("Tourism Procurement Readiness Scores")
        
        # Check if new structure (with sector) or old structure
        has_sector = 'sector' in opportunity_df_filtered.columns and 'procurement_readiness_score' in opportunity_df_filtered.columns
        
        if has_sector:
            # New structure: Filter for Tourism & Hospitality sector
            tourism_scores = opportunity_df_filtered[opportunity_df_filtered['sector'] == 'Tourism & Hospitality'].copy()
            
            if not tourism_scores.empty:
                fig_tourism_score = px.bar(
                    tourism_scores,
                    x='country',
                    y='procurement_readiness_score',
                    labels={'country': 'Country', 'procurement_readiness_score': 'Procurement Readiness Score'},
                    title="Tourism Procurement Readiness Score by Country"
                )
                st.plotly_chart(fig_tourism_score, use_container_width=True, key="tourism_procurement_chart")
                
                # Summary Metrics
                st.subheader("Summary Metrics")
                avg_tourism_score = tourism_scores['procurement_readiness_score'].mean()
                max_tourism_score = tourism_scores['procurement_readiness_score'].max()
                min_tourism_score = tourism_scores['procurement_readiness_score'].min()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Score", f"{avg_tourism_score:.1f}")
                with col2:
                    st.metric("Highest Score", f"{max_tourism_score:.1f}")
                with col3:
                    st.metric("Lowest Score", f"{min_tourism_score:.1f}")
        else:
            # Old structure: backward compatibility
            if 'tourism_score' in opportunity_df_filtered.columns:
                fig_tourism_score = px.bar(
                    opportunity_df_filtered,
                    x='country',
                    y='tourism_score',
                    labels={'country': 'Country', 'tourism_score': 'Tourism Score'},
                    title="Tourism Score by Country"
                )
                st.plotly_chart(fig_tourism_score, use_container_width=True, key="tourism_score_chart")
    
    # Governance Flags Section
    if not governance_df_filtered.empty:
        st.subheader("Governance Flags")
        
        # Governance Flags - Create count for visualization
        governance_counts = governance_df_filtered['governance_flag'].value_counts().reset_index()
        governance_counts.columns = ['governance_flag', 'count']
        
        if not governance_counts.empty:
            fig_governance_tourism = px.bar(
                governance_counts,
                x='governance_flag',
                y='count',
                labels={'governance_flag': 'Governance Flag', 'count': 'Number of Countries'},
                title="Governance Flags Distribution",
                color='governance_flag',
                color_discrete_map={'HIGH': '#2ecc71', 'LOW': '#e74c3c'}
            )
            st.plotly_chart(fig_governance_tourism, use_container_width=True, key="tourism_governance_chart")
    
    # Data Table Preview
    st.subheader("Data Preview")
    
    if not opportunity_df_filtered.empty:
        # Show only Tourism & Hospitality sector data
        tourism_data = opportunity_df_filtered[opportunity_df_filtered['sector'] == 'Tourism & Hospitality']
        if not tourism_data.empty:
            st.write("**Tourism & Hospitality Opportunity Scores**")
            st.dataframe(tourism_data, use_container_width=True)
    
    if not governance_df_filtered.empty:
        st.write("**Governance Flags**")
        st.dataframe(governance_df_filtered, use_container_width=True)

