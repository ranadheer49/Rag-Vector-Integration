import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
sys.path.append('..')

from loaders.document_loader import DocumentLoader
from vector_db.chroma_store import ChromaVectorStore
from rag.rag_graph import RAGPipeline

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="RAG System API",
    description="Document retrieval and question answering using RAG pipeline",
    version="1.0.0"
)

# Get configuration from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")

# Validate API key if using cloud provider
if LLM_PROVIDER in ["anthropic", "openai", "groq"]:
    API_KEY = os.getenv(f"{LLM_PROVIDER.upper()}_API_KEY")
    if not API_KEY:
        raise ValueError(
            f"{LLM_PROVIDER.upper()}_API_KEY not found in environment variables. "
            f"Please set it in your .env file."
        )
else:
    API_KEY = None  # Local providers like Ollama don't need API key


# Initialize components
print("Initializing RAG System components...")
document_loader = DocumentLoader()
vector_store = ChromaVectorStore()
# Initialize RAG pipeline with environment-based configuration
rag_pipeline = RAGPipeline(
    vector_store=vector_store,
    llm_provider=LLM_PROVIDER,
    llm_api_key=API_KEY
)

class QueryRequest(BaseModel):
    question: str
    
class LoadRequest(BaseModel):
    directory: str

class SearchRequest(BaseModel):
    query: str
    n_results: int = 5

@app.post("/load-documents")
async def load_documents(request: LoadRequest):
    """Load documents from directory"""
    try:
        # docs = document_loader.load_documents(request.directory)
        docs = document_loader.load_documents('/Users/ranadheersammeta/Documents/GitHub/Rag-Vector-Integration/rag-system/documents')
        vector_store.add_documents(docs)
        
        return {
            "status": "success",
            "message": f"Loaded {len(docs)} document chunks"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_rag(request: QueryRequest):
    """Query the RAG system"""
    try:
        result = rag_pipeline.query(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_docs(request: SearchRequest):
    """Search vector database"""
    try:
        results = vector_store.search(request.query, request.n_results)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
async def clear_db():
    """Clear vector database"""
    try:
        vector_store.clear_collection()
        return {"status": "success", "message": "Database cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}