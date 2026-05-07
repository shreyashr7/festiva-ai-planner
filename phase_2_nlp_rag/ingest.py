"""
RAG Ingestion Pipeline for Bengaluru Event Planning Knowledge Base
Loads knowledge.txt, chunks it, creates embeddings, and builds a FAISS vector store.
"""

import os
import pickle
from pathlib import Path
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("=" * 80)
print("BENGALURU EVENT PLANNING - RAG KNOWLEDGE BASE INGESTION")
print("=" * 80)

# ============================================================================
# PHASE 1: LOAD KNOWLEDGE BASE
# ============================================================================
print("\n[1] Loading knowledge base from knowledge.txt...")

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
knowledge_path = os.path.join(script_dir, 'knowledge.txt')

try:
    with open(knowledge_path, 'r', encoding='utf-8') as f:
        knowledge_text = f.read()
    print(f"   ✓ Loaded {len(knowledge_text)} characters from knowledge.txt")
    if len(knowledge_text) > 0:
        print(f"   Sample: {knowledge_text[:200]}...")
    else:
        print("   ✗ Warning: File is empty or could not be read")
except FileNotFoundError:
    print(f"   ✗ Error: knowledge.txt not found at {knowledge_path}")
    exit(1)
except Exception as e:
    print(f"   ✗ Error reading file: {e}")
    exit(1)

# ============================================================================
# PHASE 2: TEXT CHUNKING
# ============================================================================
print("\n[2] Chunking knowledge base (500 chars, 50 char overlap)...")

text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separator="\n"
)

chunks = text_splitter.split_text(knowledge_text)
print(f"   ✓ Created {len(chunks)} chunks")

if chunks:
    print(f"   Chunk size stats:")
    print(f"      - Min: {min(len(c) for c in chunks)} chars")
    print(f"      - Max: {max(len(c) for c in chunks)} chars")
    print(f"      - Avg: {sum(len(c) for c in chunks) / len(chunks):.1f} chars")
    
    # Display first 2 chunks as preview
    print(f"\n   Preview of first 2 chunks:")
    for i, chunk in enumerate(chunks[:2]):
        print(f"\n   Chunk {i+1}:")
        print(f"   {chunk[:200]}...")
else:
    print("   ✗ Warning: No chunks created from knowledge base")
    exit(1)

# ============================================================================
# PHASE 3: EMBEDDING & VECTOR STORE CREATION
# ============================================================================
print("\n[3] Creating embeddings using HuggingFaceEmbeddings...")
print("   Model: all-MiniLM-L6-v2")

try:
    embeddings = HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("   ✓ HuggingFaceEmbeddings initialized")
except Exception as e:
    print(f"   ✗ Error initializing embeddings: {e}")
    exit(1)

print("\n[4] Building FAISS vector store...")
try:
    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )
    print(f"   ✓ FAISS vector store created with {len(chunks)} vectors")
except Exception as e:
    print(f"   ✗ Error creating FAISS index: {e}")
    exit(1)

# ============================================================================
# PHASE 4: SAVE FAISS INDEX
# ============================================================================
print("\n[5] Saving FAISS index to disk...")

index_folder = os.path.join(script_dir, 'faiss_index')
os.makedirs(index_folder, exist_ok=True)

try:
    vector_store.save_local(index_folder)
    print(f"   ✓ FAISS index saved to '{index_folder}' folder")
    print(f"   Files in {index_folder}:")
    for file in os.listdir(index_folder):
        file_path = os.path.join(index_folder, file)
        file_size = os.path.getsize(file_path)
        print(f"      - {file} ({file_size:,} bytes)")
except Exception as e:
    print(f"   ✗ Error saving FAISS index: {e}")
    exit(1)

# ============================================================================
# PHASE 5: VERIFY & TEST
# ============================================================================
print("\n[6] Loading FAISS index from disk (verification)...")

try:
    loaded_vector_store = FAISS.load_local(
        index_folder,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"   ✓ FAISS index loaded successfully")
    print(f"   ✓ Index contains {loaded_vector_store.index.ntotal} vectors")
except Exception as e:
    print(f"   ✗ Error loading FAISS index: {e}")
    exit(1)

# ============================================================================
# PHASE 6: TEST RETRIEVAL FUNCTION
# ============================================================================
def test_retrieval(query: str, k: int = 2):
    """
    Test function to retrieve relevant chunks for a given query.
    
    Args:
        query (str): The search query
        k (int): Number of chunks to retrieve (default: 2)
    """
    print(f"\n[7] TEST RETRIEVAL")
    print(f"   Query: '{query}'")
    print(f"   Retrieving top {k} relevant chunks...\n")
    
    try:
        results = loaded_vector_store.similarity_search(query, k=k)
        
        if not results:
            print("   ✗ No results found")
            return
        
        for i, doc in enumerate(results, 1):
            print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"   Chunk {i} (Relevance: High)")
            print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"   {doc.page_content}")
            print()
        
        return results
    
    except Exception as e:
        print(f"   ✗ Error during retrieval: {e}")
        return None

# Run test with sample query
sample_query = "Where is a good place for a corporate event in Whitefield?"
test_retrieval(sample_query, k=2)

print("=" * 80)
print("✓ RAG INGESTION PIPELINE COMPLETE")
print(f"✓ Vector store saved to: {index_folder}/")
print("=" * 80)
