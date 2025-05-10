#!/usr/bin/env python3
"""Execute the complete pipeline for knowledge graph construction."""

import subprocess
import sys
import os

def run_step(name, command, required=True):
    """Execute a pipeline step."""
    print(f"\n{'='*50}")
    print(f"Running: {name}")
    print(f"{'='*50}")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        if required:
            print(f"ERROR: Failed at {name}")
            sys.exit(1)
        else:
            print(f"WARNING: {name} failed but continuing...")
            return False
    
    print(f"✓ {name} completed")
    return True

def main():
    """Main pipeline execution."""
    # Ensure directories exist
    os.makedirs("data/papers", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    
    # Pipeline steps (name, command, is_required)
    steps = [
        ("Preprocessing", "python src/preprocess.py", True),
        ("Topic Modeling", "python src/topic_model.py", True),
        ("Similarity Analysis", "python src/similarity.py", True),
        ("Named Entity Recognition", "python src/ner_ack.py", True),
        ("Wikidata Enrichment", "python src/wikidata_enrich.py", False),
        ("ROR Enrichment", "python src/ror_enrich.py", False),
        ("Knowledge Graph Construction", "python src/build_kg.py", True),
    ]
    
    # Execute each step
    success_count = 0
    for name, command, required in steps:
        if run_step(name, command, required):
            success_count += 1
    
    print("\n" + "="*50)
    print(f"Pipeline completed! {success_count}/{len(steps)} steps successful")
    print("To visualize results, run:")
    print("streamlit run streamlit_app/app.py")
    print("="*50)

if __name__ == "__main__":
    main()