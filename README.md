# Knowledge Graph Project — Advanced Data Analysis on Research Publications

## Objetivo
Analizar un corpus de 30 papers, extraer metadatos, realizar topic modeling, calcular similitud entre abstracts, reconocer entidades en los acknowledgements y construir un Knowledge Graph en RDF enriquecido con Wikidata y ROR.

## Estructura
- `data/papers/` → PDFs o XML de papers  
- `data/processed/` → JSON con metadatos extraídos  
- `data/output/` → RDF, modelos, resultados  
- `src/` → scripts principales

## Scripts
1. `preprocess.py` → extrae texto, title, abstract, acknowledgements  
2. `topic_model.py` → topic modeling con BERTopic  
3. `similarity.py` → calcula similitud con SentenceTransformers  
4. `build_kg.py` → genera RDF básico

## Entorno virtual
Antes de instalar los requisitos, se recomienda crear y activar un entorno virtual de Python:

```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual (Windows)
venv\Scripts\activate

# Activar el entorno virtual (Linux/macOS)
source venv/bin/activate
