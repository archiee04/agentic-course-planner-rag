from embeddings import build_vector_store
import re
import os


def extract_course_info(context, course_code):
    context = context.replace("\xa0", " ")
    parts = context.split("CS ")

    for part in parts:
        if course_code.split()[1] in part:
            return "CS " + part.strip()

    return "Course not found."


def extract_prereq(text):
    text = text.replace("\xa0", " ")

    match = re.search(r"Prerequisite:(.*?)(This course|Credit|$)", text, re.DOTALL)

    if match:
        return match.group(1).strip()

    return "No prerequisite found."


def answer_question(query):

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "raw", "thapar_test.txt")

    vectorstore = build_vector_store(file_path)

    results = vectorstore.similarity_search(query, k=10)

    if not results:
        print("No information found.")
        return

    sources = [
        f"{doc.metadata['source']} ({doc.metadata['chunk_id']})"
        for doc in results
    ]

    context = "\n\n".join([doc.page_content for doc in results])

    course_match = re.search(r"CS\s?\d+", query)
    course_code = course_match.group(0) if course_match else "UNKNOWN"

    course_info = extract_course_info(context, course_code)
    prereq = extract_prereq(course_info)

    print("\n===== FINAL ANSWER =====\n")
    print(f"Question: {query}\n")

    print("Answer:")
    print(f"Course: {course_code}")
    print(f"Prerequisite: {prereq}\n")

    print("Citations:")
    for s in sources:
        print("-", s)


def check_eligibility(query, completed_courses):

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "raw", "thapar_test.txt")

    vectorstore = build_vector_store(file_path)

    results = vectorstore.similarity_search(query, k=10)

    # ✅ SAFE ABSTENTION
    if not results:
        print("\n===== FINAL RESPONSE =====\n")

        print("Answer:")
        print("I don’t have enough information in the provided catalog.")

        print("\nWhy:")
        print("No relevant course information was retrieved.")

        print("\nCitations:")
        print("None")

        print("\nClarifying Questions:")
        print("Can you уточнить the course code or provide more details?")

        print("\nAssumptions:")
        print("Assumes missing data in catalog.")

        return

    # ✅ NORMAL FLOW
    sources = [
        f"{doc.metadata['source']} ({doc.metadata['chunk_id']})"
        for doc in results
    ]

    context = "\n\n".join([doc.page_content for doc in results])

    course_match = re.search(r"CS\s?\d+", query)
    course_code = course_match.group(0) if course_match else "UNKNOWN"

    course_info = extract_course_info(context, course_code)
    prereq = extract_prereq(course_info)

    prereq_clean = prereq.replace("\n", " ")

    courses = re.findall(r"[A-Z]{2,4}\s\d+", prereq_clean)

    has_or = "one of" in prereq_clean.lower()

    completed_set = set(completed_courses)

    # ✅ LOGIC
    if has_or:
        mandatory = [c for c in courses if "STAT" in c or "CS" in c]
        optional = [c for c in courses if c not in mandatory]

        missing_mandatory = [c for c in mandatory if c not in completed_set]
        has_optional = any(c in completed_set for c in optional)

        eligible = (not missing_mandatory) and has_optional

        missing = []
        if missing_mandatory:
            missing.extend(missing_mandatory)
        if not has_optional:
            missing.append("one of: " + ", ".join(optional))

    else:
        missing = [course for course in courses if course not in completed_set]
        eligible = len(missing) == 0

    print("\n===== FINAL RESPONSE =====\n")

    print("Answer:")
    if eligible:
        print(f"You ARE eligible to take {course_code}.")
    else:
        print(f"You are NOT eligible to take {course_code}.")

    print("\nWhy:")
    if eligible:
        print("All prerequisite conditions are satisfied.")
    else:
        print(f"Missing required courses: {missing}")

    print("\nCitations:")
    for s in sources:
        print("-", s)

    print("\nClarifying Questions:")
    print("Do you have any equivalent transfer credits or substitutions?")

    print("\nAssumptions:")
    print("Assumes catalog prerequisites are complete and no exceptions apply.")