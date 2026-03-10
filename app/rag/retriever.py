from app.rag.vector_store import load_vector_store


def retrieve_documents(query: str, k: int = 3):

    vectordb = load_vector_store()

    results = vectordb.similarity_search_with_score(query, k=k)

    documents = []

    for doc, score in results:
        documents.append(
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "score": score
            }
        )

    return documents