import spacy
import json
import os

def load_acknowledgements():
    acks, ids = [], []
    for file in os.listdir("data/processed"):
        with open(f"data/processed/{file}") as f:
            data = json.load(f)
            acks.append(data['acknowledgements'])
            ids.append(data['id'])
    return ids, acks

def extract_entities():
    nlp = spacy.load("en_core_web_sm")
    ids, acks = load_acknowledgements()
    all_entities = {}
    for paper_id, ack in zip(ids, acks):
        doc = nlp(ack)
        persons = list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"]))
        orgs = list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"]))
        all_entities[paper_id] = {"persons": persons, "organizations": orgs}
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/entities.json", "w") as f:
        json.dump(all_entities, f, indent=2)
    print("Entity extraction completed and saved.")

if __name__ == "__main__":
    extract_entities()