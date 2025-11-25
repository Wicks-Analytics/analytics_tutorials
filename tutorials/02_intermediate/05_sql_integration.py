"""
Tutorial 05: SQL Database Integration
======================================

In this tutorial, you'll learn:
- How to load data from SQL databases using Polars
- Working with SQLite, PostgreSQL, and MySQL
- Efficient data loading strategies
- Combining SQL queries with analytics_store functions

Scenario:
Your insurance data is stored in a SQL database. You need to load the data
efficiently and perform analytics using analytics_store.
"""

import sys
from pathlib import Path

import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation

from utils.database_helpers import create_sqlite_tables, get_sqlite_connection, load_from_sql


def main():
    """Run the SQL integration tutorial."""

    print("=" * 70)
    print("Tutorial 05: SQL Database Integration")
    print("=" * 70)

    # Step 1: Set up SQLite database
    print("\n Step 1: Setting up SQLite database...")
    db_path = project_root / "data" / "insurance.db"

    if not db_path.exists():
        print("Creating database and loading sample data...")
        try:
            create_sqlite_tables(str(db_path))
        except Exception as e:
            print(f"[ERROR] Error creating database: {e}")
            print("Make sure you have run: python utils/data_generators.py")
            return
    else:
        print(f"[OK] Database already exists at: {db_path}")

    # Step 2: Connect to database
    print("\n Step 2: Connecting to database...")
    connection_string = get_sqlite_connection(str(db_path))
    print(f"Connection string: {connection_string}")

    # Step 3: Load data using SQL queries
    print("\n Step 3: Loading data from SQL...")

    # Simple query
    print("\n3a. Loading all policies...")
    policies_df = load_from_sql("SELECT * FROM policies", connection_string)
    print(f"[OK] Loaded {len(policies_df)} policies")
    print("\nFirst few rows:")
    print(policies_df.head())

    # Step 4: Filtered query
    print("\n Step 4: Using SQL filters...")

    # Load only California policies
    ca_policies = load_from_sql(
        """
        SELECT * FROM policies
        WHERE state = 'CA'
        AND customer_age >= 30
        """,
        connection_string,
    )
    print(f"[OK] Loaded {len(ca_policies)} California policies (age >= 30)")

    # Step 5: Aggregated query
    print("\n Step 5: Loading aggregated data...")

    policy_summary = load_from_sql(
        """
        SELECT
            policy_type,
            state,
            COUNT(*) as policy_count,
            AVG(annual_premium) as avg_premium,
            SUM(coverage_amount) as total_coverage
        FROM policies
        GROUP BY policy_type, state
        ORDER BY policy_count DESC
        LIMIT 10
        """,
        connection_string,
    )
    print("\nTop 10 policy type/state combinations:")
    print(policy_summary)

    # Step 6: Join queries
    print("\n Step 6: Loading data with joins...")

    claims_with_policies = load_from_sql(
        """
        SELECT
            c.claim_id,
            c.claim_amount,
            c.claim_type,
            c.is_fraud,
            c.fraud_score,
            p.policy_type,
            p.customer_age,
            p.state,
            p.annual_premium
        FROM claims c
        INNER JOIN policies p ON c.policy_id = p.policy_id
        WHERE c.claim_status = 'Approved'
        """,
        connection_string,
    )
    print(f"[OK] Loaded {len(claims_with_policies)} approved claims with policy details")
    print("\nSample joined data:")
    print(claims_with_policies.head())

    # Step 7: Use loaded data with analytics_store
    print("\n Step 7: Analyzing fraud predictions from database...")

    fraud_data = load_from_sql("SELECT * FROM fraud_predictions", connection_string)

    # Calculate lift curve
    lift_result = model_validation.calculate_lift_curve(
        fraud_data, target_column="actual_fraud", score_column="model1_fraud_score", n_bins=10
    )

    print("\nFraud Detection Performance (from SQL data):")
    print(f"- AUC Lift: {lift_result.auc_score_lift:.4f}")
    print(f"- Top decile lift: {lift_result.score_lift_values[0]:.2f}x")

    # Step 8: Efficient loading strategies
    print("\n Step 8: Efficient data loading strategies...")

    print("\nStrategy 1: Load only needed columns")
    limited_cols = load_from_sql(
        """
        SELECT policy_id, customer_age, annual_premium, policy_type
        FROM policies
        LIMIT 1000
        """,
        connection_string,
    )
    print(f"[OK] Loaded {len(limited_cols)} rows with 4 columns")

    print("\nStrategy 2: Use WHERE clauses to filter in database")
    print("(Faster than loading all data and filtering in Python)")
    recent_claims = load_from_sql(
        """
        SELECT * FROM claims
        WHERE claim_date >= date('now', '-365 days')
        """,
        connection_string,
    )
    print(f"[OK] Loaded {len(recent_claims)} recent claims")

    print("\nStrategy 3: Use aggregations in SQL when possible")
    monthly_stats = load_from_sql(
        """
        SELECT
            strftime('%Y-%m', claim_date) as month,
            COUNT(*) as claim_count,
            AVG(claim_amount) as avg_amount,
            SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count
        FROM claims
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
        """,
        connection_string,
    )
    print("\nMonthly claim statistics:")
    print(monthly_stats)

    # Step 9: Save results back to database
    print("\n Step 9: Writing results back to database...")

    # Calculate metrics and save
    premium_data = load_from_sql("SELECT * FROM premium_predictions LIMIT 1000", connection_string)

    metrics = model_validation.calculate_regression_metrics(
        premium_data, actual_column="actual_premium", predicted_column="model1_predicted_premium"
    )

    # Convert to DataFrame and save
    metrics_df = metrics.to_polars()
    metrics_df = metrics_df.with_columns(
        [pl.lit("model1").alias("model_name"), pl.lit(pl.datetime("now")).alias("calculated_at")]
    )

    # Write to database
    from sqlalchemy import create_engine

    engine = create_engine(connection_string)

    with engine.connect() as conn:
        metrics_df.write_database(
            table_name="model_metrics", connection=conn, if_table_exists="replace"
        )

    print("[OK] Metrics saved to 'model_metrics' table")

    # Verify
    saved_metrics = load_from_sql("SELECT * FROM model_metrics", connection_string)
    print("\nSaved metrics:")
    print(saved_metrics)

    # Step 10: Best practices
    print("\n Step 10: Best Practices Summary...")
    print(
        """
    [OK] Use SQL WHERE clauses to filter data before loading
    [OK] Select only the columns you need
    [OK] Use SQL aggregations when possible (faster than Python)
    [OK] For large datasets, consider pagination or chunking
    [OK] Use indexes on frequently queried columns
    [OK] Close connections when done (handled automatically here)
    [OK] Use parameterized queries to prevent SQL injection
    """
    )

    # Step 11: Exercise
    print("\n[EXERCISE] EXERCISE: Complex Query Analysis")
    print("\nTry this exercise:")
    print(
        """
    1. Load claims data joined with policies
    2. Filter for high-value claims (amount > $50,000)
    3. Calculate fraud detection metrics by policy type
    4. Save results to a new table

    Example query:
    SELECT
        p.policy_type,
        c.claim_id,
        c.claim_amount,
        c.is_fraud,
        c.fraud_score
    FROM claims c
    INNER JOIN policies p ON c.policy_id = p.policy_id
    WHERE c.claim_amount > 50000
    """
    )

    print("\n" + "=" * 70)
    print("[SUCCESS] Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Polars can efficiently load data from SQL databases")
    print("2. Use SQL for filtering and aggregation when possible")
    print("3. Join data in SQL before loading for better performance")
    print("4. analytics_store works seamlessly with SQL-loaded data")
    print("\nNext: Tutorial 06 - Population Testing")

    # Note about other databases
    print("\n[INFO] Note: For PostgreSQL or MySQL:")
    print("   - Update connection string in utils/database_helpers.py")
    print("   - Install appropriate driver (psycopg2 or pymysql)")
    print("   - Use get_postgres_connection() or similar")


if __name__ == "__main__":
    main()
