# Rag-Vector-Integration

RAG System with LangGraph, ChromaDB, and MCP Server
A production-ready Retrieval-Augmented Generation (RAG) system that loads documents into a vector database and provides intelligent question-answering capabilities through both REST API and Model Context Protocol (MCP) interfaces.

🌟 Features
Document Processing: Automatically loads and chunks PDF, DOCX, TXT, and Markdown files
Vector Search: ChromaDB-powered semantic search with persistent storage
RAG Pipeline: LangGraph-based workflow for context-aware question answering
Dual Interface:

REST API (FastAPI) for web applications
MCP Server for AI assistants like Claude Desktop

Multiple LLM Support: Works with Ollama (local/free), Claude, OpenAI, or Groq
Interactive Dashboard: Streamlit-based UI for exploring embeddings and querying documents

📋 Table of Contents

Architecture
Installation
Quick Start
Configuration
Usage
API Documentation
MCP Integration
Project Structure
Troubleshooting
Contributing
License

🏗️ Architecture
┌─────────────────────────────────────────────────────────┐
│ RAG SYSTEM │
├─────────────────────────────────────────────────────────┤
│ │
│ ┌────────────────┐ ┌─────────────────┐ │
│ │ FastAPI Server│ │ MCP Server │ │
│ │ (Port 8000) │ │ (stdio) │ │
│ └───────┬────────┘ └────────┬────────┘ │
│ │ │ │
│ └─────────────┬───────────────────┘ │
│ ↓ │
│ ┌──────────────────────────────┐ │
│ │ Shared Components │ │
│ ├──────────────────────────────┤ │
│ │ • DocumentLoader │ │
│ │ • ChromaVectorStore │ │
│ │ • RAGPipeline (LangGraph) │ │
│ │ • LLM Integration │ │
│ └──────────────────────────────┘ │
│ ↓ │
│ ┌──────────────────────────────┐ │
│ │ ChromaDB (Persistent) │ │
│ └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
🚀 Installation
Prerequisites

Python 3.9 or higher
pip package manager

Step 1: Clone the Repository
bashgit clone https://github.com/yourusername/rag-system.git
cd rag-system
Step 2: Create Project Structure
bashmkdir -p src/{loaders,embeddings,vector_db,rag,mcp,api}
mkdir -p {data,documents}
Step 3: Install Dependencies
bashpip install -r requirements.txt
Step 4: Set Up Environment Variables
Create a .env file in the project root:
bash# LLM Configuration (choose one)
LLM_PROVIDER=ollama # Options: ollama, anthropic, openai, groq

# API Keys (only for cloud providers)

ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
GROQ_API_KEY=gsk_your-key-here

# Database Configuration

CHROMA_DB_PATH=./chroma_db
DOCUMENTS_PATH=./documents

# Document Loading Behavior

AUTO_LOAD_DOCUMENTS=true
RELOAD_ON_STARTUP=false
Step 5: Install LLM (Choose One)
Option A: Ollama (Free, Local)
bash# Install Ollama

# macOS: brew install ollama

# Linux: curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from https://ollama.com/download

# Pull a model

ollama pull llama3.2

# Start Ollama service

ollama serve
Option B: Groq (Free, Cloud)

Sign up at https://console.groq.com
Get API key from https://console.groq.com/keys
Add to .env: GROQ_API_KEY=gsk_your_key_here

Option C: Anthropic Claude

Sign up at https://console.anthropic.com
Get $5 free credits
Generate API key
Add to .env: ANTHROPIC_API_KEY=sk-ant-your-key-here

⚡ Quick Start

1. Add Your Documents
   Place your documents in the ./documents folder:
   bashcp /path/to/your/documents/_.pdf ./documents/
   cp /path/to/your/documents/_.docx ./documents/
2. Start the FastAPI Server
   bashcd src/api
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   Access the API at: http://localhost:8000
3. (Optional) Start the MCP Server
   bash# In a separate terminal
   python main.py
4. Run Tests
   bashpython test_rag.py
5. Launch the Dashboard
   bashstreamlit run chromadb_dashboard.py
   Access the dashboard at: http://localhost:8501
   ⚙️ Configuration
   Environment Variables
   VariableDescriptionDefaultRequiredLLM_PROVIDERLLM to use (ollama/anthropic/openai/groq)ollamaNoANTHROPIC_API_KEYAnthropic API key-If using ClaudeOPENAI_API_KEYOpenAI API key-If using GPTGROQ_API_KEYGroq API key-If using GroqCHROMA_DB_PATHChromaDB storage location./chroma_dbNoDOCUMENTS_PATHDocuments directory./documentsNoAUTO_LOAD_DOCUMENTSAuto-load docs on startuptrueNo
   Supported Document Types

PDF (.pdf)
Microsoft Word (.docx)
Text files (.txt)
Markdown (.md)

📖 Usage
REST API Examples
Load Documents
bashcurl -X POST http://localhost:8000/load-documents \
 -H "Content-Type: application/json" \
 -d '{"directory": "./documents"}'
Query the RAG System
bashcurl -X POST http://localhost:8000/query \
 -H "Content-Type: application/json" \
 -d '{"question": "What is machine learning?"}'
Search Vector Database
bashcurl -X POST http://localhost:8000/search \
 -H "Content-Type: application/json" \
 -d '{"query": "neural networks", "n_results": 5}'
Check System Health
bashcurl http://localhost:8000/health
Python Client Example
pythonimport requests

# Query the system

response = requests.post(
"http://localhost:8000/query",
json={"question": "Explain transformers in NLP"}
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
Dashboard Features
The Streamlit dashboard provides:

Overview Tab: Statistics and source file distribution
Search Tab: Semantic search with similarity scores
Browse Tab: Paginated document browsing with filtering
Visualize Tab: 2D/3D embedding visualization using PCA

📡 API Documentation
Endpoints
MethodEndpointDescriptionGET/API informationGET/healthHealth checkPOST/load-documentsLoad documents into vector DBPOST/queryRAG query with LLMPOST/searchDirect vector search (no LLM)GET/browseBrowse stored documentsGET/sourcesList unique source filesGET/statsDatabase statisticsDELETE/clearClear vector database
Request/Response Examples
POST /query
Request:
json{
"question": "What are the benefits of RAG?"
}
Response:
json{
"answer": "RAG (Retrieval-Augmented Generation) provides several benefits...",
"sources": ["document1.pdf", "document2.txt"],
"num_docs_retrieved": 5
}
POST /search
Request:
json{
"query": "machine learning",
"n_results": 3
}
Response:
json{
"results": [
{
"content": "Machine learning is a subset of artificial intelligence...",
"metadata": {"source": "ml_intro.pdf", "page": 1},
"distance": 0.234
}
]
}
🔌 MCP Integration
Using with Claude Desktop

Install Claude Desktop from https://claude.ai/download
Configure MCP Server
Edit Claude Desktop config:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%/Claude/claude_desktop_config.json

json {
"mcpServers": {
"rag-system": {
"command": "python",
"args": ["/absolute/path/to/rag-system/main.py"],
"env": {
"LLM_PROVIDER": "ollama",
"CHROMA_DB_PATH": "/absolute/path/to/rag-system/chroma_db",
"DOCUMENTS_PATH": "/absolute/path/to/rag-system/documents"
}
}
}
}

```

3. **Restart Claude Desktop**

4. **Use the Tools** in Claude:
   - "Load documents from my project folder"
   - "Search for information about X in my documents"
   - "Answer this question based on my documents"

### Available MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `load_documents_to_vectordb` | Load documents into database | `directory` (string) |
| `search_documents` | Semantic search | `query` (string), `n_results` (int) |
| `rag_query` | Full RAG query with LLM | `question` (string) |
| `clear_vectordb` | Clear all documents | None |

## 📁 Project Structure
```

rag-system/
├── main.py # MCP server entry point
├── test_rag.py # API testing script
├── chromadb_dashboard.py # Streamlit dashboard
├── inspect_chromadb.py # Database inspection tool
├── requirements.txt # Python dependencies
├── .env # Environment configuration
├── README.md # This file
│
├── documents/ # Source documents (add yours here)
├── chroma_db/ # Vector database storage (auto-created)
│
└── src/ # Source code
├── loaders/
│ └── document_loader.py # Document loading and chunking
├── vector_db/
│ └── chroma_store.py # ChromaDB integration
├── rag/
│ └── rag_graph.py # LangGraph RAG pipeline
├── mcp/
│ └── server.py # MCP server implementation
└── api/
└── main.py # FastAPI application
🔧 Troubleshooting
Common Issues

1. "Module not found" errors
   bash# Ensure you're in the project root
   pip install -r requirements.txt
2. "Already running asyncio" error
   bashpip install nest-asyncio

# Or use the fixed main.py from the repository

3. ChromaDB not persisting data

Check CHROMA_DB_PATH in .env
Ensure write permissions for ./chroma_db/
Verify the directory exists

4. LLM connection issues
   Ollama:
   bash# Check if Ollama is running
   curl http://localhost:11434/api/tags

# Restart Ollama

ollama serve
API-based LLMs:

Verify API key in .env
Check credit balance
Ensure correct LLM_PROVIDER value

5. Document loading fails
   bash# Check document permissions
   ls -la ./documents/

# Test with a simple text file first

echo "Test document" > ./documents/test.txt
python -c "from src.loaders.document_loader import DocumentLoader; dl = DocumentLoader(); print(dl.load_documents('./documents'))"
Debugging Tools
Inspect ChromaDB
bashpython inspect_chromadb.py
Check API Health
bashcurl http://localhost:8000/health
View Logs
bash# FastAPI logs
cd src/api
uvicorn main:app --log-level debug

# MCP server logs

python main.py 2>&1 | tee mcp_server.log
🧪 Testing
Run All Tests
bashpython test_rag.py
Manual Testing
bash# 1. Load documents
curl -X POST http://localhost:8000/load-documents \
 -H "Content-Type: application/json" \
 -d '{"directory": "./documents"}'

# 2. Search

curl -X POST http://localhost:8000/search \
 -H "Content-Type: application/json" \
 -d '{"query": "test query", "n_results": 3}'

# 3. Query

curl -X POST http://localhost:8000/query \
 -H "Content-Type: application/json" \
 -d '{"question": "What is in the documents?"}'
🎨 Customization
Change Chunk Size
Edit src/loaders/document_loader.py:
pythonDocumentLoader(chunk_size=1500, chunk_overlap=300)
Change Embedding Model
Edit src/vector_db/chroma_store.py:
pythonSentenceTransformer("all-mpnet-base-v2") # Better quality, slower

# or

SentenceTransformer("all-MiniLM-L6-v2") # Faster, smaller
Add Custom Document Loaders
python# In src/loaders/document_loader.py
from langchain_community.document_loaders import UnstructuredHTMLLoader

# Add to \_load_file method

elif ext == '.html':
loader = UnstructuredHTMLLoader(file_path)
Change LLM Parameters
Edit src/rag/rag_graph.py:
pythonChatOllama(
model="llama3.2",
temperature=0.7, # Adjust creativity (0.0-1.0)
top_p=0.9
)
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Development Setup
bash# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests

pytest

# Format code

black src/
isort src/

# Lint

flake8 src/
📊 Performance
Benchmarks
Tested on MacBook Pro M1 (16GB RAM):
OperationTimeNotesLoad 100 documents~15sPDF + DOCX mixGenerate embeddings (100 chunks)~3sall-MiniLM-L6-v2Vector search (top 5)~50msFrom 10K documentsFull RAG query~2-5sDepends on LLM
Optimization Tips

Use smaller embedding models for faster indexing
Batch document loading for large collections
Adjust chunk size based on document type
Use Groq for fastest cloud inference
Use Ollama for no-cost local inference

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

LangChain for document processing
ChromaDB for vector storage
LangGraph for workflow orchestration
FastMCP for MCP server implementation
Anthropic for Claude and MCP protocol

📧 Contact

GitHub Issues: Create an issue
Email: ranadheer.sammeta@gmail.com , mitheshjain88@gmail.com
Twitter:

🗺️ Roadmap

Add support for more document types (HTML, CSV, JSON)
Implement document versioning
Add multi-language support
Create web-based UI
Add user authentication
Implement caching layer
Add monitoring and analytics
Support for multiple collections
Hybrid search (keyword + semantic)
Export/import functionality

Star ⭐ this repository if you find it helpful!
Built with ❤️ using LangChain, ChromaDB, and FastAPI Sonnet 4.5Claude is AI and can make mistakes. Please double-check responses.
