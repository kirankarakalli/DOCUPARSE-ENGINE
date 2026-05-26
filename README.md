# DocuParse Engine

AI-powered document intelligence platform built with FastAPI, OCR pipelines, LLM-based structured extraction, PostgreSQL storage, and RAG-powered document chat.

DocuParse Engine allows users to upload documents (PDFs/images), extract text using OCR, generate structured JSON using LLMs, validate outputs, store results in Postgres, and chat with uploaded documents using vector search.

---

## Features

✔ Multi-format document ingestion (PDF / Image / Text)

✔ OCR-based text extraction

✔ LLM-powered structured data extraction

✔ JSON Schema validation

✔ Background document processing

✔ PostgreSQL persistence layer

✔ Chroma vector indexing

✔ RAG-powered document chat

✔ REST APIs with Swagger/OpenAPI support

✔ Modular and extensible architecture

---

## System Architecture

```text
User Upload
    ↓
FastAPI API Layer
    ↓
File Storage
    ↓
OCR Pipeline
(pdf2image + Tesseract OCR)
    ↓
LLM Structured Extraction
(OpenAI)
    ↓
Validation Layer
(JSON Schema + Rule Validators)
    ↓
PostgreSQL Storage
    ↓
Chroma Vector Database
    ↓
RAG Chat API
```

---

## Tech Stack

### Backend

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### AI / NLP

- OpenAI API
- LangChain
- ChromaDB
- Retrieval-Augmented Generation (RAG)

### OCR & Document Processing

- Tesseract OCR
- pdf2image
- Pillow

### Database

- PostgreSQL

---

## Project Structure

```text
app/
│
├── api/
├── services/
├── models/
├── schemas/
├── database/
├── GenAI/
├── utils/
├── uploads/
│
├── main.py
│
config/
├── configuration.py
│
params.yaml
requirements.txt
README.md
```

---

## Processing Pipeline

### 1. Document Upload

Users upload files through:

```http
POST /api/uploadfile
```

Supported formats:

- PDF
- PNG
- JPG
- JPEG
- TXT
- DOC
- DOCX

---

### 2. OCR & Text Extraction

#### PDF Processing

PDF pages are converted into images using `pdf2image`, then OCR is performed on each page.

#### Image Processing

Images are preprocessed and passed through Tesseract OCR.

---

### 3. LLM Structured Extraction

Extracted text is sent to the OpenAI API to generate structured JSON output.

Example output:

```json
{
  "document_type": "invoice",
  "confidence_score": 0.93,
  "data": {
    "document_number": "INV-1024",
    "date": "2026-05-21",
    "total_amount": 2450.75,
    "vendor_or_party": "ABC Pvt Ltd",
    "currency": "INR"
  }
}
```

---

### 4. Validation Layer

Validation includes:

- Document-type validators
- JSON Schema validation
- Structured field checks
- Error handling for malformed LLM outputs

---

### 5. Persistence Layer

Processed results are stored in PostgreSQL.

#### Tables

**documents**

Stores:

- Upload metadata
- File path
- Processing status
- Timestamps

**document_content**

Stores:

- OCR extracted text
- Structured JSON output
- Validation output

---

### 6. Vector Indexing & RAG Chat

Extracted text is indexed into Chroma for semantic retrieval.

Users can chat with uploaded documents using:

```http
POST /api/chat
```

Example questions:

- What is the invoice amount?
- Summarize the contract.
- What is the due date?
- What are the payment terms?

---

## API Endpoints

| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | `/home` | Health check |
| POST | `/api/uploadfile` | Upload document |
| GET | `/api/documents/{document_id}` | Get document status |
| GET | `/api/docuemnts` | List all documents |
| POST | `/api/chat` | RAG chat |

**Note:** `/api/docuemnts` contains a typo in the current implementation.

---

## Installation

### Clone Repository

```bash
git clone <your_repo_url>
cd DocuParse-Engine
```

### Create Virtual Environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

### `.env`

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

### `params.yaml`

```yaml
uploads_dir: "./uploads"

allowed_extensions:
  - jpg
  - jpeg
  - png
  - pdf
  - txt
  - doc
  - docx

max_file_size_bytes: 10485760

database_url: "postgresql://postgres:password@localhost:5432/docuparse_db"

host: "localhost"
port: 8000
```

---

## OCR Dependencies

### Tesseract OCR

Windows:

Install Tesseract and add it to PATH.

Linux:

```bash
sudo apt install tesseract-ocr
```

### Poppler

Required for PDF rendering.

Windows:

Install Poppler and add `/bin` to PATH.

Linux:

```bash
sudo apt install poppler-utils
```

---

## Running the Application

### Option 1

```bash
python app/main.py
```

### Option 2 (Recommended)

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

---

## Usage Examples

### Upload Document

```bash
curl -X POST "http://localhost:8000/api/uploadfile" \
-H "accept: application/json" \
-F "file=@document.pdf"
```

Response:

```json
{
  "upload_id": "UUID-HERE",
  "stored_filename": "UUID-HERE.pdf",
  "size_in_bytes": 12345,
  "status": "uploaded"
}
```

### Fetch Document Status

```bash
curl "http://localhost:8000/api/documents/UUID-HERE"
```

### Chat with Documents

```bash
curl -X POST "http://localhost:8000/api/chat" \
-H "content-type: application/json" \
-d '{
"question":"What is the total amount?",
"session_id":"demo",
"document_id":["UUID-HERE"]
}'
```

---

## Engineering Challenges Solved

- OCR handling across PDFs and images
- Structured extraction from unstructured documents
- Validation of inconsistent LLM outputs
- Semantic retrieval using vector databases
- Multi-stage AI pipeline orchestration
- Async/background document processing
- Cross-platform compatibility handling

---

## Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Layout-aware extraction (LayoutLM)
- Multi-query RAG
- RAG Fusion
- Docker deployment
- CI/CD integration
- Streaming chat responses
- Authentication & RBAC
- Extraction evaluation framework

---

## Known Issues

### Schema Alignment

Current LLM output nests extracted fields under:

```json
{
  "data": {}
}
```

Some validators currently expect top-level fields.

### Route Typo

Current implementation uses:

```text
/api/docuemnts
```

---

## Performance Notes

- Supports multi-page PDF processing
- Background task execution
- Semantic vector retrieval
- Supports files up to 10MB
- Modular architecture for scalability

---

## Author

Built as an end-to-end AI document intelligence system combining:

- OCR
- LLM orchestration
- RAG pipelines
- Backend engineering
- AI system design

---

## License

MIT License