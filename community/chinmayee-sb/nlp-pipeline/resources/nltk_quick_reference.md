# NLTK Quick Reference

A cheat sheet for the most commonly used NLTK functions in a text preprocessing
workflow. Use this as a lookup when writing or debugging pipeline code.

---

## Setup

```python
import nltk

# Download everything you need (run once per environment)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

# Check where NLTK looks for data
print(nltk.data.path)
```

---

## Tokenization

| Function | What it does | Returns |
|---|---|---|
| `word_tokenize(text)` | Splits text into word tokens | `list[str]` |
| `sent_tokenize(text)` | Splits text into sentences | `list[str]` |
| `TweetTokenizer().tokenize(text)` | Tokenizes social media text, preserves emojis | `list[str]` |
| `MWETokenizer` | Handles multi-word expressions like "New York" | `list[str]` |

```python
from nltk.tokenize import word_tokenize, sent_tokenize, TweetTokenizer

word_tokenize("Don't stop now.")
# ["Do", "n't", "stop", "now", "."]

sent_tokenize("Hello world. How are you?")
# ["Hello world.", "How are you?"]

tweet_tok = TweetTokenizer()
tweet_tok.tokenize("I love #NLP @nltk 😊")
# ["I", "love", "#NLP", "@nltk", "😊"]
```

---

## Stopwords

```python
from nltk.corpus import stopwords

# Get default English stopwords
sw = set(stopwords.words('english'))
print(len(sw))   # 179 words

# Available languages
print(stopwords.fileids())
# ['arabic', 'azerbaijani', 'basque', 'bengali', 'catalan', 'chinese', ...]

# Filter tokens
tokens = ["the", "cat", "sat", "on", "mat"]
filtered = [t for t in tokens if t not in sw]
# ["cat", "sat", "mat"]
```

---

## Stemming

```python
from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer

porter = PorterStemmer()
snowball = SnowballStemmer("english")
lancaster = LancasterStemmer()   # most aggressive

words = ["running", "studies", "generously", "university"]

for w in words:
    print(f"{w:15} | Porter: {porter.stem(w):10} | Snowball: {snowball.stem(w):10} | Lancaster: {lancaster.stem(w)}")

# running         | Porter: run        | Snowball: run        | Lancaster: run
# studies         | Porter: studi      | Snowball: studi      | Lancaster: study
# generously      | Porter: generous   | Snowball: generous   | Lancaster: gen
# university      | Porter: univers    | Snowball: univers    | Lancaster: univers
```

**Which stemmer to use:**
- `SnowballStemmer` — recommended default, supports 15+ languages
- `PorterStemmer` — classic, English only, slightly less accurate than Snowball
- `LancasterStemmer` — most aggressive, creates shortest stems, often over-reduces

---

## Lemmatization

```python
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

lemmatizer = WordNetLemmatizer()

# Without POS — defaults to NOUN, misses verbs
lemmatizer.lemmatize("running")        # "running" (wrong)
lemmatizer.lemmatize("running", "v")   # "run" (correct)

# Helper to auto-detect POS
def get_wordnet_pos(word: str) -> str:
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_map = {"J": wordnet.ADJ, "V": wordnet.VERB,
               "N": wordnet.NOUN, "R": wordnet.ADV}
    return tag_map.get(tag, wordnet.NOUN)

# Correct usage
words = ["running", "studies", "better", "quickly"]
for w in words:
    pos = get_wordnet_pos(w)
    print(f"{w} → {lemmatizer.lemmatize(w, pos)}")

# running → run
# studies → study
# better  → good    (adjective detected)
# quickly → quickly (adverb, no lemma change)
```

---

## POS Tagging

```python
import nltk

tokens = ["The", "quick", "brown", "fox", "jumps"]
tags = nltk.pos_tag(tokens)
# [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ('jumps', 'VBZ')]
```

**Common Penn Treebank POS tags:**

| Tag | Meaning | Example |
|---|---|---|
| `NN` | Noun, singular | "dog" |
| `NNS` | Noun, plural | "dogs" |
| `VB` | Verb, base form | "run" |
| `VBG` | Verb, gerund | "running" |
| `JJ` | Adjective | "quick" |
| `RB` | Adverb | "quickly" |
| `DT` | Determiner | "the" |
| `IN` | Preposition | "in", "on" |

---

## Frequency Distribution

```python
from nltk import FreqDist

tokens = ["cat", "dog", "cat", "bird", "cat", "dog"]
fdist = FreqDist(tokens)

fdist.most_common(3)     # [('cat', 3), ('dog', 2), ('bird', 1)]
fdist["cat"]             # 3
fdist.N()                # total tokens: 6
fdist.B()                # unique tokens: 3

# Plot (requires matplotlib)
fdist.plot(10, cumulative=False)
```

---

## N-Grams

```python
from nltk import ngrams, bigrams, trigrams

tokens = ["I", "love", "NLP", "with", "NLTK"]

list(bigrams(tokens))
# [('I', 'love'), ('love', 'NLP'), ('NLP', 'with'), ('with', 'NLTK')]

list(trigrams(tokens))
# [('I', 'love', 'NLP'), ('love', 'NLP', 'with'), ('NLP', 'with', 'NLTK')]

list(ngrams(tokens, 4))
# [('I', 'love', 'NLP', 'with'), ('love', 'NLP', 'with', 'NLTK')]
```

---

## Concordance & Collocations (Text object)

```python
from nltk.text import Text

tokens = word_tokenize("The cat sat on the mat. The cat ate the rat.")
text = Text(tokens)

text.concordance("cat")       # shows context around "cat"
text.similar("cat")           # words that appear in similar contexts
text.collocations()           # frequent bigrams
text.count("cat")             # 2
text.index("cat")             # first occurrence index
```

---

## Useful One-Liners

```python
# Clean + tokenize in one shot
tokens = word_tokenize(re.sub(r"[^a-z\s]", "", text.lower()))

# Remove stopwords inline
sw = set(stopwords.words("english"))
clean = [t for t in tokens if t not in sw and len(t) > 2]

# Stem all tokens
stemmed = [PorterStemmer().stem(t) for t in tokens]

# Lemmatize all tokens with POS
lemmatized = [lemmatizer.lemmatize(t, get_wordnet_pos(t)) for t in tokens]

# Count vocabulary size
vocab_size = len(set(tokens))

# Get top 10 words
from nltk import FreqDist
top10 = FreqDist(tokens).most_common(10)
```
