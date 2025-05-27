import os
import json
import requests
from lxml import etree
from pdfminer.high_level import extract_text
import re

GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

def extract_text_from_pdf(pdf_path):
    """Extract full text from PDF for fallback extraction (acknowledgements)."""
    return extract_text(pdf_path)

def grobid_parse_pdf(pdf_path):
    """Send PDF to GROBID and get XML."""
    with open(pdf_path, 'rb') as f:
        response = requests.post(GROBID_URL, files={'input': f})
        if response.status_code != 200:
            print(f"[!] Error con GROBID: {response.status_code}")
            return None
        return response.text

def extract_from_grobid_xml(xml_text):
    """Parse XML response from GROBID to extract title, authors, abstract."""
    root = etree.fromstring(xml_text.encode('utf-8'))
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # Title
    title_el = root.find('.//tei:titleStmt/tei:title', namespaces=ns)
    title = title_el.text.strip() if title_el is not None and title_el.text else "Unknown Title"

    # Authors
    authors = []
    for author in root.findall('.//tei:author', namespaces=ns):
        forename_el = author.find('.//tei:forename', namespaces=ns)
        surname_el = author.find('.//tei:surname', namespaces=ns)
        forename = forename_el.text.strip() if forename_el is not None and forename_el.text else ""
        surname = surname_el.text.strip() if surname_el is not None and surname_el.text else ""
        full_name = f"{forename} {surname}".strip()
        if full_name:
            authors.append(full_name)

    # Abstract
    abstract_el = root.find('.//tei:abstract//tei:p', namespaces=ns)
    abstract = abstract_el.text.strip() if abstract_el is not None and abstract_el.text else ""

    return title, authors, abstract

def extract_section(text, start_markers, end_markers):
    """Extract a section from raw PDF text between start and end markers."""
    lines = text.split('\n')
    lower_lines = [line.lower().strip() for line in lines]

    # Find start marker
    start_idx = -1
    for i, line in enumerate(lower_lines):
        for marker in start_markers:
            if re.fullmatch(rf'\b{re.escape(marker)}\b', line):
                start_idx = i
                break
        if start_idx != -1:
            break

    if start_idx == -1:
        return ""

    # Collect lines until end marker
    extracted_lines = []
    for i in range(start_idx + 1, len(lines)):
        if any(end in lower_lines[i] for end in end_markers):
            break
        if len(lines[i].strip()) == 0:
            continue
        extracted_lines.append(lines[i].strip())
        if len(extracted_lines) >= 10:
            break

    extracted = ' '.join(extracted_lines).strip()
    if len(extracted.split()) < 5 or len(extracted.split()) > 300:
        return ""
    return extracted

def save_metadata(paper_id, title, authors, abstract, acknowledgements):
    """Save extracted metadata to JSON."""
    metadata = {
        'id': paper_id,
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'acknowledgements': acknowledgements
    }
    os.makedirs("data/processed", exist_ok=True)
    with open(f"data/processed/{paper_id}.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

def preprocess_papers():
    """Process all PDFs in data/papers/ using GROBID and PDFMiner."""
    pdf_dir = "./data/papers"
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            print(f"📄 Procesando: {pdf_file}")
            
            xml = grobid_parse_pdf(pdf_path)
            if not xml:
                print(f"[!] Falló GROBID para: {pdf_file}")
                continue

            title, authors, abstract = extract_from_grobid_xml(xml)

            # Para acknowledgements usamos el texto completo extraído
            text = extract_text_from_pdf(pdf_path)
            acknowledgements = extract_section(
                text,
                ["acknowledgements", "acknowledgment"],
                ["references", "bibliography", "appendix"]
            )

            paper_id = pdf_file.replace(".pdf", "")
            save_metadata(paper_id, title, authors, abstract, acknowledgements)
            print(f"✅ Guardado: {paper_id}\n")

if __name__ == "__main__":
    preprocess_papers()