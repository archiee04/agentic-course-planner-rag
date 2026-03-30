from embeddings import build_vector_store


def query_system(query):
    vectorstore = build_vector_store("../data/raw/thapar_test.txt")

    # search top 3 relevant chunks
    results = vectorstore.similarity_search(query, k=3)

    print("\n🔍 Top Results:\n")

    for i, doc in enumerate(results):
        print(f"--- Result {i+1} ---")
        print(doc.page_content)
        print("Source:", doc.metadata["source"])
        print("Chunk:", doc.metadata["chunk_id"])
        print("\n")