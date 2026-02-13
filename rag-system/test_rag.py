# test_rag.py (ROOT LEVEL)
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test API health"""
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_load_documents():
    """Test loading documents"""
    print("2. Loading documents...")
    response = requests.post(
        f"{BASE_URL}/load-documents",
        json={"directory": "./documents"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_search():
    """Test direct vector search"""
    print("3. Testing vector search...")
    response = requests.post(
        f"{BASE_URL}/search",
        json={
            "query": "how to make Api request idempotent",
            "n_results": 3
        }
    )
    print(f"Status: {response.status_code}")
    results = response.json()
    print(f"Found {len(results.get('results', []))} results")
    
    for i, result in enumerate(results.get('results', [])[:2], 1):
        print(f"\nResult {i}:")
        print(f"  Source: {result['metadata'].get('source', 'Unknown')}")
        print(f"  Content: {result['content'][:150]}...")
        print(f"  Distance: {result['distance']:.4f}")
    print()

def test_rag_query():
    """Test RAG query"""
    print("4. Testing RAG query...")
    questions = [
        "What is the main topic discussed in the documents?",
        "Summarize the key points from the documents",
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": question}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nAnswer: {result['answer']}")
            print(f"\nSources ({len(result['sources'])}):")
            for src in result['sources']:
                print(f"  - {src}")
            print(f"\nDocuments retrieved: {result['num_docs_retrieved']}")
        else:
            print(f"Error: {response.text}")
        print("-" * 80)

def test_clear():
    """Test clearing database"""
    print("\n5. Testing clear database...")
    response = requests.delete(f"{BASE_URL}/clear")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == "__main__":
    print("=" * 80)
    print("RAG SYSTEM TEST SUITE")
    print("=" * 80)
    
    try:
        test_health()
        test_load_documents()
        test_search()
        test_rag_query()
        # Uncomment to test clearing (will delete all data!)
        # test_clear()
        
        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETED")
        print("=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Make sure the FastAPI server is running:")
        print("  cd src/api && uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")