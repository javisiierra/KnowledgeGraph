import streamlit as st
import pandas as pd
import kg_utils

st.set_page_config(layout="wide")
st.title("Knowledge Graph Explorer")

# Load KG
g = kg_utils.load_kg()

# Section 1: Papers by Topic
st.header("Papers by Topic")
df_topics = kg_utils.get_papers_by_topic(g)
topics = df_topics['topic'].unique()
selected_topic = st.selectbox("Select Topic", topics)
filtered = df_topics[df_topics['topic'] == selected_topic]
st.write(f"Papers in {selected_topic}", filtered['paper'].tolist())

# Section 2: Similar Papers
st.header("Find Similar Papers")
selected_paper = st.selectbox("Select Paper", df_topics['paper'].unique())
similar_papers = kg_utils.get_similar_papers(g, selected_paper)
st.write(f"Papers similar to {selected_paper}", similar_papers)

# Section 3: Organizations (optional: map)
st.header("Organizations (by ROR)")
orgs = kg_utils.get_organizations(g)
st.write(f"Organizations acknowledged", orgs)