import os
import json
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def save_metadata(paper_id, title, abstract, acknowledgements):
    metadata = {
        'id': paper_id,
        'title': title,
        'abstract': abstract,
        'acknowledgements': acknowledgements
    }
    os.makedirs("data/processed", exist_ok=True)
    with open(f"data/processed/{paper_id}.json", "w") as f:
        json.dump(metadata, f, indent=2)

def extract_section(text, start_marker, end_marker):
    lower_text = text.lower()
    try:
        start = lower_text.index(start_marker.lower())
        end = lower_text.index(end_marker.lower(), start)
        return text[start:end].strip()
    except ValueError:
        return ""

def preprocess_papers():
    pdf_dir = "./data/papers"
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            title = text.split("\n")[0]
            abstract = extract_section(text, "abstract", "introduction")
            acknowledgements = extract_section(text, "acknowledgements", "references")
            paper_id = pdf_file.replace(".pdf", "")
            save_metadata(paper_id, title, abstract, acknowledgements)

if __name__ == "__main__":
    preprocess_papers()