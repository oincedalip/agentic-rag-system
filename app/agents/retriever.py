from app.graph.state import AgentState, RetrievedDocument
from app.rag.retriever import retrieve_documents

class RetrievalAgent:
    def run(self, state: AgentState):
        print("--Retrieval Agent--")
        
        query = state.query
        docs = retrieve_documents(query)

        retrieved_docs = [
            RetrievedDocument(
                content=d["content"],
                source=d["source"],
                score=d["score"]
            )
            for d in docs
        ]

        print(f"Successfully retrieved {len(retrieved_docs)} documents.")
        return {"retrieved_docs": retrieved_docs}