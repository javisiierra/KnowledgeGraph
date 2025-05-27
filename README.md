# Research Knowledge Graph Builder

A pipeline for analyzing research publications and building Knowledge Graphs from PDFs.

## Overview

This project extracts metadata from research papers, performs text analysis using AI models, and generates an interactive Knowledge Graph. Main features:

* PDF text extraction
* Topic modeling with BERTopic
* Semantic similarity analysis
* Named Entity Recognition (NER)
* Entity enrichment with Wikidata and ROR
* RDF Knowledge Graph generation
* Interactive visualization with Streamlit

## Architecture

PDFs → Text Extraction → Metadata Processing → AI Analysis → Entity Enrichment → Knowledge Graph → Visualization

## Project Structure

```
knowledge-graph-project/
├── data/
│   ├── papers/              # Input PDFs
│   ├── processed/           # Extracted metadata
│   └── output/              # Analysis results
├── src/                     # Pipeline components
├── streamlit_app/           # Web interface
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Installation and Usage

### Docker (Recommended)

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

1. **Clone and prepare:**
```bash
git clone https://github.com/javisiierra/KnowledgeGraph.git
cd KnowledgeGraph
mkdir -p data/papers data/processed data/output
# Place your PDF files in data/papers/
```

2. **Run pipeline:**
```bash
docker compose up --build pipeline
```

3. **Launch dashboard:**
```bash
docker compose up -d streamlit
# Access at http://localhost:8501
```

**Management:**
```bash
docker compose down              # Stop services
docker compose logs streamlit    # View logs
```

### Manual Installation

1. **Setup environment:**
```bash
git clone https://github.com/javisiierra/KnowledgeGraph.git
cd KnowledgeGraph

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Prepare data:**
```bash
mkdir -p data/papers data/processed data/output
# Place your PDF files in data/papers/
```

4. **Run pipeline:**
```bash
python src/run_pipeline.py
```

5. **Launch visualization:**
```bash
streamlit run streamlit_app/app.py
# Access at http://localhost:8501
```

## Input Requirements

* PDFs in `data/papers/`
* PDFs should contain: title, abstract, acknowledgements
* Recommended: 10-30 papers

## Output

* Processed metadata: `data/processed/`
* Analysis results: `data/output/`
* Knowledge Graph: `data/output/kg.ttl`
* Interactive visualization via Streamlit

## Knowledge Graph Schema

Uses vocabularies:
* Dublin Core (dcterms)
* FOAF
* Custom vocabulary (ex:)

Key relationships:
* `paper → belongs_to_topic → topic`
* `paper → similar_to → paper`  
* `paper → acknowledges → person/organization`

## License

Apache 2.0 License
