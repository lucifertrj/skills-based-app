---
name: nltk-nlp-text-cleaning
description: >
  Use this skill when the user asks to clean, preprocess, tokenize, stem, lemmatize,
  or vectorize raw text data using Python's NLTK library. Triggers include requests like
  "clean this text dataset", "tokenize my corpus", "build an NLP preprocessing pipeline",
  "convert text to TF-IDF or Bag of Words", "compare stemming vs lemmatization",
  or "evaluate my NLP model". Also use when the user asks about stopword removal,
  punctuation stripping, frequency analysis, or building scikit-learn compatible
  text pipelines with NLTK. Do NOT use for deep learning NLP (transformers/BERT/spaCy)
  or for tasks that don't involve text preprocessing.
version: "1.0"
author: chinmayee-sb
tags: [nlp, nltk, text-cleaning, preprocessing, python]
license: MIT
---

# NLTK NLP Text Cleaning Skill

A comprehensive guide for cleaning and preprocessing raw text using Python's NLTK
library. This skill covers the full pipeline: from raw string to model-ready numeric
features, with emphasis on edge cases and production-grade patterns.

For deeper reference material, see the `resources/` folder:
- [`resources/nltk_quick_reference.md`](resources/nltk_quick_reference.md) — cheat sheet for all key NLTK functions
- [`resources/edge_cases.md`](resources/edge_cases.md) — common failure modes and fixes
- [`resources/vectorization_guide.md`](resources/vectorization_guide.md) — deep dive on BoW, TF-IDF, and n-grams

---

## Scope

**Use this skill for:**
- Cleaning raw text (social media, documents, CSV columns, scraped web data)
- Tokenization of words and sentences
- Stemming and lemmatization workflows
- Stopword removal and punctuation handling
- Vectorization (Bag of Words, TF-IDF, n-grams)
- Building reusable preprocessing pipelines
- Evaluating NLP model outputs

**Do NOT use this skill for:**
- Transformer-based models (BERT, GPT, HuggingFace) — those have their own tokenizers
- spaCy-specific pipelines
- Real-time streaming text processing
- Non-English corpora without first checking NLTK language pack availability

---

## Level 1 — Metadata & Environment Setup

### Required Packages

```python
pip install nltk scikit-learn pandas
```

### NLTK Data Downloads (run once)

```python
import nltk
nltk.download('punkt')                       # tokenizer models
nltk.download('punkt_tab')                   # updated punkt tables (NLTK >= 3.8.2)
nltk.download('stopwords')                   # stopword lists
nltk.download('wordnet')                     # WordNet lexical database for lemmatization
nltk.download('averaged_perceptron_tagger')  # POS tagger (needed for accurate lemmatization)
nltk.download('omw-1.4')                     # Open Multilingual WordNet
```

> **Edge case:** On headless servers or CI environments, downloads may fail silently.
> Always call `nltk.data.path` to verify the download location, or pass
> `download_dir` explicitly.

---

## Level 2 — Instructions

### Step 1: Basic Text Cleaning

Start with lowercasing, punctuation removal, and whitespace normalization before
any linguistic processing.

```python
import re
import html

def basic_clean(text: str) -> str:
    """Normalize raw text before any NLP processing."""
    if not isinstance(text, str):                    # handles NaN / numeric cells in DataFrames
        return ""
    text = html.unescape(text)                       # decode &amp; &lt; etc. before regex
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)       # remove URLs
    text = re.sub(r"@\w+|#\w+", "", text)            # remove @mentions and #hashtags
    text = re.sub(r"[^a-z\s]", "", text)             # keep only letters and spaces
    text = re.sub(r"\s+", " ", text).strip()         # collapse whitespace
    return text
```

**When to call `basic_clean` first:** Always run this before tokenization. Passing
raw text with punctuation into `word_tokenize` produces noisy tokens like `"."`,
`","`, `"'s"` that pollute your vocabulary.

---

### Step 2: Tokenization

**Word tokenization** splits a string into individual word tokens.
**Sentence tokenization** splits a document into sentences — useful when you need
to process text sentence-by-sentence before word-level work.

```python
from nltk.tokenize import word_tokenize, sent_tokenize

def tokenize_words(text: str) -> list[str]:
    """Word-level tokenization using NLTK's Punkt tokenizer."""
    return word_tokenize(text)

def tokenize_sentences(text: str) -> list[str]:
    """Sentence-level tokenization."""
    return sent_tokenize(text)

# Example
text = "NLTK makes NLP easy. Let's tokenize this!"
cleaned = basic_clean(text)
print(tokenize_words(cleaned))
# ['nltk', 'makes', 'nlp', 'easy', 'let', 'tokenize', 'this']
```

**Why Punkt?** NLTK's Punkt tokenizer is trained on real text and handles
abbreviations (e.g., "Dr.", "U.S.") intelligently, unlike simple `split()`.

---

### Step 3: Stopword Removal

Stopwords are high-frequency words ("the", "is", "at") that carry little semantic
meaning for most NLP tasks.

```python
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def remove_stopwords(tokens: list[str]) -> list[str]:
    """Filter out English stopwords from a token list."""
    return [t for t in tokens if t not in STOPWORDS]

# Add domain-specific noise words
CUSTOM_STOPS = {"said", "also", "would", "could", "one"}
STOPWORDS.update(CUSTOM_STOPS)
```

**When NOT to remove stopwords:** Sentiment analysis tasks depend on negation words
like "not", "no", "never" — removing them turns "not good" into "good". Skip this
step or use a negation-aware approach for sentiment.

---

### Step 4: Stemming vs Lemmatization

Both reduce words to a base form. The choice matters for downstream model quality.

| | Stemming | Lemmatization |
|---|---|---|
| **Method** | Chops suffix by rule | Looks up dictionary root |
| **Speed** | Fast | Slower (WordNet lookup) |
| **Output** | May not be a real word | Always a valid word |
| **Best for** | Search / information retrieval | Classification, sentiment, NER |
| **Example** | "studies" → "studi" | "studies" → "study" |

```python
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

stemmer = PorterStemmer()
snowball = SnowballStemmer("english")   # Snowball is less aggressive than Porter
lemmatizer = WordNetLemmatizer()

def stem_tokens(tokens: list[str]) -> list[str]:
    return [snowball.stem(t) for t in tokens]

def get_wordnet_pos(word: str) -> str:
    """Map Penn Treebank POS tag to WordNet format.
    Without this, lemmatizer defaults everything to NOUN,
    so 'running' stays 'running' instead of becoming 'run'.
    """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_map = {
        "J": wordnet.ADJ,
        "V": wordnet.VERB,
        "N": wordnet.NOUN,
        "R": wordnet.ADV
    }
    return tag_map.get(tag, wordnet.NOUN)

def lemmatize_tokens(tokens: list[str]) -> list[str]:
    return [lemmatizer.lemmatize(t, get_wordnet_pos(t)) for t in tokens]
```

**Rule of thumb:** Use lemmatization when output quality matters (e.g., you'll
read the tokens or feed them to a classifier). Use stemming when speed matters
more than interpretability (e.g., large-scale search indexing).

---

### Step 5: Vectorization

After cleaning, you need to convert text to numbers. See
[`resources/vectorization_guide.md`](resources/vectorization_guide.md) for a
full deep-dive. The two core methods:

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Bag of Words — raw term counts
bow = CountVectorizer()
X_bow = bow.fit_transform(clean_corpus)

# TF-IDF — downweights common terms, rewards distinctive ones
tfidf = TfidfVectorizer(
    max_features=5000,    # cap vocabulary size
    ngram_range=(1, 2),   # unigrams + bigrams
    min_df=2,             # ignore very rare terms
    max_df=0.95,          # ignore near-universal terms
    sublinear_tf=True     # log-scale term frequency
)
X_tfidf = tfidf.fit_transform(clean_corpus)
```

> **Critical rule:** Always call `.fit_transform()` on training data only.
> Call `.transform()` (no fit) on validation and test sets. Fitting on test data
> leaks information and inflates accuracy.

---

### Step 6: Full Pipeline

```python
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

class NLTKTextPipeline:
    """
    End-to-end NLTK text preprocessing pipeline.

    Parameters
    ----------
    mode : str
        "lemmatize" (default, higher quality) or "stem" (faster)
    remove_stops : bool
        Set False for sentiment tasks to preserve negation words.

    Usage
    -----
    pipeline = NLTKTextPipeline(mode="lemmatize")
    clean_docs = pipeline.run(raw_texts)
    """

    def __init__(self, mode: str = "lemmatize", remove_stops: bool = True):
        assert mode in ("stem", "lemmatize"), "mode must be 'stem' or 'lemmatize'"
        self.mode = mode
        self.remove_stops = remove_stops
        self.stemmer = SnowballStemmer("english")
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words("english"))

    def process(self, text: str) -> str:
        text = basic_clean(text)
        if not text:                   # guard against empty strings post-cleaning
            return ""
        tokens = word_tokenize(text)
        if self.remove_stops:
            tokens = [t for t in tokens if t not in self.stopwords]
        if not tokens:                 # guard against all-stopword documents
            return ""
        if self.mode == "stem":
            tokens = [self.stemmer.stem(t) for t in tokens]
        else:
            tokens = [self.lemmatizer.lemmatize(t, get_wordnet_pos(t)) for t in tokens]
        return " ".join(tokens)

    def run(self, texts: list[str]) -> list[str]:
        return [self.process(t) for t in texts]
```

---

### Step 7: Evaluation Metrics

```python
from sklearn.metrics import classification_report, confusion_matrix, f1_score

# Full per-class breakdown
print(classification_report(y_test, y_pred, target_names=["neg", "pos"], zero_division=0))

# Single number for model comparison
f1 = f1_score(y_test, y_pred, average="weighted")

# Confusion matrix — shows which classes are being confused with which
cm = confusion_matrix(y_test, y_pred)
```

| Metric | When to use |
|---|---|
| **Accuracy** | Balanced classes only |
| **Precision** | Cost of false positives is high (e.g., spam filter) |
| **Recall** | Cost of false negatives is high (e.g., disease detection) |
| **F1 (weighted)** | Imbalanced classes, general purpose |
| **F1 (macro)** | When all classes matter equally regardless of size |

---

## Common Pitfalls Summary

| Pitfall | Symptom | Fix |
|---|---|---|
| `punkt_tab` not downloaded | `LookupError` on tokenize | `nltk.download('punkt_tab')` |
| Fit vectorizer on test set | Inflated accuracy | `.fit_transform()` on train only |
| Lemmatize without POS | Verbs not reduced | Use `get_wordnet_pos()` helper |
| Remove stopwords in sentiment | "not good" becomes "good" | Set `remove_stops=False` |
| Empty string after cleaning | `IndexError` downstream | Guard with `if not text: return ""` |
| Large n-gram range | Memory error on big corpora | Cap `max_features`, use `(1,2)` max |
| Accuracy on imbalanced data | Misleading 95% accuracy | Report F1 + confusion matrix |
