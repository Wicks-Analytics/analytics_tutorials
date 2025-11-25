# Analytics Store Tutorials - Insurance Data Analysis

[![CI](https://github.com/Wicks-Analytics/analytics_tutorials/actions/workflows/ci.yml/badge.svg)](https://github.com/Wicks-Analytics/analytics_tutorials/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive tutorial series demonstrating the capabilities of the `analytics_store` package using insurance industry datasets. These exercises cover data loading, model validation, performance monitoring, and advanced analytics techniques.

## 📚 Tutorial Overview

This repository contains hands-on exercises organized by difficulty level and topic:

### **Getting Started** (Start Here!)
0. **Project Setup and Polars Basics** - Environment setup and data manipulation fundamentals

### **Beginner Tutorials**
1. **Introduction to Lift Analysis** - Understanding lift curves with insurance claim predictions
2. **ROC Curve Analysis** - Evaluating binary classification models for fraud detection
3. **Regression Metrics** - Analyzing premium prediction models

### **Intermediate Tutorials**
4. **Model Comparison** - Comparing multiple models using double lift analysis
5. **Data Loading from SQL** - Connecting to databases and loading insurance data
6. **Population Testing** - Statistical tests for comparing customer segments

### **Advanced Tutorials**
7. **Model Monitoring & Drift Detection** - Tracking model performance over time
8. **Snowflake Integration** - Working with cloud data warehouses
9. **End-to-End Pipeline** - Complete workflow from data loading to reporting

## 🎯 Learning Objectives

By completing these tutorials, you will learn to:
- Use `analytics_store` for comprehensive model evaluation
- Work with Polars DataFrames for high-performance data analysis
- Load data from various sources (CSV, SQL, Snowflake)
- Evaluate classification and regression models
- Monitor model performance and detect data drift
- Compare multiple models and scoring approaches
- Generate professional analytics reports

## 📋 Prerequisites

- Python 3.8 or higher
- Basic understanding of Python and pandas/polars
- Familiarity with machine learning concepts (helpful but not required)

## 🚀 Getting Started

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Wicks-Analytics/analytics_tutorials.git
cd analytics_tutorials
```

2. **Choose your environment manager:**

#### Option A: Using uv (Recommended - Fast & Modern)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver.

```bash
# Install uv (if not already installed)
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Install optional dependencies
uv pip install -e ".[jupyter]"  # For Jupyter notebooks
uv pip install -e ".[snowflake]"  # For Snowflake tutorials
uv pip install -e ".[all]"  # Install everything

# Install analytics_store
uv pip install git+https://github.com/Wicks-Analytics/analytics_store
```

#### Option B: Using pip (Traditional)

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install analytics_store
pip install git+https://github.com/Wicks-Analytics/analytics_store
```

### Running Tutorials

**Option 1: Python Scripts**

Start with Tutorial 00, then proceed through the beginner tutorials:

```bash
# Start here - setup and Polars basics
python tutorials/00_getting_started/00_setup_and_polars_basics.py

# Then proceed to beginner tutorials
python tutorials/01_beginner/01_lift_analysis.py
python tutorials/01_beginner/02_roc_analysis.py
python tutorials/01_beginner/03_regression_metrics.py
```

**Option 2: Jupyter Notebooks (Recommended for Learning)**

Interactive notebook versions are available in the `notebooks/` folder:

```bash
# Install Jupyter
pip install jupyter jupyterlab

# Start JupyterLab
jupyter lab

# Navigate to notebooks/01_beginner/01_lift_analysis.ipynb
```

**Converting Scripts to Notebooks**

Generate notebook versions from Python scripts:

```bash
python convert_to_notebooks.py
```

## 📁 Repository Structure

```
analytics_tutorials/
├── README.md                          # This file
├── QUICKSTART.md                      # 5-minute setup guide
├── TUTORIAL_INDEX.md                  # Complete tutorial reference
├── requirements.txt                   # Python dependencies
├── setup_database.py                  # Script to set up local SQLite database
├── convert_to_notebooks.py            # Convert Python scripts to Jupyter notebooks
├── data/                              # Sample datasets
│   ├── insurance_claims.csv          # Dummy insurance claims data
│   ├── insurance_policies.csv        # Dummy policy data
│   └── fraud_predictions.csv         # Model predictions for fraud detection
├── tutorials/                         # Tutorial exercises (Python scripts)
│   ├── 00_getting_started/
│   │   └── 00_setup_and_polars_basics.py
│   ├── 01_beginner/
│   │   ├── 01_lift_analysis.py
│   │   ├── 02_roc_analysis.py
│   │   └── 03_regression_metrics.py
│   ├── 02_intermediate/
│   │   ├── 04_model_comparison.py
│   │   ├── 05_sql_integration.py
│   │   └── 06_population_testing.py
│   └── 03_advanced/
│       ├── 07_model_monitoring.py
│       ├── 08_snowflake_integration.py
│       └── 09_end_to_end_pipeline.py
├── notebooks/                         # Jupyter notebook versions
│   ├── README.md                      # Notebook usage guide
│   ├── 01_beginner/
│   ├── 02_intermediate/
│   └── 03_advanced/
├── solutions/                         # Solutions with detailed explanations
│   ├── 01_beginner/
│   ├── 02_intermediate/
│   └── 03_advanced/
├── utils/                             # Helper utilities
│   ├── __init__.py
│   ├── data_generators.py            # Functions to generate dummy data
│   └── database_helpers.py           # Database connection utilities
└── outputs/                           # Generated plots and reports (gitignored)
```

## 📊 Sample Datasets

The repository includes realistic dummy insurance datasets:

- **insurance_claims.csv** - Historical claims data with features and outcomes
- **insurance_policies.csv** - Policy information and customer demographics
- **fraud_predictions.csv** - Model predictions for fraud detection exercises

All data is synthetically generated and does not contain real customer information.

## 🔌 Database Integration

### SQLite (Local)
Run the setup script to create a local SQLite database:
```bash
python setup_database.py
```

### PostgreSQL/MySQL
Update the connection strings in `utils/database_helpers.py` with your credentials.

### Snowflake
For Snowflake tutorials, you'll need:
- Snowflake account credentials
- Appropriate permissions to read data
- Update `config/snowflake_config.py` with your connection details

## 📝 Tutorial Descriptions

### Beginner Level

**01 - Lift Analysis**
Learn to calculate and visualize lift curves for insurance claim predictions. Understand how to interpret lift metrics and identify model performance across deciles.

**02 - ROC Analysis**
Evaluate binary classification models using ROC curves and AUC scores. Learn to find optimal thresholds for fraud detection models.

**03 - Regression Metrics**
Analyze regression model performance for premium predictions. Calculate RMSE, MAE, R-squared, and create diagnostic plots.

### Intermediate Level

**04 - Model Comparison**
Compare multiple scoring models using double lift analysis. Understand joint and conditional lift metrics.

**05 - SQL Integration**
Load insurance data from SQL databases using Polars. Learn efficient data loading patterns and query optimization.

**06 - Population Testing**
Perform statistical tests to compare different customer segments. Use t-tests and Mann-Whitney U tests with effect size calculations.

### Advanced Level

**07 - Model Monitoring**
Implement comprehensive model monitoring with drift detection. Track feature drift using PSI and performance metrics over time.

**08 - Snowflake Integration**
Connect to Snowflake data warehouse and perform analytics at scale. Learn best practices for cloud data integration.

**09 - End-to-End Pipeline**
Build a complete analytics pipeline from data loading through model evaluation to automated reporting.

## 🎓 Learning Path

**Recommended order for beginners:**
1. Start with tutorials 01-03 to understand core concepts
2. Move to tutorials 04-06 for practical integration skills
3. Complete tutorials 07-09 for production-ready workflows

**For experienced users:**
- Jump directly to intermediate or advanced tutorials
- Use beginner tutorials as reference material

## � Testing & Development

### Running Tests

This project uses pytest for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=term-missing

# Run tests in parallel (faster)
pytest -n auto
```

### Code Quality

We use Ruff and Black for code quality:

```bash
# Lint with Ruff
ruff check .

# Format with Ruff
ruff format .

# Format with Black
black .
```

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
uv pip install -e ".[dev]"
pre-commit install
```

### Continuous Integration

All pull requests are automatically tested with GitHub Actions:
- ✅ Linting (Ruff)
- ✅ Formatting (Black + Ruff)
- ✅ Tests (Python 3.8-3.12, Ubuntu/Windows/macOS)
- ✅ Tutorial validation

## �� Contributing

We welcome contributions! If you have ideas for new tutorials or improvements:
1. Fork the repository
2. Create a feature branch
3. Follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md)
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development setup and guidelines.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built using the `analytics_store` package by Wicks Analytics LTD
- Powered by Polars for high-performance data processing

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Check the analytics_store documentation
- Review the solutions folder for detailed explanations

---

**Happy Learning! 🎉**
