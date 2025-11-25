"""
Tutorial 03: Regression Metrics
================================

In this tutorial, you'll learn:
- How to evaluate regression models for premium prediction
- Understanding RMSE, MAE, and R-squared metrics
- Creating diagnostic plots to identify model issues
- Analyzing model performance by segments

Scenario:
You have built models to predict insurance premiums based on customer
characteristics. You need to evaluate which model performs best and
understand where the models might be making errors.
"""

import sys
from pathlib import Path

import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation, validation_plots


def main():
    """Run the regression metrics tutorial."""

    print("=" * 70)
    print("Tutorial 03: Regression Metrics for Premium Prediction")
    print("=" * 70)

    # Step 1: Load data
    print("\n Step 1: Loading premium prediction data...")
    data_path = project_root / "data" / "premium_predictions.csv"

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
    print("Actual premium statistics:")
    print(f"- Mean: ${df['actual_premium'].mean():.2f}")
    print(f"- Median: ${df['actual_premium'].median():.2f}")
    print(f"- Std Dev: ${df['actual_premium'].std():.2f}")
    print(f"- Min: ${df['actual_premium'].min():.2f}")
    print(f"- Max: ${df['actual_premium'].max():.2f}")

    # Step 3: Calculate regression metrics for Model 1
    print("\n Step 3: Calculating regression metrics for Model 1...")
    metrics = model_validation.calculate_regression_metrics(
        df,
        actual_column="actual_premium",
        predicted_column="model1_predicted_premium",
        n_features=4,  # We have 4 features: age, credit_score, prior_claims, coverage
    )

    print("\nRegression Metrics:")
    print(f"- RMSE (Root Mean Square Error): ${metrics.rmse:.2f}")
    print(f"- MAE (Mean Absolute Error): ${metrics.mae:.2f}")
    print(f"- R-squared: {metrics.r2:.4f}")
    print(f"- Adjusted R-squared: {metrics.adj_r2:.4f}")
    print(f"- Number of samples: {metrics.n_samples}")

    # Step 4: Interpret the metrics
    print("\n[INFO] Step 4: Interpreting the metrics...")

    print(f"\nRMSE: ${metrics.rmse:.2f}")
    print(f"  -> On average, predictions are off by about ${metrics.rmse:.2f}")
    print(f"  -> As % of mean premium: {(metrics.rmse / df['actual_premium'].mean()) * 100:.1f}%")

    print(f"\nMAE: ${metrics.mae:.2f}")
    print(f"  -> Median absolute error is ${metrics.mae:.2f}")
    print("  -> More robust to outliers than RMSE")

    print(f"\nR-squared: {metrics.r2:.4f}")
    print(f"  -> Model explains {metrics.r2 * 100:.1f}% of variance in premiums")

    if metrics.r2 >= 0.9:
        interpretation = "Excellent fit"
    elif metrics.r2 >= 0.7:
        interpretation = "Good fit"
    elif metrics.r2 >= 0.5:
        interpretation = "Moderate fit"
    else:
        interpretation = "Poor fit"
    print(f"  -> {interpretation}")

    # Step 5: Compare all three models
    print("\n Step 5: Comparing all three models...")

    models = {
        "Model 1": "model1_predicted_premium",
        "Model 2": "model2_predicted_premium",
        "Model 3": "model3_predicted_premium",
    }

    print("\nModel Performance Comparison:")
    print(f"{'Model':<12} {'RMSE':<12} {'MAE':<12} {'R^2':<10}")
    print("-" * 50)

    all_metrics = []
    for model_name, pred_col in models.items():
        m = model_validation.calculate_regression_metrics(
            df, actual_column="actual_premium", predicted_column=pred_col, n_features=4
        )
        print(f"{model_name:<12} ${m.rmse:<11.2f} ${m.mae:<11.2f} {m.r2:<10.4f}")

        # Store for later analysis
        metrics_df = m.to_polars()
        metrics_df = metrics_df.with_columns(pl.lit(model_name).alias("model_name"))
        all_metrics.append(metrics_df)

    # Step 6: Save combined metrics
    print("\n Step 6: Saving combined metrics...")
    combined_metrics = pl.concat(all_metrics)

    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)
    combined_metrics.write_csv(output_dir / "03_regression_metrics.csv")
    print(f"[OK] Metrics saved to: {output_dir / '03_regression_metrics.csv'}")

    # Step 7: Create diagnostic plots
    print("\n Step 7: Creating diagnostic plots for Model 1...")
    try:
        validation_plots.plot_regression_diagnostics(
            df,
            actual_column="actual_premium",
            predicted_column="model1_predicted_premium",
            title="Premium Prediction Model 1 - Diagnostics",
        )
        print("[OK] Diagnostic plots displayed")
        print("\nThe diagnostic plots show:")
        print("  1. Actual vs Predicted: Should follow diagonal line")
        print("  2. Residual Plot: Should be randomly scattered around 0")
        print("  3. Q-Q Plot: Should follow diagonal if residuals are normal")
        print("(Close the plot window to continue)")
    except Exception as e:
        print(f"[WARNING] Could not create plot: {e}")

    # Step 8: Analyze errors by customer age groups
    print("\n Step 8: Analyzing errors by customer segments...")

    # Add age groups
    df_with_groups = df.with_columns(
        [
            pl.when(pl.col("customer_age") < 30)
            .then(pl.lit("Under 30"))
            .when(pl.col("customer_age") < 50)
            .then(pl.lit("30-49"))
            .when(pl.col("customer_age") < 65)
            .then(pl.lit("50-64"))
            .otherwise(pl.lit("65+"))
            .alias("age_group")
        ]
    )

    # Calculate errors by group
    df_with_errors = df_with_groups.with_columns(
        [
            (pl.col("model1_predicted_premium") - pl.col("actual_premium")).alias("error"),
            ((pl.col("model1_predicted_premium") - pl.col("actual_premium")).abs()).alias(
                "abs_error"
            ),
        ]
    )

    print("\nError Analysis by Age Group:")
    print(f"{'Age Group':<12} {'Count':<8} {'Mean Error':<15} {'Mean Abs Error':<15}")
    print("-" * 55)

    for age_group in ["Under 30", "30-49", "50-64", "65+"]:
        group_df = df_with_errors.filter(pl.col("age_group") == age_group)
        count = len(group_df)
        mean_error = group_df["error"].mean()
        mean_abs_error = group_df["abs_error"].mean()
        print(f"{age_group:<12} {count:<8} ${mean_error:<14.2f} ${mean_abs_error:<14.2f}")

    # Step 9: Exercise
    print("\n[EXERCISE] EXERCISE: Analyze by Coverage Amount")
    print("\nTry analyzing model performance by coverage amount:")
    print(
        """
    # Create coverage groups
    df_coverage = df.with_columns([
        pl.when(pl.col('coverage_amount') < 50000).then(pl.lit('Low'))
        .when(pl.col('coverage_amount') < 250000).then(pl.lit('Medium'))
        .otherwise(pl.lit('High')).alias('coverage_group')
    ])

    # Calculate metrics for each group
    for group in ['Low', 'Medium', 'High']:
        group_df = df_coverage.filter(pl.col('coverage_group') == group)
        metrics = model_validation.calculate_regression_metrics(
            group_df,
            actual_column='actual_premium',
            predicted_column='model1_predicted_premium'
        )
        print(f"{group}: RMSE=${metrics.rmse:.2f}, R^2={metrics.r2:.4f}")
    """
    )

    print("\n" + "=" * 70)
    print("[SUCCESS] Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. RMSE and MAE measure prediction error in original units")
    print("2. R-squared shows proportion of variance explained (0-1)")
    print("3. Diagnostic plots help identify systematic errors")
    print("4. Segment analysis reveals where models perform well/poorly")
    print("\nNext: Tutorial 04 - Model Comparison (Intermediate)")


if __name__ == "__main__":
    main()
