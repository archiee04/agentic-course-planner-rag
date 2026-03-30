from embeddings import build_vector_store

vectorstore = build_vector_store("../data/raw/thapar_test.txt")

print("Vector store created!")