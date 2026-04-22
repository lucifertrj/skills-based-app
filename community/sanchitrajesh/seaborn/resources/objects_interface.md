from seaborn import objects as so
import seaborn as sns

# Basic plot
p = so.Plot(df, x='x', y='y')
p.add(so.Dot()).show()

# With mappings
(
    so.Plot(df, x='x', y='y', color='group')
    .add(so.Dot(), alpha=0.5)
    .add(so.Line(), so.PolyFit(order=2))
)

# Faceting
(
    so.Plot(df, x='x', y='y')
    .facet(col='category')
    .add(so.Dot())
)

# Pair plot
(
    so.Plot(df)
    .pair(x=['a','b','c'])
    .add(so.Dot())
)

# Aggregation
(
    so.Plot(df, x='cat', y='val')
    .add(so.Bar(), so.Agg())
)

# Estimation
(
    so.Plot(df, x='x', y='y')
    .add(so.Line(), so.Est(errorbar=('ci',95)))
)

# Histogram
(
    so.Plot(df, x='x')
    .add(so.Bars(), so.Hist())
)

# KDE
(
    so.Plot(df, x='x')
    .add(so.Area(alpha=0.5), so.KDE())
)

# Moves
(
    so.Plot(df, x='cat', y='val', color='group')
    .add(so.Bar(), so.Agg(), so.Dodge())
)

# Scale + labels
(
    so.Plot(df, x='x', y='y', color='group')
    .add(so.Dot())
    .scale(color=so.Nominal())
    .label(title='Plot Title', x='X', y='Y')
)

# Save
p = so.Plot(df, x='x', y='y').add(so.Dot())
p.save("plot.png")