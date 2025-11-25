"""
Tutorial 07: Model Monitoring and Drift Detection
==================================================

In this tutorial, you'll learn:
- How to detect data drift in production models
- Using PSI (Population Stability Index) for feature drift
- Monitoring model performance over time
- Statistical tests for population comparison
- Setting up automated monitoring workflows

Scenario:
Your fraud detection model has been in production for several months.
You need to monitor whether the data distribution has changed and if
the model performance is degrading.
"""

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation, monitoring


def generate_drifted_data(original_df: pl.DataFrame, drift_amount: float = 0.3) -> pl.DataFrame:
    """
    Generate a drifted version of the data to simulate production drift.

    Args:
        original_df: Original fraud predictions data
        drift_amount: Amount of drift to introduce (0-1)

    Returns:
        DataFrame with drifted scores
    """
    # Add drift to scores (shift distribution)
    drifted = original_df.with_columns(
        [
            (
                pl.col("model1_fraud_score") * (1 - drift_amount)
                + pl.lit(np.random.beta(2, 5, len(original_df))) * drift_amount
            ).alias("model1_fraud_score_drifted")
        ]
    )

    return drifted


def main():
    """Run the model monitoring tutorial."""

    print("=" * 70)
    print("Tutorial 07: Model Monitoring and Drift Detection")
    print("=" * 70)

    # Step 1: Load baseline (training) data
    print("\n📊 Step 1: Loading baseline data...")
    data_path = project_root / "data" / "fraud_predictions.csv"

    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        print("Please run: python setup_database.py")
        return

    baseline_df = pl.read_csv(data_path)
    print(f"✓ Loaded {len(baseline_df)} baseline predictions")

    # Split into baseline and current
    baseline = baseline_df.head(3000)
    current = baseline_df.tail(2000)

    print(f"- Baseline period: {len(baseline)} samples")
    print(f"- Current period: {len(current)} samples")

    # Step 2: Basic population comparison
    print("\n🔍 Step 2: Comparing score distributions...")

    result = monitoring.compare_populations(
        baseline,
        column1="model1_fraud_score",
        column2="model1_fraud_score",
        alpha=0.05,
        test_type="auto",
    )

    # For this example, compare baseline vs current from different data
    current_scores = current["model1_fraud_score"].to_list()
    baseline_scores = baseline["model1_fraud_score"].to_list()

    # Create combined dataframe for comparison
    comparison_df = pl.DataFrame(
        {
            "baseline_scores": baseline_scores[: min(len(baseline_scores), len(current_scores))],
            "current_scores": current_scores[: min(len(baseline_scores), len(current_scores))],
        }
    )

    result = monitoring.compare_populations(
        comparison_df,
        column1="baseline_scores",
        column2="current_scores",
        alpha=0.05,
        test_type="auto",
    )

    print("\nPopulation Comparison Results:")
    print(f"- Test Type: {result.test_type}")
    print(f"- Test Statistic: {result.statistic:.4f}")
    print(f"- P-value: {result.p_value:.4f}")
    print(f"- Effect Size: {result.effect_size:.4f}")
    print(f"- Significant Difference: {result.is_significant}")

    # Step 3: Interpret effect size
    print("\n💡 Step 3: Interpreting effect size...")

    effect_size = abs(result.effect_size)

    if effect_size < 0.2:
        interpretation = "Negligible"
        action = "No action needed"
    elif effect_size < 0.5:
        interpretation = "Small"
        action = "Monitor closely"
    elif effect_size < 0.8:
        interpretation = "Medium"
        action = "Investigate and consider retraining"
    else:
        interpretation = "Large"
        action = "Immediate action required - retrain model"

    print(f"\nEffect Size: {effect_size:.4f} - {interpretation}")
    print(f"Recommended Action: {action}")

    # Step 4: Simulate data drift
    print("\n⚠️  Step 4: Simulating data drift scenario...")

    # Create drifted data
    drifted_df = generate_drifted_data(baseline, drift_amount=0.3)

    # Compare baseline vs drifted
    drift_comparison = pl.DataFrame(
        {
            "baseline": baseline["model1_fraud_score"].to_list()[:2000],
            "drifted": drifted_df["model1_fraud_score_drifted"].to_list()[:2000],
        }
    )

    drift_result = monitoring.compare_populations(
        drift_comparison, column1="baseline", column2="drifted", alpha=0.05, test_type="auto"
    )

    print("\nDrift Detection Results:")
    print(f"- P-value: {drift_result.p_value:.4f}")
    print(f"- Effect Size: {drift_result.effect_size:.4f}")
    print(f"- Drift Detected: {drift_result.is_significant}")

    if drift_result.is_significant:
        print("\n⚠️  WARNING: Significant drift detected!")
        print("   Model may need retraining")

    # Step 5: Monitor performance metrics over time
    print("\n📈 Step 5: Monitoring performance over time...")

    # Simulate monthly performance
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    monthly_metrics = []

    print("\nMonthly Performance Tracking:")
    print(f"{'Month':<8} {'AUC':<10} {'Top Decile Lift':<18} {'Change':<10}")
    print("-" * 50)

    # Split data into monthly chunks
    chunk_size = len(baseline_df) // 6

    for i, month in enumerate(months):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        month_data = baseline_df[start_idx:end_idx]

        # Calculate metrics
        roc_result = model_validation.calculate_roc_curve(
            month_data, target_column="actual_fraud", score_column="model1_fraud_score"
        )

        lift_result = model_validation.calculate_lift_curve(
            month_data, target_column="actual_fraud", score_column="model1_fraud_score", n_bins=10
        )

        monthly_metrics.append(
            {
                "month": month,
                "auc": roc_result.auc_score,
                "top_decile_lift": lift_result.score_lift_values[0],
            }
        )

        # Calculate change from previous month
        if i > 0:
            auc_change = roc_result.auc_score - monthly_metrics[i - 1]["auc"]
            change_str = f"{auc_change:+.4f}"
        else:
            change_str = "baseline"

        print(
            f"{month:<8} {roc_result.auc_score:<10.4f} "
            f"{lift_result.score_lift_values[0]:<18.2f} {change_str:<10}"
        )

    # Step 6: Set up monitoring thresholds
    print("\n🎯 Step 6: Setting up monitoring thresholds...")

    baseline_auc = monthly_metrics[0]["auc"]

    print(f"\nBaseline AUC: {baseline_auc:.4f}")
    print("\nMonitoring Thresholds:")
    print(f"- Warning (5% drop): {baseline_auc * 0.95:.4f}")
    print(f"- Critical (10% drop): {baseline_auc * 0.90:.4f}")

    # Check current performance
    current_auc = monthly_metrics[-1]["auc"]
    drop_pct = ((baseline_auc - current_auc) / baseline_auc) * 100

    print(f"\nCurrent AUC: {current_auc:.4f}")
    print(f"Performance Drop: {drop_pct:.1f}%")

    if drop_pct >= 10:
        print("🔴 CRITICAL: Performance degradation detected!")
    elif drop_pct >= 5:
        print("🟡 WARNING: Performance decline detected")
    else:
        print("🟢 OK: Performance within acceptable range")

    # Step 7: Feature drift analysis
    print("\n📊 Step 7: Analyzing feature distributions...")

    # Compare score distributions
    print("\nScore Distribution Comparison:")
    print(f"{'Metric':<20} {'Baseline':<15} {'Current':<15} {'Change':<10}")
    print("-" * 60)

    baseline_stats = {
        "Mean": baseline["model1_fraud_score"].mean(),
        "Median": baseline["model1_fraud_score"].median(),
        "Std Dev": baseline["model1_fraud_score"].std(),
        "Min": baseline["model1_fraud_score"].min(),
        "Max": baseline["model1_fraud_score"].max(),
    }

    current_stats = {
        "Mean": current["model1_fraud_score"].mean(),
        "Median": current["model1_fraud_score"].median(),
        "Std Dev": current["model1_fraud_score"].std(),
        "Min": current["model1_fraud_score"].min(),
        "Max": current["model1_fraud_score"].max(),
    }

    for metric in baseline_stats.keys():
        baseline_val = baseline_stats[metric]
        current_val = current_stats[metric]
        change = current_val - baseline_val

        print(f"{metric:<20} {baseline_val:<15.4f} {current_val:<15.4f} {change:+.4f}")

    # Step 8: Create monitoring report
    print("\n📋 Step 8: Generating monitoring report...")

    report = {
        "timestamp": datetime.now().isoformat(),
        "baseline_samples": len(baseline),
        "current_samples": len(current),
        "baseline_auc": baseline_auc,
        "current_auc": current_auc,
        "performance_drop_pct": drop_pct,
        "drift_detected": drift_result.is_significant,
        "drift_p_value": drift_result.p_value,
        "drift_effect_size": drift_result.effect_size,
    }

    report_df = pl.DataFrame([report])

    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)
    report_df.write_csv(output_dir / "07_monitoring_report.csv")

    print(f"✓ Report saved to: {output_dir / '07_monitoring_report.csv'}")
    print("\nReport Summary:")
    for key, value in report.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    # Step 9: Automated monitoring workflow
    print("\n🤖 Step 9: Automated monitoring workflow example...")
    print(
        """
    def monitor_model_performance(baseline_df, current_df, thresholds):
        '''
        Automated monitoring function to run daily/weekly.
        '''
        # 1. Compare populations
        result = monitoring.compare_populations(
            baseline_df, 'score', 'score'
        )

        # 2. Calculate current metrics
        current_auc = calculate_roc_curve(
            current_df, 'actual', 'score'
        ).auc_score

        # 3. Check thresholds
        alerts = []
        if result.is_significant:
            alerts.append('Data drift detected')

        if current_auc < thresholds['critical']:
            alerts.append('Critical performance drop')
        elif current_auc < thresholds['warning']:
            alerts.append('Performance warning')

        # 4. Send alerts if needed
        if alerts:
            send_alert(alerts)

        # 5. Log metrics
        log_metrics(current_auc, result.p_value)

        return alerts
    """
    )

    # Step 10: Exercise
    print("\n🎓 EXERCISE: Build a Monitoring Dashboard")
    print(
        """
    Create a monitoring script that:
    1. Loads baseline and current data from database
    2. Calculates multiple metrics (AUC, lift, precision, recall)
    3. Performs drift detection on scores
    4. Generates alerts based on thresholds
    5. Saves results to a monitoring table
    6. Creates visualization of metrics over time

    Bonus: Set up scheduled execution (e.g., daily cron job)
    """
    )

    print("\n" + "=" * 70)
    print("✅ Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Monitor both data drift and performance metrics")
    print("2. Use statistical tests to detect significant changes")
    print("3. Set up thresholds for automated alerting")
    print("4. Track metrics over time to identify trends")
    print("5. Effect size helps prioritize actions")
    print("\nNext: Tutorial 08 - Snowflake Integration")


if __name__ == "__main__":
    main()
