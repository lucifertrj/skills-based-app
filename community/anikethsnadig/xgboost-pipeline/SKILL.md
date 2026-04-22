---
name: xgboost-pipeline
description: Helps build complete machine learning workflows using XGBoost for classification, regression, feature engineering, tuning, evaluation, and deployment readiness.
---

# XGBoost Pipeline Skill

## Purpose

Use this skill when users need help building XGBoost machine learning models for structured datasets.

## Capabilities

- Data preprocessing
- Classification workflows
- Regression workflows
- Hyperparameter tuning
- Cross validation
- Model evaluation
- Feature importance analysis
- Deployment suggestions

## Instructions

1. Identify whether task is classification or regression.

2. Understand dataset:
- target column
- missing values
- categorical features

3. Build workflow:

### Preprocessing
- null handling
- encoding
- train test split

### Modeling
- XGBClassifier
- XGBRegressor

### Tuning
- learning_rate
- max_depth
- n_estimators
- subsample

### Evaluation

Classification:
- Accuracy
- Precision
- Recall
- F1 Score

Regression:
- RMSE
- MAE
- R2 Score

4. Explain feature importance.

## Example Prompts

- Build XGBoost model for churn prediction
- Tune XGBoost classifier
- Compare RandomForest vs XGBoost

## Success Criteria

- Good metrics
- Clean workflow
- Explainable results
