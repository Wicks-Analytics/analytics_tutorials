"""
Tutorial 04: Model Comparison with Double Lift
===============================================

In this tutorial, you'll learn:
- How to compare two models using double lift analysis
- Understanding joint lift and conditional lift metrics
- Analyzing score correlation between models
- Making informed decisions about model selection

Scenario:
You have multiple fraud detection models and need to understand:
- Which model performs better
- Whether models are capturing different patterns
- If combining models could improve performance
"""

import sys
from pathlib import Path

import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation, validation_plots


def main():
    """Run the model comparison tutorial."""

    print("=" * 70)
    print("Tutorial 04: Model Comparison with Double Lift")
    print("=" * 70)

    # Step 1: Load data
    print("\n Step 1: Loading fraud prediction data...")
    data_path = project_root / "data" / "fraud_predictions.csv"

    if not data_path.exists():
        print(f"[ERROR] Data file not found: {data_path}")
        print("Please run: python setup_database.py")
        return

    df = pl.read_csv(data_path)
    print(f"[OK] Loaded {len(df)} predictions with 3 models")

    # Step 2: Individual model performance
    print("\n Step 2: Evaluating individual model performance...")

    models = {
        "Model 1": "model1_fraud_score",
        "Model 2": "model2_fraud_score",
        "Model 3": "model3_fraud_score",
    }

    print("\nIndividual Model Metrics:")
    print(f"{'Model':<12} {'AUC Lift':<12} {'AUC ROC':<12} {'Top Decile Lift':<15}")
    print("-" * 55)

    individual_results = {}
    for model_name, score_col in models.items():
        # Lift analysis
        lift_result = model_validation.calculate_lift_curve(
            df, target_column="actual_fraud", score_column=score_col, n_bins=10
        )

        # ROC analysis
        roc_result = model_validation.calculate_roc_curve(
            df, target_column="actual_fraud", score_column=score_col
        )

        individual_results[model_name] = {"lift": lift_result, "roc": roc_result}

        print(
            f"{model_name:<12} {lift_result.auc_score_lift:<12.4f} "
            f"{roc_result.auc_score:<12.4f} {lift_result.score_lift_values[0]:<15.2f}"
        )

    # Step 3: Double lift analysis - Model 1 vs Model 2
    print("\n Step 3: Comparing Model 1 vs Model 2 (Double Lift)...")

    double_lift_result = model_validation.calculate_double_lift(
        df,
        target_column="actual_fraud",
        score1_column="model1_fraud_score",
        score2_column="model2_fraud_score",
        n_bins=10,
    )

    print("\nDouble Lift Metrics:")
    print(f"- Score Correlation: {double_lift_result.correlation:.4f}")
    print(f"- Joint Lift: {double_lift_result.joint_lift:.4f}")
    print(f"- Conditional Lift: {double_lift_result.conditional_lift:.4f}")

    # Step 4: Interpret correlation
    print("\n[INFO] Step 4: Interpreting score correlation...")

    corr = double_lift_result.correlation
    print(f"\nCorrelation: {corr:.4f}")

    if abs(corr) >= 0.9:
        interpretation = "Very high - models are highly similar"
    elif abs(corr) >= 0.7:
        interpretation = "High - models capture similar patterns"
    elif abs(corr) >= 0.5:
        interpretation = "Moderate - some overlap in patterns"
    elif abs(corr) >= 0.3:
        interpretation = "Low - models capture different patterns"
    else:
        interpretation = "Very low - models are largely independent"

    print(f"Interpretation: {interpretation}")

    if abs(corr) < 0.7:
        print("\n[OK] Low correlation suggests models could be combined for better performance")
    else:
        print("\n[WARNING] High correlation suggests models are redundant")

    # Step 5: Understand joint and conditional lift
    print("\n Step 5: Understanding joint and conditional lift...")

    print(f"\nJoint Lift: {double_lift_result.joint_lift:.4f}")
    print("  -> Lift when BOTH models score high")
    print("  -> Measures agreement between models")

    print(f"\nConditional Lift: {double_lift_result.conditional_lift:.4f}")
    print("  -> Lift of Model 2 when Model 1 scores high")
    print("  -> Measures incremental value of Model 2")

    if double_lift_result.conditional_lift > 1.2:
        print("  [OK] Model 2 adds significant value beyond Model 1")
    elif double_lift_result.conditional_lift > 1.0:
        print("  ~ Model 2 adds some value beyond Model 1")
    else:
        print("  [X] Model 2 adds little value beyond Model 1")

    # Step 6: Visualize double lift
    print("\n Step 6: Visualizing double lift comparison...")
    try:
        validation_plots.plot_double_lift(
            df,
            target_column="actual_fraud",
            score1_column="model1_fraud_score",
            score2_column="model2_fraud_score",
            score1_name="Model 1",
            score2_name="Model 2",
            title="Model Comparison: Model 1 vs Model 2",
        )
        print("[OK] Double lift plot displayed")
        print("(Close the plot window to continue)")
    except Exception as e:
        print(f"[WARNING] Could not create plot: {e}")

    # Step 7: Compare all model pairs
    print("\n Step 7: Comparing all model pairs...")

    model_pairs = [
        ("Model 1", "model1_fraud_score", "Model 2", "model2_fraud_score"),
        ("Model 1", "model1_fraud_score", "Model 3", "model3_fraud_score"),
        ("Model 2", "model2_fraud_score", "Model 3", "model3_fraud_score"),
    ]

    print("\nPairwise Comparison:")
    print(f"{'Pair':<20} {'Correlation':<15} {'Joint Lift':<15} {'Conditional Lift':<15}")
    print("-" * 70)

    for name1, col1, name2, col2 in model_pairs:
        result = model_validation.calculate_double_lift(
            df, target_column="actual_fraud", score1_column=col1, score2_column=col2, n_bins=10
        )
        pair_name = f"{name1} vs {name2}"
        print(
            f"{pair_name:<20} {result.correlation:<15.4f} "
            f"{result.joint_lift:<15.4f} {result.conditional_lift:<15.4f}"
        )

    # Step 8: Model selection recommendation
    print("\n Step 8: Model Selection Recommendation...")

    # Find best model by AUC
    best_model = max(individual_results.items(), key=lambda x: x[1]["roc"].auc_score)

    print(f"\nBest Individual Model: {best_model[0]}")
    print(f"- AUC: {best_model[1]['roc'].auc_score:.4f}")
    print(f"- Top Decile Lift: {best_model[1]['lift'].score_lift_values[0]:.2f}x")

    # Check if models are complementary
    print("\nModel Combination Potential:")
    m1_m2_corr = model_validation.calculate_double_lift(
        df, "actual_fraud", "model1_fraud_score", "model2_fraud_score"
    ).correlation

    if abs(m1_m2_corr) < 0.7:
        print("[OK] Models 1 and 2 are complementary - consider ensemble")
    else:
        print("[X] Models are too similar - use best individual model")

    # Step 9: Create ensemble score
    print("\n Step 9: Creating a simple ensemble...")

    # Simple average ensemble
    df_ensemble = df.with_columns(
        [
            ((pl.col("model1_fraud_score") + pl.col("model2_fraud_score")) / 2).alias(
                "ensemble_score"
            )
        ]
    )

    # Evaluate ensemble
    ensemble_lift = model_validation.calculate_lift_curve(
        df_ensemble, target_column="actual_fraud", score_column="ensemble_score", n_bins=10
    )

    ensemble_roc = model_validation.calculate_roc_curve(
        df_ensemble, target_column="actual_fraud", score_column="ensemble_score"
    )

    print("\nEnsemble Performance:")
    print(f"- AUC: {ensemble_roc.auc_score:.4f}")
    print(f"- Top Decile Lift: {ensemble_lift.score_lift_values[0]:.2f}x")

    # Compare with best individual
    improvement = ensemble_roc.auc_score - best_model[1]["roc"].auc_score
    print(f"\nImprovement over best individual: {improvement:+.4f}")

    if improvement > 0.01:
        print("[OK] Ensemble shows meaningful improvement")
    else:
        print("~ Ensemble shows marginal improvement")

    # Step 10: Save results
    print("\n Step 10: Saving comparison results...")

    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)

    # Save double lift results
    double_lift_df = double_lift_result.to_polars()
    double_lift_df.write_csv(output_dir / "04_double_lift_results.csv")
    print(f"[OK] Results saved to: {output_dir / '04_double_lift_results.csv'}")

    # Step 11: Exercise
    print("\n[EXERCISE] EXERCISE: Weighted Ensemble")
    print("\nTry creating a weighted ensemble based on individual model performance:")
    print(
        """
    # Weight models by their AUC scores
    auc1 = individual_results['Model 1']['roc'].auc_score
    auc2 = individual_results['Model 2']['roc'].auc_score

    total_auc = auc1 + auc2
    weight1 = auc1 / total_auc
    weight2 = auc2 / total_auc

    df_weighted = df.with_columns([
        (pl.col('model1_fraud_score') * weight1 +
         pl.col('model2_fraud_score') * weight2)
        .alias('weighted_ensemble')
    ])

    # Evaluate weighted ensemble
    # Compare with simple average ensemble
    """
    )

    print("\n" + "=" * 70)
    print("[SUCCESS] Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Double lift analysis reveals model complementarity")
    print("2. Low correlation suggests models capture different patterns")
    print("3. Joint lift measures agreement between models")
    print("4. Conditional lift shows incremental value")
    print("5. Ensemble models can outperform individual models")
    print("\nNext: Tutorial 05 - SQL Integration")


if __name__ == "__main__":
    main()
