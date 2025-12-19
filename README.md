# AlgoEconomics – UK–Africa Aviation & Tourism (Beta)

A Streamlit beta dashboard for an economic intelligence platform displaying aviation and tourism procurement readiness scores for UK–Africa routes.

## Project Description

This is a beta demo application that computes and visualizes procurement readiness scores based on governance flags for Aviation and Tourism & Hospitality sectors. The dashboard provides insights into:

- Procurement readiness scores by country and sector
- Governance flags (HIGH/LOW) based on governance indicators
- AI procurement indices computed from governance flags
- Country-specific modifiers and sector scores

**Note: This is a beta demo using sample data.**

## Project Structure

```
/
├── data/
│   └── processed/
│       ├── fact_aviation_governance_flags.csv          # Input: Aviation governance flags
│       ├── fact_tourism_governance_flags.csv          # Input: Tourism governance flags
│       ├── fact_aviation_governance_flags_computed.csv # Output: Aviation scores with AI procurement index
│       ├── fact_tourism_governance_flags_computed.csv # Output: Tourism scores with AI procurement index
│       ├── fact_governance_flags.csv                   # Output: Computed governance flags (HIGH/LOW)
│       └── fact_uk_africa_aviation_opportunity.csv    # Output: Procurement readiness scores by sector
├── scripts/
│   ├── data_loader.py      # Functions to load CSV data
│   ├── metrics.py          # Calculation functions
│   ├── pipeline.py          # Scoring pipeline orchestrator
│   ├── scoring.py          # Core scoring logic (AI procurement index calculation)
│   └── generate_scores.py  # Standalone script to generate scores
├── app.py                   # Main Streamlit application
├── requirements.txt
└── README.md
```

## Data Flow

1. **Input Files:**
   - `fact_aviation_governance_flags.csv` - Contains governance flags for Aviation sector
   - `fact_tourism_governance_flags.csv` - Contains governance flags for Tourism & Hospitality sector

2. **Scoring Pipeline** (`scripts/pipeline.py`):
   - Loads governance flags CSVs
   - Computes AI procurement indices using `scoring.py`
   - Generates governance flags (HIGH/LOW) based on governance scores
   - Creates opportunity scores with procurement readiness scores

3. **Output Files:**
   - `fact_aviation_governance_flags_computed.csv` - Aviation scores with `ai_procurement_index`
   - `fact_tourism_governance_flags_computed.csv` - Tourism scores with `ai_procurement_index`
   - `fact_governance_flags.csv` - Governance flags (HIGH/LOW) by country
   - `fact_uk_africa_aviation_opportunity.csv` - Procurement readiness scores (0-100 scale) by country and sector

## Scoring Logic

The AI Procurement Index is calculated using:

```
AI Procurement Index = Sector Score × Governance Score × Country Modifier
```

Where:
- **Sector Scores:**
  - Aviation: 0.85
  - Tourism & Hospitality: 0.75

- **Governance Score:** Sum of weighted flags:
  - Digital Procurement: 0.30
  - Open Contracting: 0.25
  - AI Policy: 0.20
  - Vendor Transparency: 0.25

- **Country Modifier:** Country-specific adjustment factor (default: 1.0)

The Procurement Readiness Score is the AI Procurement Index multiplied by 100 (0-100 scale).

## How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scoring pipeline (optional - runs automatically in app):**
   ```bash
   python scripts/generate_scores.py
   ```
   Or use the pipeline module:
   ```bash
   python -c "from scripts.pipeline import run_scoring_pipeline; run_scoring_pipeline()"
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

4. **Access the app:**
   The app will open in your default web browser at `http://localhost:8501`

## How to Deploy on Streamlit Cloud

1. **Push your code to GitHub:**
   - Create a new repository on GitHub
   - Push all project files to the repository

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://your-app-name.streamlit.app`

## Features

### Aviation Tab:
- Procurement readiness scores bar chart by country (Aviation sector)
- Summary metrics (average scores)
- Governance flags distribution
- Data table previews

### Tourism & Hospitality Tab:
- Procurement readiness scores bar chart by country (Tourism & Hospitality sector)
- Summary metrics (average, highest, lowest scores)
- Governance flags distribution
- Data table previews

### Country Filter:
- Dropdown to filter data by country (default: All)
- Updates all charts and metrics dynamically

## Requirements

- Python 3.7+
- streamlit
- pandas
- plotly

## Input CSV Schema

### Governance Flags CSV Format:
```csv
country,sector,digital_procurement,open_contracting,ai_policy,vendor_transparency,country_modifier
Nigeria,Aviation,True,True,False,True,1.00
```

## Output CSV Schema

### Opportunity Scores (`fact_uk_africa_aviation_opportunity.csv`):
```csv
country,year,sector,procurement_readiness_score
Nigeria,2023,Aviation,68.0
Nigeria,2023,Tourism & Hospitality,41.3
```

### Governance Flags (`fact_governance_flags.csv`):
```csv
country,year,governance_flag
Nigeria,2023,HIGH
```
