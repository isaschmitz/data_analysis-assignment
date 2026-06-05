# AMOC Analysis Assignment

> 📊 Data analysis for physical oceanography - analyzing AMOC transport data using Python

This assignment provides a framework for analyzing Atlantic Meridional Overturning Circulation (AMOC) transport data from the RAPID-MOCHA array at 26°N.

## 🚀 What's Included

- ✅ Python package for AMOC analysis: `amoc_analysis/*.py`
- 📓 Jupyter notebook demo: `notebooks/demo.ipynb`
- 🔍 Tests with `pytest` in `tests/`
- 🎨 Code formatting with `black` and `ruff`
- 📦 Package configuration via `pyproject.toml`

---

## Project Structure

```
amoc-analysis/
├── notebooks/                  # Jupyter notebooks for analysis
├── amoc_analysis/             # Main Python package
│   ├── data.py                # Data loading functions
│   ├── analysis.py            # Analysis tools and utilities
│   └── plotting.py            # Visualization functions
├── tests/                     # Test suite
│   ├── test_data.py           # Tests for data loading
│   ├── test_analysis.py       # Tests for analysis functions
│   └── test_plotting.py       # Tests for plotting functions
├── data/                      # Data files (downloaded automatically)
├── pyproject.toml             # Package configuration
├── requirements.txt           # Core dependencies
├── requirements-dev.txt       # Development dependencies
├── GETTING_STARTED.md         # Step-by-step guide for beginners
└── INSTRUCTIONS.md            # Detailed project structure explanation
```

## Assignment Goals

- 📊 **Load and explore AMOC transport data** from the RAPID array
- 🔍 **Analyze temporal variability** in the meridional overturning circulation
- 📈 **Create visualizations** to understand AMOC behavior
- 🧪 **Apply scientific Python tools** including xarray, pandas, and matplotlib
- 📝 **Document your analysis** using Jupyter notebooks

---

## 🔧 Getting Started

> 💡 **New to Python projects?** Check out [GETTING_STARTED.md](GETTING_STARTED.md) for a beginner-friendly progression from simple to advanced.

1. **Install the package in development mode:**

```bash
# Clone the repository (or download from your course platform)

# Install dependencies and the package
pip install -e ".[dev]"
```

2. **Start Jupyter Lab:**

```bash
jupyter lab
```

3. **Open the demo notebook:**
   - Navigate to `notebooks/demo.ipynb`
   - Run the cells to see example analysis

4. **Run tests to verify installation:**

```bash
pytest
```

---

## 📊 Data

The assignment uses transport data from the RAPID-MOCHA array at 26°N. Data will be automatically downloaded when you run the analysis functions. The main dataset includes:

- **Time series**: 2004-present
- **Variables**: Meridional overturning streamfunction, heat transport, volume transport
- **Resolution**: 12-hourly and daily values
- **Units**: Sverdrups (Sv) for volume transport, Petawatts (PW) for heat transport

---

## 🎯 Assignment Tasks

Work through the following analysis tasks in your notebook:

1. **Data Exploration**: Load the RAPID dataset and examine its structure
2. **Time Series Analysis**: Plot and analyze AMOC variability over time
3. **Statistical Analysis**: Calculate means, trends, and seasonal cycles
4. **Visualization**: Create publication-quality plots of your results
5. **Interpretation**: Discuss the oceanographic significance of your findings

---

## 🛠️ Key Functions

The `amoc_analysis` package provides several useful functions:

```python
from amoc_analysis import data, plotting, analysis

# Load sample AMOC data
ds = data.load_sample_dataset("rapid")

# Create visualizations
plotting.plot_monthly_transport(ds)

# Convert units
transport_sv = analysis.convert_units_var(transport_m3s, "m^3/s", "Sv")
```

You also have access to the **amocatlas** package for additional AMOC tools and datasets:

```python
import amocatlas
# Explore additional AMOC datasets and analysis tools
```

---

## 📝 Code Quality

Use the provided tools to maintain clean code:

```bash
# Format code
black amoc_analysis/ tests/

# Check code style  
ruff check amoc_analysis/ tests/

# Run tests
pytest
```

---

## 📚 Useful Resources

- [RAPID-MOCHA Array](https://rapid.ac.uk/rapidmoc)
- [Xarray Documentation](https://xarray.pydata.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Physical Oceanography Concepts](https://www.whoi.edu/know-your-ocean/)

---

## 🤝 Getting Help

If you encounter issues:

1. Check that all dependencies are installed correctly
2. Verify your Python environment is activated
3. Review the example notebook for guidance
4. Ask questions during office hours or class

Good luck with your analysis! 🌊
