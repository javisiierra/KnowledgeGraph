import rdflib
import json
from urllib.parse import quote

def create_kg():
    g = rdflib.Graph()
    EX = rdflib.Namespace("http://example.org/")
    WD = rdflib.Namespace("http://www.wikidata.org/entity/")
    ROR = rdflib.Namespace("https://ror.org/")

    g.bind("ex", EX)
    g.bind("wd", WD)
    g.bind("ror", ROR)

    # Cargar los archivos JSON
    with open("data/output/topic_assignments.json") as f:
        topic_data = json.load(f)
    with open("data/output/similar_pairs.json") as f:
        similar_pairs = json.load(f)
    with open("data/output/enriched_wikidata.json") as f:
        wd_data = json.load(f)
    with open("data/output/enriched_ror.json") as f:
        ror_data = json.load(f)

    # Crear las triples en el grafo
    for paper_id, topic in topic_data.items():
        # Normalizar el ID del paper para evitar espacios y caracteres especiales
        paper_safe_id = quote(paper_id)
        paper_uri = EX[f"paper_{paper_safe_id}"]
        topic_uri = EX[f"topic_{topic}"]
        g.add((paper_uri, EX.belongs_to_topic, topic_uri))
        
        # Personas
        for person in wd_data[paper_id]["persons"]:
            if person["wikidata_id"]:
                person_uri = WD[person["wikidata_id"]]
                g.add((paper_uri, EX.acknowledges, person_uri))
        
        # Organizaciones
        for org in wd_data[paper_id]["organizations"]:
            if org["wikidata_id"]:
                org_uri = WD[org["wikidata_id"]]
                g.add((paper_uri, EX.acknowledges, org_uri))
        for org in ror_data[paper_id]:
            if org["ror_id"]:
                org_uri = ROR[org["ror_id"]]
                g.add((paper_uri, EX.acknowledges, org_uri))

    # Relaciones de similitud entre artículos
    for pair in similar_pairs:
        p1_safe = quote(pair['paper1'])
        p2_safe = quote(pair['paper2'])
        p1 = EX[f"paper_{p1_safe}"]
        p2 = EX[f"paper_{p2_safe}"]
        g.add((p1, EX.similar_to, p2))

    # Serializar el grafo en formato Turtle en la ruta correcta
    g.serialize(destination="./data/output/kg.ttl", format="turtle")
    print("KG with external IDs saved.")

if __name__ == "__main__":
    create_kg()