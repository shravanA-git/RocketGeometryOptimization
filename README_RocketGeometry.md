
# Rocket Geometry Optimization Project

This project combines 3D modeling, fluid simulation, and machine learning to optimize rocket geometries for minimal drag. The process involves generating custom rocket shapes, simulating their aerodynamics using OpenFOAM, and training machine learning models to predict and explain drag based on geometric features.

---

## 📁 Project Workflow

### 1. Generate Rocket Geometry

- Run the geometry generation Python script.
- This script outputs 3D rocket models as `.scad` files.
- Install [OpenSCAD](https://openscad.org/downloads.html) to:
  - View the models
  - Export them as `.stl` files for simulation

### 2. Run CFD Simulations with OpenFOAM

- Install [OpenFOAM](https://openfoam.org/download/) on your system.
- Use the provided shell script to:
  - Mesh the exported STL rocket models
  - Set up simulation parameters (boundary conditions, solver setup, etc.)
  - Run simulations to compute drag and flow behavior
- Simulation outputs are stored for feature extraction.

### 3. Parse the Results

- After simulations, run the results-parsing Python script.
- It extracts relevant aerodynamic metrics (like drag coefficient) and geometric parameters.
- Output: a structured `.csv` file used for machine learning.

---

## 🤖 Machine Learning Models

There are two main approaches to modeling drag from geometry:

### A. Baseline Model (Manual ML)

- Trains traditional models like:
  - Random Forest
  - Gradient Boosting
  - XGBoost (if installed)
- Performs model evaluation with:
  - Accuracy
  - Mean squared error
  - Feature importance plots
- Also includes **SHAP analysis** to visualize which geometry features impact drag the most.

### B. AutoGluon Model

- Uses [AutoGluon](https://auto.gluon.ai/stable/index.html) to automate:
  - Model selection
  - Hyperparameter tuning
  - Stacking/ensembling
- Produces leaderboard of models ranked by validation score.
- Great for benchmarking against the manual ML models.

---

## 💻 Requirements

- **Python 3.8+**
- **OpenSCAD** – for geometry generation
- **OpenFOAM** – for CFD simulations
- **Python packages**:
  ```
  pandas
  numpy
  scikit-learn
  matplotlib
  shap
  autogluon
  ```

Install with:
```bash
pip install pandas numpy scikit-learn matplotlib shap autogluon
```

---

## 🚀 Summary

| Step                         | Tool           | Output                         |
|------------------------------|----------------|--------------------------------|
| Rocket model generation      | OpenSCAD       | `.scad` and `.stl` files       |
| CFD simulation               | OpenFOAM       | Drag and flow data             |
| Result parsing               | Python script  | Feature dataset (`.csv`)       |
| Baseline ML training         | scikit-learn   | Predictive model + SHAP plots  |
| AutoGluon training           | AutoGluon      | Leaderboard of best models     |

This end-to-end workflow allows you to design rocket geometries, simulate their performance, and use machine learning to find which shapes are best for minimizing drag.
