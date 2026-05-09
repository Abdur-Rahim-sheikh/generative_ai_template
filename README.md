# Generative AI Backend

Production-ready multimodal AI backend featuring LLM, image generation, and TTS. Built with **FastAPI**, **PostgreSQL**, **Redis**, and **ARQ**.

## Highlights

### Architecture Patterns

- **Clean Architecture** — Layered design with interfaces, services, repositories, and schemas
- **Dependency Injection** — Centralized service initialization for testability
- **Unit of Work Pattern** — Transaction management across data layers
- **Async-First** — Non-blocking FastAPI endpoints with background job processing

### Database & Data

- **Redis** — In-memory caching and persistent job queue
- **Repository Pattern** — Abstract data access layer with CRUD operations
- **Pydantic Schemas** — Type-safe request/response validation

### AI Integration

- **Ollama LLM** — Local text generation with abstract base interface
- **ComfyUI** — Image diffusion with dynamic workflow generation
- **Coqui TTS** — Text-to-speech service integration
- **Service Abstraction** — Swappable implementations for any AI provider

### Asynchronous Processing

- **ARQ Queue** — Background job workers for long-running tasks
- **Immediate Responses** — API endpoints return job IDs without blocking
- **Batch Processing** — Handle multiple concurrent image generations
- **Job Persistence** — Redis-backed queue survives worker restarts

---

## Project Structure

```
.
├── config/          # Settings, logging, connections
├── data/            # External service clients (Ollama, ComfyUI, Coqui, Redis)
├── domain/          # Core business entities
├── interfaces/      # Abstract contracts (BaseRepository, BaseLLM, BaseTTS)
├── dependencies/    # Dependency injection & initialization
├── repositories/    # Data access layer (Unit of Work)
├── services/        # Business logic (Chat, Product, TTS, Workflow)
├── schemas/         # Pydantic validation (Chat, Image, User, Product)
├── entrypoints/     # API routes & ARQ workers
├── utils/           # Decorators, image processing, watermarking
├── tests/           # Unit tests with dummy mocks
└── main.py          # FastAPI application entry point
```

---

## API Endpoints

```
POST /api/llm/generate          → Text generation
POST /api/diffusion/generate    → Image generation (async)
POST /api/tts/generate          → Text-to-speech
GET  /api/jobs/{job_id}         → Check job status

Also, CRUD endpoints in progress.
```

---

## Tech Stack

| Layer                | Technology              |
| -------------------- | ----------------------- |
| **API Framework**    | FastAPI (async)         |
| **Database**         | PostgreSQL              |
| **Cache/Queue**      | Redis + ARQ             |
| **Data Validation**  | Pydantic                |
| **LLM**              | Ollama                  |
| **Image Generation** | ComfyUI                 |
| **Text-to-Speech**   | Coqui TTS               |
| **Deployment**       | Docker + Docker Compose |

<!-- | **Testing**          | pytest + mock fixtures  | -->

## Quick Start

```bash
# Environment setup
cp .env.example .env # fill the env values with example values

# Run with Docker
docker compose up -d
# or if not enough gpu resources
# docker compose -f dummy-compose.yml up -d

# API docs
open http://localhost:8000/docs
```

---

## Sample Output

This mug of mine was interpolated by one of my ComfyUI workflows, and placed it in this beautiful background.

<p align="center">
<img src="resources/images/reference_cup.png" alt="Generated via ComfyUI" width="400" height="400"/>
</p>

---
