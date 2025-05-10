import requests
import json
import time

def search_ror(name):
    """Search for an organization in ROR database."""
    url = "https://api.ror.org/organizations"
    params = {"query": name}
    headers = {
        'User-Agent': 'Research-KG-Project/1.0 (research-project)'
    }
    
    try:
        # Add timeout and headers
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            results = data.get("items", [])
            if results:
                return results[0]["id"], results[0]["name"]
        else:
            print(f"ROR API returned status code: {response.status_code} for '{name}'")
        
    except requests.exceptions.RequestException as e:
        print(f"Error searching ROR for '{name}': {e}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON response for '{name}': {e}")
    
    return None, None

def enrich_ror():
    """Enrich organizations with ROR identifiers."""
    try:
        with open("data/output/entities.json") as f:
            entities = json.load(f)
    except FileNotFoundError:
        print("entities.json not found. Skipping ROR enrichment.")
        return
    
    enriched = {}
    
    # Process each paper's organizations
    for i, (paper_id, data) in enumerate(entities.items()):
        print(f"Processing paper {i+1}/{len(entities)}: {paper_id}")
        enriched[paper_id] = []
        
        for org in data["organizations"]:
            print(f"  Searching for organization: {org}")
            
            # Add delay to avoid rate limiting
            time.sleep(0.5)
            
            ror_id, ror_name = search_ror(org)
            
            if ror_id:
                print(f"    Found: {ror_name} ({ror_id})")
            else:
                print(f"    Not found in ROR")
            
            enriched[paper_id].append({
                "name": org, 
                "ror_id": ror_id,
                "ror_name": ror_name if ror_name else org
            })
    
    # Save results
    with open("data/output/enriched_ror.json", "w") as f:
        json.dump(enriched, f, indent=2)
    
    print("\nROR enrichment completed and saved.")

if __name__ == "__main__":
    enrich_ror()