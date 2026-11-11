AI Knowledge Assistant
An AI-powered knowledge assistant that allows users to upload documents, ask natural-language questions, and receive answers grounded in retrieved document content.

The project demonstrates practical implementation of Retrieval-Augmented Generation (RAG), REST API development, document processing, vector-based retrieval, and AI model integration.

Key Features
Document Management — Upload, list, retrieve, and delete documents.

Document Processing — Extract text from supported PDF and TXT files and prepare content for retrieval.

Semantic Retrieval — Generate embeddings and retrieve relevant document chunks for a user's question.

AI-Powered Q&A — Use retrieved context to generate answers with an LLM.

Source References — Return source document information and relevant content alongside answers.

Local AI Inference — Integrate with Ollama to run language and embedding models locally.

Automated Testing — Validate core application behaviour and API functionality.

Technology Stack
Layer	Technology
Frontend	Next.js, React, TypeScript
Backend	Python, FastAPI
Data Validation	Pydantic
Database	SQLite, SQLAlchemy
Embeddings	Ollama, nomic-embed-text
Language Model	Ollama, llama3.2
Testing	pytest
Architecture
The application follows a client-server architecture. The backend processes uploaded documents, stores document and embedding data, retrieves relevant content, and passes the retrieved context to the language model.

See the architecture diagram below.

Getting Started
Prerequisites
Python and pip

Node.js and npm

Ollama

The llama3.2 language model

The nomic-embed-text embedding model

1. Start Ollama
Install Ollama and download the required models:

ollama pull llama3.2
ollama pull nomic-embed-text
Ensure Ollama is running and accessible at:

http://localhost:11434

2. Configure the Backend
Navigate to the backend project directory. Create and activate a virtual environment:

```powershell
py -3.14 -m venv venv314
.\venv314\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Configure the local environment variables in .env:

LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434

Create or update the SQLite database schema before starting the backend:

```powershell
python create_tables.py
```

Start the FastAPI application using the project's actual application entry point. For example:

uvicorn app.main:app --reload
The API documentation should be available at:

http://127.0.0.1:8000/docs

Run the backend with Docker
---------------------------
From the backend directory, build and start the API:

```powershell
docker build -t enterprise-ai-backend .
docker run --name enterprise-ai-backend -p 8000:8000 `
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 `
  -v backend-data:/data `
  -v backend-uploads:/app/app/storage `
  enterprise-ai-backend
```

The container initializes the SQLite schema at startup. The named volumes
preserve the database and uploaded files when the container is removed. The
Ollama URL above assumes Ollama is running on the Windows host; change it if
Ollama is running elsewhere. The API docs are available at
http://localhost:8000/docs.

Run the frontend and backend with Docker Compose
------------------------------------------------
From the `src` directory, build and start both services:

```powershell
docker compose up --build
```

The frontend is available at http://localhost:3000, the API at
http://localhost:8000, and the API docs at http://localhost:8000/docs.
Compose waits for the backend health check before starting the frontend.
Ollama is expected to run on the host at
http://host.docker.internal:11434 by default; set `OLLAMA_BASE_URL` if it is
running elsewhere.

To run in the background, use `docker compose up --build -d`. View status and
logs with `docker compose ps` and `docker compose logs -f`; stop the services
with `docker compose down`. The named volumes preserve the SQLite database and
uploaded files. Avoid `docker compose down -v` unless you intend to delete
those data volumes.

For the local Kubernetes deployment and `kubectl` walkthrough, see
[the Kubernetes guide](../k8s/README.md).

3. Configure the Frontend
Navigate to the frontend directory:

npm install
Create .env.local:

NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
Start the development server:

npm run dev
Open http://localhost:3000 in your browser.

4. Run Tests
From the backend directory, install the development dependencies and run the test suite:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -v
```
API Endpoints
Method	Endpoint	Description
POST	/documents/upload	Upload a document
GET	/documents/all	List documents
GET	/documents/{document_id}	Retrieve a document
DELETE	/documents/{document_id}	Delete a document
POST	/chat	Ask a question and retrieve an answer with sources
Example: Ask a Question
Request:

{
  "question": "How many days of annual leave are provided?",
  "top_k": 3
}
Example response structure:

{
  "answer": "The annual leave entitlement is 30 days per year.",
  "sources": [
    {
      "document_id": 1,
      "chunk_id": 1,
      "filename": "employee_handbook.txt",
      "content": "The annual leave entitlement is 30 days per year.",
      "score": 0.85
    }
  ]
}
The response values above are illustrative; actual answers, document IDs, and retrieval scores depend on the uploaded content and retrieval results.

Design Considerations
Separation of concerns: API routes, business services, repositories, and AI provider integrations have distinct responsibilities.

Provider abstraction: Language model and embedding providers can be configured independently.

Context-grounded responses: Retrieved document content is supplied to the language model to support answers based on the knowledge base.

Local execution: Ollama supports local model inference without requiring a paid external LLM API key.

Future Improvements
Docker Compose deployment

Authentication and user-specific document access

Improved retrieval evaluation and relevance ranking

Streaming responses

More comprehensive automated tests

Production-ready logging, monitoring, and error handling

Project Status
The core application is implemented, and the current test suite has been reported to run successfully. Deployment packaging and further production hardening remain future improvements.

how to run the application 
1. cd .\src\backend\  
2. py -3.14 -m venv venv314
3. .\venv314\Scripts\Activate.ps1
4. python -m pip install -r requirements.txt
5. python create_tables.py
6. uvicorn app.main:app --reload

how to restart the application
1. cd .\src\backend\
2. .\venv314\Scripts\Activate.ps1
3. uvicorn app.main:app --reload