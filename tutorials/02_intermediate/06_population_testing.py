"""
Tutorial 06: Population Testing
================================

In this tutorial, you'll learn:
- How to compare different customer segments statistically
- Using t-tests and Mann-Whitney U tests
- Calculating and interpreting effect sizes
- Making data-driven decisions about segment differences

Scenario:
You want to understand if different customer segments (e.g., by state,
age group, policy type) have significantly different claim rates or
premium amounts. Statistical tests help you make objective decisions.
"""

import sys
from pathlib import Path

import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import monitoring


def main():
    """Run the population testing tutorial."""

    print("=" * 70)
    print("Tutorial 06: Population Testing")
    print("=" * 70)

    # Step 1: Load data
    print("\n Step 1: Loading premium prediction data...")
    data_path = project_root / "data" / "premium_predictions.csv"

    if not data_path.exists():
        print(f"[ERROR] Data file not found: {data_path}")
        print("Please run: python setup_database.py")
        return

    df = pl.read_csv(data_path)
    print(f"[OK] Loaded {len(df)} predictions")

    # Step 2: Create age groups
    print("\n Step 2: Creating customer segments...")

    df_segments = df.with_columns(
        [
            pl.when(pl.col("customer_age") < 30)
            .then(pl.lit("Young"))
            .when(pl.col("customer_age") < 50)
            .then(pl.lit("Middle"))
            .when(pl.col("customer_age") < 65)
            .then(pl.lit("Senior"))
            .otherwise(pl.lit("Elderly"))
            .alias("age_group"),
            pl.when(pl.col("coverage_amount") < 100000)
            .then(pl.lit("Low"))
            .when(pl.col("coverage_amount") < 250000)
            .then(pl.lit("Medium"))
            .otherwise(pl.lit("High"))
            .alias("coverage_group"),
        ]
    )

    print("[OK] Created age_group and coverage_group segments")

    # Step 3: Compare two age groups
    print("\n Step 3: Comparing Young vs Elderly premiums...")

    young = df_segments.filter(pl.col("age_group") == "Young")
    elderly = df_segments.filter(pl.col("age_group") == "Elderly")

    print(f"- Young customers: {len(young)}")
    print(f"- Elderly customers: {len(elderly)}")

    # Create comparison dataframe
    min_len = min(len(young), len(elderly))
    comparison_df = pl.DataFrame(
        {
            "young_premiums": young["actual_premium"].to_list()[:min_len],
            "elderly_premiums": elderly["actual_premium"].to_list()[:min_len],
        }
    )

    # Perform statistical test
    result = monitoring.compare_populations(
        comparison_df,
        column1="young_premiums",
        column2="elderly_premiums",
        alpha=0.05,
        test_type="auto",
    )

    print("\nStatistical Test Results:")
    print(f"- Test Type: {result.test_type}")
    print(f"- Test Statistic: {result.statistic:.4f}")
    print(f"- P-value: {result.p_value:.6f}")
    print(f"- Effect Size: {result.effect_size:.4f}")
    print(f"- Significant Difference: {result.is_significant}")

    # Step 4: Interpret the results
    print("\n[INFO] Step 4: Interpreting the results...")

    young_mean = young["actual_premium"].mean()
    elderly_mean = elderly["actual_premium"].mean()

    print("\nMean Premiums:")
    print(f"- Young: ${young_mean:.2f}")
    print(f"- Elderly: ${elderly_mean:.2f}")
    print(f"- Difference: ${elderly_mean - young_mean:.2f}")

    if result.is_significant:
        print("\n[OK] The difference IS statistically significant (p < 0.05)")
        print("  We can be confident this difference is not due to chance")
    else:
        print("\n[X] The difference is NOT statistically significant (p >= 0.05)")
        print("  The difference could be due to random variation")

    # Step 5: Understand effect size
    print("\n Step 5: Understanding effect size...")

    effect_size = abs(result.effect_size)

    if result.test_type == "t-test":
        print("\nEffect Size (Cohen's d):")
    else:
        print("\nEffect Size (Rank-Biserial Correlation):")

    if effect_size < 0.2:
        interpretation = "Negligible - very small practical difference"
    elif effect_size < 0.5:
        interpretation = "Small - noticeable but modest difference"
    elif effect_size < 0.8:
        interpretation = "Medium - substantial difference"
    else:
        interpretation = "Large - very substantial difference"

    print(f"- Value: {effect_size:.4f}")
    print(f"- Interpretation: {interpretation}")

    print("\nEffect Size Guidelines:")
    print("- < 0.2: Negligible")
    print("- 0.2-0.5: Small")
    print("- 0.5-0.8: Medium")
    print("- > 0.8: Large")

    # Step 6: Compare all age groups
    print("\n Step 6: Comparing all age group pairs...")

    age_groups = ["Young", "Middle", "Senior", "Elderly"]

    print("\nPairwise Comparisons:")
    print(
        f"{'Comparison':<25} {'Mean Diff':<12} {'P-value':<12} {'Effect Size':<12} {'Significant':<12}"
    )
    print("-" * 75)

    for i, group1 in enumerate(age_groups):
        for group2 in age_groups[i + 1 :]:
            g1_data = df_segments.filter(pl.col("age_group") == group1)
            g2_data = df_segments.filter(pl.col("age_group") == group2)

            min_len = min(len(g1_data), len(g2_data))
            comp_df = pl.DataFrame(
                {
                    "group1": g1_data["actual_premium"].to_list()[:min_len],
                    "group2": g2_data["actual_premium"].to_list()[:min_len],
                }
            )

            result = monitoring.compare_populations(
                comp_df, column1="group1", column2="group2", alpha=0.05, test_type="auto"
            )

            mean_diff = g2_data["actual_premium"].mean() - g1_data["actual_premium"].mean()
            sig_marker = "[OK]" if result.is_significant else "[X]"

            comparison_name = f"{group1} vs {group2}"
            print(
                f"{comparison_name:<25} ${mean_diff:<11.2f} {result.p_value:<12.6f} "
                f"{abs(result.effect_size):<12.4f} {sig_marker:<12}"
            )

    # Step 7: Compare by coverage groups
    print("\n Step 7: Comparing coverage groups...")

    low_cov = df_segments.filter(pl.col("coverage_group") == "Low")
    high_cov = df_segments.filter(pl.col("coverage_group") == "High")

    min_len = min(len(low_cov), len(high_cov))
    cov_comparison = pl.DataFrame(
        {
            "low_coverage": low_cov["actual_premium"].to_list()[:min_len],
            "high_coverage": high_cov["actual_premium"].to_list()[:min_len],
        }
    )

    cov_result = monitoring.compare_populations(
        cov_comparison,
        column1="low_coverage",
        column2="high_coverage",
        alpha=0.05,
        test_type="auto",
    )

    print("\nLow vs High Coverage:")
    print(f"- Low coverage mean: ${low_cov['actual_premium'].mean():.2f}")
    print(f"- High coverage mean: ${high_cov['actual_premium'].mean():.2f}")
    print(f"- P-value: {cov_result.p_value:.6f}")
    print(f"- Effect size: {abs(cov_result.effect_size):.4f}")
    print(f"- Significant: {cov_result.is_significant}")

    # Step 8: Test selection (automatic vs manual)
    print("\n Step 8: Understanding test selection...")

    print("\nAutomatic Test Selection:")
    print("- Checks normality using Shapiro-Wilk test")
    print("- If both groups are normal -> t-test")
    print("- If either group is non-normal -> Mann-Whitney U test")

    print("\nManual Test Selection:")
    print(
        """
    # Force t-test (assumes normality)
    result_t = monitoring.compare_populations(
        df, 'group1', 'group2', test_type='t-test'
    )

    # Force Mann-Whitney U (non-parametric)
    result_mw = monitoring.compare_populations(
        df, 'group1', 'group2', test_type='mann-whitney'
    )
    """
    )

    # Step 9: Multiple comparisons consideration
    print("\n[WARNING]  Step 9: Multiple comparisons consideration...")

    print("\nWhen performing multiple tests, consider:")
    print("- Bonferroni correction: Divide alpha by number of tests")
    print("- False Discovery Rate (FDR) control")
    print("- Family-wise error rate")

    n_comparisons = 6  # From age group comparisons
    bonferroni_alpha = 0.05 / n_comparisons

    print(f"\nExample: {n_comparisons} comparisons")
    print("- Original alpha: 0.05")
    print(f"- Bonferroni-corrected alpha: {bonferroni_alpha:.4f}")
    print("- Use this stricter threshold to control false positives")

    # Step 10: Practical applications
    print("\n Step 10: Practical applications...")

    print("\nUse population testing for:")
    print("[OK] A/B testing (comparing control vs treatment groups)")
    print("[OK] Segment analysis (comparing customer segments)")
    print("[OK] Model monitoring (comparing baseline vs current data)")
    print("[OK] Quality control (comparing batches or time periods)")
    print("[OK] Feature importance (comparing groups with/without feature)")

    # Step 11: Save results
    print("\n Step 11: Saving comparison results...")

    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)

    # Create summary report
    summary = pl.DataFrame(
        {
            "comparison": ["Young vs Elderly", "Low vs High Coverage"],
            "test_type": [result.test_type, cov_result.test_type],
            "p_value": [result.p_value, cov_result.p_value],
            "effect_size": [result.effect_size, cov_result.effect_size],
            "is_significant": [result.is_significant, cov_result.is_significant],
        }
    )

    summary.write_csv(output_dir / "06_population_tests.csv")
    print(f"[OK] Results saved to: {output_dir / '06_population_tests.csv'}")

    # Step 12: Exercise
    print("\n[EXERCISE] EXERCISE: Credit Score Analysis")
    print(
        """
    Analyze if credit scores differ significantly between groups:

    1. Create credit score groups (Low: <650, Medium: 650-750, High: >750)
    2. Compare premiums across credit score groups
    3. Test if high credit score customers pay less
    4. Calculate effect sizes for each comparison
    5. Create a summary report

    Bonus: Test if model errors differ by credit score group
    """
    )

    print("\n" + "=" * 70)
    print("[SUCCESS] Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Statistical tests determine if differences are significant")
    print("2. P-value < 0.05 typically indicates significance")
    print("3. Effect size measures practical importance")
    print("4. Automatic test selection handles normality assumptions")
    print("5. Consider multiple comparison corrections when needed")
    print("\nNext: Tutorial 07 - Model Monitoring (Advanced)")


if __name__ == "__main__":
    main()
