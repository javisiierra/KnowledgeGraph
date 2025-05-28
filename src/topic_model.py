from bertopic import BERTopic
import json
import os

def load_abstracts():
    abstracts, ids = [], []
    for file in os.listdir("data/processed"):
        with open(f"data/processed/{file}") as f:
            data = json.load(f)
            abstracts.append(data['abstract'])
            ids.append(data['id'])
    return ids, abstracts

def run_topic_model():
    ids, abstracts = load_abstracts()
    topic_model = BERTopic(min_topic_size=2)
    topics, _ = topic_model.fit_transform(abstracts)
    os.makedirs("data/output", exist_ok=True)
    topic_model.save("data/output/bertopic_model")
    topic_assignments = dict(zip(ids, topics))
    with open("data/output/topic_assignments.json", "w") as f:
        json.dump(topic_assignments, f, indent=2)
    print("Topic modeling completed and saved.")

if __name__ == "__main__":
    run_topic_model()