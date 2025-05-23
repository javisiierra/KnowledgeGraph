import os
import json
from pdfminer.high_level import extract_text
import re

def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF file."""
    text = extract_text(pdf_path)
    return text

def extract_title(text):
    """Extract title from the first few lines of the document."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        # Assume title is in the first significant lines
        title = " ".join(lines[:3])  # Take first 3 lines
        return title[:200]  # Limit to 200 characters
    return "Unknown Title"

def extract_authors(text):
    """Extract authors from text - basic heuristic approach."""
    authors = []
    lines = text.split('\n')[:20]  # Search in first 20 lines
    
    # Look for common author name patterns
    for line in lines:
        # Look for lines with names (Initial + Surname pattern)
        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', line):
            authors.append(line.strip())
    
    return authors[:10]  # Limit to 10 authors maximum

def extract_section(text, start_markers, end_markers):
    """Extract a section between start and end markers."""
    lower_text = text.lower()
    
    # Try multiple markers
    for start_marker in start_markers:
        for end_marker in end_markers:
            try:
                start = lower_text.index(start_marker.lower())
                end = lower_text.index(end_marker.lower(), start)
                return text[start:end].strip()
            except ValueError:
                continue
    return ""

def save_metadata(paper_id, title, authors, abstract, acknowledgements):
    """Save extracted metadata to JSON file."""
    metadata = {
        'id': paper_id,
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'acknowledgements': acknowledgements
    }
    os.makedirs("data/processed", exist_ok=True)
    with open(f"data/processed/{paper_id}.json", "w") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

def preprocess_papers():
    """Process all PDFs in the data/papers directory."""
    pdf_dir = "./data/papers"
    
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            
            # Extract metadata
            title = extract_title(text)
            authors = extract_authors(text)
            
            # Extract sections with multiple possible markers
            abstract = extract_section(
                text, 
                ["abstract", "summary", "resumen"], 
                ["introduction", "1. introduction", "keywords", "1 introduction"]
            )
            
            acknowledgements = extract_section(
                text, 
                ["acknowledgements", "acknowledgments", "acknowledgement", "acknowledgment"],
                ["references", "bibliography", "appendix", "citations"]
            )
            
            paper_id = pdf_file.replace(".pdf", "")
            save_metadata(paper_id, title, authors, abstract, acknowledgements)
            print(f"Processed: {paper_id}")

if __name__ == "__main__":
    preprocess_papers()