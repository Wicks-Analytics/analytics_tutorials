# Getting Started Tutorials

Welcome! Start here if you're new to the analytics_tutorials repository or Polars.

## Tutorial 00: Project Setup and Polars Basics

**File:** `00_setup_and_polars_basics.py`  
**Duration:** 30-40 minutes  
**Prerequisites:** Python 3.8+, basic Python knowledge

### What You'll Learn

1. **Environment Setup**
   - Verify Python packages are installed
   - Check data directory structure
   - Confirm analytics_store is available

2. **Polars Fundamentals**
   - Loading CSV files with Polars
   - Understanding DataFrame structure
   - Column selection and filtering

3. **Data Manipulation**
   - Selecting columns by name or type
   - Filtering rows with conditions
   - Adding and modifying columns
   - Creating calculated fields

4. **Aggregations**
   - Grouping data by categories
   - Computing summary statistics
   - Multi-level grouping

5. **Advanced Operations**
   - Sorting and ranking
   - Handling missing data
   - Joining datasets
   - Complex expressions

6. **Performance**
   - Lazy evaluation
   - Memory efficiency
   - File format comparison (CSV vs Parquet)

### Running the Tutorial

```bash
cd c:\Users\Max\Documents\Projects\analytics_tutorials
python tutorials\00_getting_started\00_setup_and_polars_basics.py
```

### Practice Exercises

After completing the tutorial, try these exercises:

1. **Basic Filtering**
   - Find all policies from the "Northeast" region
   - Filter for female drivers with premiums over $1200

2. **Aggregations**
   - Calculate average premium by vehicle type
   - Find the region with the highest total premium

3. **Transformations**
   - Create a "high_value" boolean column for premiums > $1500
   - Calculate age groups (18-25, 26-40, 41-60, 60+)

4. **Joins**
   - Join policies with claims data
   - Find policies that have never had a claim

5. **Complex Analysis**
   - Create a risk score combining age, vehicle type, and region
   - Find the top 10 policies by risk score

### Solutions

Solutions to the practice exercises are available in the `solutions/00_getting_started/` folder.

### Why Polars?

Polars is used throughout these tutorials because:

- **Fast** - 5-10x faster than pandas for most operations
- **Memory efficient** - Processes large datasets with less RAM
- **Parallel** - Automatically uses all CPU cores
- **Modern API** - Clean, expressive syntax
- **Type safe** - Better error messages and data validation

### Polars vs Pandas

If you're coming from pandas, here are the key differences:

| Operation | Pandas | Polars |
|-----------|--------|--------|
| Load CSV | `pd.read_csv()` | `pl.read_csv()` |
| Select columns | `df[['col1', 'col2']]` | `df.select(['col1', 'col2'])` |
| Filter rows | `df[df['age'] > 30]` | `df.filter(pl.col('age') > 30)` |
| Add column | `df['new'] = df['old'] * 2` | `df.with_columns((pl.col('old') * 2).alias('new'))` |
| Group by | `df.groupby('col').agg()` | `df.group_by('col').agg()` |

### Common Issues

**Import Error: No module named 'polars'**
```bash
pip install polars
```

**Import Error: No module named 'analytics_store'**
```bash
pip install git+https://github.com/Wicks-Analytics/analytics_store
```

**Data files not found**
```bash
python setup_database.py
```

**Path issues in notebooks**
- Make sure you're running from the correct directory
- Check that `project_root` points to the repository root

### Next Steps

Once you're comfortable with Polars basics:

1. **Tutorial 01** - Lift Analysis (classification metrics)
2. **Tutorial 02** - ROC Analysis (model evaluation)
3. **Tutorial 03** - Regression Metrics (continuous predictions)

### Additional Resources

- [Polars Documentation](https://pola-rs.github.io/polars/)
- [Polars User Guide](https://pola-rs.github.io/polars-book/)
- [Polars Cheat Sheet](https://franzdiebold.github.io/polars-cheat-sheet/Polars_cheat_sheet.pdf)
- [Coming from Pandas](https://pola-rs.github.io/polars-book/user-guide/migration/pandas/)

---

**Ready to start?** Run the tutorial and complete the exercises!
