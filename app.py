import streamlit as st
import plotly.express as px
from pathlib import Path
from datetime import datetime

from scripts.data_loader import (
    load_passenger_flow,
    load_cargo_flow,
    load_governance_flags,
    load_opportunity_scores
)
from scripts.pipeline import run_scoring_pipeline


# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="AlgoEconomics | UK–Africa Intelligence",
    layout="wide"
)

# =====================================================
# Global Styling (Minimal / Professional)
# =====================================================
st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none; }

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

h1, h2 {
    font-weight: 600;
}

h2 {
    margin-top: 1.5rem;
}

.summary-box {
    padding: 0.9rem 1rem;
    border-radius: 8px;
    background: #f9fafb;
    border-left: 4px solid;
    margin-bottom: 1rem;
}

.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #9ca3af;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# Colors
# =====================================================
AVIATION_COLOR = "#2563EB"   # Professional blue
TOURISM_COLOR = "#059669"    # Professional green


# =====================================================
# Header (Minimal, Professional)
# =====================================================
logo_path = Path("assets/algoeconomics_logo.png")

col_logo, col_text = st.columns([1.5, 10])

with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=140)

with col_text:
    st.markdown(
        "<div style='margin-top:8px; color:#6b7280; font-size:0.95rem;'>"
        "UK–Africa Aviation & Tourism Intelligence Platform"
        "</div>",
        unsafe_allow_html=True
    )

st.markdown(
    f"<div style='color:#9ca3af; font-size:0.8rem;'>"
    f"Last updated: {datetime.utcnow().strftime('%d %b %Y, %H:%M UTC')}"
    f"</div>",
    unsafe_allow_html=True
)

st.markdown("<hr style='margin:1rem 0;'>", unsafe_allow_html=True)


# =====================================================
# Summary Box Utility (HIGH CONTRAST FIX)
# =====================================================
def summary_box(title, value, subtitle="", color="#2563EB"):
    st.markdown(f"""
    <div class="summary-box" style="
        border-left-color:{color};
        background: linear-gradient(
            90deg,
            rgba(37,99,235,0.08),
            rgba(255,255,255,1)
        );
    ">
        <div style="font-size:0.8rem; color:#6b7280; margin-bottom:2px;">
            {title}
        </div>
        <div style="
            font-size:1.9rem;
            font-weight:700;
            color:{color};
            line-height:1.2;
        ">
            {value}
        </div>
        <div style="font-size:0.75rem; color:#9ca3af;">
            {subtitle}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# Run Scoring Pipeline
# =====================================================
try:
    run_scoring_pipeline()
except Exception:
    pass


# =====================================================
# Load Data
# =====================================================
passenger_df = load_passenger_flow()
cargo_df = load_cargo_flow()
governance_df = load_governance_flags()
opportunity_df = load_opportunity_scores()


# =====================================================
# Country Selector
# =====================================================
countries = sorted(
    set(passenger_df.get("country", []))
    | set(cargo_df.get("country", []))
    | set(governance_df.get("country", []))
    | set(opportunity_df.get("country", []))
)

selected_country = st.selectbox(
    "Country",
    ["All"] + countries,
    label_visibility="collapsed"
)

def filter_df(df):
    if selected_country == "All" or df.empty:
        return df
    return df[df["country"] == selected_country]

passenger_df = filter_df(passenger_df)
cargo_df = filter_df(cargo_df)
governance_df = filter_df(governance_df)
opportunity_df = filter_df(opportunity_df)


# =====================================================
# Tabs
# =====================================================
tab1, tab2 = st.tabs(["Aviation", "Tourism & Hospitality"])


# =====================================================
# Aviation
# =====================================================
with tab1:
    st.markdown("<h2>Aviation</h2>", unsafe_allow_html=True)

    if not passenger_df.empty:
        summary_box(
            "Passenger Volume",
            f"{passenger_df['passenger_volume'].sum():,}",
            "Annual passengers",
            AVIATION_COLOR
        )

        fig = px.bar(
            passenger_df,
            x="country",
            y="passenger_volume",
            color_discrete_sequence=[AVIATION_COLOR]
        )
        fig.update_layout(
            title="Passenger Volume by Country",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    if not opportunity_df.empty and "sector" in opportunity_df.columns:
        aviation_scores = opportunity_df[opportunity_df["sector"] == "Aviation"]

        if not aviation_scores.empty:
            summary_box(
                "Procurement Readiness",
                f"{aviation_scores['procurement_readiness_score'].mean():.1f}/100",
                "Average score",
                AVIATION_COLOR
            )

            fig = px.bar(
                aviation_scores,
                x="country",
                y="procurement_readiness_score",
                color_discrete_sequence=[AVIATION_COLOR]
            )
            fig.update_layout(
                title="Aviation Procurement Readiness",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)


# =====================================================
# Tourism
# =====================================================
with tab2:
    st.markdown("<h2>Tourism & Hospitality</h2>", unsafe_allow_html=True)

    if not opportunity_df.empty and "sector" in opportunity_df.columns:
        tourism_scores = opportunity_df[
            opportunity_df["sector"] == "Tourism & Hospitality"
        ]

        if not tourism_scores.empty:
            summary_box(
                "Procurement Readiness",
                f"{tourism_scores['procurement_readiness_score'].mean():.1f}/100",
                "Average score",
                TOURISM_COLOR
            )

            fig = px.bar(
                tourism_scores,
                x="country",
                y="procurement_readiness_score",
                color_discrete_sequence=[TOURISM_COLOR]
            )
            fig.update_layout(
                title="Tourism Procurement Readiness",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)


# =====================================================
# Footer
# =====================================================
st.markdown("""
<div class="footer">
Powered by <strong>AlgoCentric AI</strong> · UK–Africa Intelligence Platform
</div>
""", unsafe_allow_html=True)
