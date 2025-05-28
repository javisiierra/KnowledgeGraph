import rdflib
import pandas as pd
from urllib.parse import unquote

# Loads the RDF graph from disk
def load_kg(path="./data/output/kg.ttl"):
    g = rdflib.Graph()
    g.parse(path, format="turtle")
    return g

# Gets all papers with their assigned topics (for DataFrame)
def get_papers_by_topic(g):
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?paper ?title ?topic ?topic_id WHERE {
      ?paper a ex:Paper ;
             dcterms:title ?title .
      OPTIONAL {
        ?paper ex:belongs_to_topic ?topic .
        ?topic dcterms:identifier ?topic_id .
      }
    }
    """
    qres = g.query(query)

    rows = []
    for row in qres:
        paper = str(row.paper)
        title = str(row.title)
        topic_uri = str(row.topic) if row.topic else None
        topic_id = str(row.topic_id) if row.topic_id else None
        
        # Extract topic name from URI if exists
        topic_name = None
        if topic_uri:
            topic_name = topic_uri.split("topic_")[-1]
        
        rows.append({
            "paper": paper,
            "title": title,
            "topic_uri": topic_uri,
            "topic": topic_name,
            "topic_id": topic_id
        })
    return pd.DataFrame(rows)

# Gets all papers (title and URI) for dropdown lists
def get_all_papers(g):
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?paper ?title WHERE {
      ?paper a ex:Paper ;
             dcterms:title ?title .
    }
    """
    qres = g.query(query)

    papers = []
    for row in qres:
        papers.append({
            "uri": str(row.paper),
            "title": str(row.title)
        })
    return papers

# Gets details of a paper given its URI
def get_paper_details(g, paper_uri):
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    SELECT ?title ?abstract WHERE {
      BIND (<%s> AS ?paper)
      ?paper dcterms:title ?title ;
             dcterms:abstract ?abstract .
    }
    """ % paper_uri

    qres = g.query(query)
    for row in qres:
        return {
            "title": str(row.title),
            "abstract": str(row.abstract)
        }
    return None

# Gets papers similar to a given one (by URI)
def get_similar_papers(g, paper_uri):
    query = """
    PREFIX ex: <http://example.org/>
    
    SELECT ?similar ?title WHERE {
      BIND (<%s> AS ?paper)
      ?paper ex:similar_to ?similar .
      ?similar <http://purl.org/dc/terms/title> ?title .
    }
    """ % paper_uri

    qres = g.query(query)
    similars = []
    for row in qres:
        similars.append({
            "uri": str(row.similar),
            "title": str(row.title)
        })
    return similars

# Gets organizations recognized in all papers
def get_organizations(g):
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT DISTINCT ?org ?name WHERE {
      ?paper ex:acknowledges ?org .
      ?org a foaf:Organization ;
           foaf:name ?name .
    }
    """
    qres = g.query(query)
    orgs = []
    for row in qres:
        orgs.append({
            "uri": str(row.org),
            "name": str(row.name)
        })
    return orgs

# Gets people recognized in a paper given its URI
def get_people_by_paper(g, paper_uri):
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT DISTINCT ?person ?name WHERE {
      BIND (<%s> AS ?paper)
      ?paper ex:acknowledges ?person .
      ?person a foaf:Person ;
              foaf:name ?name .
    }
    """ % paper_uri

    qres = g.query(query)
    people = []
    for row in qres:
        people.append({
            "uri": str(row.person),
            "name": str(row.name)
        })
    return people

# Gets organizations recognized in a paper given its URI
def get_organizations_by_paper(g, paper_uri):
    query = """
    PREFIX ex: <http://example.org/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT DISTINCT ?org ?name WHERE {
      BIND (<%s> AS ?paper)
      ?paper ex:acknowledges ?org .
      ?org a foaf:Organization ;
           foaf:name ?name .
    }
    """ % paper_uri

    qres = g.query(query)
    orgs = []
    for row in qres:
        orgs.append({
            "uri": str(row.org),
            "name": str(row.name)
        })
    return orgs