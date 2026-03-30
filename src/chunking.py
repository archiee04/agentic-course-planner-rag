import re

def split_into_courses(text):
    text = text.replace("\xa0", " ")

    pattern = r"(CS\s\d+.*?)(?=CS\s\d+|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    chunks = []

    for i, match in enumerate(matches):
        chunk_text = match.strip()

        if len(chunk_text) > 50:  # avoid junk
            chunks.append({
                "text": chunk_text,
                "source": f"https://catalog.illinois.edu/courses-of-instruction/cs/#chunk-{i}",
                "chunk_id": f"chunk_{i}"
            })

    return chunks