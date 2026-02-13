from fastmcp import FastMCP
from pathlib import Path
import json

mcp = FastMCP("Document RAG Server")

# Global state for vector store and RAG pipeline
vector_store = None
rag_pipeline = None
document_loader = None

@mcp.tool()
def load_documents_to_vectordb(directory: str) -> str:
    """Load all documents from directory into vector database"""
    global vector_store, document_loader
    
    try:
        docs = document_loader.load_documents(directory)
        vector_store.add_documents(docs)
        
        return f"Successfully loaded {len(docs)} document chunks from {directory}"
    except Exception as e:
        return f"Error loading documents: {str(e)}"

@mcp.tool()
def search_documents(query: str, n_results: int = 5) -> str:
    """Search for relevant documents in the vector database"""
    global vector_store
    
    try:
        results = vector_store.search(query, n_results=n_results)
        
        output = []
        for i, result in enumerate(results, 1):
            output.append(f"\n--- Result {i} ---")
            output.append(f"Source: {result['metadata'].get('source', 'Unknown')}")
            output.append(f"Content: {result['content'][:200]}...")
            output.append(f"Distance: {result['distance']:.4f}")
        
        return "\n".join(output)
    except Exception as e:
        return f"Error searching: {str(e)}"

@mcp.tool()
def rag_query(question: str) -> str:
    """Query the RAG system with a question"""
    global rag_pipeline
    
    try:
        result = rag_pipeline.query(question)
        
        output = [
            "=== Answer ===",
            result["answer"],
            "\n=== Sources ===",
            "\n".join(f"- {src}" for src in result["sources"]),
            f"\n(Retrieved {result['num_docs_retrieved']} documents)"
        ]
        
        return "\n".join(output)
    except Exception as e:
        return f"Error in RAG query: {str(e)}"

@mcp.tool()
def clear_vectordb() -> str:
    """Clear all documents from the vector database"""
    global vector_store
    
    try:
        vector_store.clear_collection()
        return "Vector database cleared successfully"
    except Exception as e:
        return f"Error clearing database: {str(e)}"

def initialize_mcp(vs, rag, loader):
    """Initialize MCP server with dependencies"""
    global vector_store, rag_pipeline, document_loader
    vector_store = vs
    rag_pipeline = rag
    document_loader = loader