from chunking import split_into_courses

# read your file
with open("../data/raw/thapar_test.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = split_into_courses(text)

print(f"Total chunks: {len(chunks)}\n")

# print first 2 chunks
for i, chunk in enumerate(chunks[:2]):
    print(f"--- CHUNK {i+1} ---")
    print(chunk[:500])  # preview
    print("\n")