"""
Setup script to generate sample data and create SQLite database.

Run this script to set up the tutorial environment:
    python setup_database.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.data_generators import (
    generate_fraud_predictions,
    generate_insurance_claims,
    generate_insurance_policies,
    generate_premium_predictions,
)
from utils.database_helpers import create_sqlite_tables


def main():
    """Set up the tutorial environment."""

    print("=" * 70)
    print("Analytics Tutorials - Setup Script")
    print("=" * 70)

    # Create data directory
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"\n✓ Data directory: {data_dir}")

    # Create outputs directory
    outputs_dir = project_root / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    print(f"✓ Outputs directory: {outputs_dir}")

    # Step 1: Generate CSV files
    print("\n" + "=" * 70)
    print("Step 1: Generating CSV datasets")
    print("=" * 70)

    print("\nGenerating insurance policies...")
    policies = generate_insurance_policies(10000)
    policies.write_csv(data_dir / "insurance_policies.csv")
    print(f"✓ Generated {len(policies)} policies → insurance_policies.csv")

    print("\nGenerating insurance claims...")
    claims = generate_insurance_claims(5000, policies)
    claims.write_csv(data_dir / "insurance_claims.csv")
    print(f"✓ Generated {len(claims)} claims → insurance_claims.csv")

    print("\nGenerating fraud predictions...")
    fraud_preds = generate_fraud_predictions(5000)
    fraud_preds.write_csv(data_dir / "fraud_predictions.csv")
    print(f"✓ Generated {len(fraud_preds)} predictions → fraud_predictions.csv")

    print("\nGenerating premium predictions...")
    premium_preds = generate_premium_predictions(5000)
    premium_preds.write_csv(data_dir / "premium_predictions.csv")
    print(f"✓ Generated {len(premium_preds)} predictions → premium_predictions.csv")

    # Step 2: Create SQLite database
    print("\n" + "=" * 70)
    print("Step 2: Creating SQLite database")
    print("=" * 70)

    db_path = data_dir / "insurance.db"
    print(f"\nDatabase location: {db_path}")

    try:
        create_sqlite_tables(str(db_path))
        print("\n✓ SQLite database created successfully")
    except Exception as e:
        print(f"\n❌ Error creating database: {e}")
        return

    # Step 3: Summary
    print("\n" + "=" * 70)
    print("Setup Complete!")
    print("=" * 70)

    print("\n📁 Generated Files:")
    print(f"   CSV Files: {data_dir}")
    print(f"   - insurance_policies.csv ({len(policies)} rows)")
    print(f"   - insurance_claims.csv ({len(claims)} rows)")
    print(f"   - fraud_predictions.csv ({len(fraud_preds)} rows)")
    print(f"   - premium_predictions.csv ({len(premium_preds)} rows)")
    print(f"\n   SQLite Database: {db_path}")
    print("   - policies table")
    print("   - claims table")
    print("   - fraud_predictions table")
    print("   - premium_predictions table")

    print("\n🚀 Next Steps:")
    print("   1. Install analytics_store:")
    print("      pip install git+https://github.com/Wicks-Analytics/analytics_store")
    print("   2. Run beginner tutorials:")
    print("      python tutorials/01_beginner/01_lift_analysis.py")
    print("      python tutorials/01_beginner/02_roc_analysis.py")
    print("      python tutorials/01_beginner/03_regression_metrics.py")
    print("   3. Explore intermediate and advanced tutorials")

    print("\n✅ Setup successful! Happy learning!")


if __name__ == "__main__":
    main()
