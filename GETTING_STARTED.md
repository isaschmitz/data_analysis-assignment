# Getting Started: From Simple to Sophisticated

This guide shows you how to approach the AMOC analysis assignment with increasing levels of complexity. **Start simple** and build up your skills gradually!

## 🎯 Learning Progression

### Level 1: Notebook-Only Approach (Start Here!)
*Goal: Get comfortable with the data and basic analysis*

**What you'll do:**
- Work entirely in a Jupyter notebook
- Copy functions from the package modules directly into notebook cells
- Focus on understanding the data and creating plots

**Why start here:**
- Immediate feedback and experimentation
- No need to worry about imports and module structure yet
- Focus on the science, not the software engineering

**Example workflow:**
```python
# In your notebook, copy functions directly:
def load_sample_dataset():
    # Copy the function from amoc_analysis/data.py
    pass

def plot_time_series():
    # Copy the function from amoc_analysis/plotting.py  
    pass

# Use them immediately:
ds = load_sample_dataset()
plot_time_series(ds, 'moc_mar_hc10')
```

**Rubric expectations at this level:**
- **Code Organization (3.0 - Passed)**: "Basic organization with some functions in modules; implementation works but could be cleaner"
- This is totally fine for your first attempt!

---

### Level 2: Mixed Approach 
*Goal: Start using the package while keeping flexibility*

**What you'll do:**
- Use some functions from the `amoc_analysis` package
- Write custom analysis functions in notebook cells
- Begin to separate data loading from analysis

**Example workflow:**
```python
# Import from the package
from amoc_analysis import data, plotting

# Load data using the package
ds = data.load_sample_dataset()

# Custom analysis in notebook
def calculate_annual_mean(ds):
    return ds.resample(TIME='YE').mean()

# Use both package and custom functions
annual_data = calculate_annual_mean(ds)
plotting.plot_time_series(annual_data, 'moc_mar_hc10')
```

**When to move to this level:**
- You understand what the data looks like
- You want to create custom analysis functions
- You're comfortable with basic imports

---

### Level 3: Package-Focused Approach
*Goal: Write reusable, well-organized code*

**What you'll do:**
- Add your own functions to the package modules
- Use notebooks primarily for analysis and presentation
- Write tests for your new functions

**Example workflow:**

1. **Add to `amoc_analysis/analysis.py`:**
```python
def calculate_trend(ds, var_name):
    """Calculate linear trend in a time series."""
    # Your implementation here
    pass
```

2. **Use in notebook:**
```python
from amoc_analysis import data, analysis, plotting

ds = data.load_sample_dataset()
trend = analysis.calculate_trend(ds, 'moc_mar_hc10')
plotting.plot_time_series(ds, 'moc_mar_hc10')
```

3. **Add tests in `tests/test_analysis.py`:**
```python
def test_calculate_trend():
    # Test your new function
    pass
```

**Rubric expectations at this level:**
- **Code Organization (2.0 - Solid)**: "Decent organization with functions in appropriate modules; implementation meets requirements"
- **Testing (2.0 - Solid)**: "Basic tests present and passing"

---

### Level 4: Advanced Integration
*Goal: Professional-level code organization and testing*

**What you'll do:**
- Function documentation
- Good test coverage
- Clean, reusable notebook that tells a complete scientific story
- Consider creating new modules for specialized analysis

**Rubric expectations at this level:**
- **Code Organization (1.3 - Very good)**: "Well-organized modules and clean function design; good notebook integration"
- **Code Quality (1.3 - Very good)**: "Good adherence to style guidelines, well-documented functions"
- **Testing (1.3 - Very good)**: "Good test coverage using pytest"

---

## 🚀 Quick Start Instructions

### For Complete Beginners (Level 1):

1. **Install and explore:**
```bash
pip install -e ".[dev]"
jupyter lab
```

2. **Open the demo notebook** (`notebooks/demo.ipynb`) and run it
3. **Create a new notebook** for your analysis
4. **Copy functions you need** from the package files into your notebook
5. **Experiment freely** - don't worry about "proper" code organization yet

### For Those Ready to Use the Package (Level 2+):

1. **Start with imports:**
```python
from amoc_analysis import data, plotting, analysis
```

2. **Load and explore data:**
```python
ds = data.load_sample_dataset()
plotting.show_variables(ds)  # Explore what's in the dataset
```

3. **Create your analysis step by step**

---

## 📈 Progression Tips

**How to know when to move to the next level:**

- **Level 1 → 2**: When you understand the data structure and want to avoid copying/pasting functions
- **Level 2 → 3**: When you're writing the same custom function in multiple notebooks
- **Level 3 → 4**: When you want to ensure your code works correctly and could be used by others

**What if you get stuck?**

- **Drop back a level** - there's no shame in working in notebooks!  These are incredibly useful to get to know your data.
- **Focus on one improvement at a time** - don't try to jump from Level 1 to Level 4
- **Ask for help** - the complexity is there to teach you, not to frustrate you

---

## 🎯 Assignment Strategy

**For your first submission:**
- Aim for Level 2 or 3
- Focus more on the scientific analysis than perfect code organization
- Make sure your notebooks tell a clear story about AMOC variability

**Remember:** The rubric shows that "Solid standard (2.0)" is perfectly acceptable. You don't need to achieve "Exceptional" in code organization to do excellent science!

**The goal is learning**, not perfection. Start where you're comfortable and build your skills gradually.

---

## 🔧 Common Workflows by Level

### Level 1 Workflow:
```
Create notebook → Copy functions → Analyze → Submit notebook
```

### Level 2 Workflow:  
```
Create notebook → Import some functions → Write custom analysis → Submit notebook
```

### Level 3 Workflow:
```
Add function to package → Write test → Import in notebook → Analyze → Submit both
```

### Level 4 Workflow:
```
Design module structure → Implement & test → Document → Create analysis notebook → Submit complete package
```

Depending on your starting level with Python, aim to jump 1-2 steps for your first assignment, and another 1-2 steps for your second assignment.