"""
Data pipeline module for orchestrating scoring and CSV generation.

This module loads raw processed CSVs, calls the scoring engine,
and writes computed output CSVs.
"""

import pandas as pd
from pathlib import Path
from scripts.scoring import compute_scores


def run_scoring_pipeline():
    """
    Run the complete scoring pipeline.
    
    Loads raw processed CSVs, computes scores, and writes output CSVs.
    
    Returns:
        tuple: (governance_df, opportunity_df) or (None, None) on error
    """
    try:
        # Define paths
        base_path = Path(__file__).parent.parent
        data_path = base_path / "data" / "processed"
        
        # Load raw processed CSVs
        passenger_df = pd.read_csv(data_path / "fact_route_passenger_flow.csv")
        cargo_df = pd.read_csv(data_path / "fact_route_cargo_flow.csv")
        tourism_df = pd.read_csv(data_path / "fact_tourism_inbound.csv")
        
        # Validate required columns
        if not all(col in passenger_df.columns for col in ['country', 'year', 'passenger_volume']):
            raise ValueError("Passenger flow CSV missing required columns")
        if not all(col in cargo_df.columns for col in ['country', 'year', 'cargo_tonnage']):
            raise ValueError("Cargo flow CSV missing required columns")
        if not all(col in tourism_df.columns for col in ['country', 'year', 'inbound_tourists']):
            raise ValueError("Tourism inbound CSV missing required columns")
        
        # Optionally load AI procurement index if available
        ai_procurement_index_df = None
        ai_procurement_path = data_path / "fact_ai_procurement_index.csv"
        if ai_procurement_path.exists():
            try:
                ai_procurement_index_df = pd.read_csv(ai_procurement_path)
                if not all(col in ai_procurement_index_df.columns for col in ['country', 'year', 'ai_procurement_index']):
                    print("Warning: AI procurement index CSV missing required columns, using default values")
                    ai_procurement_index_df = None
            except Exception as e:
                print(f"Warning: Could not load AI procurement index: {str(e)}, using default values")
        
        # Compute scores
        governance_df, opportunity_df = compute_scores(passenger_df, cargo_df, tourism_df, ai_procurement_index_df)
        
        # Write output CSVs (overwrite safely)
        governance_df.to_csv(
            data_path / "fact_aviation_governance_flags_computed.csv",
            index=False
        )
        
        opportunity_df.to_csv(
            data_path / "fact_uk_africa_aviation_opportunity.csv",
            index=False
        )
        
        return governance_df, opportunity_df
        
    except Exception as e:
        print(f"Error in scoring pipeline: {str(e)}")
        return None, None

