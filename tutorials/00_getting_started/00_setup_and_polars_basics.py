"""
Tutorial 00: Project Setup and Polars Basics
=============================================

In this tutorial, you'll learn:
- How to set up your analytics environment
- Basic Polars DataFrame operations
- Loading and exploring insurance data
- Essential data manipulation techniques
- Preparing data for analysis

This is a foundational tutorial - complete this before moving to Tutorial 01.
"""

import sys
from pathlib import Path

# Add project root to path to import utilities
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Run the setup and Polars basics tutorial."""

    print("=" * 70)
    print("Tutorial 00: Project Setup and Polars Basics")
    print("=" * 70)

    # Step 1: Verify environment setup
    print("\n Step 1: Verifying environment setup...")

    try:
        import polars as pl

        print(f"[OK] Polars version: {pl.__version__}")
    except ImportError:
        print("[X] Polars not found. Install with: pip install polars")
        return

    try:
        from analytics_store import model_validation

        print("[OK] analytics_store package found")
    except ImportError:
        print("[X] analytics_store not found. Install with:")
        print("  pip install git+https://github.com/Wicks-Analytics/analytics_store")
        return

    # Check if data exists
    data_dir = project_root / "data"
    if not data_dir.exists():
        print(f"[X] Data directory not found: {data_dir}")
        print("  Run: python setup_database.py")
        return

    print(f"[OK] Data directory found: {data_dir}")
    print("\n[SUCCESS] Environment setup verified!")

    # Step 2: Loading data with Polars
    print("\n Step 2: Loading data with Polars...")

    # Load insurance policies data
    policies_path = data_dir / "insurance_policies.csv"

    if not policies_path.exists():
        print(f"[X] Data file not found: {policies_path}")
        print("  Run: python setup_database.py")
        return

    # Load with Polars - note how fast this is!
    df = pl.read_csv(policies_path)
    print(f"[OK] Loaded {len(df)} insurance policies")
    print(f"[OK] Columns: {df.shape[1]}")
    print(f"[OK] Memory usage: {df.estimated_size('mb'):.2f} MB")

    # Step 3: Exploring the data
    print("\n Step 3: Exploring the data structure...")

    print("\nColumn names and types:")
    for col, dtype in zip(df.columns, df.dtypes):
        print(f"  - {col:20s} : {dtype}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nBasic statistics:")
    print(df.describe())

    # Step 4: Selecting columns
    print("\n Step 4: Selecting and filtering columns...")

    # Select specific columns
    customer_info = df.select(["policy_id", "age", "gender", "region"])
    print("\nSelected customer info columns:")
    print(customer_info.head())

    # Select by data type
    numeric_cols = df.select(pl.col(pl.NUMERIC_DTYPES))
    print(f"\nNumeric columns: {numeric_cols.columns}")

    # Step 5: Filtering rows
    print("\n Step 5: Filtering rows...")

    # Filter by condition
    young_drivers = df.filter(pl.col("age") < 30)
    print(f"\nPolicies for drivers under 30: {len(young_drivers)}")

    # Multiple conditions
    high_value_young = df.filter((pl.col("age") < 30) & (pl.col("annual_premium") > 1000))
    print(f"Young drivers with premium > $1000: {len(high_value_young)}")

    # Filter by string matching
    urban_policies = df.filter(pl.col("region").str.contains("Urban"))
    print(f"Urban region policies: {len(urban_policies)}")

    # Step 6: Adding and modifying columns
    print("\n+ Step 6: Adding and modifying columns...")

    # Add a new column
    df_with_monthly = df.with_columns([(pl.col("annual_premium") / 12).alias("monthly_premium")])
    print("\nAdded monthly_premium column:")
    print(df_with_monthly.select(["policy_id", "annual_premium", "monthly_premium"]).head())

    # Create age groups
    df_with_groups = df.with_columns(
        [
            pl.when(pl.col("age") < 25)
            .then(pl.lit("Young"))
            .when(pl.col("age") < 40)
            .then(pl.lit("Middle"))
            .otherwise(pl.lit("Senior"))
            .alias("age_group")
        ]
    )
    print("\nAge group distribution:")
    print(df_with_groups.group_by("age_group").agg(pl.count()).sort("age_group"))

    # Step 7: Aggregations and grouping
    print("\n Step 7: Aggregations and grouping...")

    # Group by region
    region_stats = (
        df.group_by("region")
        .agg(
            [
                pl.count().alias("policy_count"),
                pl.col("annual_premium").mean().alias("avg_premium"),
                pl.col("annual_premium").median().alias("median_premium"),
                pl.col("annual_premium").std().alias("std_premium"),
            ]
        )
        .sort("avg_premium", descending=True)
    )

    print("\nPremium statistics by region:")
    print(region_stats)

    # Multiple grouping columns
    gender_region_stats = (
        df.group_by(["gender", "region"])
        .agg([pl.count().alias("count"), pl.col("annual_premium").mean().alias("avg_premium")])
        .sort(["gender", "avg_premium"], descending=[False, True])
    )

    print("\nPremium by gender and region:")
    print(gender_region_stats.head(10))

    # Step 8: Sorting and ranking
    print("\n Step 8: Sorting and ranking...")

    # Sort by premium
    top_premiums = (
        df.select(["policy_id", "age", "vehicle_type", "annual_premium"])
        .sort("annual_premium", descending=True)
        .head(10)
    )

    print("\nTop 10 highest premiums:")
    print(top_premiums)

    # Add rank
    df_with_rank = df.with_columns(
        [pl.col("annual_premium").rank(descending=True).alias("premium_rank")]
    )
    print("\nPolicies with premium rank:")
    print(df_with_rank.select(["policy_id", "annual_premium", "premium_rank"]).head())

    # Step 9: Handling missing data
    print("\n Step 9: Handling missing data...")

    # Check for null values
    null_counts = df.null_count()
    print("\nNull values per column:")
    print(null_counts)

    # Fill null values (example)
    df.with_columns([pl.col("annual_premium").fill_null(pl.col("annual_premium").median())])
    print("[OK] Filled null values with median")

    # Drop rows with any nulls
    df_clean = df.drop_nulls()
    print(f"[OK] Rows after dropping nulls: {len(df_clean)}")

    # Step 10: Joining datasets
    print("\n Step 10: Joining datasets...")

    # Load claims data
    claims_path = data_dir / "insurance_claims.csv"
    if claims_path.exists():
        claims_df = pl.read_csv(claims_path)
        print(f"[OK] Loaded {len(claims_df)} claims")

        # Join policies with claims
        joined = df.join(claims_df, on="policy_id", how="left")
        print(f"[OK] Joined data shape: {joined.shape}")

        # Count claims per policy
        claims_per_policy = joined.group_by("policy_id").agg([pl.count().alias("claim_count")])
        print("\nClaims per policy distribution:")
        print(claims_per_policy.group_by("claim_count").agg(pl.count()).sort("claim_count"))

    # Step 11: Expressions and transformations
    print("\n Step 11: Advanced expressions...")

    # Multiple transformations in one go
    df_transformed = df.with_columns(
        [
            # Normalize premium (z-score)
            (
                (pl.col("annual_premium") - pl.col("annual_premium").mean())
                / pl.col("annual_premium").std()
            ).alias("premium_zscore"),
            # Premium percentile
            (pl.col("annual_premium").rank() / pl.count() * 100).alias("premium_percentile"),
            # Risk category based on age and vehicle
            pl.when((pl.col("age") < 25) & (pl.col("vehicle_type") == "Sports"))
            .then(pl.lit("High Risk"))
            .when(pl.col("age") > 60)
            .then(pl.lit("Senior"))
            .otherwise(pl.lit("Standard"))
            .alias("risk_category"),
        ]
    )

    print("\nTransformed data sample:")
    print(
        df_transformed.select(
            [
                "policy_id",
                "age",
                "vehicle_type",
                "annual_premium",
                "premium_zscore",
                "premium_percentile",
                "risk_category",
            ]
        ).head()
    )

    # Step 12: Saving results
    print("\n Step 12: Saving results...")

    # Create outputs directory
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)

    # Save to CSV
    output_path = output_dir / "00_polars_practice.csv"
    df_transformed.write_csv(output_path)
    print(f"[OK] Saved results to: {output_path}")

    # Save to Parquet (more efficient)
    parquet_path = output_dir / "00_polars_practice.parquet"
    df_transformed.write_parquet(parquet_path)
    print(f"[OK] Saved to Parquet: {parquet_path}")

    # Compare file sizes
    csv_size = output_path.stat().st_size / 1024 / 1024
    parquet_size = parquet_path.stat().st_size / 1024 / 1024
    print("\nFile size comparison:")
    print(f"  CSV:     {csv_size:.2f} MB")
    print(f"  Parquet: {parquet_size:.2f} MB")
    print(f"  Savings: {(1 - parquet_size / csv_size) * 100:.1f}%")

    # Step 13: Performance tips
    print("\n Step 13: Polars performance tips...")

    print("\nKey performance advantages of Polars:")
    print("1. [OK] Lazy evaluation - operations are optimized before execution")
    print("2. [OK] Parallel processing - uses all CPU cores automatically")
    print("3. [OK] Memory efficient - processes data in chunks")
    print("4. [OK] Fast I/O - optimized CSV and Parquet readers")
    print("5. [OK] Expression API - vectorized operations")

    # Demonstrate lazy evaluation
    print("\nLazy evaluation example:")
    lazy_query = (
        pl.scan_csv(policies_path)  # Lazy read
        .filter(pl.col("age") > 30)
        .group_by("region")
        .agg(pl.col("annual_premium").mean())
        .sort("annual_premium", descending=True)
    )
    print("[OK] Query built (not executed yet)")

    # Execute the query
    result = lazy_query.collect()
    print("[OK] Query executed")
    print(result)

    print("\n" + "=" * 70)
    print("[SUCCESS] Tutorial Complete!")
    print("=" * 70)

    print("\n[EXERCISE] Key Takeaways:")
    print("1. Polars is fast and memory-efficient for data analysis")
    print("2. Use .select() for columns, .filter() for rows")
    print("3. .with_columns() adds/modifies columns efficiently")
    print("4. .group_by() + .agg() for aggregations")
    print("5. Expressions (pl.col()) are powerful and composable")
    print("6. Lazy evaluation optimizes complex queries")
    print("7. Parquet format is more efficient than CSV")

    print("\n Practice Exercises:")
    print("1. Find the average premium for each vehicle type")
    print("2. Create a 'high_value' flag for premiums > $1500")
    print("3. Calculate the age distribution by region")
    print("4. Join policies with claims and find policies with no claims")
    print("5. Create a risk score based on age, vehicle type, and region")

    print("\n Polars Resources:")
    print("- Documentation: https://pola-rs.github.io/polars/")
    print("- User Guide: https://pola-rs.github.io/polars-book/")
    print("- GitHub: https://github.com/pola-rs/polars")

    print("\n->  Next: Tutorial 01 - Lift Analysis")


if __name__ == "__main__":
    main()
