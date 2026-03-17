from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import os

class RAGState(TypedDict):
    query: str
    context: List[str]
    retrieved_docs: List[dict]
    answer: str
    sources: List[str]

class RAGPipeline:
    def __init__(self, vector_store, llm_provider: str = "anthropic", llm_api_key: str = None):
        self.vector_store = vector_store
        self.llm = self._initialize_llm(llm_provider, llm_api_key)
        self.graph = self._build_graph()
    
    def _initialize_llm(self, provider: str, api_key: str):
        """Initialize LLM based on provider"""
        
        if provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-sonnet-4-20250514",
                api_key=api_key,
                max_tokens=2000
            )
        
        elif provider == "ollama":
            from langchain_community.llms import Ollama
            return Ollama(
                model="llama3.2",
                base_url="http://localhost:11434"
            )
        
        elif provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=api_key
            )
        
        elif provider == "groq":
            from langchain_groq import ChatGroq
            return ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=api_key
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    # ... rest of the code stays the same
    
    def _retrieve_documents(self, state: RAGState) -> RAGState:
        """Retrieve relevant documents from vector store"""
        results = self.vector_store.search(state["query"], n_results=5)
        
        state["retrieved_docs"] = results
        state["context"] = [doc["content"] for doc in results]
        state["sources"] = [
            doc["metadata"].get("source", "Unknown") 
            for doc in results
        ]
        
        return state
    
    def _generate_answer(self, state: RAGState) -> RAGState:
        """Generate answer using LLM with retrieved context"""
        context_text = "\n\n".join([
            f"Document {i+1}:\n{ctx}" 
            for i, ctx in enumerate(state["context"])
        ])
        
        prompt = f"""Based on the following documents, answer the user's question.
If the answer cannot be found in the documents, say so clearly.

Documents:
{context_text}

Question: {state["query"]}

Answer:"""
        
        response = self.llm.invoke(prompt)
        state["answer"] = response.content
        
        return state
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(RAGState)
        
        # Add nodes
        workflow.add_node("retrieve", self._retrieve_documents)
        workflow.add_node("generate", self._generate_answer)
        
        # Add edges
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    
    def query(self, user_query: str) -> dict:
        """Execute RAG pipeline"""
        initial_state = {
            "query": user_query,
            "context": [],
            "retrieved_docs": [],
            "answer": "",
            "sources": []
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            "answer": result["answer"],
            "sources": list(set(result["sources"])),
            "num_docs_retrieved": len(result["retrieved_docs"])
        }