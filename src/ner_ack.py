import json
import os
from transformers import pipeline

def load_acknowledgements():
    acks, ids = [], []
    for file in os.listdir("./data/processed"):
        with open(f"data/processed/{file}") as f:
            data = json.load(f)
            acks.append(data['acknowledgements'])
            ids.append(data['id'])
    return ids, acks

def detokenize(text):
    tokens = text.split()
    new_text = ""
    for token in tokens:
        if token.startswith("##"):
            new_text += token[2:]
        else:
            if new_text:
                new_text += " " + token
            else:
                new_text += token
    return new_text

def extract_entities():
    # We use a NER model from Hugging Face
    ner = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

    ids, acks = load_acknowledgements()
    all_entities = {}

    for paper_id, ack in zip(ids, acks):
        results = ner(ack)

        persons = set()
        organizations = set()

        for ent in results:
            label = ent["entity_group"]
            text = detokenize(ent["word"])
            if label == "PER":
                persons.add(text)
            elif label == "ORG":
                organizations.add(text)

        all_entities[paper_id] = {
            "persons": sorted(persons),
            "organizations": sorted(organizations)
        }

    os.makedirs("./data/output", exist_ok=True)
    with open("./data/output/entities.json", "w") as f:
        json.dump(all_entities, f, indent=2)

    print("Entity extraction (via Hugging Face) completed and saved.")

if __name__ == "__main__":
    extract_entities()