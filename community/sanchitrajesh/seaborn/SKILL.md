---
name: seaborn
description: "Statistical visualization. Scatter, box, violin, heatmaps, pair plots, regression, correlation matrices, KDE, faceted plots, for exploratory analysis and publication figures."
---

# Seaborn Statistical Visualization

## Overview

Seaborn is a Python visualization library for creating publication-quality statistical graphics. Use this skill for dataset-oriented plotting, multivariate analysis, automatic statistical estimation, and complex multi-panel figures with minimal code.

## Design Philosophy

Seaborn follows these core principles:

1. **Dataset-oriented**: Work directly with DataFrames and named variables rather than abstract coordinates
2. **Semantic mapping**: Automatically translate data values into visual properties (colors, sizes, styles)
3. **Statistical awareness**: Built-in aggregation, error estimation, and confidence intervals
4. **Aesthetic defaults**: Publication-ready themes and color palettes out of the box
5. **Matplotlib integration**: Full compatibility with matplotlib customization when needed

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load dataset
df = sns.load_dataset('tips')

# ================= BASIC PLOTS =================
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()

sns.lineplot(data=df, x='total_bill', y='tip')
plt.show()

# ================= OBJECTS INTERFACE =================
from seaborn import objects as so
(
    so.Plot(df, x='total_bill', y='tip')
    .add(so.Dot(), color='day')
    .add(so.Line(), so.PolyFit())
)

# ================= RELATIONAL PLOTS =================
sns.scatterplot(data=df, x='total_bill', y='tip', hue='time')
sns.scatterplot(data=df, x='total_bill', y='tip', style='sex')
sns.lineplot(data=df, x='size', y='total_bill')
sns.relplot(data=df, x='total_bill', y='tip', col='time', hue='sex')
plt.show()

# ================= DISTRIBUTION PLOTS =================
sns.histplot(data=df, x='total_bill', bins=20)
sns.histplot(data=df, x='total_bill', hue='time', kde=True)
sns.kdeplot(data=df, x='total_bill', fill=True)
sns.ecdfplot(data=df, x='total_bill')
sns.displot(data=df, x='total_bill', col='time')
plt.show()

# ================= CATEGORICAL PLOTS =================
sns.boxplot(data=df, x='day', y='total_bill')
sns.violinplot(data=df, x='day', y='total_bill')
sns.stripplot(data=df, x='day', y='total_bill', jitter=True)
sns.swarmplot(data=df, x='day', y='total_bill')
sns.barplot(data=df, x='day', y='total_bill')
sns.countplot(data=df, x='day')
sns.catplot(data=df, x='day', y='total_bill', kind='box')
plt.show()

# ================= REGRESSION PLOTS =================
sns.regplot(data=df, x='total_bill', y='tip')
sns.lmplot(data=df, x='total_bill', y='tip', col='time')
sns.residplot(data=df, x='total_bill', y='tip')
plt.show()

# ================= MATRIX PLOTS =================
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm')
sns.clustermap(corr)
plt.show()

# ================= MULTI-PLOT GRIDS =================
g = sns.FacetGrid(df, col='time', row='sex')
g.map(sns.scatterplot, 'total_bill', 'tip')
g.add_legend()

sns.pairplot(df)
sns.jointplot(data=df, x='total_bill', y='tip', kind='scatter')
plt.show()

# ================= AXES VS FIGURE =================
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='total_bill', y='tip', ax=ax)

sns.relplot(data=df, x='total_bill', y='tip', col='time')
plt.show()

# ================= DATA TRANSFORMATION =================
df_long = df.melt()
df_pivot = df.pivot_table(values='total_bill', index='day', columns='time')

# ================= COLOR PALETTES =================
sns.set_palette("colorblind")
sns.color_palette("Set2")
sns.color_palette("viridis")

# ================= THEMES =================
sns.set_theme(style='whitegrid')
sns.set_theme(style='darkgrid')
sns.set_context("talk")

# ================= CUSTOMIZATION =================
ax = sns.scatterplot(data=df, x='total_bill', y='tip', hue='sex')
ax.set(title='Custom Title', xlabel='Bill', ylabel='Tip')
plt.axhline(y=5, linestyle='--')
plt.axvline(x=20, linestyle='--')
plt.show()

# ================= GROUPED ANALYSIS =================
grouped = df.groupby('day')['total_bill'].mean()
print(grouped)

# ================= ADVANCED EXAMPLES =================
sns.scatterplot(data=df, x='total_bill', y='tip', size='size', hue='sex')
sns.lineplot(data=df, x='size', y='tip', hue='time')
sns.boxenplot(data=df, x='day', y='total_bill')
sns.violinplot(data=df, x='day', y='total_bill', hue='sex', split=True)
plt.show()

# ================= TIME SERIES SIMULATION =================
dates = pd.date_range(start='2023-01-01', periods=50)
values = np.random.randn(50).cumsum()

ts_df = pd.DataFrame({'date': dates, 'value': values})
sns.lineplot(data=ts_df, x='date', y='value')
plt.xticks(rotation=45)
plt.show()

# ================= MULTI-PANEL =================
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

sns.scatterplot(data=df, x='total_bill', y='tip', ax=axes[0, 0])
sns.histplot(data=df, x='total_bill', ax=axes[0, 1])
sns.boxplot(data=df, x='day', y='total_bill', ax=axes[1, 0])
sns.kdeplot(data=df, x='total_bill', ax=axes[1, 1])

plt.tight_layout()
plt.show()

# ================= SAVING FIGURES =================
plt.figure()
sns.scatterplot(data=df, x='total_bill', y='tip')
plt.savefig('plot.png', dpi=300)

# ================= EDA =================
sns.pairplot(df)
sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.show()

# ================= PUBLICATION STYLE =================
sns.set_theme(style='ticks')
sns.catplot(data=df, x='day', y='total_bill', kind='box')
plt.show()

# ================= TROUBLESHOOTING =================
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='total_bill', y='tip')
plt.xticks(rotation=45)

sns.set_palette("bright")
sns.kdeplot(data=df, x='total_bill', bw_adjust=0.5)

plt.show()