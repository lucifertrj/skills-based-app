---
name: polars
description: "Polars skill — Arrow-backed DataFrame library. Covers expression API, lazy/eager evaluation, group_by, joins, window functions, CSV/Parquet I/O, and pandas migration for high-performance data pipelines."
---

# Polars

## What This Is

Polars is a DataFrame library built on Apache Arrow — think pandas, but faster, stricter, and designed from scratch for modern hardware. It parallelizes by default, evaluates lazily when you want it to, and doesn't silently do weird things to your types.

Use this when you're working with data that's too slow in pandas, building a pipeline that needs to scale, or just want an API that makes more sense.

Install:
```python
uv pip install polars
```

---

## The Mental Model

Two things to internalize before anything else:

**Expressions** — not direct column access. Everything in Polars is built around `pl.col(...)` expressions that describe *what to do*, not *doing it immediately*. They compose, chain, and run in parallel.

**Lazy vs Eager** — choose your execution mode:

```python
# Eager: runs immediately, like pandas
df = pl.read_csv("data.csv")
result = df.filter(pl.col("age") > 25)

# Lazy: builds a plan, optimizes it, runs on .collect()
lf = pl.scan_csv("data.csv")
result = lf.filter(pl.col("age") > 25).select("name", "age").collect()
```

Default to lazy for anything non-trivial. The optimizer handles predicate pushdown, projection pruning, and parallelism automatically.

---

## Core Operations

### Select
```python
# Basic
df.select("name", "age")

# With transformation
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_months")
)

# Regex pattern match across columns
df.select(pl.col("^.*_id$"))
```

### Filter
```python
# Single
df.filter(pl.col("age") > 25)

# Multiple — comma-separated, not chained &
df.filter(
    pl.col("age") > 25,
    pl.col("city") == "Bangalore"
)

# OR condition
df.filter(
    (pl.col("age") > 25) | (pl.col("city") == "Mumbai")
)
```

### With Columns
```python
# Add/modify, all computed in parallel
df.with_columns(
    age_bucket=pl.col("age") + 10,
    name_clean=pl.col("name").str.to_uppercase()
)
```

### Group By + Aggregations
```python
# Standard
df.group_by("city").agg(
    pl.col("age").mean().alias("avg_age"),
    pl.len().alias("n")
)

# Multi-key
df.group_by("city", "dept").agg(
    pl.col("salary").sum()
)

# Conditional count
df.group_by("city").agg(
    (pl.col("age") > 30).sum().alias("seniors")
)
```

Quick reference for agg functions: `pl.len()`, `.sum()`, `.mean()`, `.min()`, `.max()`, `pl.first()`, `pl.last()`

---

## Window Functions

Use `.over()` when you want group-level aggregations *without* collapsing rows — like SQL window functions.

```python
df.with_columns(
    city_avg_age=pl.col("age").mean().over("city"),
    salary_rank=pl.col("salary").rank().over("city")
)

# Multi-column window
df.with_columns(
    group_avg=pl.col("score").mean().over("region", "category")
)
```

Mapping strategies (passed to `.over()`):
- `group_to_rows` — default, keeps original row order
- `explode` — faster, groups rows together
- `join` — produces list columns

---

## I/O

```python
# CSV
df = pl.read_csv("file.csv")                  # eager
lf = pl.scan_csv("file.csv")                  # lazy — prefer this for large files
df.write_csv("out.csv")

# Parquet — best for performance
df = pl.read_parquet("file.parquet")
df.write_parquet("out.parquet")

# JSON
df = pl.read_json("file.json")
df.write_json("out.json")
```

Polars also handles cloud storage (S3, GCS, Azure), databases, Excel, BigQuery, and partitioned/multi-file reads. Load `references/io_guide.md` for those.

---

## Joins and Reshaping

```python
# Joins
df1.join(df2, on="id", how="inner")
df1.join(df2, on="id", how="left")
df1.join(df2, left_on="user_id", right_on="id")

# Concat
pl.concat([df1, df2], how="vertical")    # stack rows
pl.concat([df1, df2], how="horizontal")  # add columns
pl.concat([df1, df2], how="diagonal")    # union, different schemas

# Reshape
df.pivot(values="sales", index="date", columns="product")  # wide
df.unpivot(index="id", on=["col1", "col2"])                # long
```

---

## Coming from Pandas

The biggest mindset shift: **no index**, **no silent type coercion**, **expressions instead of bracket access**.

| What you want | Pandas | Polars |
|---|---|---|
| Select column | `df["col"]` | `df.select("col")` |
| Filter rows | `df[df["col"] > 10]` | `df.filter(pl.col("col") > 10)` |
| Add column | `df.assign(x=...)` | `df.with_columns(x=...)` |
| Group by | `df.groupby("col").agg(...)` | `df.group_by("col").agg(...)` |
| Window fn | `df.groupby().transform(...)` | `.over("col")` |

**The parallel difference:**
```python
# Pandas — sequential, each lambda waits on the previous
df.assign(
    col_a=lambda df_: df_.value * 10,
    col_b=lambda df_: df_.value * 100
)

# Polars — both computed at the same time
df.with_columns(
    col_a=pl.col("value") * 10,
    col_b=pl.col("value") * 100,
)
```

Full migration guide: `references/pandas_migration.md`

---

## Performance Notes

A few rules that actually matter:

**Go lazy early.** `scan_csv` > `read_csv` for anything you're filtering or projecting.
```python
lf = pl.scan_csv("big.csv")
lf.filter(...).select(...).collect()
```

**Stay in the expression API.** The moment you use `.map_elements()` with a Python lambda, you lose parallelism. Use native Polars ops wherever possible.

**Stream for truly large data:**
```python
lf.collect(streaming=True)
```

**Column selection order matters:**
```python
# Do this — push projection early
lf.select("col1", "col2").filter(...)

# Not this
lf.filter(...).select("col1", "col2")
```

**Useful expression patterns:**
```python
# Conditional
pl.when(pl.col("score") > 90).then("A").otherwise("B")

# Regex multi-column
df.select(pl.col("^.*_value$") * 2)

# Null handling
pl.col("x").fill_null(0)
pl.col("x").is_null()
pl.col("x").drop_nulls()
```

---

## References

Deeper docs live in `references/`:

- `core_concepts.md` — expressions, lazy evaluation, type system
- `operations.md` — full operation coverage with examples
- `pandas_migration.md` — migration guide
- `io_guide.md` — all I/O formats, cloud, databases
- `transformations.md` — joins, concat, pivot, unpivot
- `best_practices.md` — optimization patterns

Load whichever is relevant when the quick reference above isn't enough.
