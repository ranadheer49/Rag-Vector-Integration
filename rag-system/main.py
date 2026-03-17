# main.py (ROOT LEVEL)
import asyncio
import os
from dotenv import load_dotenv
from src.loaders.document_loader import DocumentLoader
from src.vector_db.chroma_store import ChromaVectorStore
from src.rag.rag_graph import RAGPipeline
from src.mcp.server import mcp, initialize_mcp

# Load environment variables
load_dotenv()

def main():
    # Initialize components
    print("=" * 50)
    print("Initializing RAG System with MCP Server")
    print("=" * 50)
    
    document_loader = DocumentLoader(chunk_size=1000, chunk_overlap=200)
    vector_store = ChromaVectorStore(
        persist_directory=os.getenv("CHROMA_DB_PATH", "./chroma_db"),
        collection_name="documents"
    )
    
    # Get API key from environment
    # api_key = os.getenv("ANTHROPIC_API_KEY")
    # Get LLM configuration
    llm_provider = os.getenv("LLM_PROVIDER", "ollama")  # Default to free Ollama
    api_key = os.getenv(f"{llm_provider.upper()}_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    rag_pipeline = RAGPipeline(vector_store, llm_api_key=api_key)
    
    # Initialize MCP server
    initialize_mcp(vector_store, rag_pipeline, document_loader)
    
    # Check if database is empty
    current_count = vector_store.collection.count()
    print(f"\nCurrent documents in database: {current_count}")
    
    # Only load documents if database is empty
    if current_count == 0:
        print("\n📂 Database is empty. Loading initial documents...")
        documents_path = os.getenv("DOCUMENTS_PATH", "./documents")
        
        if os.path.exists(documents_path):
            docs = document_loader.load_documents(documents_path)
            print(f"Loaded {len(docs)} document chunks")
            
            if docs:
                vector_store.add_documents(docs)
                print("✓ Documents added to vector database")
            else:
                print("⚠ No documents found to load")
        else:
            print(f"⚠ Warning: {documents_path} directory not found")
            os.makedirs(documents_path, exist_ok=True)
            print(f"Created {documents_path} directory - add documents here")
    else:
        print("✓ Database already contains documents. Skipping initial load.")
        print("  Use the load_documents_to_vectordb tool to add more documents.")
    
    # Start MCP server
    print("\n" + "=" * 50)
    print("MCP Server Starting...")
    print("Available tools: load_documents_to_vectordb, search_documents, rag_query, clear_vectordb")
    print("=" * 50 + "\n")
    
    mcp.run()

if __name__ == "__main__":
    main()