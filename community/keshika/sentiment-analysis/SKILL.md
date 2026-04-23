# Skill: Context-Aware Sentiment Analyzer

## 🧩 Overview
This skill focuses on understanding the *context* of a sentence rather than just individual words to determine sentiment. It can handle subtle expressions like sarcasm, mixed opinions, and emotional tone.

## 🎯 Goal
To build an AI capability that interprets human language more naturally and classifies sentiment as Positive, Negative, or Neutral based on context.

## ⚙️ Working Principle
1. Accept user input text
2. Normalize text (lowercasing, punctuation removal)
3. Break text into tokens
4. Capture context using sequence-based models
5. Analyze relationships between words
6. Predict sentiment using trained models
7. Return final sentiment label

## 🧠 Techniques Used
- Tokenization and text cleaning
- Word embeddings (Word2Vec / GloVe)
- Sequence modeling (LSTM)
- Contextual understanding (Transformer models like BERT)

## 📥 Sample Input
"I expected this movie to be boring, but it turned out amazing!"

## 📤 Sample Output
Sentiment: Positive

## ⚠️ Special Feature
Unlike basic models, this skill considers *contrast words* like "but", which can completely change sentiment meaning.

## 📦 Requirements
- Python
- NLTK / spaCy
- NumPy
- TensorFlow / PyTorch
- Transformers library

## 📚 References
- https://huggingface.co/docs/transformers
- https://www.tensorflow.org/tutorials/text/text_classification
- https://nlp.stanford.edu/projects/glove/

## 🚀 Applications
- Detecting fake or misleading reviews
- Customer opinion mining
- Chatbot response improvement
- Social media sentiment tracking

## 📝 Remarks
- Performance improves with larger datasets
- Transformer models provide highest accuracy
- Context understanding is key for real-world NLP
