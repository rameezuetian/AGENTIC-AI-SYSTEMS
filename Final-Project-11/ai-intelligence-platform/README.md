# AI Intelligence Platform

An advanced AI-powered conversational platform built with LangGraph, FastAPI, and React. This system integrates multiple AI capabilities including intelligent agents, memory persistence, RAG (Retrieval-Augmented Generation), streaming responses, and MCP (Model Context Protocol) server integration.

## 🎯 Features

- **Intelligent Chat Interface** - Real-time conversational AI with Google Gemini integration
- **Streaming Responses** - Progressive response delivery for better UX
- **Memory System** - Persistent short-term and long-term memory for context awareness
- **Session Management** - Track and manage multiple chat sessions
- **Document Upload & Processing** - Upload and process documents for RAG
- **Vector Search** - Semantic search across documents using Chroma vectorstore
- **Agent Workflows** - LangGraph-based agentic workflows with tool integration
- **MCP Server Integration** - File operations and search capabilities via Model Context Protocol
- **Safety & Guardrails** - Input validation and response filtering

## 🏗️ Architecture

### Tech Stack

**Backend:**
- FastAPI - High-performance Python web framework
- LangChain & LangGraph - AI orchestration and agent workflows
- Google Gemini API - LLM backbone
- Chroma - Vector database for semantic search
- FAISS - In-memory vector search
- SQLAlchemy - Database ORM
- MCP (Model Context Protocol) - Tool integration

**Frontend:**
- React 19 - UI framework
- Vite - Build tool and dev server
- Modern JavaScript/CSS

## 📁 Project Structure

```
ai-intelligence-platform/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and settings
│   ├── requirements.txt         # Python dependencies
│   ├── agents/                 # Agentic workflows
│   ├── api/                    # API endpoints
│   │   ├── chat.py            # Chat endpoint
│   │   ├── chat_stream.py      # Streaming chat endpoint
│   │   ├── memory.py          # Memory management
│   │   ├── sessions.py        # Session management
│   │   └── upload.py          # Document upload
│   ├── graph/                  # LangGraph workflow definitions
│   ├── mcp/                    # MCP server integrations
│   │   ├── client.py          # MCP client helpers
│   │   ├── file_server.py     # File operations server
│   │   └── search_server.py   # Document search server
│   ├── memory/                 # Memory storage and management
│   ├── rag/                    # RAG components and retrieval
│   ├── safety/                 # Safety checks and guardrails
│   ├── services/               # Business logic services
│   ├── logs/                   # Application logs
│   ├── uploads/                # Uploaded documents storage
│   └── vectorstore/            # Vector database storage
│
└── frontend/
    ├── src/                    # React source code
    ├── public/                 # Static assets
    ├── index.html              # HTML entry point
    ├── vite.config.js          # Vite configuration
    ├── package.json            # NPM dependencies
    └── eslint.config.js        # ESLint configuration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- pip/npm
- Google API Key for Gemini API

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd ai-intelligence-platform/backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Create a `.env` file in the backend directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
CHROMA_DB_DIR=./vectorstore
UPLOAD_DIR=./uploads
LOG_DIR=./logs
```

5. **Run the backend server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd ai-intelligence-platform/frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run development server:**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 📡 API Endpoints

### Chat & Conversation
- `POST /api/chat` - Send a message and get a response
- `POST /api/chat/stream` - Get streaming response
- `POST /api/sessions` - Create new session
- `GET /api/sessions/{session_id}` - Get session details
- `GET /api/sessions` - List all sessions

### Memory & Context
- `GET /api/memory/{session_id}` - Get session memory
- `POST /api/memory/{session_id}` - Update session memory
- `DELETE /api/memory/{session_id}` - Clear session memory

### Document Management
- `POST /api/upload` - Upload document
- `GET /api/documents` - List uploaded documents
- `DELETE /api/documents/{doc_id}` - Delete document

### System
- `GET /` - Health check
- `GET /api/status` - System status (includes Gemini connectivity)

## 🔧 Core Components

### Agents (`agents/`)
LangGraph-based agent workflows that orchestrate complex tasks with tool integration and memory management.

### API Routes (`api/`)
FastAPI routes for:
- Chat interactions
- Streaming responses
- Session management
- Memory operations
- Document uploads

### Graph (`graph/`)
LangGraph workflow definitions for agentic behavior and conversation flow.

### Memory System (`memory/`)
- Session-based conversation history
- Persistent memory store
- Context window management

### RAG System (`rag/`)
- Document ingestion and chunking
- Vector embeddings
- Semantic search and retrieval

### MCP Integration (`mcp/`)
- **client.py**: MCP client connection management
- **file_server.py**: File read/write operations
- **search_server.py**: Document search capabilities

### Safety (`safety/`)
Input validation, prompt injection detection, and response filtering.

## 📊 Data Flow

```
User Input
    ↓
API Endpoint
    ↓
Safety Checks
    ↓
Session Context + Memory
    ↓
LangGraph Agent
    ↓
Tool Calls (File/Search via MCP)
    ↓
LLM (Google Gemini)
    ↓
Response Processing
    ↓
Memory Update
    ↓
Stream/Return to Frontend
```

## 🔐 Security

- CORS middleware for cross-origin requests
- Path validation for file operations
- Input sanitization
- Environment variable management
- API error handling

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📝 Configuration

### Environment Variables

**Backend (`backend/.env`):**
```env
GOOGLE_API_KEY=your_key_here
CHROMA_DB_DIR=./vectorstore
UPLOAD_DIR=./uploads
LOG_DIR=./logs
```

### Main Settings (`backend/config.py`)
- `google_api_key` - Gemini API authentication
- `chroma_db_dir` - Vector store location
- `upload_dir` - Document upload directory
- `log_dir` - Log file directory
- `memory_store_file` - Persistent memory storage
- `session_store_file` - Session data storage

## 📚 Dependencies

### Backend
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `langchain` & `langchain-core` - AI orchestration
- `langgraph` - Agent workflows
- `langchain-google-genai` - Gemini integration
- `chromadb` - Vector database
- `faiss-cpu` - Vector search
- `mcp` - Model Context Protocol
- `pydantic` - Data validation
- `sqlalchemy` - ORM

### Frontend
- `react` - UI framework
- `react-dom` - DOM rendering
- `vite` - Build tool

## 🚦 Running the Full Stack

### Terminal 1 - Backend
```bash
cd ai-intelligence-platform/backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
cd ai-intelligence-platform/frontend
npm run dev
```

Access the application at `http://localhost:5173`

## 🔍 Debugging

### Backend Logs
Check `backend/logs/` directory for detailed logs.

### Frontend Dev Tools
Open browser DevTools (F12) for console and network inspection.

### API Testing
Use tools like Postman, curl, or the built-in OpenAPI docs:
- FastAPI Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📈 Performance Optimization

- Streaming responses for long-running operations
- Memory caching for frequently accessed data
- Vector store indexing for fast semantic search
- Session-based context for reduced processing

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

Proprietary - Internal Use Only

## 📞 Support

For issues and questions:
1. Check the logs in `backend/logs/`
2. Review API documentation at `/docs`
3. Verify environment configuration
4. Check backend/frontend console for errors

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

**Last Updated:** 2026-06-12  
**Version:** 1.0.0
