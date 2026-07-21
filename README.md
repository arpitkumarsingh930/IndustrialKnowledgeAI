# Industrial Knowledge AI

**A Unified Asset & Operations Brain for asset-intensive industries.**

Industrial Knowledge AI ingests heterogeneous industrial documents — equipment manuals, maintenance reports, inspection records, engineering docs — and turns them into a single, queryable intelligence layer. Ask operational questions in plain English and get precise, source-grounded answers, powered by **hybrid retrieval that fuses semantic vector search with a knowledge graph**.

---

## Why

In asset-heavy industries, critical knowledge is scattered across disconnected systems — P&IDs in one place, work orders in another, manuals and inspection reports elsewhere. Engineers lose hours hunting for information that already exists, and decades of operational expertise walk out the door as experienced staff retire. This project consolidates that fragmented knowledge into one brain that is instant to query, grounded in source documents, and built to scale.

---

## Key Features

- **Universal document ingestion** — upload a PDF; the system extracts, chunks, embeds, and indexes it automatically.
- **Semantic search (RAG)** — questions are matched against document meaning, not just keywords, using sentence-transformer embeddings in a vector store.
- **Knowledge graph** — entities and their relationships are extracted into Neo4j, enabling reasoning *across* documents, not just within one.
- **Hybrid retrieval** — every question runs vector search **and** a graph lookup; both contexts are fused before answer generation. Vectors give recall; the graph gives relationships.
- **Grounded answers** — a large language model (Google Gemini) generates the final answer strictly from retrieved context.
- **Clean web UI** — upload documents and chat with your knowledge base from the browser.

---

## Architecture

A three-tier system with a decoupled AI microservice.

```
┌──────────────┐     upload PDF      ┌─────────────────────┐
│   Frontend   │ ──────────────────▶ │   Backend (Java)    │
│ React + Vite │                     │    Spring Boot      │
│              │ ◀───── answer ───── │                     │
└──────┬───────┘                     │  • PDFBox extract   │
       │                             │  • Text chunking    │
       │  ask question               │  • PostgreSQL store │
       │  (POST /ask)                └──────────┬──────────┘
       │                                        │ POST /process
       ▼                                        ▼
┌───────────────────────────────────────────────────────────┐
│                 AI Service (Python · FastAPI)              │
│                                                           │
│   Ingestion:  chunk ──▶ embed (MiniLM) ──▶ ChromaDB       │
│               chunk ──▶ spaCy NER ──────▶ Neo4j graph     │
│                                                           │
│   Query:      question ──▶ vector search (ChromaDB)  ┐    │
│               question ──▶ graph lookup (Neo4j)      ├─▶  │
│               fused context ──▶ Gemini ──▶ answer    ┘    │
└───────────────────────────────────────────────────────────┘
```

### Ingestion flow
1. User uploads a PDF from the React frontend.
2. Spring Boot receives the file, extracts text with **Apache PDFBox**, and splits it into overlapping chunks (1000 chars, 200 overlap).
3. Document metadata and chunks are saved to **PostgreSQL**.
4. Chunks are forwarded to the FastAPI service (`POST /process`).
5. Each chunk is embedded with **all-MiniLM-L6-v2** and stored in **ChromaDB**; entities are extracted with **spaCy** and written into a **Neo4j** knowledge graph.

### Query flow
1. User asks a question from the chat UI (`POST /ask`).
2. The question is embedded and matched against ChromaDB (top-k vector search).
3. Entities in the question are extracted with spaCy and looked up in Neo4j.
4. Vector context + graph context are fused into a single prompt.
5. **Google Gemini** generates a grounded answer, returned to the UI.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS, Axios |
| Backend | Java, Spring Boot, Apache PDFBox, Spring Data JPA |
| AI Service | Python, FastAPI, Uvicorn |
| Embeddings | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| Vector DB | ChromaDB |
| Knowledge Graph | Neo4j |
| Entity Extraction | spaCy (`en_core_web_sm`) |
| LLM | Google Gemini |
| Relational DB | PostgreSQL |

---

## Project Structure

```
IndustrialKnowledgeAI/
├── ai-service/                 # Python FastAPI AI microservice
│   └── app/
│       ├── api.py              # FastAPI app: /process and /ask endpoints
│       ├── services.py         # Ingestion pipeline (embed + extract + store)
│       ├── embedder.py         # Sentence-transformer embeddings
│       ├── vector_db.py        # ChromaDB store + search
│       ├── entity_extractor.py # spaCy NER + relationship extraction
│       ├── neo4j_service.py    # Write entities/relationships to Neo4j
│       ├── query.py            # Graph lookup for a given entity
│       ├── retriever.py        # Vector retrieval wrapper
│       ├── gemini_service.py   # Gemini answer generation
│       ├── models.py           # SQLAlchemy models
│       └── database.py         # DB session
│
├── backend/                    # Java Spring Boot ingestion backend
│   └── src/main/java/com/industrial/backend/
│       ├── controller/DocumentController.java   # /api/documents/upload
│       ├── service/DocumentService.java         # Orchestration
│       ├── util/PdfExtractor.java               # PDFBox text extraction
│       ├── ai/TextChunker.java                  # Chunking (1000/200)
│       ├── entity/ · repository/ · dto/ · config/
│       └── resources/application.properties
│
└── frontend/                   # React + Vite web app
    └── src/
        ├── App.jsx
        ├── components/          # UploadBox, ChatBox, Message, Navbar, Loader
        └── services/api.js
```

---

## Getting Started

### Prerequisites
- **Java 17+** and Maven (the project includes the Maven wrapper `mvnw`)
- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL** running locally
- **Neo4j** running locally
- A **Google Gemini API key**

### 1. Databases

**PostgreSQL** — create the database used by both the backend and the AI service:
```sql
CREATE DATABASE industrial_ai;
```
Default credentials expected by the code are user `postgres` / password `1234` on `localhost:5432`. Update them in `backend/src/main/resources/application.properties` and `ai-service/app/database.py` if yours differ.

**Neo4j** — start a local instance. The code connects to `bolt://127.0.0.1:7687` with user `neo4j` / password `12345678`. Update these in `ai-service/app/neo4j_service.py` and `graph_retriever.py` if yours differ.

### 2. AI Service (FastAPI)
```bash
cd ai-service

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# install dependencies
pip install fastapi uvicorn sentence-transformers chromadb spacy neo4j \
            google-genai python-dotenv sqlalchemy psycopg2-binary pydantic

# download the spaCy English model
python -m spacy download en_core_web_sm
```

Create a `.env` file in `ai-service/`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Run the service:
```bash
uvicorn app.api:app --reload --port 8000
```
The API is now at `http://127.0.0.1:8000`.

> Tip: create a `requirements.txt` from your environment (`pip freeze > requirements.txt`) so the install step becomes `pip install -r requirements.txt`.

### 3. Backend (Spring Boot)
```bash
cd backend
./mvnw spring-boot:run             # Windows: mvnw.cmd spring-boot:run
```
The backend starts on `http://localhost:8080`.

### 4. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
The app runs on `http://localhost:5173`.

---

## Usage

1. Open `http://localhost:5173`.
2. In the **Upload** panel, select an industrial PDF (equipment manual, maintenance report, inspection doc) and upload it. Wait for the success confirmation.
3. In the **Ask** panel, type an operational question, e.g. *"What is the recommended maintenance interval for the pump?"*
4. The system retrieves relevant context from both the vector store and the knowledge graph, and returns a grounded answer.

---

## API Reference

### Backend (Spring Boot · `http://localhost:8080`)

**`POST /api/documents/upload`** — upload and ingest a document.
- Body: `multipart/form-data` with field `file` (PDF)
- Returns: the saved document record. Triggers extraction, chunking, storage, and forwarding to the AI service.

### AI Service (FastAPI · `http://127.0.0.1:8000`)

**`GET /`** — health check.

**`POST /process`** — index chunks (called by the backend).
```json
{ "documentId": 1, "chunks": ["chunk text 1", "chunk text 2"] }
```

**`POST /ask`** — ask a question against the knowledge base.
```json
{ "question": "What is the recommended maintenance interval?" }
```
Returns:
```json
{ "question": "...", "answer": "..." }
```

---

## Roadmap

- Source citations and confidence scores on every answer.
- Domain-specific industrial ontology for richer, higher-precision graph relationships.
- OCR support for scanned drawings and P&IDs.
- Predictive maintenance and compliance-gap detection built on top of the knowledge graph.
- Multi-format ingestion beyond PDF (spreadsheets, emails, CAD exports).

---

## Notes

- The `backend/uploads/` folder and `ai-service/chroma_db/` are runtime artifacts. Consider adding them to `.gitignore` so uploaded files and local vector data are not committed.
- Ports, database credentials, and the Gemini model name are currently set in code/config; move them to environment variables for production.

---

## License

Add a license of your choice (e.g. MIT) here.
