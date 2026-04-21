# Edge Cases in NLTK NLP Pipelines

This file documents the most common failure modes, silent bugs, and tricky
situations you'll encounter when building NLTK preprocessing pipelines —
along with the correct fix for each.

---

## 1. Environment & Setup

### `LookupError: Resource punkt not found`
**Cause:** NLTK data hasn't been downloaded in this environment.
```python
# Fix
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')   # required for NLTK >= 3.8.2
```

### `punkt_tab` missing on NLTK >= 3.8.2
**Cause:** Newer NLTK versions split `punkt` into `punkt` + `punkt_tab`. Downloading
only `punkt` is no longer sufficient.
```python
# Fix — download both
nltk.download('punkt')
nltk.download('punkt_tab')
```

### Downloads fail silently on servers / CI
**Cause:** Headless environments may lack write permissions to the default NLTK
data directory, or have no internet access.
```python
# Fix — specify download directory explicitly
import nltk
import os
NLTK_DATA = "/tmp/nltk_data"
os.makedirs(NLTK_DATA, exist_ok=True)
nltk.download('punkt', download_dir=NLTK_DATA)
nltk.data.path.append(NLTK_DATA)
```

---

## 2. Input Data

### NaN / None values from pandas DataFrames
**Cause:** When reading CSVs, missing text cells become `float('nan')`, not `""`.
Calling `.lower()` on NaN raises `AttributeError`.
```python
# Wrong
df['text'].apply(lambda x: x.lower())   # crashes on NaN

# Fix — guard at the top of your cleaning function
def basic_clean(text):
    if not isinstance(text, str):
        return ""
    return text.lower()
```

### HTML entities in scraped text
**Cause:** Web scrapers often return raw HTML source where `&amp;` wasn't decoded.
Regex won't catch `&amp;` as punctuation, leaving it in tokens.
```python
# Wrong
text = "I love cats &amp; dogs"
re.sub(r"[^a-z\s]", "", text.lower())
# "i love cats amp dogs"  ← "amp" becomes a word

# Fix — decode before cleaning
import html
text = html.unescape("I love cats &amp; dogs")
# "I love cats & dogs"  ← then strip & with regex
```

### Mixed-language text
**Cause:** NLTK's English stopwords and Punkt tokenizer don't handle other scripts.
Arabic or Chinese characters pass through `[^a-z\s]` stripping as spaces,
but may cause issues with POS taggers.
```python
# Fix — either restrict to ASCII or use language-specific pipelines
text = text.encode("ascii", errors="ignore").decode()   # strip non-ASCII
# OR — download language-specific NLTK packs
nltk.download('stopwords')
sw = set(stopwords.words('french'))   # for French text
```

---

## 3. Tokenization

### Contractions split unexpectedly
**Cause:** `word_tokenize("don't")` → `["do", "n't"]`. This may break downstream
vocabulary matching.
```python
# Option A — pre-expand contractions before tokenizing
import contractions   # pip install contractions
text = contractions.fix("I don't know")   # "I do not know"

# Option B — accept the split and treat "n't" as a negation token
# (actually useful for sentiment tasks)
```

### Hyphenated words treated as 3 tokens
**Cause:** `word_tokenize("well-known")` → `["well", "-", "known"]`
```python
# Fix — pre-process hyphenated compounds you want to keep whole
text = re.sub(r"(\w)-(\w)", r"\1_\2", text)   # "well_known"
# tokenize, then restore
tokens = [t.replace("_", "-") for t in word_tokenize(text)]
```

### Empty string after cleaning becomes empty token list
**Cause:** A document that was all punctuation or URLs returns `""` from `basic_clean`.
`word_tokenize("")` returns `[]` — safe, but downstream code may not expect it.
```python
# Fix — always guard before using the token list
tokens = word_tokenize(cleaned)
if not tokens:
    return ""   # or None, or skip this document
```

---

## 4. Stopword Removal

### Removing stopwords breaks sentiment analysis
**Cause:** "not good" → remove "not" → "good". Negation is lost.
```python
# Fix — skip stopword removal for sentiment, OR use negation tagging
# Simple negation tagging: mark tokens after "not/no/never" with _NEG suffix
def negate_tokens(tokens):
    negated = []
    negate = False
    for t in tokens:
        if t in {"not", "no", "never", "n't"}:
            negate = True
            negated.append(t)
        elif t in {".", ",", "!", "?"}:
            negate = False
            negated.append(t)
        else:
            negated.append(t + "_NEG" if negate else t)
    return negated
```

### Document becomes empty after stopword removal
**Cause:** Short documents (tweets, titles) may consist almost entirely of stopwords.
```python
# Fix — add a minimum length guard
tokens = remove_stopwords(word_tokenize(cleaned))
if len(tokens) < 2:
    return ""   # or handle separately
```

---

## 5. Stemming & Lemmatization

### Lemmatization without POS tag — verbs not reduced
**Cause:** `WordNetLemmatizer` defaults to NOUN when no POS is given.
`lemmatize("running")` → `"running"` instead of `"run"`.
```python
# Wrong
lemmatizer.lemmatize("running")         # "running"

# Fix — always pass POS
lemmatizer.lemmatize("running", "v")    # "run"
# Or use the get_wordnet_pos() helper defined in SKILL.md
```

### Porter stemmer over-reduces words
**Cause:** Porter is aggressive. `"university"` → `"univers"`, `"generously"` → `"generous"`.
These are real strings your model has to work with.
```python
# Fix — prefer SnowballStemmer for less aggressive stemming
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english")
stemmer.stem("university")   # "univers" (same, but better on average)

# Or switch to lemmatization entirely for readable output
```

### Stemming produces the same stem from different words (collision)
**Cause:** "operational" and "operate" both stem to "oper". Now they're identical
in your vocabulary, which may or may not be what you want.
```python
# This is expected behaviour, not a bug.
# If it causes problems (e.g., for NER), use lemmatization instead.
```

---

## 6. Vectorization

### Fitting vectorizer on test data (train-test leakage)
**Cause:** Calling `.fit_transform()` on the test set lets the vectorizer learn
test vocabulary. Your accuracy looks better but won't generalize.
```python
# Wrong
X_train = tfidf.fit_transform(train_texts)
X_test = tfidf.fit_transform(test_texts)   # ← leaks test vocab

# Correct
X_train = tfidf.fit_transform(train_texts)
X_test = tfidf.transform(test_texts)        # transform only, no fit
```

### Out-of-vocabulary (OOV) words at inference time
**Cause:** After fitting on train, new words at test/prod time are silently ignored
by sklearn's vectorizer. No error is raised — they just don't appear in the output.
```python
# This is expected and acceptable behaviour.
# To reduce OOV impact: use larger training corpus, or use character n-grams
tfidf = TfidfVectorizer(analyzer='char_wb', ngram_range=(3,5))
# Character n-grams are robust to unseen words and spelling variation
```

### Memory error with large n-gram range
**Cause:** `ngram_range=(1, 3)` on a 100K document corpus can produce millions of
features and exhaust RAM.
```python
# Fix — always cap with max_features
tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=50000)

# Also consider hashing trick for very large corpora
from sklearn.feature_extraction.text import HashingVectorizer
hv = HashingVectorizer(ngram_range=(1, 2), n_features=2**18)
```

### `min_df` and `max_df` interaction
**Cause:** Setting `min_df` too high prunes useful rare domain terms.
Setting `max_df` too low removes meaningful high-frequency domain words.
```python
# Good starting defaults for general corpora
tfidf = TfidfVectorizer(
    min_df=2,        # must appear in at least 2 documents
    max_df=0.95,     # must not appear in more than 95% of documents
)

# For small corpora (<1000 docs), lower min_df to 1 or use absolute count
tfidf = TfidfVectorizer(min_df=1)
```

---

## 7. Evaluation

### Zero-division warning in `classification_report`
**Cause:** A class has no predictions (model never predicts it). Precision = 0/0.
```python
# Fix
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred, zero_division=0))
```

### Accuracy looks great but model is useless
**Cause:** Class imbalance. If 95% of documents are class A, predicting A always
gives 95% accuracy.
```python
# Fix — use weighted or macro F1 as primary metric
from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred, average="weighted")

# Also look at per-class recall in classification_report
# A collapsed model shows recall=1.0 for majority class, recall=0.0 for minority
```

### Model performs well on train, poorly on test
**Cause:** Overfitting. Common causes in NLP:
1. Vocabulary too large (no `max_features` limit) — model memorizes rare train words
2. `min_df=1` — keeps hapax legomena that only appear in train set
3. No regularization on the classifier
```python
# Fix
tfidf = TfidfVectorizer(max_features=10000, min_df=2)
# Plus use regularized classifier e.g. LogisticRegression(C=1.0)
```
