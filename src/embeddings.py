from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from chunking import split_into_courses


def build_vector_store(file_path):
    # read file
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = split_into_courses(text)

    print(f"Total chunks: {len(chunks)}")

    # ✅ extract text + metadata separately
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in chunks
    ]

    # embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ✅ pass metadata into FAISS
    vectorstore = FAISS.from_texts(
        texts,
        embeddings,
        metadatas=metadatas
    )

    return vectorstore