from langchain_community.vectorstores import Chroma
from app.rag.embeddings import get_embeddings
from pathlib import Path

VECTOR_STORE_PATH = str(Path(__file__).parent / "vector_db")


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )

    vectordb.persist()

    return vectordb


def load_vector_store():

    embeddings = get_embeddings()

    return Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )