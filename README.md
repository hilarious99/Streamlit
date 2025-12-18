# AlgoEconomics – UK–Africa Aviation & Tourism (Beta)

A Streamlit beta dashboard for an economic intelligence platform displaying aviation and tourism data for UK–Africa routes.

## Project Description

This is a beta demo application that loads and visualizes aviation and tourism CSV data. The dashboard provides insights into:
- Passenger flow volumes by country
- Cargo tonnage by country
- Inbound tourism statistics by country

**Note: This is a beta demo using sample data.**

## Project Structure

```
/
├── data/
│   └── processed/
│       ├── fact_route_passenger_flow.csv
│       ├── fact_route_cargo_flow.csv
│       └── fact_tourism_inbound.csv
├── scripts/
│   ├── data_loader.py
│   └── metrics.py
├── app.py
├── requirements.txt
└── README.md
```

## How to Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

3. **Access the app:**
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

- **Aviation Tab:**
  - Passenger volume bar chart by country
  - Cargo tonnage bar chart by country
  - Summary metrics (total passengers, total cargo)
  - Data table preview

- **Tourism & Hospitality Tab:**
  - Inbound tourists bar chart by country
  - Summary metrics (total inbound tourists)
  - Data table preview

- **Country Filter:**
  - Dropdown to filter data by country (default: All)

## Requirements

- Python 3.7+
- streamlit
- pandas
- plotly

