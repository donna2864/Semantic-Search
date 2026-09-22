from app.search import search

def test_search_return_results():
    results = search("What is SQL used for?", top_k=5)
    assert "documents" in results
    assert "metadatas" in results
    assert "distances" in results

    assert len(results["documents"][0]) == 5

def test_search_return_relavant_documents():
    results = search("What is SQL used for?", top_k=5)
    sources = [metadata["filename"] for metadata in results["metadatas"][0]]
    assert "database.txt" in sources

def test_search_respects_top_k():
    results = search("machine learning algorithms", top_k=3)
    assert len(results["documents"][0]) == 3


    