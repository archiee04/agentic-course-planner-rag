def check_eligibility(query, completed_courses):
    vectorstore = build_vector_store("../data/raw/thapar_test.txt")

    results = vectorstore.similarity_search(query, k=10)
    context = "\n\n".join([doc.page_content for doc in results])

    course_match = re.search(r"CS\s?\d+", query)
    course_code = course_match.group(0)

    course_info = extract_course_info(context, course_code)
    prereq = extract_prereq(course_info)

    prereq_clean = prereq.replace("\n", " ")

    # extract all course codes
    courses = re.findall(r"[A-Z]{2,4}\s\d+", prereq_clean)

    # split logic
    has_or = "one of" in prereq_clean.lower()

    # check conditions
    completed_set = set(completed_courses)

    if has_or:
        # OR condition
        eligible = any(course in completed_set for course in courses)
    else:
        # AND condition
        eligible = all(course in completed_set for course in courses)

    print("\n===== ELIGIBILITY CHECK =====\n")

    print(f"Target Course: {course_code}")
    print(f"Completed Courses: {completed_courses}\n")

    print(f"Prerequisite: {prereq}\n")

    if eligible:
        print("Decision: ✅ Eligible")
    else:
        print("Decision: ❌ Not Eligible")

    print("\nReason:")
    print("Evaluated prerequisite conditions (AND/OR logic).")