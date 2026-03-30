# 🎓 Agentic Course Planner (RAG-based)

An intelligent AI system that helps students understand course prerequisites, check eligibility, and plan academic pathways using Retrieval-Augmented Generation (RAG) and structured reasoning.

---

## 🚀 Demo

Run locally:

```bash
python -m streamlit run app.py
```
🎯 Problem Statement

Students often struggle to:

Understand course prerequisites
Check eligibility for advanced courses
Plan their academic path

This system solves that by:

Retrieving relevant catalog information
Applying logical reasoning over prerequisites
Providing grounded, explainable answers

🧠 Approach

We built a RAG (Retrieval-Augmented Generation) system with rule-based reasoning.

🔹 Pipeline
Data Ingestion
University course catalog (UIUC CS)
Chunking (Key Design Choice ⭐)
Each chunk = one complete course

Regex used:
```
(CS\s\d+.*?)(?=CS\s\d+|$)
```

Preserves prerequisite structure
Embeddings
Model: sentence-transformers/all-MiniLM-L6-v2
Vector Store
FAISS for semantic search
Stores:
course text
metadata (source + chunk_id)
Retriever
Top-k similarity search retrieves relevant courses
Reasoning Layer (Core Innovation)
Extracts prerequisites using regex
Handles:
AND conditions
OR conditions ("one of")
Compares with completed courses

✅ Features
🔹 Eligibility Checking

Input:
```
Can I take CS 225?
Completed: CS 125
```
Output:
```
Answer:
You are NOT eligible to take CS 225.

Why:
Missing required courses: ['STAT 207', 'one of: MATH 220, MATH 221, MATH 234']

Citations:
- https://catalog.illinois.edu/... (#chunk_57)

Clarifying Questions:
Do you have any equivalent transfer credits?

Assumptions:
Assumes catalog prerequisites are complete.
```

🔹 Grounded Responses

Every answer includes:
Source URL
Chunk ID
Ensures traceability and prevents hallucination

🔹 Safe Abstention

If information is missing:
I don’t have enough information in the provided catalog.

🔹 Streamlit UI

Interactive interface
Real-time eligibility checking
Clean output display

📊 Evaluation

Tested on ~25 queries including:

Eligibility checks
Prerequisite extraction
Edge cases
✔ Observations
Correct prerequisite detection
Handles OR/AND logic
Provides explainable reasoning
⚠️ Limitations
Does not handle:
Co-requisites
Course availability (semester-wise)
Timetable conflicts
Rule-based logic (not fully semantic)
Assumes catalog completeness and correctness

🏗️ Project Structure
```
agentic-course-planner-rag/
│
├── src/
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── qa_system.py
│
├── data/
├── evaluation/
├── app.py
├── requirements.txt
├── README.md
```

🧪 Installation
pip install -r requirements.txt

▶️ Run
```
python -m streamlit run app.py
```

💡 Key Design Decisions

Course-level chunking → preserves semantic meaning
Metadata in FAISS → enables traceable citations
Rule-based reasoning → ensures deterministic decisions
Structured outputs → improves clarity and evaluation

🚀 Future Improvements

LLM-based reasoning instead of regex
Better parsing of complex prerequisites
Multi-university support
Enhanced UI

🙌 Conclusion

This project demonstrates:

End-to-end RAG pipeline
Structured reasoning over academic data
Explainable and grounded AI system
