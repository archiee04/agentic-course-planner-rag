from embeddings import build_vector_store

def generate_plan(completed_courses):
    vectorstore = build_vector_store("../data/raw/thapar_test.txt")

    results = vectorstore.similarity_search("CS courses", k=20)

    print("\n===== COURSE PLAN =====\n")

    suggested = []

    for doc in results:
        text = doc.page_content
        if "CS" in text:
            course = text.split("\n")[0]
            suggested.append(course)

    suggested = list(set(suggested))[:5]

    print("Suggested Next Courses:")
    for s in suggested:
        print("-", s)

    print("\nAssumptions:")
    print("Schedule and availability not considered.")