# Jupyter Notebook Tutorials

Interactive Jupyter notebook versions of all Python tutorials.

## 🚀 Quick Start

### 1. Install Jupyter

```bash
pip install jupyter jupyterlab
```

### 2. Start Jupyter

```bash
# Option 1: Classic Jupyter Notebook
jupyter notebook

# Option 2: JupyterLab
jupyter lab
```

### 3. Navigate to Notebooks

Open your browser and navigate to the `notebooks/` folder, then start with:
- `01_beginner/01_lift_analysis.ipynb`

## 📚 Available Notebooks

### Beginner Level
- **01_lift_analysis.ipynb** - Introduction to lift curves
- **02_roc_analysis.ipynb** - ROC curves and AUC scores
- **03_regression_metrics.ipynb** - Regression model evaluation

### Intermediate Level
- **04_model_comparison.ipynb** - Double lift and model comparison
- **05_sql_integration.ipynb** - Loading data from SQL databases
- **06_population_testing.ipynb** - Statistical hypothesis testing

### Advanced Level
- **07_model_monitoring.ipynb** - Drift detection and monitoring
- **08_snowflake_integration.ipynb** - Cloud data warehouse integration
- **09_end_to_end_pipeline.ipynb** - Complete analytics pipeline

## 🔄 Converting Python Scripts to Notebooks

If you want to regenerate the notebooks from the Python scripts:

```bash
python convert_to_notebooks.py
```

This will automatically convert all `.py` files in `tutorials/` to `.ipynb` files in `notebooks/`.

## 💡 Tips for Using Notebooks

### Running Cells
- **Shift + Enter**: Run current cell and move to next
- **Ctrl + Enter**: Run current cell and stay
- **Alt + Enter**: Run current cell and insert new cell below

### Useful Commands
```python
# Display dataframes nicely
display(df)

# Show plots inline
%matplotlib inline

# Auto-reload modules (useful during development)
%load_ext autoreload
%autoreload 2
```

### Saving Results
All notebooks save results to the `outputs/` folder, just like the Python scripts.

## 🎨 Customization

### Change Plot Style
```python
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-darkgrid')
```

### Adjust Figure Size
```python
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12, 6)
```

### Display More Rows
```python
import polars as pl
pl.Config.set_tbl_rows(20)
```

## 📊 Interactive Features

Notebooks support:
- ✓ Inline plots and visualizations
- ✓ Interactive data exploration
- ✓ Step-by-step execution
- ✓ Markdown documentation
- ✓ Code experimentation
- ✓ Easy sharing and collaboration

## 🔧 Troubleshooting

### Kernel Not Found
```bash
python -m ipykernel install --user --name=analytics_env
```

### Module Not Found
Make sure you're in the correct directory and have installed all requirements:
```bash
cd c:\Users\Max\Documents\Projects\analytics_tutorials
pip install -r requirements.txt
```

### Plots Not Showing
Add this at the top of your notebook:
```python
%matplotlib inline
```

### Path Issues
The notebooks use `Path.cwd().parent.parent` to find the project root. Make sure you're running Jupyter from within the `notebooks/` directory structure.

## 📝 Best Practices

1. **Run cells in order** - Each cell may depend on previous cells
2. **Restart kernel if needed** - Kernel → Restart & Clear Output
3. **Save frequently** - Ctrl + S or File → Save
4. **Experiment freely** - Notebooks are perfect for trying variations
5. **Add your own notes** - Insert markdown cells to document your learning

## 🎓 Learning Path

**Recommended order:**
1. Start with beginner notebooks (01-03)
2. Complete exercises in each notebook
3. Move to intermediate notebooks (04-06)
4. Finish with advanced notebooks (07-09)

**For quick learning:**
- Focus on notebooks 01, 02, 05, and 09

**For deep understanding:**
- Complete all notebooks in sequence
- Do all exercises
- Experiment with different parameters

## 🤝 Sharing Notebooks

### Export to HTML
```bash
jupyter nbconvert --to html notebook_name.ipynb
```

### Export to PDF
```bash
jupyter nbconvert --to pdf notebook_name.ipynb
```

### Share on GitHub
Notebooks render beautifully on GitHub - just commit and push!

## 📖 Additional Resources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
- [Polars Documentation](https://pola-rs.github.io/polars/)
- [Analytics Store Documentation](https://github.com/Wicks-Analytics/analytics_store)

---

**Happy Learning! 🎉**
