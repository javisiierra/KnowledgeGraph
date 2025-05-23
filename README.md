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
│   ├── preprocess.py
│   ├── topic_model.py
│   ├── similarity.py
│   ├── ner_ack.py
│   ├── wikidata_enrich.py
│   ├── ror_enrich.py
│   ├── build_kg.py
│   └── run_pipeline.py
|   └── kg_utils.py
├── streamlit_app/           # Web interface
│   ├── app.py
│   └── kg_utils.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone repository:

```bash
git clone https://github.com/javisiierra/KnowledgeGraph.git
cd KnowledgeGraph
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

### Quick Start

Place PDFs in `data/papers/` and run:

```bash
python src/run_pipeline.py
```

### Visualization

After pipeline completion:

```bash
streamlit run streamlit_app/app.py
```

Access at: [http://localhost:8501](http://localhost:8501)

### Manual Execution

Run individual components:

```bash
python src/preprocess.py       # Extract text
python src/topic_model.py      # Topic modeling
python src/similarity.py       # Similarity analysis
python src/ner_ack.py          # NER
python src/wikidata_enrich.py  # Wikidata enrichment
python src/ror_enrich.py       # ROR enrichment
python src/build_kg.py         # Build Knowledge Graph
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