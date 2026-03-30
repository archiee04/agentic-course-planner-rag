from ingestion import process_url

url = "https://catalog.illinois.edu/courses-of-instruction/cs/"

process_url(url, "../data/raw/thapar_test.txt")

print("Done! Check data/raw folder")