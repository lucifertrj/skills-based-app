# Transformers Skill

## When to use this skill
Use this skill when the task involves:
- Loading and using pre-trained transformer models (BERT, GPT-2, T5, etc.)
- Fine-tuning transformers on custom datasets
- Text classification, summarization, translation, or question answering
- Tokenization and encoding of text for transformer input
- Working with the Hugging Face `transformers` library

Do NOT use this skill for: CNNs, RNNs, non-NLP tasks, or raw PyTorch/TensorFlow without transformers.

---

## Overview

The Hugging Face `transformers` library provides thousands of pretrained models for NLP, vision, and audio tasks. The two core objects are:

- **Tokenizer** — converts raw text into token IDs the model understands
- **Model** — the neural network that processes those token IDs

Most workflows follow this pattern:

---

## Core Workflows

### 1. Text Classification (e.g., Sentiment Analysis)

**Prerequisites:** `pip install transformers torch`

**Steps:**
1. Import `pipeline` from `transformers`
2. Create a pipeline with task name `"text-classification"`
3. Pass your text string to get predictions

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
result = classifier("I love how easy transformers are to use!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.99}]
```

---

### 2. Loading a Model and Tokenizer Manually

Use this when you need more control than `pipeline()` provides.

**Steps:**
1. Import `AutoTokenizer` and `AutoModel` (or task-specific class like `AutoModelForSequenceClassification`)
2. Call `.from_pretrained("model-name")` on both
3. Tokenize your text with `return_tensors="pt"` for PyTorch
4. Pass tokens to the model

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
```

---

### 3. Fine-tuning on a Custom Dataset

**Prerequisites:** `pip install transformers datasets torch`

**Steps:**
1. Load your dataset using `datasets` library or a custom DataFrame
2. Tokenize using `dataset.map()` with your tokenizer
3. Load model with `AutoModelForSequenceClassification.from_pretrained(..., num_labels=N)`
4. Define `TrainingArguments`
5. Create a `Trainer` and call `.train()`

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

dataset = load_dataset("imdb")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding=True)

dataset = dataset.map(tokenize, batched=True)
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

training_args = TrainingArguments(output_dir="./results", num_train_epochs=3, per_device_train_batch_size=8)
trainer = Trainer(model=model, args=training_args, train_dataset=dataset["train"], eval_dataset=dataset["test"])
trainer.train()
```

---

### 4. Text Generation (GPT-2)

```python
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")
result = generator("Once upon a time", max_length=50, num_return_sequences=1)
print(result[0]["generated_text"])
```

---

## If/Then Decision Rules

- **If** you just need a quick result → use `pipeline()`
- **If** you need custom preprocessing or output → use `AutoTokenizer` + `AutoModel` manually
- **If** you want to adapt a model to your own data → use `Trainer` for fine-tuning
- **If** the model is too large for your machine → use `device_map="auto"` and `load_in_8bit=True` (requires `bitsandbytes`)
- **If** task is multilingual → prefer `xlm-roberta-base` over `bert-base-uncased`

---

## Guardrails & Common Pitfalls

- ❌ **Don't** forget `return_tensors="pt"` when tokenizing for PyTorch — the model will throw a type error
- ❌ **Don't** mix tokenizers and models from different model families (e.g., BERT tokenizer with GPT-2 model)
- ❌ **Don't** skip `truncation=True` on long texts — transformers have a max token limit (usually 512)
- ⚠️ **Always** call `model.eval()` during inference to disable dropout
- ⚠️ GPU memory errors → reduce `per_device_train_batch_size` or use `gradient_accumulation_steps`
- ⚠️ First run downloads model weights — ensure internet access and ~500MB+ free disk space

---

## Resources

- [Hugging Face Transformers Docs](https://huggingface.co/docs/transformers)
- [Model Hub](https://huggingface.co/models)
- [Hugging Face Course (free)](https://huggingface.co/learn/nlp-course)