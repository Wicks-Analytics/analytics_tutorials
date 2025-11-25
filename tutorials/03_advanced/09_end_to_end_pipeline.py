"""
Tutorial 09: End-to-End Analytics Pipeline
===========================================

In this tutorial, you'll learn:
- Building a complete analytics workflow from data to reporting
- Combining data loading, analysis, and monitoring
- Creating automated reports
- Best practices for production pipelines

Scenario:
Build a complete pipeline that loads insurance data, evaluates models,
monitors for drift, and generates a comprehensive report.
"""

import sys
from datetime import datetime
from pathlib import Path

import polars as pl

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from analytics_store import model_validation, monitoring

from utils.database_helpers import get_sqlite_connection, load_from_sql


class InsuranceAnalyticsPipeline:
    """End-to-end analytics pipeline for insurance models."""

    def __init__(self, db_path: str = None):
        """Initialize the pipeline."""
        self.db_path = db_path or str(project_root / "data" / "insurance.db")
        self.connection_string = get_sqlite_connection(self.db_path)
        self.results = {}
        self.timestamp = datetime.now()

    def load_data(self):
        """Step 1: Load data from database."""
        print("\n" + "=" * 70)
        print("Step 1: Loading Data")
        print("=" * 70)

        # Load fraud predictions
        self.fraud_data = load_from_sql("SELECT * FROM fraud_predictions", self.connection_string)
        print(f"✓ Loaded {len(self.fraud_data)} fraud predictions")

        # Load premium predictions
        self.premium_data = load_from_sql(
            "SELECT * FROM premium_predictions", self.connection_string
        )
        print(f"✓ Loaded {len(self.premium_data)} premium predictions")

        # Split into baseline and current for monitoring
        split_point = int(len(self.fraud_data) * 0.7)
        self.fraud_baseline = self.fraud_data.head(split_point)
        self.fraud_current = self.fraud_data.tail(len(self.fraud_data) - split_point)

        print(
            f"✓ Split into baseline ({len(self.fraud_baseline)}) and current ({len(self.fraud_current)})"
        )

    def evaluate_classification_models(self):
        """Step 2: Evaluate fraud detection models."""
        print("\n" + "=" * 70)
        print("Step 2: Evaluating Classification Models")
        print("=" * 70)

        models = ["model1_fraud_score", "model2_fraud_score", "model3_fraud_score"]

        self.results["classification"] = []

        for model_col in models:
            # Calculate lift
            lift_result = model_validation.calculate_lift_curve(
                self.fraud_data, target_column="actual_fraud", score_column=model_col, n_bins=10
            )

            # Calculate ROC
            roc_result = model_validation.calculate_roc_curve(
                self.fraud_data, target_column="actual_fraud", score_column=model_col
            )

            result = {
                "model": model_col,
                "auc": roc_result.auc_score,
                "auc_lift": lift_result.auc_score_lift,
                "top_decile_lift": lift_result.score_lift_values[0],
                "optimal_threshold": roc_result.optimal_threshold,
            }

            self.results["classification"].append(result)

            print(f"\n{model_col}:")
            print(f"  AUC: {result['auc']:.4f}")
            print(f"  AUC Lift: {result['auc_lift']:.4f}")
            print(f"  Top Decile Lift: {result['top_decile_lift']:.2f}x")

        # Find best model
        best_model = max(self.results["classification"], key=lambda x: x["auc"])
        print(f"\n✓ Best Model: {best_model['model']} (AUC: {best_model['auc']:.4f})")
        self.results["best_classification_model"] = best_model["model"]

    def evaluate_regression_models(self):
        """Step 3: Evaluate premium prediction models."""
        print("\n" + "=" * 70)
        print("Step 3: Evaluating Regression Models")
        print("=" * 70)

        models = [
            "model1_predicted_premium",
            "model2_predicted_premium",
            "model3_predicted_premium",
        ]

        self.results["regression"] = []

        for model_col in models:
            metrics = model_validation.calculate_regression_metrics(
                self.premium_data,
                actual_column="actual_premium",
                predicted_column=model_col,
                n_features=4,
            )

            result = {
                "model": model_col,
                "rmse": metrics.rmse,
                "mae": metrics.mae,
                "r2": metrics.r2,
                "adj_r2": metrics.adj_r2,
            }

            self.results["regression"].append(result)

            print(f"\n{model_col}:")
            print(f"  RMSE: ${result['rmse']:.2f}")
            print(f"  MAE: ${result['mae']:.2f}")
            print(f"  R²: {result['r2']:.4f}")

        # Find best model
        best_model = max(self.results["regression"], key=lambda x: x["r2"])
        print(f"\n✓ Best Model: {best_model['model']} (R²: {best_model['r2']:.4f})")
        self.results["best_regression_model"] = best_model["model"]

    def monitor_drift(self):
        """Step 4: Monitor for data drift."""
        print("\n" + "=" * 70)
        print("Step 4: Monitoring for Data Drift")
        print("=" * 70)

        # Compare baseline vs current scores
        min_len = min(len(self.fraud_baseline), len(self.fraud_current))

        comparison_df = pl.DataFrame(
            {
                "baseline": self.fraud_baseline["model1_fraud_score"].to_list()[:min_len],
                "current": self.fraud_current["model1_fraud_score"].to_list()[:min_len],
            }
        )

        drift_result = monitoring.compare_populations(
            comparison_df, column1="baseline", column2="current", alpha=0.05, test_type="auto"
        )

        self.results["drift"] = {
            "test_type": drift_result.test_type,
            "p_value": drift_result.p_value,
            "effect_size": drift_result.effect_size,
            "is_significant": drift_result.is_significant,
        }

        print("\nDrift Detection Results:")
        print(f"  Test: {drift_result.test_type}")
        print(f"  P-value: {drift_result.p_value:.6f}")
        print(f"  Effect Size: {drift_result.effect_size:.4f}")

        if drift_result.is_significant:
            print("  ⚠️  WARNING: Significant drift detected!")
        else:
            print("  ✓ No significant drift detected")

    def check_performance_degradation(self):
        """Step 5: Check for performance degradation."""
        print("\n" + "=" * 70)
        print("Step 5: Checking Performance Degradation")
        print("=" * 70)

        # Calculate metrics on baseline
        baseline_roc = model_validation.calculate_roc_curve(
            self.fraud_baseline, target_column="actual_fraud", score_column="model1_fraud_score"
        )

        # Calculate metrics on current
        current_roc = model_validation.calculate_roc_curve(
            self.fraud_current, target_column="actual_fraud", score_column="model1_fraud_score"
        )

        auc_drop = baseline_roc.auc_score - current_roc.auc_score
        drop_pct = (auc_drop / baseline_roc.auc_score) * 100

        self.results["performance"] = {
            "baseline_auc": baseline_roc.auc_score,
            "current_auc": current_roc.auc_score,
            "auc_drop": auc_drop,
            "drop_percentage": drop_pct,
        }

        print("\nPerformance Comparison:")
        print(f"  Baseline AUC: {baseline_roc.auc_score:.4f}")
        print(f"  Current AUC: {current_roc.auc_score:.4f}")
        print(f"  Drop: {auc_drop:.4f} ({drop_pct:.1f}%)")

        if drop_pct >= 10:
            print("  🔴 CRITICAL: Significant performance degradation!")
        elif drop_pct >= 5:
            print("  🟡 WARNING: Performance decline detected")
        else:
            print("  🟢 OK: Performance stable")

    def generate_report(self):
        """Step 6: Generate comprehensive report."""
        print("\n" + "=" * 70)
        print("Step 6: Generating Report")
        print("=" * 70)

        # Create report sections
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("INSURANCE ANALYTICS PIPELINE REPORT")
        report_lines.append("=" * 70)
        report_lines.append(f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Classification models
        report_lines.append("CLASSIFICATION MODELS (Fraud Detection)")
        report_lines.append("-" * 70)
        for model in self.results["classification"]:
            report_lines.append(f"\n{model['model']}:")
            report_lines.append(f"  AUC: {model['auc']:.4f}")
            report_lines.append(f"  Top Decile Lift: {model['top_decile_lift']:.2f}x")
            report_lines.append(f"  Optimal Threshold: {model['optimal_threshold']:.4f}")

        report_lines.append(f"\nBest Model: {self.results['best_classification_model']}")
        report_lines.append("")

        # Regression models
        report_lines.append("REGRESSION MODELS (Premium Prediction)")
        report_lines.append("-" * 70)
        for model in self.results["regression"]:
            report_lines.append(f"\n{model['model']}:")
            report_lines.append(f"  RMSE: ${model['rmse']:.2f}")
            report_lines.append(f"  R²: {model['r2']:.4f}")

        report_lines.append(f"\nBest Model: {self.results['best_regression_model']}")
        report_lines.append("")

        # Drift monitoring
        report_lines.append("DRIFT MONITORING")
        report_lines.append("-" * 70)
        drift = self.results["drift"]
        report_lines.append(f"Test Type: {drift['test_type']}")
        report_lines.append(f"P-value: {drift['p_value']:.6f}")
        report_lines.append(f"Effect Size: {drift['effect_size']:.4f}")
        report_lines.append(f"Drift Detected: {'YES ⚠️' if drift['is_significant'] else 'NO ✓'}")
        report_lines.append("")

        # Performance monitoring
        report_lines.append("PERFORMANCE MONITORING")
        report_lines.append("-" * 70)
        perf = self.results["performance"]
        report_lines.append(f"Baseline AUC: {perf['baseline_auc']:.4f}")
        report_lines.append(f"Current AUC: {perf['current_auc']:.4f}")
        report_lines.append(f"Performance Drop: {perf['drop_percentage']:.1f}%")

        if perf["drop_percentage"] >= 10:
            status = "CRITICAL 🔴"
        elif perf["drop_percentage"] >= 5:
            status = "WARNING 🟡"
        else:
            status = "OK 🟢"
        report_lines.append(f"Status: {status}")
        report_lines.append("")

        # Recommendations
        report_lines.append("RECOMMENDATIONS")
        report_lines.append("-" * 70)

        if drift["is_significant"]:
            report_lines.append("• Data drift detected - investigate input data changes")

        if perf["drop_percentage"] >= 10:
            report_lines.append("• Critical performance drop - retrain model immediately")
        elif perf["drop_percentage"] >= 5:
            report_lines.append("• Performance declining - schedule model retraining")

        if not drift["is_significant"] and perf["drop_percentage"] < 5:
            report_lines.append("• All systems normal - continue monitoring")

        report_lines.append("")
        report_lines.append("=" * 70)

        # Print report
        report_text = "\n".join(report_lines)
        print("\n" + report_text)

        # Save report
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)

        report_file = output_dir / f"pipeline_report_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, "w") as f:
            f.write(report_text)

        print(f"\n✓ Report saved to: {report_file}")

        # Save metrics as CSV
        metrics_file = (
            output_dir / f"pipeline_metrics_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
        )

        metrics_df = pl.DataFrame(
            {
                "timestamp": [self.timestamp.isoformat()],
                "best_classification_model": [self.results["best_classification_model"]],
                "best_classification_auc": [max(m["auc"] for m in self.results["classification"])],
                "best_regression_model": [self.results["best_regression_model"]],
                "best_regression_r2": [max(m["r2"] for m in self.results["regression"])],
                "drift_detected": [drift["is_significant"]],
                "drift_p_value": [drift["p_value"]],
                "performance_drop_pct": [perf["drop_percentage"]],
            }
        )

        metrics_df.write_csv(metrics_file)
        print(f"✓ Metrics saved to: {metrics_file}")

    def run(self):
        """Execute the complete pipeline."""
        print("=" * 70)
        print("INSURANCE ANALYTICS PIPELINE")
        print("=" * 70)
        print(f"Started: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            self.load_data()
            self.evaluate_classification_models()
            self.evaluate_regression_models()
            self.monitor_drift()
            self.check_performance_degradation()
            self.generate_report()

            print("\n" + "=" * 70)
            print("✅ PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 70)

        except Exception as e:
            print(f"\n❌ PIPELINE FAILED: {e}")
            raise


def main():
    """Run the end-to-end pipeline tutorial."""

    print("=" * 70)
    print("Tutorial 09: End-to-End Analytics Pipeline")
    print("=" * 70)

    # Check if database exists
    db_path = project_root / "data" / "insurance.db"
    if not db_path.exists():
        print(f"\n❌ Database not found: {db_path}")
        print("Please run: python setup_database.py")
        return

    # Run the pipeline
    pipeline = InsuranceAnalyticsPipeline(str(db_path))
    pipeline.run()

    # Additional insights
    print("\n" + "=" * 70)
    print("Pipeline Architecture")
    print("=" * 70)
    print(
        """
    This pipeline demonstrates:

    1. Data Loading
       - Centralized data access from SQL database
       - Efficient querying with Polars

    2. Model Evaluation
       - Automated evaluation of multiple models
       - Standardized metrics across model types

    3. Monitoring
       - Data drift detection
       - Performance degradation tracking

    4. Reporting
       - Automated report generation
       - Actionable recommendations

    5. Production Readiness
       - Error handling
       - Logging and timestamps
       - Reproducible results
    """
    )

    print("\n🎓 EXERCISE: Extend the Pipeline")
    print(
        """
    Enhance this pipeline with:

    1. Email alerts for critical issues
    2. Visualization generation (plots saved to files)
    3. Database logging of all metrics
    4. Scheduled execution (cron job or task scheduler)
    5. Model retraining trigger
    6. Slack/Teams notifications
    7. Dashboard integration
    8. A/B test comparison
    """
    )

    print("\n" + "=" * 70)
    print("✅ Tutorial Complete!")
    print("=" * 70)
    print("\nCongratulations! You've completed all tutorials!")
    print("\nYou now know how to:")
    print("✓ Evaluate classification and regression models")
    print("✓ Load data from various sources (CSV, SQL, Snowflake)")
    print("✓ Compare models and populations statistically")
    print("✓ Monitor for drift and performance degradation")
    print("✓ Build production-ready analytics pipelines")
    print("\nNext steps:")
    print("- Apply these techniques to your own data")
    print("- Build custom pipelines for your use cases")
    print("- Contribute to the analytics_store package")
    print("\nHappy analyzing! 🎉")


if __name__ == "__main__":
    main()
