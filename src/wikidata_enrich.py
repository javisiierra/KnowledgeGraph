import requests
import json

def search_wikidata(name):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": name,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)
    results = response.json().get("search", [])
    if results:
        return results[0]["id"], results[0]["label"]
    return None, None

def enrich_entities():
    with open("data/output/entities.json") as f:
        entities = json.load(f)
    enriched = {}
    for paper_id, data in entities.items():
        enriched[paper_id] = {"persons": [], "organizations": []}
        for person in data["persons"]:
            qid, label = search_wikidata(person)
            enriched[paper_id]["persons"].append({"name": person, "wikidata_id": qid})
        for org in data["organizations"]:
            qid, label = search_wikidata(org)
            enriched[paper_id]["organizations"].append({"name": org, "wikidata_id": qid})
    with open("data/output/enriched_wikidata.json", "w") as f:
        json.dump(enriched, f, indent=2)
    print("Wikidata enrichment completed and saved.")

if __name__ == "__main__":
    enrich_entities()