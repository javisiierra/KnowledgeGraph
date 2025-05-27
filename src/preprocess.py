import os
import json
import requests
from lxml import etree
from pdfminer.high_level import extract_text

GROBID_URL = os.environ.get("GROBID_URL", "http://localhost:8070/api/processFulltextDocument")

def extract_text_from_pdf(pdf_path):
    """Extract full text from PDF (used for acknowledgements)."""
    return extract_text(pdf_path)

def grobid_parse_pdf(pdf_path):
    """Send PDF to GROBID and get TEI XML."""
    with open(pdf_path, 'rb') as f:
        response = requests.post(GROBID_URL, files={'input': f})
        if response.status_code != 200:
            print(f"[!] Error con GROBID: {response.status_code}")
            return None
        return response.text

def extract_from_grobid_xml(xml_text):
    """Parse XML from GROBID to get title, authors, abstract."""
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
    """Extract a section between start and end markers from full text."""
    lower_text = text.lower()
    
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
    """Process PDFs using Grobid (for metadata) and PDFMiner (for acknowledgements)."""
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

            # Extraer acknowledgements desde texto plano completo
            text = extract_text_from_pdf(pdf_path)
            acknowledgements = extract_section(
                text,
                ["acknowledgements", "acknowledgment", "acknowledgments", "acknowledgement"],
                ["references", "bibliography", "appendix", "citations"]
            )

            paper_id = pdf_file.replace(".pdf", "")
            save_metadata(paper_id, title, authors, abstract, acknowledgements)
            print(f"✅ Guardado: {paper_id}\n")

if __name__ == "__main__":
    preprocess_papers()