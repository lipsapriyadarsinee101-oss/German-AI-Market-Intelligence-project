import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "sector",
    "adoption_index",
    "growth_potential",
    "investment_index",
    "talent_availability",
    "trust_index",
    "regulatory_risk",
}


def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    if start_value <= 0 or end_value <= 0 or years <= 0:
        raise ValueError("Values and years must be positive.")
    return (end_value / start_value) ** (1 / years) - 1


def forecast_market(start_value: float, end_value: float, start_year: int, end_year: int) -> pd.DataFrame:
    years = end_year - start_year
    growth = calculate_cagr(start_value, end_value, years)
    timeline = np.arange(start_year, end_year + 1)
    values = [start_value * (1 + growth) ** offset for offset in range(len(timeline))]
    return pd.DataFrame({"year": timeline, "market_eur_bn": np.round(values, 2)})


def score_sectors(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = df.copy()
    positive = (
        0.30 * result["adoption_index"]
        + 0.25 * result["growth_potential"]
        + 0.20 * result["investment_index"]
        + 0.15 * result["talent_availability"]
        + 0.10 * result["trust_index"]
    )
    penalty = 0.15 * result["regulatory_risk"]
    result["opportunity_score"] = (positive - penalty).clip(0, 100).round(1)
    return result.sort_values("opportunity_score", ascending=False).reset_index(drop=True)


def simulate_policy(
    df: pd.DataFrame,
    skills_investment: int,
    data_infrastructure: int,
    trust_program: int,
    regulatory_clarity: int,
) -> pd.DataFrame:
    """Create a transparent what-if digital twin without pretending to predict reality."""
    scenario = df.copy()
    scenario["talent_availability"] = (
        scenario["talent_availability"] + skills_investment * 0.25
    ).clip(0, 100)
    scenario["investment_index"] = (
        scenario["investment_index"] + data_infrastructure * 0.18
    ).clip(0, 100)
    scenario["trust_index"] = (
        scenario["trust_index"] + trust_program * 0.22
    ).clip(0, 100)
    scenario["regulatory_risk"] = (
        scenario["regulatory_risk"] - regulatory_clarity * 0.20
    ).clip(0, 100)
    scored = score_sectors(scenario)
    scored["scenario_name"] = "Policy simulation"
    return scored


def evidence_confidence(evidence_type: str, source_count: int = 1) -> int:
    """Score provenance confidence; this evaluates evidence, not truth itself."""
    base = {"observed": 75, "derived": 60, "scenario": 30}.get(evidence_type, 20)
    return min(100, base + max(0, source_count - 1) * 5)
