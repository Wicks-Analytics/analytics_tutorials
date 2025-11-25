# Tutorial Index

Complete guide to all tutorials in this repository.

## 📚 Tutorial Structure

### Getting Started (Start Here First!)

#### Tutorial 00: Project Setup and Polars Basics
**File:** `tutorials/00_getting_started/00_setup_and_polars_basics.py`  
**Duration:** 30-40 minutes  
**Topics:**
- Environment setup verification
- Loading data with Polars
- DataFrame operations (select, filter, group_by)
- Adding and modifying columns
- Aggregations and statistics
- Joining datasets
- Handling missing data
- Performance tips and lazy evaluation

**Key Functions:**
- `pl.read_csv()`, `pl.scan_csv()`
- `df.select()`, `df.filter()`, `df.with_columns()`
- `df.group_by()`, `df.agg()`
- `df.join()`, `df.sort()`

**Datasets:** `insurance_policies.csv`, `insurance_claims.csv`

**Prerequisites:** Python 3.8+, basic Python knowledge

---

### Beginner Level

#### Tutorial 01: Lift Analysis
**File:** `tutorials/01_beginner/01_lift_analysis.py`  
**Duration:** 15-20 minutes  
**Topics:**
- Understanding lift curves
- Calculating lift metrics with analytics_store
- Interpreting decile analysis
- Visualizing model performance

**Key Functions:**
- `model_validation.calculate_lift_curve()`
- `validation_plots.plot_lift_curve()`

**Datasets:** `fraud_predictions.csv`

---

#### Tutorial 02: ROC Analysis
**File:** `tutorials/01_beginner/02_roc_analysis.py`  
**Duration:** 20-25 minutes  
**Topics:**
- ROC curves and AUC scores
- Finding optimal thresholds
- Sensitivity vs specificity trade-offs
- Comparing multiple models

**Key Functions:**
- `model_validation.calculate_roc_curve()`
- `validation_plots.plot_roc_curve()`

**Datasets:** `fraud_predictions.csv`

---

#### Tutorial 03: Regression Metrics
**File:** `tutorials/01_beginner/03_regression_metrics.py`  
**Duration:** 20-25 minutes  
**Topics:**
- RMSE, MAE, and R-squared
- Diagnostic plots
- Segment analysis
- Model comparison

**Key Functions:**
- `model_validation.calculate_regression_metrics()`
- `validation_plots.plot_regression_diagnostics()`

**Datasets:** `premium_predictions.csv`

---

### Intermediate Level

#### Tutorial 04: Model Comparison
**File:** `tutorials/02_intermediate/04_model_comparison.py`  
**Duration:** 25-30 minutes  
**Topics:**
- Double lift analysis
- Joint and conditional lift
- Score correlation
- Ensemble models

**Key Functions:**
- `model_validation.calculate_double_lift()`
- `validation_plots.plot_double_lift()`

**Datasets:** `fraud_predictions.csv`

---

#### Tutorial 05: SQL Integration
**File:** `tutorials/02_intermediate/05_sql_integration.py`  
**Duration:** 30-35 minutes  
**Topics:**
- Loading data from SQL databases
- Efficient querying strategies
- SQLite, PostgreSQL, MySQL
- Writing results back to database

**Key Functions:**
- `load_from_sql()`
- `get_sqlite_connection()`
- `get_postgres_connection()`

**Datasets:** `insurance.db` (SQLite)

---

#### Tutorial 06: Population Testing
**File:** `tutorials/02_intermediate/06_population_testing.py`  
**Duration:** 25-30 minutes  
**Topics:**
- Statistical hypothesis testing
- T-tests and Mann-Whitney U tests
- Effect size interpretation
- Multiple comparisons

**Key Functions:**
- `monitoring.compare_populations()`

**Datasets:** `premium_predictions.csv`

---

### Advanced Level

#### Tutorial 07: Model Monitoring
**File:** `tutorials/03_advanced/07_model_monitoring.py`  
**Duration:** 35-40 minutes  
**Topics:**
- Data drift detection
- Performance degradation tracking
- Monitoring thresholds
- Automated alerting

**Key Functions:**
- `monitoring.compare_populations()`
- `model_validation.calculate_roc_curve()`
- `model_validation.calculate_lift_curve()`

**Datasets:** `fraud_predictions.csv`

---

#### Tutorial 08: Snowflake Integration
**File:** `tutorials/03_advanced/08_snowflake_integration.py`  
**Duration:** 30-35 minutes  
**Topics:**
- Connecting to Snowflake
- Cloud data warehouse best practices
- Cost optimization
- Incremental loading

**Key Functions:**
- `load_from_snowflake()`
- `get_snowflake_connection()`

**Datasets:** Requires Snowflake account (demo mode available)

---

#### Tutorial 09: End-to-End Pipeline
**File:** `tutorials/03_advanced/09_end_to_end_pipeline.py`  
**Duration:** 40-45 minutes  
**Topics:**
- Complete analytics workflow
- Automated reporting
- Production-ready code
- Pipeline architecture

**Key Functions:**
- All major analytics_store functions
- Custom pipeline class

**Datasets:** `insurance.db` (SQLite)

---

## 🎯 Learning Paths

### Path 1: Complete Beginner (7-9 hours)
For those new to Polars and analytics:
0. Tutorial 00 - Setup and Polars Basics
1. Tutorial 01 - Lift Analysis
2. Tutorial 02 - ROC Analysis
3. Tutorial 03 - Regression Metrics
4. Tutorial 05 - SQL Integration

### Path 2: Quick Start (2-3 hours)
For those familiar with Polars who want to get productive quickly:
1. Tutorial 01 - Lift Analysis
2. Tutorial 02 - ROC Analysis
3. Tutorial 05 - SQL Integration
4. Tutorial 09 - End-to-End Pipeline

### Path 3: Comprehensive (8-10 hours)
Complete all tutorials in order for full mastery:
0. Getting Started tutorial (00)
1. All Beginner tutorials (01-03)
2. All Intermediate tutorials (04-06)
3. All Advanced tutorials (07-09)

### Path 4: Classification Focus (3-4 hours)
For fraud detection and binary classification:
0. Tutorial 00 - Setup and Polars Basics (if needed)
1. Tutorial 01 - Lift Analysis
2. Tutorial 02 - ROC Analysis
3. Tutorial 04 - Model Comparison
4. Tutorial 07 - Model Monitoring

### Path 5: Regression Focus (3-4 hours)
For premium prediction and regression:
0. Tutorial 00 - Setup and Polars Basics (if needed)
1. Tutorial 03 - Regression Metrics
2. Tutorial 06 - Population Testing
3. Tutorial 07 - Model Monitoring
4. Tutorial 09 - End-to-End Pipeline

### Path 6: Data Engineering Focus (3-4 hours)
For data loading and integration:
0. Tutorial 00 - Setup and Polars Basics
1. Tutorial 05 - SQL Integration
2. Tutorial 08 - Snowflake Integration
3. Tutorial 09 - End-to-End Pipeline

---

## 📊 Datasets Overview

### fraud_predictions.csv
- **Rows:** 5,000
- **Columns:** 5
- **Use Cases:** Binary classification, lift analysis, ROC curves
- **Models:** 3 fraud detection models with varying performance

### premium_predictions.csv
- **Rows:** 5,000
- **Columns:** 9
- **Use Cases:** Regression analysis, segment analysis
- **Models:** 3 premium prediction models with varying accuracy

### insurance_policies.csv
- **Rows:** 10,000
- **Columns:** 10
- **Use Cases:** Customer segmentation, feature analysis
- **Content:** Policy details, demographics, coverage

### insurance_claims.csv
- **Rows:** 5,000
- **Columns:** 8
- **Use Cases:** Claims analysis, fraud investigation
- **Content:** Claim details, amounts, fraud indicators

### insurance.db (SQLite)
- **Tables:** 4 (policies, claims, fraud_predictions, premium_predictions)
- **Use Cases:** SQL integration, database queries
- **Content:** All CSV data in relational format

---

## 🛠️ Utility Functions

### Data Generators (`utils/data_generators.py`)
- `generate_insurance_policies()` - Create policy data
- `generate_insurance_claims()` - Create claims data
- `generate_fraud_predictions()` - Create fraud model results
- `generate_premium_predictions()` - Create premium model results

### Database Helpers (`utils/database_helpers.py`)
- `get_sqlite_connection()` - SQLite connection string
- `get_postgres_connection()` - PostgreSQL connection string
- `get_snowflake_connection()` - Snowflake connection params
- `load_from_sql()` - Load data from SQL database
- `load_from_snowflake()` - Load data from Snowflake
- `create_sqlite_tables()` - Set up SQLite database

---

## 📈 Skills Matrix

| Tutorial | Polars | Lift | ROC | Regression | SQL | Monitoring | Advanced |
|----------|--------|------|-----|------------|-----|------------|----------|
| 00       | ✓✓✓    | -    | -   | -          | -   | -          | -        |
| 01       | ✓      | ✓✓✓  | -   | -          | -   | -          | -        |
| 02       | ✓      | -    | ✓✓✓ | -          | -   | -          | -        |
| 03       | ✓      | -    | -   | ✓✓✓        | -   | -          | -        |
| 04       | ✓      | ✓✓   | ✓   | -          | -   | -          | ✓        |
| 05       | ✓✓     | ✓    | -   | -          | ✓✓✓ | -          | ✓        |
| 06       | ✓      | -    | -   | ✓          | -   | ✓✓         | ✓        |
| 07       | ✓      | ✓    | ✓   | -          | -   | ✓✓✓        | ✓✓       |
| 08       | ✓✓     | -    | -   | -          | ✓✓✓ | -          | ✓✓✓      |
| 09       | ✓✓     | ✓✓   | ✓✓  | ✓✓         | ✓✓  | ✓✓         | ✓✓✓      |

Legend: ✓ = Covered, ✓✓ = Major Focus, ✓✓✓ = Primary Topic

---

## 🎓 Exercises

Each tutorial includes hands-on exercises. Solutions are available in the `solutions/` folder.

### Beginner Exercises
- Calculate lift for different models
- Find optimal ROC thresholds
- Analyze regression errors by segment

### Intermediate Exercises
- Create weighted ensemble models
- Optimize SQL queries
- Perform multi-group comparisons

### Advanced Exercises
- Build monitoring dashboards
- Implement Snowflake pipelines
- Create automated reporting systems

---

## 📝 Additional Resources

- **README.md** - Main repository documentation
- **QUICKSTART.md** - 5-minute setup guide
- **requirements.txt** - Python dependencies
- **.env.example** - Configuration template
- **setup_database.py** - Data generation script

---

## 🤝 Getting Help

1. Check tutorial comments for detailed explanations
2. Review the analytics_store documentation
3. Look at solutions folder for complete examples
4. Open an issue on GitHub for questions

---

**Happy Learning! 🎉**
