"""
Scoring module for procurement readiness scoring.

This module computes procurement readiness scores based on governance flags,
AI procurement index, and sector information.
"""

import pandas as pd
import numpy as np


def score_entry(entry):
    """
    Compute a procurement readiness score for a single record.
    
    Parameters:
        entry (dict): A dictionary containing:
            - governance_flag (str)
            - ai_procurement_index (float)
            - sector (str)
    
    Returns:
        int: The computed score.
    """
    score = 0
    
    # Governance weighting
    if entry.get('governance_flag') == 'High' or entry.get('governance_flag') == 'HIGH':
        score += 30
    
    # AI procurement readiness weighting
    if entry.get('ai_procurement_index', 0) > 0.7:
        score += 40
    
    # Sector-specific weighting
    if entry.get('sector') in ['Aviation', 'Tourism']:
        score += 20
    
    return score


def compute_scores(passenger_df, cargo_df, tourism_df, ai_procurement_index_df=None):
    """
    Compute procurement readiness scores using the score_entry function.
    
    Args:
        passenger_df: DataFrame with columns ['country', 'year', 'passenger_volume']
        cargo_df: DataFrame with columns ['country', 'year', 'cargo_tonnage']
        tourism_df: DataFrame with columns ['country', 'year', 'inbound_tourists']
        ai_procurement_index_df: Optional DataFrame with columns ['country', 'year', 'ai_procurement_index']
                                 If not provided, defaults to 0.5 for all countries
    
    Returns:
        governance_df: DataFrame with columns ['country', 'year', 'governance_flag']
        opportunity_df: DataFrame with columns ['country', 'year', 'sector', 'procurement_readiness_score']
    """
    # Merge dataframes on country and year
    merged_df = passenger_df.merge(
        cargo_df, 
        on=['country', 'year'], 
        how='outer'
    ).merge(
        tourism_df,
        on=['country', 'year'],
        how='outer'
    )
    
    # Fill missing values with 0 for calculations
    merged_df['passenger_volume'] = merged_df['passenger_volume'].fillna(0)
    merged_df['cargo_tonnage'] = merged_df['cargo_tonnage'].fillna(0)
    merged_df['inbound_tourists'] = merged_df['inbound_tourists'].fillna(0)
    
    # ============================================
    # GOVERNANCE FLAG LOGIC
    # ============================================
    # HIGH if passenger_volume > median, LOW otherwise
    median_passenger = merged_df['passenger_volume'].median()
    merged_df['governance_flag'] = merged_df['passenger_volume'].apply(
        lambda x: 'HIGH' if x > median_passenger else 'LOW'
    )
    
    # Create governance DataFrame
    governance_df = merged_df[['country', 'year', 'governance_flag']].copy()
    
    # ============================================
    # AI PROCUREMENT INDEX
    # ============================================
    # Merge AI procurement index if provided, otherwise default to 0.5
    if ai_procurement_index_df is not None:
        merged_df = merged_df.merge(
            ai_procurement_index_df,
            on=['country', 'year'],
            how='left'
        )
        merged_df['ai_procurement_index'] = merged_df['ai_procurement_index'].fillna(0.5)
    else:
        merged_df['ai_procurement_index'] = 0.5
    
    # ============================================
    # PROCUREMENT READINESS SCORING
    # ============================================
    # Create entries for both Aviation and Tourism sectors
    opportunity_records = []
    
    for _, row in merged_df.iterrows():
        # Aviation sector entry
        aviation_entry = {
            'country': row['country'],
            'year': row['year'],
            'governance_flag': row['governance_flag'],
            'ai_procurement_index': row['ai_procurement_index'],
            'sector': 'Aviation'
        }
        aviation_score = score_entry(aviation_entry)
        opportunity_records.append({
            'country': row['country'],
            'year': row['year'],
            'sector': 'Aviation',
            'procurement_readiness_score': aviation_score
        })
        
        # Tourism sector entry
        tourism_entry = {
            'country': row['country'],
            'year': row['year'],
            'governance_flag': row['governance_flag'],
            'ai_procurement_index': row['ai_procurement_index'],
            'sector': 'Tourism'
        }
        tourism_score = score_entry(tourism_entry)
        opportunity_records.append({
            'country': row['country'],
            'year': row['year'],
            'sector': 'Tourism',
            'procurement_readiness_score': tourism_score
        })
    
    # Create opportunity DataFrame
    opportunity_df = pd.DataFrame(opportunity_records)
    
    return governance_df, opportunity_df

