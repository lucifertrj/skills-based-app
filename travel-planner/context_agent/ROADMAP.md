# 🗺️ Roadmap — Booking.com Trip Planner (Open Source PoC)

> This file tracks features that are **out of scope for the current implementation** but are logged for future contributors or future versions of this project.

---

## ✅ Currently In Scope (v1.0 PoC)

| Feature | Status | Description |
|---------|--------|-------------|
| Smart Filter — Step 1: Structured Intent Extraction | 🔨 Building | GPT-4o-mini → `FilterSchema` (Pydantic) |
| Smart Filter — Step 3: Semantic Ranker | 🔨 Building | Qdrant hybrid search on property embeddings |
| Smart Filter — Step 4: Composite Scorer | 🔨 Building | RRF scoring across semantic + filter + quality + memory signals |
| Memory Layer — Travel DNA (Cognee) | 🔨 Building | User preference graph built from interactions |
| Property RAG Layer (Qdrant) | 🔨 Building | Property + review embeddings for semantic search |
| Property Q&A | 📋 Planned | RAG over property data to answer specific traveler questions |

---

## 🔮 Future Scope — Not Implementing Now

### 🏷️ F-001: Intent Classification using NER (Named Entity Recognition)

**What it is:**  
A dedicated NER pipeline that parses a user's natural language query and classifies intent at a fine-grained token level — extracting entities like `DESTINATION`, `AMENITY`, `VIBE`, `PROPERTY_TYPE`, `DATE`, `BUDGET`, `TRAVELER_TYPE` as labeled spans directly from text.

**Why it's powerful:**  
Rather than relying on an LLM to do free-form extraction (Step 1 in our current plan), a trained NER model provides:
- **Faster inference** — no LLM API call needed for extraction
- **Deterministic, labeled output** — consistent entity types
- **Lower cost at scale** — a small fine-tuned model (spaCy / BERT-NER) handles millions of queries cheaply
- **Auditability** — you can see exactly which span in the query triggered which filter

**How it would integrate:**  
```
User Query → NER Model → Entity Spans → FilterSchema → (same pipeline continues)
```
The NER output replaces the current GPT-4o-mini structured extraction in Step 1.  
The rest of the pipeline (memory enricher, semantic ranker, composite scorer) stays identical.

**What's needed to implement:**  
- A labeled dataset of travel queries with entity spans (e.g., spaCy NER format)
- Fine-tuned NER model (likely on `en_core_web_trf` or a travel-domain BERT model)
- Integration layer to map NER entity types → `FilterSchema` fields
- Evaluation pipeline: Precision/Recall on entity extraction

**Why deferred:**  
- Booking.com's own engineering blog doesn't mention this publicly — it's likely internal
- Requires a labeled training dataset (significant effort)
- For PoC purposes, GPT-4o-mini structured extraction is sufficient and cheaper to build
- This is a **production optimization**, not a PoC requirement

**Future contributor note:**  
This is the single most impactful algorithmic improvement for scaling the Smart Filter to production. If you are building on this open source project and want to take it beyond PoC, start here.

---

### 🏷️ F-002: Real-time Behavioral Signal Streaming

**What it is:**  
A streaming pipeline (Kafka / Kinesis) that captures user behavioral signals (clicks, scroll depth, hover time, abandonment) in real-time and updates the Cognee memory graph without batch processing.

**Why deferred:**  
For PoC, signals are recorded synchronously on click/booking events. Real-time streaming is an infrastructure concern, not a core feature concern.

---

### 🏷️ F-003: Multi-modal Property Indexing (Images)

**What it is:**  
Embedding property images using CLIP or a travel-domain vision model, and including visual similarity in the ranking pipeline. "Sunset views" would match photos showing warm-toned, panoramic balcony shots.

**Why deferred:**  
Requires a separate image embedding model, multimodal Qdrant collection, and image dataset. Significant scope expansion beyond current text-based PoC.

---

### 🏷️ F-004: A/B Testing Infrastructure

**What it is:**  
A framework to run controlled experiments on ranking weights, memory enrichment strategies, and filter schemas to measure conversion impact.

**Why deferred:**  
Only relevant when multiple users are using the system. PoC uses fixed RRF weights.

---

## 📅 Revision Log

| Date | Entry |
|------|-------|
| 2026-03-08 | Initial roadmap created. F-001 (NER Intent Classification) deferred from v1 scope. |
