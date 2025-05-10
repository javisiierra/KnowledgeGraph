import rdflib
import pandas as pd

def load_kg(path='./data/output/kg.ttl'):
    """Load the knowledge graph from TTL file."""
    g = rdflib.Graph()
    g.parse(path, format='ttl')
    return g

def get_papers_by_topic(g):
    """Get all papers grouped by their topics."""
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?paper ?topic ?title WHERE {
        ?paper ex:belongs_to_topic ?topic .
        ?paper dcterms:title ?title .
    }
    """
    results = g.query(query)
    data = []
    for r in results:
        topic_id = str(r['topic']).split('_')[-1]
        data.append({
            'paper': str(r['paper']), 
            'topic': f"Topic {topic_id}",
            'title': str(r['title'])
        })
    return pd.DataFrame(data)

def get_paper_details(g, paper_uri):
    """Get detailed information about a specific paper."""
    query = f"""
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX ex: <http://example.org/>
    
    SELECT ?title ?abstract WHERE {{
        <{paper_uri}> dcterms:title ?title ;
                      dcterms:abstract ?abstract .
    }}
    """
    results = g.query(query)
    for r in results:
        return {
            'title': str(r['title']),
            'abstract': str(r['abstract'])
        }
    return None

def get_similar_papers(g, paper_uri):
    """Get papers similar to a given paper."""
    query = f"""
    PREFIX ex: <http://example.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?similar ?title WHERE {{
        <{paper_uri}> ex:similar_to ?similar .
        ?similar dcterms:title ?title .
    }}
    """
    results = g.query(query)
    return [{'uri': str(r['similar']), 'title': str(r['title'])} for r in results]

def get_organizations(g):
    """Get all organizations mentioned in acknowledgements."""
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT DISTINCT ?org ?name WHERE {
        ?paper ex:acknowledges ?org .
        OPTIONAL { ?org foaf:name ?name }
        FILTER(regex(str(?org), "ror.org") || regex(str(?org), "wikidata"))
    }
    """
    results = g.query(query)
    orgs = []
    for r in results:
        org_info = {
            'uri': str(r['org']),
            'name': str(r['name']) if r['name'] else 'Unknown'
        }
        orgs.append(org_info)
    return orgs

def get_all_papers(g):
    """Get all papers in the knowledge graph."""
    query = """
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX ex: <http://example.org/>
    
    SELECT ?paper ?title WHERE {
        ?paper a ex:Paper ;
               dcterms:title ?title .
    }
    """
    results = g.query(query)
    return [{'uri': str(r['paper']), 'title': str(r['title'])} for r in results]