import rdflib
import json
from urllib.parse import quote
import os

def add_person(g, EX, FOAF, WD, person):
    if person.get("wikidata_id"):
        person_uri = WD[person["wikidata_id"]]
    else:
        safe_name = quote(person["name"].replace(" ", "_"))
        person_uri = EX[f"person_{safe_name}"]
    g.add((person_uri, rdflib.RDF.type, FOAF.Person))
    g.add((person_uri, FOAF.name, rdflib.Literal(person["name"])))
    return person_uri

def add_organization(g, EX, FOAF, WD, ROR, org):
    if org.get("wikidata_id"):
        org_uri = WD[org["wikidata_id"]]
    elif org.get("ror_id"):
        org_uri = ROR[org["ror_id"]]
    else:
        safe_name = quote(org["name"].replace(" ", "_"))
        org_uri = EX[f"org_{safe_name}"]
    g.add((org_uri, rdflib.RDF.type, FOAF.Organization))
    g.add((org_uri, FOAF.name, rdflib.Literal(org["name"])))
    return org_uri

def create_kg():
    """Create RDF Knowledge Graph from processed data."""
    g = rdflib.Graph()
    
    # Define namespaces
    EX = rdflib.Namespace("http://example.org/")
    DCTERMS = rdflib.Namespace("http://purl.org/dc/terms/")
    FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
    WD = rdflib.Namespace("http://www.wikidata.org/entity/")
    ROR = rdflib.Namespace("https://ror.org/")
    
    # Bind prefixes
    g.bind("ex", EX)
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("wd", WD)
    g.bind("ror", ROR)
    
    # Load processed paper metadata
    papers_metadata = {}
    processed_dir = "data/processed"
    
    if not os.path.exists(processed_dir):
        print("Error: processed data directory not found")
        return
    
    for file in os.listdir(processed_dir):
        if file.endswith(".json"):
            with open(os.path.join(processed_dir, file)) as f:
                data = json.load(f)
                papers_metadata[data['id']] = data
    
    # Load additional data with error handling
    try:
        with open("data/output/topic_assignments.json") as f:
            topic_data = json.load(f)
    except FileNotFoundError:
        print("Warning: topic_assignments.json not found")
        topic_data = {}
    
    try:
        with open("data/output/similar_pairs.json") as f:
            similar_pairs = json.load(f)
    except FileNotFoundError:
        print("Warning: similar_pairs.json not found")
        similar_pairs = []
    
    # Load enriched data if available
    try:
        with open("data/output/enriched_wikidata.json") as f:
            wd_data = json.load(f)
    except FileNotFoundError:
        print("Warning: enriched_wikidata.json not found")
        wd_data = {}
    
    try:
        with open("data/output/enriched_ror.json") as f:
            ror_data = json.load(f)
    except FileNotFoundError:
        print("Warning: enriched_ror.json not found")
        ror_data = {}
    
    # Create triples for each paper
    for paper_id, metadata in papers_metadata.items():
        paper_safe_id = quote(paper_id)
        paper_uri = EX[f"paper_{paper_safe_id}"]
        
        # Basic paper metadata
        g.add((paper_uri, rdflib.RDF.type, EX.Paper))
        g.add((paper_uri, DCTERMS.title, rdflib.Literal(metadata['title'])))
        g.add((paper_uri, DCTERMS.abstract, rdflib.Literal(metadata['abstract'])))
        g.add((paper_uri, EX.identifier, rdflib.Literal(paper_id)))
        
        # Authors con URI persistente
        for author in metadata.get('authors', []):
            person_uri = add_person(g, EX, FOAF, WD, {"name": author})
            g.add((paper_uri, DCTERMS.creator, person_uri))
        
        # Topic assignment
        if paper_id in topic_data:
            topic_uri = EX[f"topic_{topic_data[paper_id]}"]
            g.add((paper_uri, EX.belongs_to_topic, topic_uri))
            g.add((topic_uri, rdflib.RDF.type, EX.Topic))
            g.add((topic_uri, DCTERMS.identifier, rdflib.Literal(str(topic_data[paper_id]))))
        
        # Reconocimiento de entidades (personas y organizaciones)
        if paper_id in wd_data:
            for person in wd_data[paper_id].get("persons", []):
                person_uri = add_person(g, EX, FOAF, WD, person)
                g.add((paper_uri, EX.acknowledges, person_uri))
            
            for org in wd_data[paper_id].get("organizations", []):
                org_uri = add_organization(g, EX, FOAF, WD, ROR, org)
                g.add((paper_uri, EX.acknowledges, org_uri))
        
        if paper_id in ror_data:
            for org in ror_data[paper_id]:
                org_uri = add_organization(g, EX, FOAF, WD, ROR, org)
                g.add((paper_uri, EX.acknowledges, org_uri))
    
    # Similarity relationships
    for pair in similar_pairs:
        p1_safe = quote(pair['paper1'])
        p2_safe = quote(pair['paper2'])
        p1 = EX[f"paper_{p1_safe}"]
        p2 = EX[f"paper_{p2_safe}"]
        g.add((p1, EX.similar_to, p2))
        g.add((p2, EX.similar_to, p1))  # Make bidirectional
    
    # Save the graph
    g.serialize(destination="./data/output/kg.ttl", format="turtle")
    print(f"KG created with {len(g)} triples")

if __name__ == "__main__":
    create_kg()