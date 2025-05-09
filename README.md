# Knowledge Graph Project — Advanced Data Analysis on Research Publications

## Objetivo

Este proyecto analiza un corpus de 30 artículos científicos con el objetivo de:

- Extraer metadatos relevantes (título, autores, abstract, acknowledgements)
- Realizar topic modeling usando BERTopic
- Calcular similitudes semánticas entre abstracts con SentenceTransformers
- Reconocer entidades nombradas en los acknowledgements (NER)
- Construir un Knowledge Graph en formato RDF enriquecido con Wikidata y ROR
- Visualizar los resultados mediante una aplicación interactiva en Streamlit

## Estructura del Proyecto

```
KnowledgeGraph-main/
├── data/
│   └── papers/              # PDFs o XML de artículos
├── src/                     # Scripts principales
│   ├── preprocess.py        # Extracción de texto y metadatos
│   ├── topic_model.py       # Topic modeling con BERTopic
│   ├── similarity.py        # Similitud semántica de abstracts
│   ├── ner_ack.py           # Reconocimiento de entidades en acknowledgements
│   ├── wikidata_enrich.py   # Enriquecimiento con Wikidata
│   ├── ror_enrich.py        # Enriquecimiento con ROR
│   └── build_kg.py          # Construcción del Knowledge Graph en RDF
├── streamlit_app/
│   ├── app.py               # App principal en Streamlit
│   └── kg_utils.py          # Funciones auxiliares para la app
├── requirements.txt         # Dependencias del proyecto
└── README.md
```

## Entorno virtual

Antes de instalar los requisitos, se recomienda crear y activar un entorno virtual:

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/macOS
source venv/bin/activate
```

## Instalación

Con el entorno virtual activo, instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Ejecución

1. Asegúrate de tener tus archivos PDF en la carpeta `data/papers/`
2. Ejecuta los scripts en el siguiente orden:

```bash
python src/preprocess.py
python src/topic_model.py
python src/similarity.py
python src/ner_ack.py
python src/wikidata_enrich.py
python src/ror_enrich.py
python src/build_kg.py
```

3. Lanza la app de visualización:

```bash
streamlit run streamlit_app/app.py
```

## Requisitos del sistema

- Python 3.10 o superior
- Acceso a internet (para enriquecer con Wikidata y ROR)
- pip actualizado

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.

---
