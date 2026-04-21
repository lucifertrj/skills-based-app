# Vectorization Guide — BoW, TF-IDF, and N-Grams

Text models can't work with raw strings — everything has to become a number.
This guide explains the three main vectorization strategies used with NLTK-cleaned
text, when to use each, and how to tune them effectively.

---

## Why Vectorization?

After cleaning and normalizing text, you have a list of strings like:
```
["run model clean data", "tokenize stem lemmatize", "clean text model train"]
```

Machine learning models need a numeric matrix. Vectorization builds a
**vocabulary** (all unique words seen during training) and represents each
document as a vector of numbers based on that vocabulary.

---

## Method 1 — Bag of Words (CountVectorizer)

### What it does
Counts how many times each vocabulary word appears in each document.
Completely ignores word order — the "bag" metaphor means all words are
thrown into a bag and counted.

### How it works
```
Vocabulary: [cat, dog, log, mat, on, sat, the]
"the cat sat on the mat" → [1, 0, 0, 1, 1, 1, 2]
"the dog sat on the log" → [0, 1, 1, 0, 1, 1, 2]
```

### Code
```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(
    max_features=10000,    # keep top 10,000 most frequent words
    min_df=2,              # word must appear in at least 2 documents
    max_df=0.95,           # word must not appear in >95% of documents
    ngram_range=(1, 1)     # unigrams only (default)
)

X_train = vectorizer.fit_transform(train_texts)   # sparse matrix
X_test = vectorizer.transform(test_texts)          # same vocab as train

print(vectorizer.get_feature_names_out()[:10])    # see vocabulary
print(X_train.shape)                              # (n_docs, vocab_size)
```

### Strengths
- Simple and interpretable — you can look at the matrix and understand it
- Fast to compute
- Works well for document classification with Naive Bayes

### Weaknesses
- Common words like "the" get high counts and dominate even after stopword removal
- No notion of how important a word is across the corpus
- Vocabulary can be huge if `max_features` is not set

### Best for
- Naive Bayes text classifiers
- Keyword-based retrieval
- When you want to see raw word frequencies
- Small corpora where interpretability matters

---

## Method 2 — TF-IDF (TfidfVectorizer)

### What it does
**TF-IDF = Term Frequency × Inverse Document Frequency**

Instead of raw counts, each word gets a weight that reflects:
- How often it appears in **this** document (TF — high is good)
- How rare it is across **all** documents (IDF — rare is rewarded)

A word that appears in every document (like "the") gets a very low IDF weight
even if it appears many times. A word that's unique to a few documents gets
a high IDF weight.

### The math (you don't need to implement this — sklearn does it)
```
TF(t, d)  = count of term t in document d / total terms in d
IDF(t)    = log((1 + n) / (1 + df(t))) + 1    # sklearn's smoothed version
TF-IDF    = TF × IDF
```

### Code
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(
    max_features=5000,     # vocabulary cap — set based on corpus size
    ngram_range=(1, 2),    # unigrams and bigrams
    min_df=2,              # ignore very rare terms
    max_df=0.95,           # ignore near-universal terms (corpus-specific stopwords)
    sublinear_tf=True,     # use log(1 + tf) instead of raw tf — reduces impact of very frequent terms
    norm='l2'              # L2 normalize each document vector (default, good for cosine similarity)
)

X_train = tfidf.fit_transform(train_texts)
X_test = tfidf.transform(test_texts)
```

### `sublinear_tf=True` — when to use it
Raw TF counts grow linearly: a word appearing 100 times gets a weight 100×
a word appearing once. `sublinear_tf=True` applies `log(1 + tf)` which compresses
this. Almost always beneficial for classification tasks.

### Strengths
- Automatically downweights common words — often makes stopword removal less critical
- Better than BoW for most classification tasks
- Widely used benchmark in text classification literature

### Weaknesses
- Still ignores word order
- Doesn't capture semantic similarity (cat and feline are unrelated in TF-IDF space)
- Requires more tuning than BoW

### Best for
- Text classification (sentiment, spam, topic)
- Document similarity / search ranking
- General purpose NLP — this is the default to reach for

---

## Method 3 — N-Grams

### What they are
N-grams capture sequences of N consecutive tokens. They add word-order
information that BoW and TF-IDF miss.

| N | Name | Example |
|---|---|---|
| 1 | Unigram | "machine", "learning" |
| 2 | Bigram | "machine learning" |
| 3 | Trigram | "natural language processing" |

### Why they matter
- "not good" as unigrams: `{not: 1, good: 1}` — same as "really good"
- "not good" as bigrams: `{not_good: 1}` — different from "really good"
- Bigrams capture negation, named entities, and domain phrases

### Code — using `ngram_range` in sklearn
```python
# Unigrams only
CountVectorizer(ngram_range=(1, 1))

# Bigrams only
CountVectorizer(ngram_range=(2, 2))

# Unigrams + bigrams (most common for NLP tasks)
TfidfVectorizer(ngram_range=(1, 2))

# Unigrams + bigrams + trigrams (use with max_features to control size)
TfidfVectorizer(ngram_range=(1, 3), max_features=50000)
```

### Code — generating n-grams manually with NLTK
```python
from nltk import ngrams, bigrams, trigrams

tokens = ["machine", "learning", "is", "great"]

list(bigrams(tokens))
# [("machine", "learning"), ("learning", "is"), ("is", "great")]

# Join back to strings for use with sklearn
bigram_strings = [" ".join(bg) for bg in bigrams(tokens)]
# ["machine learning", "learning is", "is great"]
```

### Character N-Grams
Instead of word tokens, use character sequences. Robust to spelling variation,
typos, and out-of-vocabulary words.

```python
# Character n-grams (analyzer='char_wb' stays within word boundaries)
tfidf_char = TfidfVectorizer(
    analyzer='char_wb',
    ngram_range=(3, 5),
    max_features=30000
)

# "cat" with char 3-grams: [" ca", "cat", "at "]
# Useful for: social media text, medical text with abbreviations, name matching
```

---

## Comparison Summary

| | Bag of Words | TF-IDF | N-Grams (added to either) |
|---|---|---|---|
| **Captures frequency** | ✅ raw counts | ✅ weighted counts | ✅ |
| **Downweights common words** | ❌ | ✅ | depends |
| **Captures word order** | ❌ | ❌ | ✅ partially |
| **Vocabulary size** | medium | medium | large (grows fast) |
| **Speed** | fast | fast | slower |
| **Typical use** | Naive Bayes, baselines | most classifiers | when context matters |

---

## Tuning Parameters — Decision Guide

### `max_features`
Controls vocabulary size. Larger = more expressive but more memory.

| Corpus size | Recommended `max_features` |
|---|---|
| < 1,000 docs | 1,000 – 5,000 |
| 1,000 – 50,000 docs | 5,000 – 20,000 |
| > 50,000 docs | 20,000 – 100,000 |

### `min_df`
Minimum number of documents a term must appear in.
- `min_df=1` — keep everything (use on small datasets only)
- `min_df=2` — remove hapax legomena (safe default)
- `min_df=5` — more aggressive pruning for large corpora

### `max_df`
Maximum document frequency as a fraction.
- `max_df=1.0` — no upper limit (risky, corpus-specific common words stay)
- `max_df=0.95` — good default
- `max_df=0.8` — more aggressive, useful when stopword removal wasn't applied

### `ngram_range`
- `(1, 1)` — unigrams only, fast baseline
- `(1, 2)` — unigrams + bigrams, best general-purpose choice
- `(2, 2)` — bigrams only, occasionally useful for phrase-heavy tasks
- `(1, 3)` — adds trigrams, use `max_features` to prevent memory issues

---

## Full Working Example

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# --- assume clean_corpus is a list of preprocessed strings ---
# --- and labels is a list of class labels ---

X_train, X_test, y_train, y_test = train_test_split(
    clean_corpus, labels, test_size=0.2, random_state=42
)

# Vectorize
tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)
X_train_vec = tfidf.fit_transform(X_train)   # fit + transform on train
X_test_vec = tfidf.transform(X_test)          # transform only on test

# Train
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

# Evaluate
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred, zero_division=0))

# Inspect top features per class
feature_names = tfidf.get_feature_names_out()
for i, class_label in enumerate(clf.classes_):
    top_idx = clf.coef_[i].argsort()[-10:][::-1]
    top_words = [feature_names[j] for j in top_idx]
    print(f"Class '{class_label}': {top_words}")
```
