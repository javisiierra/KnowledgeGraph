import requests
import json

def search_ror(name):
    url = f"https://api.ror.org/organizations"
    params = {"query": name}
    response = requests.get(url, params=params)
    results = response.json().get("items", [])
    if results:
        return results[0]["id"], results[0]["name"]
    return None, None

def enrich_ror():
    with open("data/output/entities.json") as f:
        entities = json.load(f)
    enriched = {}
    for paper_id, data in entities.items():
        enriched[paper_id] = []
        for org in data["organizations"]:
            ror_id, ror_name = search_ror(org)
            enriched[paper_id].append({"name": org, "ror_id": ror_id})
    with open("data/output/enriched_ror.json", "w") as f:
        json.dump(enriched, f, indent=2)
    print("ROR enrichment completed and saved.")

if __name__ == "__main__":
    enrich_ror()