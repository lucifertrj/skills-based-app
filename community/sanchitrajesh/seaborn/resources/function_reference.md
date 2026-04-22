import seaborn as sns

# Relational
sns.scatterplot(data=df, x='x', y='y', hue='group', size='val', style='type')
sns.lineplot(data=df, x='time', y='value', hue='group', errorbar=('ci',95))
sns.relplot(data=df, x='x', y='y', col='cat', kind='scatter')

# Distribution
sns.histplot(data=df, x='x', hue='group', bins=30, kde=True)
sns.kdeplot(data=df, x='x', fill=True)
sns.ecdfplot(data=df, x='x', hue='group')
sns.displot(data=df, x='x', col='group', kind='kde')
sns.jointplot(data=df, x='x', y='y')
sns.pairplot(df, hue='group')

# Categorical
sns.stripplot(data=df, x='cat', y='val', hue='group', jitter=True)
sns.swarmplot(data=df, x='cat', y='val')
sns.boxplot(data=df, x='cat', y='val', hue='group')
sns.violinplot(data=df, x='cat', y='val', split=True)
sns.boxenplot(data=df, x='cat', y='val')
sns.barplot(data=df, x='cat', y='val', estimator='mean')
sns.countplot(data=df, x='cat')
sns.pointplot(data=df, x='cat', y='val')
sns.catplot(data=df, x='cat', y='val', kind='box')

# Regression
sns.regplot(data=df, x='x', y='y', order=2)
sns.lmplot(data=df, x='x', y='y', col='group')
sns.residplot(data=df, x='x', y='y')

# Matrix
sns.heatmap(df.corr(), annot=True)
sns.clustermap(df.corr())

# Grids
g = sns.FacetGrid(df, col='cat')
g.map(sns.scatterplot, 'x', 'y')