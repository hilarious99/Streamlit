import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_passenger_flow():
    """Load passenger flow data from CSV."""
    file_path = Path(__file__).parent.parent / "data" / "processed" / "fact_route_passenger_flow.csv"
    
    try:
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['country', 'year', 'passenger_volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
        
        return df
    except Exception as e:
        st.error(f"Error loading passenger flow data: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_cargo_flow():
    """Load cargo flow data from CSV."""
    file_path = Path(__file__).parent.parent / "data" / "processed" / "fact_route_cargo_flow.csv"
    
    try:
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['country', 'year', 'cargo_tonnage']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
        
        return df
    except Exception as e:
        st.error(f"Error loading cargo flow data: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_tourism_inbound():
    """Load tourism inbound data from CSV."""
    file_path = Path(__file__).parent.parent / "data" / "processed" / "fact_tourism_inbound.csv"
    
    try:
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['country', 'year', 'inbound_tourists']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
        
        return df
    except Exception as e:
        st.error(f"Error loading tourism inbound data: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_governance_flags():
    """Load computed governance flags from CSV."""
    file_path = Path(__file__).parent.parent / "data" / "processed" / "fact_aviation_governance_flags_computed.csv"
    
    try:
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['country', 'year', 'governance_flag']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
        
        return df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()


@st.cache_data
def load_opportunity_scores():
    """Load computed opportunity scores from CSV."""
    file_path = Path(__file__).parent.parent / "data" / "processed" / "fact_uk_africa_aviation_opportunity.csv"
    
    try:
        df = pd.read_csv(file_path)
        
        # Validate required columns (new structure with sector and procurement_readiness_score)
        required_columns = ['country', 'year', 'sector', 'procurement_readiness_score']
        if not all(col in df.columns for col in required_columns):
            # Try old structure for backward compatibility
            old_required = ['country', 'year', 'aviation_score', 'tourism_score', 'combined_opportunity_score']
            if all(col in df.columns for col in old_required):
                return df
            raise ValueError(f"Missing required columns. Expected: {required_columns}")
        
        return df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

