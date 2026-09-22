from fastapi import FastAPI
from pydantic import BaseModel
from app.search import search

app = FastAPI(
    title= "Semantic Search Engine",
    description="Semantic document retrieval using embeddings and ChromaDB",
    version="1.0.0"
)

class SearchRequest(BaseModel):
    query:str
    top_k: int = 5

@app.get("/")
def root():
    return {"message":"Semantic Search API is running"}

@app.post("/search")
def search_documents(request: SearchRequest):
    results = search(request.query, top_k=request.top_k)

    formatted_results = []

    for i in range(len(results["documents"][0])):
        formatted_results.append({
            "rank": i+1,
            "source": results["metadatas"][0][i]["filename"],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i]
        })

    return {
        "query": request.query,
        "results": formatted_results
    }