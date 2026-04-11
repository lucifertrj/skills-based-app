# 🧬 Dataset Generation Prompt
## Use this with Claude AI to generate the synthetic property dataset

---

## Context

This dataset powers a **Booking.com-inspired Smart Filter PoC**.  
Properties are indexed into **Qdrant** for semantic search.  
User memory using Cognee gets built **live** from real interactions — no pre-seeding needed.
Asset folder contains the design flow I need for the app

So we only need **one dataset: Properties.**

---

## 📋 PROMPT — Paste this into Claude AI

```
You are a synthetic dataset generator for a travel booking platform PoC (similar to Booking.com).

Generate a properties dataset as valid JSON. Follow the schema exactly.

## Properties (generate exactly 60 properties)

Generate 60 diverse fictional hotel/villa/boutique properties across 12 different cities.
Cities to use (6 properties each):
Amsterdam, Paris, Bali, Tokyo, Barcelona, Santorini, New York, Cape Town, Kyoto, Amalfi, Manali, Rome

Rules:
- Mix property types: "hotel" (40%), "boutique" (30%), "villa" (15%), "resort" (15%)
- Each property should have 2-3 vibe_tags from this list ONLY:
  ["romantic", "adventure", "family", "luxury", "budget", "wellness", "party", "scenic", "cultural", "quiet"]
- description must be 4-6 evocative sentences. Do NOT just list features.
  Write how a travel magazine would describe it. Include implicit amenity signals naturally
  (e.g., instead of "has a rooftop bar" write "as the sun dips below the canal, guests gather on the
  open-air terrace for evening cocktails with a view that stretches across the city")
- review_highlights are THE MOST IMPORTANT FIELD. Write 3-5 snippets exactly as a real traveler
  would post them — conversational, personal, describing experiences not amenities.
  These must contain implicit signals that a semantic search would match to queries like:
  "sunset views", "romantic atmosphere", "great gym", "quiet escape", "digital nomad friendly",
  "incredible breakfast", "felt like home", "amazing for couples", "perfect for families" etc.
- price_per_night: realistic USD integer (range: $40 to $900)
- rating: float between 6.5 and 9.9 (1 decimal place)
- review_count: integer between 50 and 5000

## Output schema (strict — follow exactly):

{
  "id": "prop_001",
  "name": "string",
  "type": "hotel | boutique | villa | resort",
  "location": {
    "city": "string",
    "country": "string",
    "neighborhood": "string",
    "location_vibe": "beachfront | city center | hilltop | countryside | riverside | old town | waterfront"
  },
  "price_per_night": 120,
  "rating": 8.7,
  "review_count": 342,
  "amenities": ["string"],
  "vibe_tags": ["string"],
  "description": "string",
  "review_highlights": ["string"],
  "available": true
}

## Amenity list (pick 5-10 per property — vary across properties):
"free wifi", "gym", "swimming pool", "rooftop bar", "spa", "restaurant",
"room service", "concierge", "pet friendly", "parking", "airport shuttle",
"beach access", "hot tub", "sauna", "yoga studio", "bicycle rental",
"kids club", "breakfast included", "bar", "garden", "private pool",
"ocean view rooms", "mountain view rooms", "city view rooms", "balcony",
"business center", "laundry service", "24hr front desk", "ev charging"

## Output format:

Return a single JSON object:

{
  "properties": [ ...60 property objects... ]
}
```

---

## 📥 After Claude generates — save as:

```
data/properties.json
```

Then share the **first 3 properties** here as a sample for schema validation before we start indexing.

---

## ✅ Quick Quality Check

- [ ] `review_highlights` sound like real traveler reviews — not just "Great hotel!"
- [ ] `description` is evocative, not a bullet list in prose form
- [ ] Different amenity combinations across properties (not the same 8 repeated)
- [ ] Vibe tags are from the approved list only
- [ ] IDs are sequential: `prop_001` → `prop_060`

