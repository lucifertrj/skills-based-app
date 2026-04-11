
# Booking.com AI Trip Planner - Case Study Implementation

## Overview
This repository contains the implementation and analysis from our case study on **Booking.com's AI-Powered Travel Platform**. This initiative focuses on understanding the AI-driven features that Booking.com built using OpenAI's models, including conversational trip planning, smart filters, property Q&A, and review summarization.

## Key Concepts from Booking.com's AI Implementation

Booking.com partnered with OpenAI to transform their travel platform with AI-powered features that enhance discovery, personalization, and user experience:

- **AI Trip Planner**: Conversational destination discovery and itinerary building using natural language prompts
- **Smart Filters**: Natural language understanding to map user requests to property filters beyond predefined options
- **Property Q&A**: AI-powered question answering about property details using fine-tuned models on user-generated content
- **AI Review Summaries**: Automated summarization of property reviews into key themes for faster decision-making
- **Help Me Reply**: Automated response generation for guest communications

> Original Booking.com Resources
- **OpenAI Case Study**: [Booking.com and OpenAI personalize travel at scale](https://openai.com/index/booking-com/)

## Before vibe coding: Initial files in the directory

```
├── asset
│   ├── 1_welcome.png
│   ├── 2_home.png
│   ├── 3_search_results.png
│   ├── 4_onboarding_questions.png
│   └── 5_setting_up_memory.png
└── context_agent
    ├── CONTEXT.md
    ├── PROMPT.md
    └── ROADMAP.md
```

## After vibe coded app, you will have frontend and backend, the instructions to setup:

### Prerequisites
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
```

### Setup the API Keys

> STRICT NOTE (since this is Google event demo): The memory layer i.e., Cognee uses OpenAI as default LLM and Embedding model, that is sole purpose we are using this while vibe coding but this can be changed to Gemini too. I have an example here: [cognee-101](https://github.com/lucifertrj/cognee-101). The app is vibe coded in Google Antigravity

- **OpenAI API Key**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Qdrant API Key**: [Qdrant Cloud](https://cloud.qdrant.io/)

```
cp .env.example .env
```

### Running the Application

```bash
# Index the data (run once)
python -m scripts.index_properties

# Start the backend
cd backend
uvicorn main:app --reload

# In another terminal, start the frontend
cd frontend
npm run dev
```

## Implementation Notes

This implementation is inspired by Booking.com's approach but adapted to our specific tech stack and use case. The focus is on understanding the core AI integration patterns and conversational travel assistance rather than replicating the exact infrastructure.

## License

This is a case study project for educational purposes only.

## Acknowledgments

- Booking.com and OpenAI for sharing insights on their AI collaboration
- Community contributors to the case study series
