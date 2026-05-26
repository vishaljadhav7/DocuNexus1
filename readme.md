# DocuNexus ([Demo](https://drive.google.com/file/d/1vF_VEiksUj3EZwPh__EMlnwX2eOQLgD4/view))

Upload a PDF contract, ask questions about it in plain English, and get a structured AI-powered analysis — risks, opportunities, key clauses, financial terms, and more.

---

## Features

- **PDF Upload & Async Processing** — Upload a contract; the system parses, chunks, and summarizes it in the background via Celery. The upload endpoint returns immediately.
- **RAG-powered Querying** — Ask questions against your document. Answers are grounded strictly in retrieved chunk context — not generic LLM output.
- **Contract Analysis** — Generates a structured analysis covering contract type, overall score, risks, opportunities, key clauses, legal compliance, negotiation points, financial terms, and compensation structure.
- **Secure Auth** — JWT access/refresh token pair. Sign-out is immediately effective via Redis JTI blacklist.

---

## Tech Stack

### Backend
| | |
|---|---|
| **FastAPI** | Async Python API framework — ASGI-native, Pydantic validation at the boundary, composable dependency injection |
| **PostgreSQL** | Primary datastore — relational schema with JSONB for chunk metadata and contract insights |
| **SQLAlchemy 2.0** | Async ORM (`asyncpg` driver), `lazy="noload"` on all relationships to prevent implicit queries |
| **Alembic** | Versioned async database migrations |
| **Celery + Redis** | Background task queue for document processing pipeline; Redis also handles token blacklisting and refresh token storage |
| **Google Gemini** | LLM (`gemini-2.5-flash-lite`) for summarization and contract analysis; embeddings (`text-embedding-004`, 768 dimensions) |
| **Pinecone** | Managed vector database for semantic chunk retrieval |
| **Cloudinary** | Cloud storage for uploaded PDFs |
| **Unstructured.io** | PDF parsing and chunking |

### Frontend
| | |
|---|---|
| **React 19 + TypeScript** | UI layer, built and bundled with Vite |
| **Redux Toolkit** | Global client state — authenticated user identity and access token via `userSlice` |
| **RTK Query** | Server cache layer — request deduplication, tag-based surgical cache invalidation, automatic Bearer token injection via `prepareHeaders` |
| **React Router v7** | Client-side routing with `ProtectedRoute` and `RedirectRoute` guard components |
| **Tailwind CSS v4** | Utility-first styling |
| **shadcn/ui + Radix UI** | Accessible component primitives |
| **React Hook Form + Zod** | Form state management with schema validation |
| **Framer Motion** | Animations |

---

## Getting Started

### Prerequisites
- Python 3.11+, PostgreSQL, Redis
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) package manager

### Backend Setup

```bash
cd server
uv sync

cp .env.example .env
# Fill in environment variables (see below)

alembic upgrade head
uvicorn app.main:app --reload --port 8000

# In a separate terminal
celery -A app.celery_app worker --loglevel=info --pool=solo
```

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

### Environment Variables

```env
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=postgresql+asyncpg://user:password@localhost/docunexus
REDIS_URL=redis://localhost:6379/0
REDIS_PREFIX=docunexus:

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash-lite
GEMINI_EMBEDDING_MODEL=text-embedding-004

PINECONE_API_KEY=
PINECONE_INDEX_NAME=
PINECONE_ENVIRONMENT=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
REDIS_PREFIX_CELERY=celery:

CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

---

## API Reference

### Auth — `/api/v1`

#### `POST /sign_up`
Register a new user.
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!"
}
```
Returns `UserResponse` with `201`.

---

#### `POST /sign_in`
Sign in. Returns access token in body; sets `refresh_token` as an `HttpOnly` cookie scoped to `/api/v1/refresh`.
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```
Returns `UserSignInResponse`:
```json
{
  "id": "...",
  "email": "...",
  "username": "...",
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 900,
  "created_at": "..."
}
```

---

#### `POST /sign_out`
Revoke access token. Requires `Authorization: Bearer <token>`. Clears the refresh token cookie.

---

#### `POST /refresh`
Rotate token pair using the `refresh_token` cookie. Returns a new `access_token`.

---

#### `GET /me`
Returns the authenticated user's profile.

---

### Documents — `/api/v1/documents`

All document routes require `Authorization: Bearer <token>`.

#### `POST /`
Upload a PDF. Accepts `multipart/form-data` with field `doc_file`.

Returns `DocumentUploadResponse`:
```json
{
  "document_id": "...",
  "filename": "contract.pdf",
  "cloudinary_url": "...",
  "processing_status": "uploaded",
  "insights_available": false,
  "created_at": "...",
  "message": "..."
}
```

---

#### `GET /`
List all documents for the authenticated user. Returns `DocumentListResponse`.

---

#### `GET /{document_id}`
Get a single document's details. Returns `DocumentListItem`.

---

#### `GET /{document_id}/status`
Poll document processing status. Returns:
```json
{
  "document_id": "...",
  "processing_status": "processing | completed | failed",
  "error_message": null
}
```

---

#### `POST /{document_id}/analyze`
Generate structured contract insights. Document must have `processing_status: completed`. Idempotent — returns `400` if insights already exist.

Returns `ContractAnalysisResponse`:
```json
{
  "document_id": "...",
  "insights": {
    "contract_type": "Employment",
    "overall_score": 74,
    "summary": "...",
    "risks": [{ "risk": "...", "risk_details": "...", "severity": "HIGH" }],
    "opportunities": [{ "opportunity": "...", "opportunity_details": "...", "impact": "MEDIUM" }],
    "recommendations": ["..."],
    "key_clauses": ["..."],
    "legal_compliance": "...",
    "negotiation_points": ["..."],
    "contract_duration": "...",
    "termination_conditions": "...",
    "financial_terms": { "description": "...", "details": ["..."] },
    "compensation_structure": { "base_salary": "...", "bonuses": null, "equity": null, "other_benefits": null },
    "performance_metrics": ["..."]
  }
}
```

---

#### `DELETE /{document_id}`
Delete a document and all associated chunks, queries, and insights.

---

### Queries — `/api/v1/contracts`

#### `POST /queries`
Submit a natural language question against a document.
```json
{
  "query_text": "What are the termination conditions?",
  "document_id": "..."
}
```
Returns `QueryResponseDTO`:
```json
{
  "id": "...",
  "query_text": "...",
  "response_text": "...",
  "confidence_score": null,
  "created_at": "..."
}
```

---

#### `GET /queries?document_id={id}`
Fetch all queries for a document, ordered by most recent.

---

## Project Structure

```
server/
├── app/
│   ├── api/v1/          # Route handlers (auth, document, query)
│   ├── services/        # Business logic
│   ├── repositories/    # Database access layer
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic request/response models
│   ├── tasks/           # Celery background tasks
│   ├── core/            # Config, database, exceptions, middleware
│   └── utils/           # Prompts and helpers
└── alembic/             # Database migrations

client/
├── src/
│   ├── app-store/       # Redux store, userSlice, RTK Query API slice
│   ├── components/      # UI components (shadcn/ui based)
│   ├── pages/           # Route-level page components
│   └── routes/          # Router config with guard components
```

---

## Interactive Docs

`http://localhost:8000/docs` — Swagger UI auto-generated by FastAPI.

