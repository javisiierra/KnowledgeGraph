from sentence_transformers import SentenceTransformer, util
import json
import os
import itertools

def load_abstracts():
    abstracts, ids = [], []
    for file in os.listdir("data/processed"):
        with open(f"data/processed/{file}") as f:
            data = json.load(f)
            abstracts.append(data['abstract'])
            ids.append(data['id'])
    return ids, abstracts

def compute_similarity():
    ids, abstracts = load_abstracts()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(abstracts, convert_to_tensor=True)
    pairs = list(itertools.combinations(range(len(ids)), 2))
    similar_pairs = []
    for i, j in pairs:
        sim = util.pytorch_cos_sim(embeddings[i], embeddings[j])
        if sim > 0.7:
            similar_pairs.append({
                "paper1": ids[i],
                "paper2": ids[j],
                "similarity": float(sim)
            })
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/similar_pairs.json", "w") as f:
        json.dump(similar_pairs, f, indent=2)
    print("Similarity computation completed and saved.")

if __name__ == "__main__":
    compute_similarity()