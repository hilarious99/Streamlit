import pandas as pd
import sys
import os

# Add the scripts directory to the path so we can import scoring
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scoring import calculate_ai_procurement_index

def flags_from_row(row):
    return {
        "digital_procurement": bool(row["digital_procurement"]),
        "open_contracting": bool(row["open_contracting"]),
        "ai_policy": bool(row["ai_policy"]),
        "vendor_transparency": bool(row["vendor_transparency"]),
    }

def compute_scores(input_file, output_file):
    df = pd.read_csv(input_file)
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
    df.to_csv(output_file, index=False)
    print(f"Generated {output_file}")
    return df

if __name__ == "__main__":
    # Get the base directory (parent of scripts)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data", "processed")
    
    print("Generating scores for Aviation...")
    aviation_input = os.path.join(data_dir, "fact_aviation_governance_flags.csv")
    aviation_output = os.path.join(data_dir, "fact_aviation_governance_flags_computed.csv")
    aviation_df = compute_scores(aviation_input, aviation_output)
    print(aviation_df)
    
    print("\nGenerating scores for Tourism & Hospitality...")
    tourism_input = os.path.join(data_dir, "fact_tourism_governance_flags.csv")
    tourism_output = os.path.join(data_dir, "fact_tourism_governance_flags_computed.csv")
    tourism_df = compute_scores(tourism_input, tourism_output)
    print(tourism_df)

