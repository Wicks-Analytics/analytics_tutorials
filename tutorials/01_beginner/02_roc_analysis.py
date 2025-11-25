"""
Tutorial 02: ROC Curve Analysis
================================

In this tutorial, you'll learn:
- What ROC curves are and how they differ from lift curves
- How to calculate AUC (Area Under Curve) scores
- How to find optimal classification thresholds
- How to interpret sensitivity, specificity, and Youden's J statistic

Scenario:
You need to choose a threshold for your fraud detection model to decide
which claims to investigate. ROC analysis helps you understand the trade-off
between catching fraud (sensitivity) and avoiding false alarms (specificity).
"""

import sys
from pathlib import Path

import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation, validation_plots


def main():
    """Run the ROC analysis tutorial."""

    print("=" * 70)
    print("Tutorial 02: ROC Curve Analysis for Fraud Detection")
    print("=" * 70)

    # Step 1: Load data
    print("\n Step 1: Loading fraud prediction data...")
    data_path = project_root / "data" / "fraud_predictions.csv"

    if not data_path.exists():
        print(f"[ERROR] Data file not found: {data_path}")
        print("Please run: python utils/data_generators.py")
        return

    df = pl.read_csv(data_path)
    print(f"[OK] Loaded {len(df)} predictions")

    # Step 2: Calculate ROC curve
    print("\n Step 2: Calculating ROC curve for Model 1...")
    roc_result = model_validation.calculate_roc_curve(
        df, target_column="actual_fraud", score_column="model1_fraud_score"
    )

    print("\nROC Metrics:")
    print(f"- AUC Score: {roc_result.auc_score:.4f}")
    print(f"- Optimal Threshold: {roc_result.optimal_threshold:.4f}")
    print(f"- Number of threshold points: {len(roc_result.thresholds)}")

    # Step 3: Understand the optimal threshold
    print("\n[INFO] Step 3: Understanding the optimal threshold...")
    print(f"\nThe optimal threshold ({roc_result.optimal_threshold:.4f}) is found using")
    print("Youden's J statistic, which maximizes (Sensitivity + Specificity - 1)")
    print("\nAt this threshold:")

    # Find metrics at optimal threshold
    optimal_idx = roc_result.thresholds.index(roc_result.optimal_threshold)
    optimal_tpr = roc_result.tpr[optimal_idx]
    optimal_fpr = roc_result.fpr[optimal_idx]

    print(f"- True Positive Rate (Sensitivity): {optimal_tpr:.2%}")
    print(f"- False Positive Rate: {optimal_fpr:.2%}")
    print(f"- Specificity: {(1 - optimal_fpr):.2%}")

    # Step 4: Interpret AUC score
    print("\n Step 4: Interpreting AUC score...")
    auc = roc_result.auc_score

    if auc >= 0.9:
        interpretation = "Excellent"
    elif auc >= 0.8:
        interpretation = "Good"
    elif auc >= 0.7:
        interpretation = "Fair"
    elif auc >= 0.6:
        interpretation = "Poor"
    else:
        interpretation = "Very Poor"

    print(f"\nAUC Score: {auc:.4f} - {interpretation}")
    print("\nAUC Interpretation Guide:")
    print("- 0.90-1.00: Excellent")
    print("- 0.80-0.90: Good")
    print("- 0.70-0.80: Fair")
    print("- 0.60-0.70: Poor")
    print("- 0.50-0.60: Very Poor (barely better than random)")

    # Step 5: Compare different thresholds
    print("\n Step 5: Comparing different threshold strategies...")

    # Conservative threshold (high specificity, low false alarms)
    conservative_threshold = 0.7
    conservative_idx = min(
        range(len(roc_result.thresholds)),
        key=lambda i: abs(roc_result.thresholds[i] - conservative_threshold),
    )

    # Aggressive threshold (high sensitivity, catch more fraud)
    aggressive_threshold = 0.3
    aggressive_idx = min(
        range(len(roc_result.thresholds)),
        key=lambda i: abs(roc_result.thresholds[i] - aggressive_threshold),
    )

    print("\nThreshold Comparison:")
    print(f"\n{'Strategy':<15} {'Threshold':<12} {'Sensitivity':<12} {'Specificity':<12}")
    print("-" * 55)
    print(
        f"{'Conservative':<15} {conservative_threshold:<12.2f} "
        f"{roc_result.tpr[conservative_idx]:<12.2%} "
        f"{(1 - roc_result.fpr[conservative_idx]):<12.2%}"
    )
    print(
        f"{'Optimal':<15} {roc_result.optimal_threshold:<12.4f} "
        f"{optimal_tpr:<12.2%} {(1 - optimal_fpr):<12.2%}"
    )
    print(
        f"{'Aggressive':<15} {aggressive_threshold:<12.2f} "
        f"{roc_result.tpr[aggressive_idx]:<12.2%} "
        f"{(1 - roc_result.fpr[aggressive_idx]):<12.2%}"
    )

    # Step 6: Convert to DataFrame
    print("\n Step 6: Converting ROC results to DataFrame...")
    roc_df = roc_result.to_polars()
    print("\nROC curve data (showing first 10 points):")
    print(roc_df.head(10))

    # Save results
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)
    roc_df.write_csv(output_dir / "02_roc_results.csv")
    print(f"\n[OK] Results saved to: {output_dir / '02_roc_results.csv'}")

    # Step 7: Visualize ROC curve
    print("\n Step 7: Creating ROC curve visualization...")
    try:
        validation_plots.plot_roc_curve(
            df,
            target_column="actual_fraud",
            score_column="model1_fraud_score",
            title="Fraud Detection Model - ROC Curve",
        )
        print("[OK] ROC curve plot displayed")
        print("(Close the plot window to continue)")
    except Exception as e:
        print(f"[WARNING] Could not create plot: {e}")

    # Step 8: Calculate metrics for all three models
    print("\n Step 8: Comparing all three models...")

    models = {
        "Model 1": "model1_fraud_score",
        "Model 2": "model2_fraud_score",
        "Model 3": "model3_fraud_score",
    }

    print("\nModel Performance Comparison:")
    print(f"{'Model':<12} {'AUC':<10} {'Optimal Threshold':<20}")
    print("-" * 45)

    for model_name, score_col in models.items():
        result = model_validation.calculate_roc_curve(
            df, target_column="actual_fraud", score_column=score_col
        )
        print(f"{model_name:<12} {result.auc_score:<10.4f} {result.optimal_threshold:<20.4f}")

    # Step 9: Exercise
    print("\n[EXERCISE] EXERCISE: ROC with Confidence Intervals")
    print("\nTry calculating ROC curve with bootstrap confidence intervals:")
    print(
        """
    roc_with_ci = model_validation.calculate_roc_curve(
        df,
        target_column='actual_fraud',
        score_column='model1_fraud_score',
        with_ci=True,
        n_iterations=1000,
        confidence_level=0.95
    )

    # Then visualize with:
    validation_plots.plot_roc_curve(
        df,
        target_column='actual_fraud',
        score_column='model1_fraud_score',
        with_ci=True,
        n_iterations=1000
    )
    """
    )

    print("\n" + "=" * 70)
    print("[SUCCESS] Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. ROC curves show the trade-off between sensitivity and specificity")
    print("2. AUC summarizes overall classification performance (0.5-1.0)")
    print("3. Optimal threshold balances true positives and false positives")
    print("4. Different thresholds suit different business needs")
    print("\nNext: Tutorial 03 - Regression Metrics")


if __name__ == "__main__":
    main()
