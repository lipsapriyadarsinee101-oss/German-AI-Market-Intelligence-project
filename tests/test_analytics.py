import pandas as pd
import pytest

from src.analytics import calculate_cagr, evidence_confidence, forecast_market, score_sectors, simulate_policy


def test_cagr_is_positive():
    assert calculate_cagr(7.3, 31.5, 8) == pytest.approx(0.2001, abs=0.001)


def test_forecast_has_both_endpoints():
    result = forecast_market(7.3, 31.5, 2022, 2030)
    assert len(result) == 9
    assert result.iloc[0]["market_eur_bn"] == 7.3
    assert result.iloc[-1]["market_eur_bn"] == 31.5


def test_score_stays_in_range():
    df = pd.DataFrame(
        [{"sector": "Test", "adoption_index": 90, "growth_potential": 90, "investment_index": 90, "talent_availability": 90, "trust_index": 90, "regulatory_risk": 10}]
    )
    score = score_sectors(df).iloc[0]["opportunity_score"]
    assert 0 <= score <= 100


def test_policy_simulation_improves_score():
    df = pd.DataFrame(
        [{"sector": "Test", "adoption_index": 50, "growth_potential": 50, "investment_index": 50, "talent_availability": 50, "trust_index": 50, "regulatory_risk": 50}]
    )
    baseline = score_sectors(df).iloc[0]["opportunity_score"]
    simulated = simulate_policy(df, 50, 50, 50, 50).iloc[0]["opportunity_score"]
    assert simulated > baseline


def test_observed_evidence_scores_above_scenario():
    assert evidence_confidence("observed") > evidence_confidence("scenario")
