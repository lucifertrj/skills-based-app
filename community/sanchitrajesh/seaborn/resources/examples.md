import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')

# EDA
sns.pairplot(df, hue='target', corner=True)
sns.displot(data=df, x='measurement', hue='condition', col='timepoint', kind='kde', fill=True)

# Correlation
corr = df.select_dtypes('number').corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', center=0)

# Multi-panel figure
fig, axes = plt.subplots(2,2, figsize=(10,8))
sns.lineplot(data=df, x='x', y='y', ax=axes[0,0])
sns.violinplot(data=df, x='cat', y='val', ax=axes[0,1])
sns.scatterplot(data=df, x='x', y='y', ax=axes[1,0])
sns.heatmap(corr, ax=axes[1,1])

# Time series
sns.lineplot(data=df, x='time', y='value', hue='sensor', errorbar=('ci',95))

# Categorical comparison
sns.barplot(data=df, x='category', y='value', hue='group')
sns.violinplot(data=df, x='category', y='value', hue='group')
sns.pointplot(data=df, x='timepoint', y='score', hue='treatment')

# Regression
sns.lmplot(data=df, x='x', y='y', hue='group', col='type')
sns.regplot(data=df, x='x', y='y', order=2)

# Joint + KDE
sns.jointplot(data=df, x='x', y='y', kind='scatter')
sns.kdeplot(data=df, x='x', y='y', fill=True)

# Clustermap
sns.clustermap(corr, cmap='viridis')

# Before/After
df_melt = df.melt(id_vars='id', value_vars=['before','after'])
sns.violinplot(data=df_melt, x='variable', y='value')

# Styling
sns.set_theme(style='ticks', context='paper')
plt.tight_layout()
plt.show()