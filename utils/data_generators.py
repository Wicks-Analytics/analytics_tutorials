"""
Data generation utilities for creating realistic insurance datasets.
"""

from datetime import datetime, timedelta

import numpy as np
import polars as pl
from faker import Faker

fake = Faker()
Faker.seed(42)
np.random.seed(42)


def generate_insurance_policies(n_policies: int = 10000) -> pl.DataFrame:
    """
    Generate dummy insurance policy data.

    Args:
        n_policies: Number of policies to generate

    Returns:
        Polars DataFrame with policy information
    """
    # Generate policy IDs
    policy_ids = [f"POL-{i:06d}" for i in range(1, n_policies + 1)]

    # Customer demographics
    ages = np.random.normal(45, 15, n_policies).clip(18, 85).astype(int)
    genders = np.random.choice(["M", "F"], n_policies, p=[0.48, 0.52])

    # Geographic data
    states = np.random.choice(
        ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"],
        n_policies,
        p=[0.15, 0.12, 0.10, 0.09, 0.08, 0.08, 0.07, 0.06, 0.06, 0.19],
    )

    # Policy details
    policy_types = np.random.choice(
        ["Auto", "Home", "Life", "Health"], n_policies, p=[0.40, 0.25, 0.20, 0.15]
    )

    # Coverage amounts based on policy type
    coverage_amounts = []
    for ptype in policy_types:
        if ptype == "Auto":
            coverage = np.random.choice([25000, 50000, 100000, 250000], p=[0.2, 0.4, 0.3, 0.1])
        elif ptype == "Home":
            coverage = np.random.choice(
                [100000, 250000, 500000, 1000000], p=[0.15, 0.45, 0.30, 0.10]
            )
        elif ptype == "Life":
            coverage = np.random.choice(
                [100000, 250000, 500000, 1000000], p=[0.25, 0.35, 0.25, 0.15]
            )
        else:  # Health
            coverage = np.random.choice([50000, 100000, 250000], p=[0.3, 0.5, 0.2])
        coverage_amounts.append(coverage)

    # Premium calculation with some randomness
    base_premiums = {"Auto": 1200, "Home": 1500, "Life": 800, "Health": 3000}

    premiums = []
    for i, ptype in enumerate(policy_types):
        base = base_premiums[ptype]
        age_factor = 1 + (ages[i] - 45) * 0.01
        coverage_factor = coverage_amounts[i] / 100000
        premium = base * age_factor * (0.5 + 0.5 * coverage_factor) * np.random.uniform(0.8, 1.2)
        premiums.append(round(premium, 2))

    # Policy dates
    start_dates = [
        datetime.now() - timedelta(days=np.random.randint(0, 1095)) for _ in range(n_policies)
    ]

    # Credit scores
    credit_scores = np.random.normal(700, 80, n_policies).clip(300, 850).astype(int)

    # Prior claims
    prior_claims = np.random.poisson(0.3, n_policies)

    # Create DataFrame
    df = pl.DataFrame(
        {
            "policy_id": policy_ids,
            "customer_age": ages,
            "customer_gender": genders,
            "state": states,
            "policy_type": policy_types,
            "coverage_amount": coverage_amounts,
            "annual_premium": premiums,
            "policy_start_date": start_dates,
            "credit_score": credit_scores,
            "prior_claims_count": prior_claims,
        }
    )

    return df


def generate_insurance_claims(
    n_claims: int = 5000, policies_df: pl.DataFrame = None
) -> pl.DataFrame:
    """
    Generate dummy insurance claims data.

    Args:
        n_claims: Number of claims to generate
        policies_df: Optional policies DataFrame to link claims to

    Returns:
        Polars DataFrame with claims information
    """
    if policies_df is None:
        policies_df = generate_insurance_policies(10000)

    # Sample policies for claims
    policy_ids = policies_df.sample(n_claims, with_replacement=True)["policy_id"].to_list()

    # Claim IDs
    claim_ids = [f"CLM-{i:06d}" for i in range(1, n_claims + 1)]

    # Claim dates
    claim_dates = [
        datetime.now() - timedelta(days=np.random.randint(0, 730)) for _ in range(n_claims)
    ]

    # Claim types
    claim_types = np.random.choice(
        ["Collision", "Theft", "Fire", "Water Damage", "Liability", "Medical", "Other"],
        n_claims,
        p=[0.25, 0.10, 0.08, 0.12, 0.20, 0.15, 0.10],
    )

    # Claim amounts (log-normal distribution)
    claim_amounts = np.random.lognormal(8.5, 1.2, n_claims).clip(100, 500000)
    claim_amounts = np.round(claim_amounts, 2)

    # Claim status
    claim_statuses = np.random.choice(
        ["Approved", "Denied", "Pending", "Under Review"], n_claims, p=[0.65, 0.15, 0.10, 0.10]
    )

    # Fraud indicators (10% fraud rate)
    is_fraud = np.random.choice([0, 1], n_claims, p=[0.90, 0.10])

    # Fraud score (higher for actual fraud)
    fraud_scores = []
    for fraud in is_fraud:
        if fraud == 1:
            score = np.random.beta(8, 2)  # Skewed high
        else:
            score = np.random.beta(2, 8)  # Skewed low
        fraud_scores.append(round(score, 4))

    # Settlement amounts (0 if denied, less than claim if approved)
    settlement_amounts = []
    for i, status in enumerate(claim_statuses):
        if status == "Denied":
            settlement = 0.0
        elif status == "Approved":
            settlement = claim_amounts[i] * np.random.uniform(0.7, 1.0)
        else:
            settlement = 0.0  # Pending/Under Review
        settlement_amounts.append(round(settlement, 2))

    # Create DataFrame
    df = pl.DataFrame(
        {
            "claim_id": claim_ids,
            "policy_id": policy_ids,
            "claim_date": claim_dates,
            "claim_type": claim_types,
            "claim_amount": claim_amounts,
            "settlement_amount": settlement_amounts,
            "claim_status": claim_statuses,
            "is_fraud": is_fraud,
            "fraud_score": fraud_scores,
        }
    )

    return df


def generate_fraud_predictions(n_samples: int = 5000) -> pl.DataFrame:
    """
    Generate fraud prediction model results for binary classification exercises.

    Args:
        n_samples: Number of samples to generate

    Returns:
        Polars DataFrame with actual fraud labels and model predictions
    """
    # Generate actual fraud labels (10% fraud rate)
    actual_fraud = np.random.choice([0, 1], n_samples, p=[0.90, 0.10])

    # Generate three model predictions with different performance levels

    # Model 1: Good performance (AUC ~0.85)
    model1_scores = []
    for fraud in actual_fraud:
        if fraud == 1:
            score = np.random.beta(7, 2)  # High scores for fraud
        else:
            score = np.random.beta(2, 5)  # Low scores for non-fraud
        model1_scores.append(score)

    # Model 2: Moderate performance (AUC ~0.75)
    model2_scores = []
    for fraud in actual_fraud:
        if fraud == 1:
            score = np.random.beta(5, 3)
        else:
            score = np.random.beta(3, 5)
        model2_scores.append(score)

    # Model 3: Poor performance (AUC ~0.65)
    model3_scores = []
    for fraud in actual_fraud:
        if fraud == 1:
            score = np.random.beta(4, 4)
        else:
            score = np.random.beta(4, 5)
        model3_scores.append(score)

    # Generate claim IDs
    claim_ids = [f"CLM-{i:06d}" for i in range(1, n_samples + 1)]

    # Create DataFrame
    df = pl.DataFrame(
        {
            "claim_id": claim_ids,
            "actual_fraud": actual_fraud,
            "model1_fraud_score": model1_scores,
            "model2_fraud_score": model2_scores,
            "model3_fraud_score": model3_scores,
        }
    )

    return df


def generate_premium_predictions(n_samples: int = 5000) -> pl.DataFrame:
    """
    Generate premium prediction model results for regression exercises.

    Args:
        n_samples: Number of samples to generate

    Returns:
        Polars DataFrame with actual premiums and model predictions
    """
    # Generate customer features
    ages = np.random.normal(45, 15, n_samples).clip(18, 85)
    credit_scores = np.random.normal(700, 80, n_samples).clip(300, 850)
    prior_claims = np.random.poisson(0.3, n_samples)
    coverage_amounts = np.random.choice(
        [25000, 50000, 100000, 250000, 500000], n_samples, p=[0.15, 0.25, 0.30, 0.20, 0.10]
    )

    # Generate actual premiums with realistic formula
    base_premium = 1000
    actual_premiums = (
        base_premium
        + (ages - 45) * 15
        + (700 - credit_scores) * 2
        + prior_claims * 200
        + coverage_amounts * 0.003
        + np.random.normal(0, 150, n_samples)
    ).clip(300, 10000)

    # Model 1: Good predictions (R² ~0.85)
    model1_predictions = actual_premiums + np.random.normal(0, 200, n_samples)

    # Model 2: Moderate predictions (R² ~0.70)
    model2_predictions = actual_premiums + np.random.normal(0, 400, n_samples)

    # Model 3: Poor predictions (R² ~0.50)
    model3_predictions = actual_premiums + np.random.normal(0, 600, n_samples)

    # Generate policy IDs
    policy_ids = [f"POL-{i:06d}" for i in range(1, n_samples + 1)]

    # Create DataFrame
    df = pl.DataFrame(
        {
            "policy_id": policy_ids,
            "customer_age": ages,
            "credit_score": credit_scores,
            "prior_claims_count": prior_claims,
            "coverage_amount": coverage_amounts,
            "actual_premium": actual_premiums,
            "model1_predicted_premium": model1_predictions,
            "model2_predicted_premium": model2_predictions,
            "model3_predicted_premium": model3_predictions,
        }
    )

    return df


if __name__ == "__main__":
    """Generate and save all datasets."""
    import os

    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)

    print("Generating insurance policies...")
    policies = generate_insurance_policies(10000)
    policies.write_csv(os.path.join(data_dir, "insurance_policies.csv"))
    print(f"✓ Generated {len(policies)} policies")

    print("\nGenerating insurance claims...")
    claims = generate_insurance_claims(5000, policies)
    claims.write_csv(os.path.join(data_dir, "insurance_claims.csv"))
    print(f"✓ Generated {len(claims)} claims")

    print("\nGenerating fraud predictions...")
    fraud_preds = generate_fraud_predictions(5000)
    fraud_preds.write_csv(os.path.join(data_dir, "fraud_predictions.csv"))
    print(f"✓ Generated {len(fraud_preds)} fraud predictions")

    print("\nGenerating premium predictions...")
    premium_preds = generate_premium_predictions(5000)
    premium_preds.write_csv(os.path.join(data_dir, "premium_predictions.csv"))
    print(f"✓ Generated {len(premium_preds)} premium predictions")

    print("\n✅ All datasets generated successfully!")
    print(f"📁 Data saved to: {data_dir}")
