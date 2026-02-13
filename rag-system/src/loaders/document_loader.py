import os
from pathlib import Path
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)

class DocumentLoader:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
    def load_documents(self, directory: str) -> List[Dict]:
        """Load all documents from directory"""
        documents = []
        supported_extensions = {'.pdf', '.txt', '.docx', '.md'}
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                ext = Path(file_path).suffix.lower()
                
                if ext in supported_extensions:
                    try:
                        docs = self._load_file(file_path, ext)
                        documents.extend(docs)
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")
        
        return documents
    
    def _load_file(self, file_path: str, ext: str) -> List[Dict]:
        """Load individual file based on extension"""
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext == '.docx':
            loader = Docx2txtLoader(file_path)
        elif ext in ['.txt', '.md']:
            loader = TextLoader(file_path)
        else:
            return []
        
        docs = loader.load()
        chunks = self.text_splitter.split_documents(docs)
        
        return [
            {
                "content": chunk.page_content,
                "metadata": {
                    **chunk.metadata,
                    "source": file_path,
                }
            }
            for chunk in chunks
        ]