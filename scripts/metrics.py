import pandas as pd


def calculate_total_passengers(df):
    """Calculate total passenger volume."""
    if df.empty or 'passenger_volume' not in df.columns:
        return 0
    return int(df['passenger_volume'].sum())


def calculate_total_cargo(df):
    """Calculate total cargo tonnage."""
    if df.empty or 'cargo_tonnage' not in df.columns:
        return 0
    return int(df['cargo_tonnage'].sum())


