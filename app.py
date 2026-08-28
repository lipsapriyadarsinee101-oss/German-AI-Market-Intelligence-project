from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics import calculate_cagr, evidence_confidence, forecast_market, score_sectors, simulate_policy
from src.compliance import classify_use_case

BASE_DIR = Path(__file__).parent

st.set_page_config(page_title="German AI Market Intelligence", page_icon="🇩🇪", layout="wide")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    sectors = pd.read_csv(BASE_DIR / "data" / "sector_indicators.csv")
    market = pd.read_csv(BASE_DIR / "data" / "market_scenarios.csv")
    return sectors, market


sectors, market = load_data()
scored = score_sectors(sectors)

st.title("🇩🇪 German AI Market Intelligence Platform")
st.caption("Sector opportunity, adoption scenarios, workforce pressure, and responsible-AI readiness")

with st.sidebar:
    st.header("Controls")
    selected_sectors = st.multiselect(
        "Sectors", scored["sector"].tolist(), default=scored["sector"].tolist()
    )
    scenario = st.selectbox("2030 market scenario", ["Low", "Base", "High"], index=1)
    st.info("Observed and scenario data are clearly separated. Verify figures before external use.")

filtered = scored[scored["sector"].isin(selected_sectors)]
start_value = float(market.loc[market["year"] == 2022, "base_eur_bn"].iloc[0])
end_column = f"{scenario.lower()}_eur_bn"
end_value = float(market.loc[market["year"] == 2030, end_column].iloc[0])
cagr = calculate_cagr(start_value, end_value, 8)

c1, c2, c3, c4 = st.columns(4)
c1.metric("2022 baseline", f"€{start_value:.1f}B", help="Illustrative baseline from the supplied concept")
c2.metric(f"2030 {scenario.lower()} scenario", f"€{end_value:.1f}B")
c3.metric("Scenario CAGR", f"{cagr:.1%}")
c4.metric("Top opportunity", filtered.iloc[0]["sector"] if not filtered.empty else "—")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Market outlook", "Sector opportunities", "Readiness Digital Twin", "Evidence Lab", "AI Act screening"]
)

with tab1:
    forecast = forecast_market(start_value, end_value, 2022, 2030)
    fig = px.line(forecast, x="year", y="market_eur_bn", markers=True, title=f"German AI market: {scenario} scenario")
    fig.update_yaxes(title="Market size (€ billions)")
    st.plotly_chart(fig, use_container_width=True)
    st.warning("This forecast is a scenario derived from user-supplied estimates, not an official market forecast.")

with tab2:
    if filtered.empty:
        st.warning("Select at least one sector.")
    else:
        fig = px.bar(
            filtered.sort_values("opportunity_score"),
            x="opportunity_score",
            y="sector",
            orientation="h",
            color="opportunity_score",
            color_continuous_scale="Blues",
            range_x=[0, 100],
            title="Explainable AI opportunity score",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            filtered[["sector", "opportunity_score", "primary_use_case", "evidence_type"]],
            use_container_width=True,
            hide_index=True,
        )
        st.download_button("Download scored sectors", filtered.to_csv(index=False), "scored_sectors.csv", "text/csv")

with tab3:
    st.subheader("German AI Readiness Digital Twin")
    st.write("Change policy levers and see how sector readiness could respond. This is a transparent simulation—not a prediction.")
    p1, p2 = st.columns(2)
    skills = p1.slider("AI skills investment", 0, 100, 40)
    data_infra = p1.slider("Data infrastructure investment", 0, 100, 40)
    trust = p2.slider("Trust and AI-literacy program", 0, 100, 40)
    clarity = p2.slider("Regulatory clarity", 0, 100, 40)
    simulated = simulate_policy(sectors, skills, data_infra, trust, clarity)
    comparison = scored[["sector", "opportunity_score"]].merge(
        simulated[["sector", "opportunity_score"]], on="sector", suffixes=("_baseline", "_simulated")
    )
    comparison["improvement"] = (
        comparison["opportunity_score_simulated"] - comparison["opportunity_score_baseline"]
    ).round(1)
    long = comparison.melt(
        id_vars="sector",
        value_vars=["opportunity_score_baseline", "opportunity_score_simulated"],
        var_name="state",
        value_name="score",
    )
    long["state"] = long["state"].map(
        {"opportunity_score_baseline": "Baseline", "opportunity_score_simulated": "Simulated"}
    )
    st.plotly_chart(
        px.bar(long, x="sector", y="score", color="state", barmode="group", range_y=[0, 100]),
        use_container_width=True,
    )
    winner = comparison.sort_values("improvement", ascending=False).iloc[0]
    st.success(f"Largest simulated improvement: {winner['sector']} (+{winner['improvement']:.1f} points)")

with tab4:
    st.subheader("Evidence Confidence Lab")
    st.write("A recruiter-visible responsible-AI feature: every claim is separated into observed evidence, derived analysis, or scenario data.")
    sources = pd.read_csv(BASE_DIR / "data" / "sources.csv")
    sources["confidence_score"] = sources["evidence_type"].apply(evidence_confidence)
    st.plotly_chart(
        px.bar(sources, x="confidence_score", y="topic", color="evidence_type", orientation="h", range_x=[0, 100]),
        use_container_width=True,
    )
    st.dataframe(sources[["topic", "claim", "evidence_type", "confidence_score", "url"]], hide_index=True, use_container_width=True)
    st.caption("Confidence measures provenance quality, not whether a claim is universally true.")

with tab5:
    st.write("Educational first-pass screening; it does not replace legal review.")
    use_case = st.selectbox(
        "Select an AI use case",
        ["Predictive maintenance", "Medical diagnosis support", "Recruitment ranking", "Credit scoring", "Customer-service chatbot", "Biometric social scoring"],
    )
    result = classify_use_case(use_case)
    st.subheader(result["risk_level"])
    st.write(result["reason"])
    st.markdown("**Suggested action:** " + result["action"])

st.divider()
st.caption("Portfolio project • Transparent methodology • Responsible AI • Last reviewed: August 2026")
