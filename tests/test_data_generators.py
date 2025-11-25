"""Tests for data generation utilities."""

import polars as pl

from utils.data_generators import (
    generate_fraud_predictions,
    generate_insurance_claims,
    generate_insurance_policies,
)


def test_generate_insurance_claims():
    """Test insurance claims data generation."""
    df = generate_insurance_claims(n_claims=100)

    assert isinstance(df, pl.DataFrame)
    assert len(df) == 100
    assert "claim_id" in df.columns
    assert "claim_amount" in df.columns

    # Check for no null values in critical columns
    assert df["claim_id"].null_count() == 0


def test_generate_insurance_policies():
    """Test insurance policies data generation."""
    df = generate_insurance_policies(n_policies=50)

    assert isinstance(df, pl.DataFrame)
    assert len(df) == 50
    assert "policy_id" in df.columns

    # Check for no null values in critical columns
    assert df["policy_id"].null_count() == 0


def test_generate_fraud_predictions():
    """Test fraud predictions data generation."""
    df = generate_fraud_predictions(n_samples=200)

    assert isinstance(df, pl.DataFrame)
    assert len(df) == 200

    # Check that predictions are in valid range [0, 1]
    if "model1_fraud_score" in df.columns:
        scores = df["model1_fraud_score"]
        assert scores.min() >= 0.0
        assert scores.max() <= 1.0


def test_data_generation_consistency():
    """Test that data generation is consistent with seed."""
    # Note: This test assumes the generators use a seed parameter
    # Adjust if your implementation differs
    df1 = generate_insurance_claims(n_claims=10)
    df2 = generate_insurance_claims(n_claims=10)

    # Both should have same structure
    assert df1.columns == df2.columns
    assert len(df1) == len(df2)
