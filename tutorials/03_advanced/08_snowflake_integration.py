"""
Tutorial 08: Snowflake Integration
===================================

In this tutorial, you'll learn:
- How to connect to Snowflake data warehouse
- Loading large datasets efficiently from Snowflake
- Best practices for cloud data warehouse integration
- Performing analytics on Snowflake data

Scenario:
Your insurance company stores data in Snowflake. You need to load data
for analysis while minimizing data transfer and compute costs.

Prerequisites:
- Snowflake account with appropriate permissions
- Environment variables or config file with credentials
- snowflake-connector-python package installed
"""

import os
import sys
from pathlib import Path

import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation

from utils.database_helpers import get_snowflake_connection


def check_snowflake_config():
    """Check if Snowflake configuration is available."""
    required_vars = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_WAREHOUSE",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print("❌ Missing Snowflake configuration:")
        for var in missing:
            print(f"   - {var}")
        print("\nPlease set these environment variables or update .env file")
        return False

    return True


def main():
    """Run the Snowflake integration tutorial."""

    print("=" * 70)
    print("Tutorial 08: Snowflake Integration")
    print("=" * 70)

    # Step 1: Check configuration
    print("\n🔧 Step 1: Checking Snowflake configuration...")

    if not check_snowflake_config():
        print("\n💡 For this tutorial, you need:")
        print("   1. A Snowflake account")
        print("   2. Credentials set in environment variables")
        print("   3. Data loaded in Snowflake tables")
        print("\nExample .env file:")
        print(
            """
        SNOWFLAKE_ACCOUNT=your_account.region
        SNOWFLAKE_USER=your_username
        SNOWFLAKE_PASSWORD=your_password
        SNOWFLAKE_WAREHOUSE=your_warehouse
        SNOWFLAKE_DATABASE=INSURANCE_DB
        SNOWFLAKE_SCHEMA=PUBLIC
        SNOWFLAKE_ROLE=ANALYST
        """
        )
        print("\nSkipping Snowflake connection (demo mode)...")
        demo_mode = True
    else:
        demo_mode = False
        print("✓ Snowflake configuration found")

    # Step 2: Connect to Snowflake
    if not demo_mode:
        print("\n🔌 Step 2: Connecting to Snowflake...")
        try:
            conn_params = get_snowflake_connection()
            print(f"✓ Connecting to account: {conn_params['account']}")
            print(f"✓ Using warehouse: {conn_params['warehouse']}")
            print(f"✓ Database: {conn_params['database']}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
            demo_mode = True

    # Step 3: Efficient data loading strategies
    print("\n📥 Step 3: Efficient Data Loading Strategies...")

    print("\nStrategy 1: Use SELECT with specific columns")
    print(
        """
    # Instead of SELECT *
    query = '''
        SELECT
            policy_id,
            customer_age,
            annual_premium,
            policy_type
        FROM INSURANCE_DB.PUBLIC.POLICIES
        LIMIT 10000
    '''
    df = load_from_snowflake(query)
    """
    )

    print("\nStrategy 2: Filter data in Snowflake (not in Python)")
    print(
        """
    # Push filtering to Snowflake
    query = '''
        SELECT *
        FROM INSURANCE_DB.PUBLIC.CLAIMS
        WHERE claim_date >= DATEADD(month, -6, CURRENT_DATE())
        AND claim_amount > 10000
        AND state IN ('CA', 'NY', 'TX')
    '''
    df = load_from_snowflake(query)
    """
    )

    print("\nStrategy 3: Use aggregations in Snowflake")
    print(
        """
    # Aggregate before loading
    query = '''
        SELECT
            policy_type,
            state,
            DATE_TRUNC('month', claim_date) as month,
            COUNT(*) as claim_count,
            AVG(claim_amount) as avg_claim,
            SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count
        FROM INSURANCE_DB.PUBLIC.CLAIMS
        GROUP BY policy_type, state, month
        ORDER BY month DESC
    '''
    df = load_from_snowflake(query)
    """
    )

    # Step 4: Sample queries for analytics
    print("\n🎯 Step 4: Sample Queries for Analytics...")

    print("\nQuery 1: Load fraud predictions for model evaluation")
    fraud_query = """
    SELECT
        claim_id,
        actual_fraud,
        model1_fraud_score,
        model2_fraud_score,
        claim_amount,
        policy_type
    FROM INSURANCE_DB.PUBLIC.FRAUD_PREDICTIONS
    WHERE prediction_date >= DATEADD(day, -30, CURRENT_DATE())
    """
    print(fraud_query)

    print("\nQuery 2: Load premium predictions with features")
    premium_query = """
    SELECT
        policy_id,
        customer_age,
        credit_score,
        coverage_amount,
        actual_premium,
        model1_predicted_premium,
        model2_predicted_premium
    FROM INSURANCE_DB.PUBLIC.PREMIUM_PREDICTIONS
    WHERE prediction_date = CURRENT_DATE()
    """
    print(premium_query)

    print("\nQuery 3: Complex join for comprehensive analysis")
    complex_query = """
    SELECT
        c.claim_id,
        c.claim_amount,
        c.claim_type,
        c.is_fraud,
        c.fraud_score,
        p.policy_type,
        p.customer_age,
        p.state,
        p.annual_premium,
        p.coverage_amount,
        p.credit_score
    FROM INSURANCE_DB.PUBLIC.CLAIMS c
    INNER JOIN INSURANCE_DB.PUBLIC.POLICIES p
        ON c.policy_id = p.policy_id
    WHERE c.claim_date >= DATEADD(year, -1, CURRENT_DATE())
    AND c.claim_status = 'Approved'
    """
    print(complex_query)

    # Step 5: Demo with local data
    print("\n📊 Step 5: Demo Analysis (using local data)...")

    # Load local data to simulate Snowflake data
    data_path = project_root / "data" / "fraud_predictions.csv"

    if data_path.exists():
        print("Loading sample data (simulating Snowflake query)...")
        df = pl.read_csv(data_path)

        # Perform analysis
        print(f"✓ Loaded {len(df)} records")

        # Calculate metrics
        lift_result = model_validation.calculate_lift_curve(
            df, target_column="actual_fraud", score_column="model1_fraud_score", n_bins=10
        )

        print("\nModel Performance:")
        print(f"- AUC Lift: {lift_result.auc_score_lift:.4f}")
        print(f"- Top decile lift: {lift_result.score_lift_values[0]:.2f}x")

        # ROC analysis
        roc_result = model_validation.calculate_roc_curve(
            df, target_column="actual_fraud", score_column="model1_fraud_score"
        )

        print(f"- AUC Score: {roc_result.auc_score:.4f}")
        print(f"- Optimal threshold: {roc_result.optimal_threshold:.4f}")
    else:
        print("⚠ Sample data not found. Run: python utils/data_generators.py")

    # Step 6: Best practices
    print("\n📚 Step 6: Snowflake Best Practices...")
    print(
        """
    ✓ Use warehouse size appropriate for your query
    ✓ Filter and aggregate in Snowflake, not in Python
    ✓ Use LIMIT for exploratory queries
    ✓ Consider result caching for repeated queries
    ✓ Use clustering keys for large tables
    ✓ Monitor query costs and optimize expensive queries
    ✓ Use appropriate data types (avoid SELECT *)
    ✓ Consider materialized views for complex aggregations
    ✓ Use query tags for cost tracking
    ✓ Implement incremental loading for large datasets
    """
    )

    # Step 7: Cost optimization
    print("\n💰 Step 7: Cost Optimization Tips...")
    print(
        """
    1. Warehouse Management:
       - Use auto-suspend (e.g., 5 minutes)
       - Use auto-resume
       - Right-size your warehouse

    2. Query Optimization:
       - Use WHERE clauses to reduce data scanned
       - Avoid SELECT * in production
       - Use LIMIT for development/testing
       - Leverage result caching

    3. Data Organization:
       - Partition large tables by date
       - Use clustering keys for frequently filtered columns
       - Consider data retention policies

    4. Monitoring:
       - Track query history and costs
       - Identify expensive queries
       - Set up cost alerts
    """
    )

    # Step 8: Incremental loading pattern
    print("\n⚡ Step 8: Incremental Loading Pattern...")
    print(
        """
    # Load only new data since last run
    last_load_date = '2024-01-01'  # From metadata table

    query = f'''
        SELECT *
        FROM INSURANCE_DB.PUBLIC.CLAIMS
        WHERE claim_date > '{last_load_date}'
        AND claim_date <= CURRENT_DATE()
    '''

    new_data = load_from_snowflake(query)

    # Process new data
    # ...

    # Update metadata table with new last_load_date
    update_query = f'''
        UPDATE INSURANCE_DB.PUBLIC.ETL_METADATA
        SET last_load_date = CURRENT_DATE()
        WHERE table_name = 'claims'
    '''
    """
    )

    # Step 9: Error handling
    print("\n🛡️ Step 9: Error Handling...")
    print(
        """
    try:
        df = load_from_snowflake(query, conn_params)
    except snowflake.connector.errors.ProgrammingError as e:
        print(f"Query error: {e}")
        # Handle SQL syntax errors
    except snowflake.connector.errors.DatabaseError as e:
        print(f"Database error: {e}")
        # Handle connection issues
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Handle other errors
    """
    )

    # Step 10: Exercise
    print("\n🎓 EXERCISE: Build a Snowflake Analytics Pipeline")
    print(
        """
    Create a script that:
    1. Connects to Snowflake
    2. Loads fraud predictions from the last 7 days
    3. Calculates lift and ROC metrics
    4. Saves results back to a Snowflake table
    5. Includes error handling and logging

    Bonus: Implement incremental loading and cost tracking
    """
    )

    print("\n" + "=" * 70)
    print("✅ Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Push computation to Snowflake when possible")
    print("2. Use specific columns and filters to minimize data transfer")
    print("3. Monitor and optimize query costs")
    print("4. Implement incremental loading for efficiency")
    print("5. Use proper error handling and connection management")
    print("\nNext: Tutorial 09 - End-to-End Pipeline")

    print("\n📖 Additional Resources:")
    print("   - Snowflake Python Connector docs")
    print("   - Polars database integration guide")
    print("   - Snowflake query optimization guide")


if __name__ == "__main__":
    main()
