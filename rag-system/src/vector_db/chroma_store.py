import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import uuid

class ChromaVectorStore:
    def __init__(self, 
                 persist_directory: str = "./chroma_db",
                 collection_name: str = "documents",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.embedding_model = SentenceTransformer(embedding_model)
        self.collection_name = collection_name
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[Dict]) -> None:
        """Add documents to vector store"""
        if not documents:
            return
        
        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        ids = [str(uuid.uuid4()) for _ in documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            self.collection.add(
                embeddings=embeddings[i:end_idx],
                documents=texts[i:end_idx],
                metadatas=metadatas[i:end_idx],
                ids=ids[i:end_idx]
            )
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        return [
            {
                "content": doc,
                "metadata": meta,
                "distance": dist
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    
    def clear_collection(self) -> None:
        """Clear all documents from collection"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )