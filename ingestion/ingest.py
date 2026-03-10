from ingestion.loaders import load_documents
from app.rag.chunking import chunk_documents
from app.rag.vector_store import create_vector_store
from pathlib import Path


def run_ingestion():
    print("Starting ingestion")

    data_path = Path(__file__).parent.parent / "data"
    docs = load_documents(data_path)

    print(f"Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)

    print(f"Created {len(chunks)} chunks")

    vectordb = create_vector_store(chunks)

    print("Vector database created")


if __name__ == "__main__":
    run_ingestion()