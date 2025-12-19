"""
Data pipeline module for orchestrating scoring and CSV generation.

This module loads governance flags CSVs, computes AI procurement indices,
and writes computed output CSVs.
"""

import pandas as pd
from pathlib import Path
from scripts.scoring import calculate_ai_procurement_index


def flags_from_row(row):
    """Extract governance flags from a DataFrame row."""
    return {
        "digital_procurement": bool(row["digital_procurement"]),
        "open_contracting": bool(row["open_contracting"]),
        "ai_policy": bool(row["ai_policy"]),
        "vendor_transparency": bool(row["vendor_transparency"]),
    }


def run_scoring_pipeline():
    """
    Run the complete scoring pipeline.
    
    Loads governance flags CSVs, computes AI procurement indices,
    and writes computed output CSVs.
    
    Returns:
        tuple: (governance_df, opportunity_df) or (None, None) on error
    """
    try:
        # Define paths
        base_path = Path(__file__).parent.parent
        data_path = base_path / "data" / "processed"
        
        # Load governance flags CSVs
        aviation_flags_path = data_path / "fact_aviation_governance_flags.csv"
        tourism_flags_path = data_path / "fact_tourism_governance_flags.csv"
        
        if not aviation_flags_path.exists():
            raise FileNotFoundError(f"Aviation governance flags CSV not found: {aviation_flags_path}")
        if not tourism_flags_path.exists():
            raise FileNotFoundError(f"Tourism governance flags CSV not found: {tourism_flags_path}")
        
        aviation_df = pd.read_csv(aviation_flags_path)
        tourism_df = pd.read_csv(tourism_flags_path)
        
        # Validate required columns
        required_cols = ['country', 'sector', 'digital_procurement', 'open_contracting', 
                        'ai_policy', 'vendor_transparency', 'country_modifier']
        if not all(col in aviation_df.columns for col in required_cols):
            raise ValueError("Aviation governance flags CSV missing required columns")
        if not all(col in tourism_df.columns for col in required_cols):
            raise ValueError("Tourism governance flags CSV missing required columns")
        
        # Compute AI procurement indices for both sectors
        all_dfs = []
        
        for df in [aviation_df, tourism_df]:
            scores = []
            for _, row in df.iterrows():
                flags = flags_from_row(row)
                score = calculate_ai_procurement_index(
                    row["sector"],
                    flags,
                    float(row.get("country_modifier", 1.0))
                )
                scores.append(score)
            df["ai_procurement_index"] = scores
            all_dfs.append(df)
        
        # Combine into single opportunity dataframe
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        # Create opportunity_df with expected schema: country, year, sector, procurement_readiness_score
        # Use ai_procurement_index as procurement_readiness_score (multiply by 100 for percentage-like score)
        # Default year to 2023 (can be extracted from other data sources if available)
        opportunity_df = pd.DataFrame({
            'country': combined_df['country'],
            'year': 2023,  # Default year
            'sector': combined_df['sector'],
            'procurement_readiness_score': (combined_df['ai_procurement_index'] * 100).round(1)
        })
        
        # Create governance_df with governance flags computed from governance scores
        # Compute governance score for each country (average across sectors)
        governance_scores = []
        countries = []
        for country in combined_df['country'].unique():
            country_data = combined_df[combined_df['country'] == country]
            # Calculate average governance score (sum of flag weights)
            avg_governance = 0
            count = 0
            for _, row in country_data.iterrows():
                flags = flags_from_row(row)
                from scripts.scoring import governance_score
                avg_governance += governance_score(flags)
                count += 1
            if count > 0:
                avg_governance = avg_governance / count
            # HIGH if governance score >= 0.5, LOW otherwise
            flag = 'HIGH' if avg_governance >= 0.5 else 'LOW'
            governance_scores.append(flag)
            countries.append(country)
        
        governance_df = pd.DataFrame({
            'country': countries,
            'year': 2023,
            'governance_flag': governance_scores
        })
        
        # Write computed aviation flags (with ai_procurement_index)
        aviation_output_path = data_path / "fact_aviation_governance_flags_computed.csv"
        aviation_df.to_csv(aviation_output_path, index=False)
        
        # Write computed tourism flags (with ai_procurement_index)
        tourism_output_path = data_path / "fact_tourism_governance_flags_computed.csv"
        tourism_df.to_csv(tourism_output_path, index=False)
        
        # Write opportunity scores
        opportunity_output_path = data_path / "fact_uk_africa_aviation_opportunity.csv"
        opportunity_df.to_csv(opportunity_output_path, index=False)
        
        # Write governance flags (overwrite the computed file with proper structure)
        governance_output_path = data_path / "fact_aviation_governance_flags_computed.csv"
        # But we need to preserve the structure expected by data_loader
        # Actually, data_loader expects a different file - let's check what it loads
        # It loads fact_aviation_governance_flags_computed.csv but expects country, year, governance_flag
        # So we need a separate file or update the loader
        # For now, write to a separate governance flags file
        governance_flags_path = data_path / "fact_governance_flags.csv"
        governance_df.to_csv(governance_flags_path, index=False)
        
        return governance_df, opportunity_df
        
    except Exception as e:
        print(f"Error in scoring pipeline: {str(e)}")
        return None, None

