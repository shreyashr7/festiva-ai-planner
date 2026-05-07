"""
RAG Ingestion Pipeline
Loads knowledge base, chunks text, creates embeddings, and builds FAISS vector store.
"""

import os

from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from festiva.config import KNOWLEDGE_FILE, FAISS_INDEX_DIR, EMBEDDING_MODEL


def load_knowledge(path=None) -> str:
    """Load the knowledge base text file."""
    path = path or KNOWLEDGE_FILE
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separator="\n",
    )
    return splitter.split_text(text)


def build_vector_store(chunks: list[str], save_path=None) -> FAISS:
    """Create FAISS vector store from text chunks."""
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)

    save_path = save_path or FAISS_INDEX_DIR
    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(str(save_path))
    print(f"FAISS index saved to {save_path} ({len(chunks)} vectors)")

    return vector_store


def load_vector_store(path=None) -> FAISS:
    """Load existing FAISS index from disk."""
    path = path or FAISS_INDEX_DIR
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return FAISS.load_local(str(path), embeddings, allow_dangerous_deserialization=True)


def main():
    """Run the full ingestion pipeline."""
    print("=" * 70)
    print("FESTIVA - RAG KNOWLEDGE BASE INGESTION")
    print("=" * 70)

    print("\n[1/3] Loading knowledge base...")
    text = load_knowledge()
    print(f"      Loaded {len(text)} characters")

    print("\n[2/3] Chunking text...")
    chunks = chunk_text(text)
    print(f"      Created {len(chunks)} chunks")

    print("\n[3/3] Building FAISS vector store...")
    build_vector_store(chunks)
    print("\nIngestion complete.")


if __name__ == "__main__":
    main()
