import rdflib
import pandas as pd

def load_kg(path='./data/output/kg.ttl'):
    g = rdflib.Graph()
    g.parse(path, format='ttl')
    return g

def get_papers_by_topic(g):
    query = """
    SELECT ?paper ?topic WHERE {
        ?paper <http://example.org/belongs_to_topic> ?topic .
    }
    """
    results = g.query(query)
    data = [{'paper': str(r['paper']), 'topic': str(r['topic'])} for r in results]
    return pd.DataFrame(data)

def get_similar_papers(g, paper_uri):
    query = f"""
    SELECT ?similar WHERE {{
        <{paper_uri}> <http://example.org/similar_to> ?similar .
    }}
    """
    results = g.query(query)
    return [str(r['similar']) for r in results]

def get_organizations(g):
    query = """
    SELECT ?org WHERE {
        ?paper <http://example.org/acknowledges> ?org .
        FILTER regex(str(?org), "ror.org")
    }
    """
    results = g.query(query)
    return list(set(str(r['org']) for r in results))