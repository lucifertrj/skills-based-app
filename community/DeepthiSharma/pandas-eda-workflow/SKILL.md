---
name: pandas-eda-workflow
description: Pandas EDA skill - Covers data loading, cleaning, transformation, aggregation, and visualization workflows used in real-world data analysis.
---
## Overview

Pandas is a powerful data analysis library in Python used for handling structured data.

This skill walks through a practical **Exploratory Data Analysis (EDA)** workflow using Pandas, including inspecting data, cleaning it, transforming features, and generating basic visual insights.

Use this when you're working on:

* Data analysis projects
* Machine learning preprocessing
* CSV / tabular datasets
* Understanding and preparing features

---

## Setup

```bash
pip install pandas matplotlib seaborn
```

---

## Getting Started

```python
import pandas as pd

df = pd.read_csv("resources/dataset.csv")

df.head()
df.info()
df.describe()
```

---

## Understanding the Dataset

### Data Structure Basics

* Series → single column
* DataFrame → table of data

```python
df.shape
df.columns
df.dtypes
```

---

## Exploring the Data

```python
df.head()
df.tail()
df.sample(5)
```

```python
df.info()
df.describe()
```

---

## Dealing with Missing Data

```python
df.isnull().sum()
```

### Removing missing values

```python
df = df.dropna()
```

### Filling missing values

```python
df.fillna(df.mean(), inplace=True)
```

---

## Cleaning and Preparing Data

### Renaming columns

```python
df.rename(columns={"old_name": "new_name"}, inplace=True)
```

### Removing duplicates

```python
df.drop_duplicates(inplace=True)
```

### Fixing data types

```python
df["column"] = df["column"].astype(int)
```

---

## Filtering and Selecting Data

```python
df[df["age"] > 25]
```

```python
df[(df["age"] > 25) & (df["salary"] > 50000)]
```

---

## Summarizing Data

```python
df.groupby("department")["salary"].mean()
```

```python
df.groupby("department").agg({
    "salary": "mean",
    "age": "max"
})
```

---

## Ordering Data

```python
df.sort_values(by="salary", ascending=False)
```

---

## Creating New Features

```python
df["bonus"] = df["salary"] * 0.1
```

---

## Visualizing Insights

Using Matplotlib and Seaborn:

### Distribution plot

```python
df["age"].hist()
```

### Salary spread

```python
import seaborn as sns

sns.boxplot(x=df["salary"])
```

### Feature relationships

```python
sns.heatmap(df.corr(), annot=True)
```

---

## Handy Operations

### Selecting specific columns

```python
df[["name", "salary"]]
```

### Applying transformations

```python
df["salary"] = df["salary"].apply(lambda x: x * 1.1)
```

---

## Best Practices

* Prefer vectorized operations over loops
* Use `.loc` and `.iloc` correctly
* Avoid unnecessary modifications
* Work on copies when needed

---

## Tool Selection Guide

* Pandas → tabular data handling
* NumPy → numerical operations
* Seaborn → statistical plots
* Matplotlib → custom visualizations

---

## References

* https://pandas.pydata.org/docs/
* https://seaborn.pydata.org/
* https://matplotlib.org/
