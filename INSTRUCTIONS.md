# Understanding Your Project Structure

This document explains why your assignment is organized the way it is, and what each file and folder does.

> 🚀 **New to coding projects?** Check out [GETTING_STARTED.md](GETTING_STARTED.md) for a step-by-step approach that starts simple and builds up complexity gradually.

## Why Use a Package Structure?

Instead of putting everything in a single Jupyter notebook, we've organized the code into **modules** (separate `.py` files). This teaches you professional Python development practices:

- **Reusability**: Functions can be imported and used across multiple notebooks
- **Testing**: Code in modules can be easily tested with automated tests
- **Collaboration**: Multiple people can work on different parts without conflicts
- **Maintainability**: Large projects become easier to understand and modify

*💡 Ask an AI: "How do I create a new Python module and import functions from it into a Jupyter notebook?"*

---

## Directory Structure Guide

### 📁 Core Project Files

**`amoc_analysis/`** - Your main Python package
- Contains all the reusable functions for data loading, plotting, and analysis
- Think of this as your "toolbox" that you import into notebooks
- Organized into 3 modules: `data.py` (loading data), `analysis.py` (calculations), `plotting.py` (visualizations)

**`notebooks/`** - Jupyter notebooks for analysis and exploration
- This is where you do your actual data analysis and write up results
- Import functions from your `amoc_analysis` package to keep notebooks clean
- Good for exploratory work, visualizations, and presenting results

**`tests/`** - Automated tests for your code
- Ensures your functions work correctly as you develop them
- Uses the `pytest` framework (see `pyproject.toml` for configuration)
- Each `test_*.py` file tests the corresponding module
- Run with `pytest` to check if everything works

**`data/`** - Data files (created automatically)
- Downloaded data files are stored here
- Keeps your project organized and data separate from code

*💡 Ask an AI: "Show me how to add a new function to the amoc_analysis package and import it in a notebook"*

*💡 Ask an AI: "I want to write a pytest test for my calculate_mean_transport function - show me how to structure the test"*

### 📄 Configuration Files

**`pyproject.toml`** - Modern Python package configuration
- Tells Python how to install your package and its dependencies
- Enables `pip install -e .` for development
- Contains tool settings (black, ruff, pytest)
- Like a "recipe" that describes your project

**`requirements.txt`** - Core dependencies needed to run your code
- Lists packages like numpy, pandas, xarray that your analysis needs
- Includes amocatlas package for additional AMOC analysis tools
- Anyone can install these with `pip install -r requirements.txt`

**`requirements-dev.txt`** - Additional tools for development
- Includes Jupyter, testing tools, code formatters
- Separate because collaborators might not need these development tools
- Install with `pip install -r requirements-dev.txt`

*💡 Ask an AI: "Help me parse this pyproject.toml line by line - what does each section do and what other sections might I want to add?"*

**`.gitignore`** - Tells Git what NOT to track
- Prevents temporary files, data files, and personal settings from being shared
- Keeps your repository clean and focused on code
- Essential for team collaboration

### 🔧 Version Control (after `git init`)

**`.git/`** - Git repository metadata (hidden folder)
- Created when you run `git init`
- Contains all the version history of your project
- Don't modify this directly - use git commands

*💡 Ask an AI: "I want to start tracking my project with Git - walk me through git init, git add, git commit for this project"*

### 📚 Documentation & Provenance

**`README.md`** - Project overview and instructions
- First thing people see when they visit your project
- Explains what the project does and how to use it
- Like the "front page" of your project

**`CITATION.cff`** - How others should cite your work
- Machine-readable citation format
- Important for academic reproducibility
- Helps others give you proper credit

**`LICENSE`** - Legal permissions for using your code
- Tells others what they can and can't do with your work
- Important for open science and collaboration
- Professional projects always include a license

*💡 Ask an AI: "Help me create a proper CITATION.cff file for my own research project with my name and details"*

---

## Development Workflow

Here's how all these pieces work together:

1. **Install your package**: `pip install -e .` (reads `pyproject.toml`)
2. **Write functions**: Add analysis code to `amoc_analysis/` modules
3. **Test your code**: Run `pytest` to check tests in `tests/`
4. **Analyze data**: Import your functions into Jupyter notebooks
5. **Version control**: Use `git` to track changes (respects `.gitignore`)
6. **Share results**: Others can install dependencies and reproduce your work

*💡 Ask an AI: "I want to add a new analysis function to this project - walk me through creating the function, writing a test for it, and using it in a notebook"*

---

## Why This Matters for Science

This structure isn't just about "good programming" - it directly supports **reproducible science**:

- **Transparency**: Others can see exactly what your code does
- **Reproducibility**: Clear dependencies and instructions let others repeat your analysis
- **Collaboration**: Multiple researchers can contribute to the same project
- **Provenance**: Version control tracks how your analysis evolved
- **Reusability**: Your methods can be applied to other datasets

The goal is to make your science **open**, **reproducible**, and **collaborative**.

*💡 Ask an AI: "I want to make my research project fully reproducible - what specific steps should I take with this codebase?"*

---

## Practical Next Steps

Ready to customize this project? Try these AI prompts:

**Package Development:**
- "I want to add a new module called `statistics.py` to my amoc_analysis package - how do I create it and make the functions importable?"
- "How do I create an `__init__.py` file to make my package imports cleaner?"

**Testing:**
- "Help me write a comprehensive test for my data loading function that checks for correct variable names and units"
- "I want to test a function that plots data - how do I write a pytest test for matplotlib plots?"

**Configuration:**
- "I want to add more dependencies to my pyproject.toml - show me the proper syntax for optional dependencies"
- "How do I configure black and ruff in pyproject.toml to use different line lengths or rules?"

**Version Control:**
- "I want to create a .gitignore file for my Jupyter notebook outputs and temporary files - what should I include?"
- "How do I commit only specific files and write good commit messages for scientific code?"

**Documentation:**
- "Help me write docstrings for my functions that follow the numpy documentation standard"
- "I want to create a proper requirements.txt file from my current environment - how do I do that?"

Remember: This structure might seem like overkill for a class assignment, but these are the same tools and practices used in professional scientific software development!

## 🎯 Getting Started

**Feeling overwhelmed?** The project structure is designed to grow with your skills:

1. **Start simple**: Work entirely in notebooks (copy functions as needed)
2. **Build gradually**: Begin using the package functions  
3. **Advance**: Add your own functions to the package modules
4. **Master**: Write comprehensive tests and documentation

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed guidance on each level.