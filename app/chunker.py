from pathlib import Path

DOCUMENTS_DIR = Path("documents")

def load_documents():
    documents = []
    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        documents.append({
            "filename": file_path.name,
            "text": text
        })
    return documents

def create_chunks(documents):
    chuncks = []
    for document in documents:
        paragraphs = document["text"].split("\n\n")
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                chuncks.append({
                    "filename": document["filename"],
                    "text": paragraph
                })
    return chuncks

if __name__ == "__main__":
    documents = load_documents()
    chuncks = create_chunks(documents)
    print("Documents loaded: ", len(documents))
    print("Chunks loaded: ", len(chuncks))

    for i, chunck in enumerate(chuncks):
        print(f"\nChunk {i+1}")
        print("Source: ", chunck["filename"])
        print("Text: ", chunck["text"])