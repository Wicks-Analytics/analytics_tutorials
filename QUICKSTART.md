# Quick Start Guide

Get up and running with the analytics tutorials in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip or uv package manager

## Installation

### 1. Clone or download this repository

```bash
cd c:\Users\Max\Documents\Projects\analytics_tutorials
```

### 2. Choose your setup method

#### Option A: Using uv (Recommended - Fast!)

```bash
# Install uv (if not already installed)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create virtual environment and install dependencies
uv venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On macOS/Linux

# Install all dependencies including Jupyter
uv pip install -e ".[all]"

# Install analytics_store
uv pip install git+https://github.com/Wicks-Analytics/analytics_store
```

#### Option B: Using pip (Traditional)

```bash
# Create a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install analytics_store
pip install git+https://github.com/Wicks-Analytics/analytics_store
```

### 3. Generate sample data

```bash
python setup_database.py
```

This will create:
- CSV files in the `data/` folder
- SQLite database at `data/insurance.db`

## Run Your First Tutorial

**Start with Tutorial 00 to learn the basics:**

```bash
python tutorials\00_getting_started\00_setup_and_polars_basics.py
```

This will teach you:
- Environment setup verification
- Polars DataFrame basics
- Data manipulation fundamentals

**Then move to analytics tutorials:**

```bash
python tutorials\01_beginner\01_lift_analysis.py
```

You should see:
- Statistical analysis output
- Lift curve metrics
- A visualization plot

## What's Next?

### Getting Started (Start Here!)
0. `tutorials\00_getting_started\00_setup_and_polars_basics.py` - Setup and Polars basics

### Beginner Path
1. `tutorials\01_beginner\01_lift_analysis.py` - Learn lift curves
2. `tutorials\01_beginner\02_roc_analysis.py` - Learn ROC curves
3. `tutorials\01_beginner\03_regression_metrics.py` - Learn regression metrics

### Intermediate Path
4. `tutorials\02_intermediate\04_model_comparison.py` - Compare models
5. `tutorials\02_intermediate\05_sql_integration.py` - Load from SQL
6. `tutorials\02_intermediate\06_population_testing.py` - Statistical tests

### Advanced Path
7. `tutorials\03_advanced\07_model_monitoring.py` - Monitor drift
8. `tutorials\03_advanced\08_snowflake_integration.py` - Cloud data
9. `tutorials\03_advanced\09_end_to_end_pipeline.py` - Full pipeline

## Troubleshooting

### Import Error: No module named 'analytics_store'
```bash
pip install git+https://github.com/Wicks-Analytics/analytics_store
```

### Data files not found
```bash
python setup_database.py
```

### Plot windows not showing
Install matplotlib backend:
```bash
pip install matplotlib --upgrade
```

### Database errors
Delete `data/insurance.db` and run setup again:
```bash
python setup_database.py
```

## Quick Reference

### Load Data
```python
import polars as pl
df = pl.read_csv('data/fraud_predictions.csv')
```

### Calculate Lift
```python
from analytics_store import model_validation

lift_result = model_validation.calculate_lift_curve(
    df,
    target_column='actual_fraud',
    score_column='model1_fraud_score',
    n_bins=10
)
print(f"AUC Lift: {lift_result.auc_score_lift:.4f}")
```

### Calculate ROC
```python
roc_result = model_validation.calculate_roc_curve(
    df,
    target_column='actual_fraud',
    score_column='model1_fraud_score'
)
print(f"AUC: {roc_result.auc_score:.4f}")
```

### Regression Metrics
```python
metrics = model_validation.calculate_regression_metrics(
    df,
    actual_column='actual_premium',
    predicted_column='model1_predicted_premium'
)
print(f"RMSE: ${metrics.rmse:.2f}")
print(f"R²: {metrics.r2:.4f}")
```

## Getting Help

- Check the README.md for detailed documentation
- Review tutorial comments for step-by-step guidance
- Look at solutions/ folder for complete examples
- Open an issue on GitHub for bugs or questions

## Happy Learning! 🎉
