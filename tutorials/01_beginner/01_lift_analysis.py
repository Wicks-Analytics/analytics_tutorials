"""
Tutorial 01: Introduction to Lift Analysis
===========================================

In this tutorial, you'll learn:
- What lift curves are and why they're important
- How to calculate lift metrics using analytics_store
- How to interpret lift results for insurance claim predictions
- How to visualize lift curves

Scenario:
You have a model that predicts which insurance claims are likely to be fraudulent.
You want to understand how well the model identifies fraud across different score ranges.
"""

import sys
from pathlib import Path

import polars as pl

# Add project root to path to import utilities
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation, validation_plots


def main():
    """Run the lift analysis tutorial."""

    print("=" * 70)
    print("Tutorial 01: Lift Analysis for Fraud Detection")
    print("=" * 70)

    # Step 1: Load the fraud predictions data
    print("\n Step 1: Loading fraud prediction data...")
    data_path = project_root / "data" / "fraud_predictions.csv"

    if not data_path.exists():
        print(f"[ERROR] Data file not found: {data_path}")
        print("Please run: python utils/data_generators.py")
        return

    df = pl.read_csv(data_path)
    print(f"[OK] Loaded {len(df)} predictions")
    print("\nData preview:")
    print(df.head())

    # Step 2: Calculate basic statistics
    print("\n Step 2: Understanding the data...")
    fraud_rate = df["actual_fraud"].mean()
    print(f"Overall fraud rate: {fraud_rate:.2%}")
    print(f"Total frauds: {df['actual_fraud'].sum()}")
    print(f"Total non-frauds: {(1 - df['actual_fraud']).sum()}")

    # Step 3: Calculate lift curve for Model 1
    print("\n Step 3: Calculating lift curve for Model 1...")
    lift_result = model_validation.calculate_lift_curve(
        df,
        target_column="actual_fraud",
        score_column="model1_fraud_score",
        n_bins=10,  # Divide data into 10 deciles
    )

    print("\nLift Metrics:")
    print(f"- Baseline (overall fraud rate): {lift_result.baseline:.4f}")
    print(f"- AUC Lift Score: {lift_result.auc_score_lift:.4f}")
    print(f"- Number of bins: {len(lift_result.score_lift_values)}")

    # Step 4: Examine lift by decile
    print("\n Step 4: Examining lift by decile...")
    print("\nDecile | Fraud Rate | Lift | Cumulative Lift")
    print("-" * 50)
    for i, (rate, lift, cum_lift) in enumerate(
        zip(
            lift_result.score_target_rates,
            lift_result.score_lift_values,
            lift_result.score_cumulative_lift,
        ),
        1,
    ):
        print(f"  {i:2d}   |   {rate:.4f}   | {lift:.2f} |      {cum_lift:.2f}")

    # Step 5: Interpret the results
    print("\n[INFO] Step 5: Interpreting the results...")
    top_decile_lift = lift_result.score_lift_values[0]
    top_decile_rate = lift_result.score_target_rates[0]

    print("\nTop decile (highest scores):")
    print(f"- Fraud rate: {top_decile_rate:.2%}")
    print(f"- Lift: {top_decile_lift:.2f}x")
    print("- Interpretation: The top 10% of claims by score contain")
    print(f"  {top_decile_lift:.1f}x more fraud than random selection")

    # Step 6: Convert results to DataFrame for further analysis
    print("\n Step 6: Converting results to DataFrame...")
    lift_df = lift_result.to_polars()
    print("\nLift curve data:")
    print(lift_df)

    # Optional: Save results
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)
    lift_df.write_csv(output_dir / "01_lift_results.csv")
    print(f"\n[OK] Results saved to: {output_dir / '01_lift_results.csv'}")

    # Step 7: Create visualization
    print("\n Step 7: Creating lift curve visualization...")
    try:
        validation_plots.plot_lift_curve(
            df,
            target_column="actual_fraud",
            score_column="model1_fraud_score",
            n_bins=10,
            title="Fraud Detection Model - Lift Curve",
        )
        print("[OK] Lift curve plot displayed")
        print("(Close the plot window to continue)")
    except Exception as e:
        print(f"[WARNING] Could not create plot: {e}")

    # Step 8: Exercise - Compare with Model 2
    print("\n[EXERCISE] EXERCISE: Try calculating lift for Model 2")
    print("Hint: Use 'model2_fraud_score' as the score_column")
    print("\nUncomment the code below to see the solution:")
    print(
        """
    # lift_result_m2 = model_validation.calculate_lift_curve(
    #     df,
    #     target_column='actual_fraud',
    #     score_column='model2_fraud_score',
    #     n_bins=10
    # )
    # print(f"Model 2 AUC Lift: {lift_result_m2.auc_score_lift:.4f}")
    # print(f"Model 1 AUC Lift: {lift_result.auc_score_lift:.4f}")
    """
    )

    print("\n" + "=" * 70)
    print("[SUCCESS] Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Lift curves show how well a model ranks predictions")
    print("2. Higher lift in top deciles = better model performance")
    print("3. AUC Lift summarizes overall ranking performance")
    print("4. Lift > 1 means better than random selection")
    print("\nNext: Tutorial 02 - ROC Curve Analysis")


if __name__ == "__main__":
    main()
