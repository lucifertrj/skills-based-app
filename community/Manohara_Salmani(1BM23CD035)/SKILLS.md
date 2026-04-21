---
name: sklearn-ml-workflow
description: "End-to-end machine learning workflows using scikit-learn, including preprocessing, model training, evaluation, pipelines, and hyperparameter tuning for tabular data."
---
# Scikit-learn ML Workflow

## Overview

Scikit-learn is a widely used Python library for building machine learning models on structured (tabular) data. It provides simple and efficient tools for data preprocessing, model training, evaluation, and deployment-ready workflows.

## When to Use

Use this skill when:

- Working with tabular datasets (CSV, Excel)
- Solving classification or regression problems
- Preprocessing data (scaling, encoding, missing values)
- Evaluating and comparing models
- Building reusable and clean ML pipelines

## Installation

```bash
pip install scikit-learn pandas numpy matplotlib
```

## Quick Start

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
data = pd.read_csv("data.csv")

X = data.drop("target", axis=1)
y = data["target"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Preprocessing
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model initialization and training
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
```

## Core Workflow

### Data Splitting

Splits the dataset into training and testing sets to evaluate model performance.

```python
from sklearn.model_selection import train_test_split
```

### Preprocessing

#### Scaling

Standardizes numerical features to improve model performance.

```python
from sklearn.preprocessing import StandardScaler
```

#### Missing Values

Handles missing data using strategies like mean or median.

```python
from sklearn.impute import SimpleImputer
```

#### Encoding

Converts categorical variables into numerical format.

```python
from sklearn.preprocessing import OneHotEncoder
```

### Model Training

#### Classification

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)
```

#### Regression

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```

## Model Evaluation

```python
from sklearn.metrics import accuracy_score, classification_report

print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

## Pipelines

Pipelines combine preprocessing and model training into a single workflow.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier())
])

pipeline.fit(X_train, y_train)
```

## Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

params = {
    "n_estimators": [50, 100],
    "max_depth": [5, 10]
}

grid = GridSearchCV(RandomForestClassifier(), params)
grid.fit(X_train, y_train)

print(grid.best_params_)
```

## Advanced Preprocessing

Applies different transformations to numerical and categorical features.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["age", "salary"]),
    ("cat", OneHotEncoder(), ["gender"])
])
```

## Saving and Loading Models

```python
import joblib

joblib.dump(model, "model.pkl")
model = joblib.load("model.pkl")
```

## Prediction

```python
model.predict([[30, 50000]])
```

## Performance Notes

- Normalize features when required.
- Use cross-validation for reliable evaluation.
- Avoid overfitting by tuning hyperparameters.
- Use pipelines for clean and maintainable code.

## References

- [Scikit-learn Official Website](https://scikit-learn.org/stable/)
- [User Guide](https://scikit-learn.org/stable/user_guide.html)
- [API Reference](https://scikit-learn.org/stable/modules/classes.html)
