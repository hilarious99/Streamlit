from typing import Dict

FLAG_WEIGHTS: Dict[str, float] = {
    "digital_procurement": 0.30,
    "open_contracting": 0.25,
    "ai_policy": 0.20,
    "vendor_transparency": 0.25,
}

SECTOR_SCORES: Dict[str, float] = {
    "Aviation": 0.85,
    "Tourism & Hospitality": 0.75,
    "Health": 0.90,
    "Education": 0.80,
    "Agriculture": 0.65,
    "Finance": 0.88,
    "Public Services": 0.70,
}

def get_sector_score(sector_name: str) -> float:
    return SECTOR_SCORES.get(sector_name, 0.50)

def governance_score(flags: Dict[str, bool]) -> float:
    return sum(FLAG_WEIGHTS[k] for k, v in flags.items() if v and k in FLAG_WEIGHTS)

def calculate_ai_procurement_index(sector_name: str, flags: Dict[str, bool], country_modifier: float = 1.0) -> float:
    s = get_sector_score(sector_name)
    g = governance_score(flags)
    score = s * g * country_modifier
    return round(score, 3)

if __name__ == "__main__":
    # Example usage
    sector = "Aviation"
    flags = {
        "digital_procurement": True,
        "open_contracting": True,
        "ai_policy": False,
        "vendor_transparency": True,
    }
    print(f"AI Procurement Index for {sector}: {calculate_ai_procurement_index(sector, flags)}")

