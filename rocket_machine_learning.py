# -*- coding: utf-8 -*-
"""Rocket_Machine_Learning

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Avjum3H_QOUEPWdneyUNSWcz4oNawLY4
"""

!pip install scikit-image==0.21.0

!pip install scipy!=1.12.0

!pip install shap

from google.colab import drive
import os
drive.mount('/content/drive', force_remount=True)
file_path = '/content/drive/MyDrive/Output Files'
os.chdir(file_path)

import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
import shap

rocket_df = pd.read_csv('Model Dataset2.csv')
print(rocket_df)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0.1, 2.5))
rocket_df['Pressure'] = scaler.fit_transform(rocket_df[['Pressure']])
print("\n".join(map(str, rocket_df['Pressure'])))

dependent = ['Pressure']
#Pressure drag is the drag force as the rocket moves through air. Heavily dependent on surface area and geometry
independent = ['fin_height', 'fin_base', 'fin_thickness', 'body_radius', 'body_height', 'cone_height', 'fin_count']
#Using the rocket geometry as different independent variables
X = rocket_df[independent]
y = rocket_df[dependent]
print(y.shape)
y = y.values[:, 0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 870)
#Splitting data. Uses same random state to ensure a reproducible split. Allows me to properly evaluate models

#iterating through different degrees
i = 1
bestR2 = 0
while i < 4:
  poly = PolynomialFeatures(degree=i)
  X_train_poly = poly.fit_transform(X_train)
  X_test_poly = poly.transform(X_test)
  model = LinearRegression()
  model.fit(X_train_poly, y_train)
  y_pred = model.predict(X_test_poly)
  mse = mean_squared_error(y_test, y_pred)
  r2 = r2_score(y_test, y_pred)
  print(f"Mean Squared Error of Degree {i}:", mse)
  print("R^2 Score:", r2)
  mae = mean_absolute_error(y_test, y_pred)
  print(f"Mean Absolute Error of Degree {i}:", mae)

  true_values = y_test

  # Residuals
  residuals = true_values - y_pred

  # Create the plot
  plt.scatter(y_pred, residuals, color='blue', alpha=0.5)
  plt.axhline(y=0, color='red', linestyle='--')

  # Set y-axis ticks with increments of 0.5
  y_min, y_max = np.floor(residuals.min()), np.ceil(residuals.max())
  plt.yticks(np.arange(y_min, y_max + 0.1, 0.1))
  plt.ylim(-0.5, 0.5)

  # Add labels and title
  plt.title('Residual Plot(Polynomial)')
  plt.xlabel('Predicted Values')
  plt.ylabel('Residuals (True - Predicted)')

  # Display the plot
  plt.show()
  if r2 > bestR2:
    bestR2 = r2
  i = i+1
print("Best R^2 value is:", bestR2)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.tree import plot_tree
#Hyperparameter tuning for optimal max depth and got 13
#Hyperparameter tuning for optimal number of trees and got 350
#Hyperparameter tuning for minimum samples needed to split and got 2
rf_regressor = RandomForestRegressor(n_estimators=350, max_depth = 13, min_samples_split = 2, random_state=42)

# Train the model
rf_regressor.fit(X_train, y_train)

# Make predictions
y_pred = rf_regressor.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Squared Error:", mse)
print("R^2 Score:", r2)
print("Mean Absolute Error:", mae)


# Print feature importances
print("Feature Importances:", rf_regressor.feature_importances_)
importances = rf_regressor.feature_importances_


# Plot feature importances
plt.figure(figsize=(8, 6))
plt.barh(independent, importances, color='skyblue')
plt.xlabel('Feature Importance')
plt.ylabel('Predictors')
plt.title('Feature Importance vs Predictors')
plt.show()

true_values = y_test

# Residuals
residuals = true_values - y_pred

# Create the plot
plt.scatter(y_pred, residuals, color='blue', alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
# Set y-axis ticks with increments of 0.5
y_min, y_max = np.floor(residuals.min()), np.ceil(residuals.max())
plt.yticks(np.arange(y_min, y_max + 0.1, 0.1))
plt.ylim(-0.5, 0.5)

# Add labels and title
plt.title('Residual Plot(Random Forest)')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals (True - Predicted)')

# Display the plot
plt.show()

# Plot multiple trees in the forest
for i in range(min(3, len(rf_regressor.estimators_))):  # Plot the first 3 trees
    plt.figure(figsize=(20, 10))
    plot_tree(rf_regressor.estimators_[i], filled=True, feature_names=independent)
    plt.show()

rocket_df['Pressure'].hist()
plt.title('Distribution of Pressure Drag Values in Rocket Dataframe', fontsize=16)  # Set title
plt.xlabel('Pressure Drag Value', fontsize=14)  # Set x-axis label
plt.ylabel('Frequency', fontsize=14)  # Set y-axis label
plt.grid(True, linestyle='--', alpha=0.6)  # Add grid with dashed lines and light transparency
plt.xticks(fontsize=12)  # Set x-ticks font size
plt.yticks(fontsize=12)  # Set y-ticks font size

# Show the plot
plt.show()

plt.figure(figsize=(8, 6))  # Set figure size
plt.hist(rocket_df['Pressure'], bins=5, color='skyblue', edgecolor='black', alpha=0.7)  # Customize color, edge color, and transparency
plt.title('Distribution of Pressure Drag Values in Rocket Dataframe', fontsize=16)  # Set title
plt.xlabel('Pressure Drag Value', fontsize=14)  # Set x-axis label
plt.ylabel('Frequency', fontsize=14)  # Set y-axis label
plt.grid(True, linestyle='--', alpha=0.6)  # Add grid with dashed lines and light transparency
plt.xticks(fontsize=12)  # Set x-ticks font size
plt.yticks(fontsize=12)  # Set y-ticks font size

# Show the plot
plt.show()

#iterating through different degrees

poly = PolynomialFeatures(degree=3)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)
model = LinearRegression()
model.fit(X_train_poly, y_train)
y_pred = model.predict(X_test_poly)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(r2)
print(mse)

def wrapper(x):
  x = x.copy()
  x_poly = poly.transform(x)

  return model.predict(x_poly)

X_train_summary = shap.kmeans(X_train, 10)
ex = shap.KernelExplainer(wrapper, X_train_summary)
shap_values = ex.shap_values(X_test)
shap.summary_plot(shap_values, X_test)

shap.initjs()
ex = shap.KernelExplainer(wrapper, X_train_summary)
shap_values = ex.shap_values(X_test.iloc[0, :])
shap.force_plot(ex.expected_value, shap_values, X_test.iloc[0, :])