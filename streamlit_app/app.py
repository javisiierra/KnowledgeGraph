import streamlit as st
import pandas as pd
import kg_utils

st.set_page_config(layout="wide", page_title="Research Knowledge Graph Explorer")
st.title("Research Knowledge Graph Explorer")

# Load Knowledge Graph
@st.cache_resource
def load_knowledge_graph():
    """Load the knowledge graph with caching."""
    return kg_utils.load_kg()

g = load_knowledge_graph()

# Sidebar navigation
st.sidebar.header("Navigation")
section = st.sidebar.selectbox(
    "Select Section",
    ["Papers by Topic", "Paper Explorer", "Similar Papers", "Organizations"]
)

# Section 1: Papers by Topic
if section == "Papers by Topic":
    st.header("Papers by Topic")
    df_topics = kg_utils.get_papers_by_topic(g)
    
    if not df_topics.empty:
        topics = df_topics['topic'].unique()
        selected_topic = st.selectbox("Select Topic", sorted(topics))
        
        filtered = df_topics[df_topics['topic'] == selected_topic]
        st.write(f"### Papers in {selected_topic}")
        
        for _, row in filtered.iterrows():
            st.write(f"**{row['title']}**")
            paper_details = kg_utils.get_paper_details(g, row['paper'])
            if paper_details:
                with st.expander("View Abstract"):
                    st.write(paper_details['abstract'])
    else:
        st.warning("No topics found in the knowledge graph.")

# Section 2: Paper Explorer
elif section == "Paper Explorer":
    st.header("Paper Explorer")
    
    all_papers = kg_utils.get_all_papers(g)
    
    if all_papers:
        paper_dict = {p['title']: p['uri'] for p in all_papers}
        selected_title = st.selectbox("Select Paper", list(paper_dict.keys()))
        selected_uri = paper_dict[selected_title]
        
        paper_details = kg_utils.get_paper_details(g, selected_uri)
        if paper_details:
            st.write("### Paper Details")
            st.write(f"**Title:** {paper_details['title']}")
            st.write("**Abstract:**")
            st.write(paper_details['abstract'])
    else:
        st.warning("No papers found in the knowledge graph.")

# Section 3: Similar Papers
elif section == "Similar Papers":
    st.header("Find Similar Papers")
    
    all_papers = kg_utils.get_all_papers(g)
    
    if all_papers:
        paper_dict = {p['title']: p['uri'] for p in all_papers}
        selected_title = st.selectbox("Select Paper", list(paper_dict.keys()))
        selected_uri = paper_dict[selected_title]
        
        similar_papers = kg_utils.get_similar_papers(g, selected_uri)
        
        if similar_papers:
            st.write(f"### Papers similar to: {selected_title}")
            for paper in similar_papers:
                st.write(f"- **{paper['title']}**")
        else:
            st.info("No similar papers found for this selection.")
    else:
        st.warning("No papers found in the knowledge graph.")

# Section 4: Organizations
elif section == "Organizations":
    st.header("Organizations Acknowledged in Papers")
    
    orgs = kg_utils.get_organizations(g)
    
    if orgs:
        df_orgs = pd.DataFrame(orgs)
        
        # Display statistics
        st.write(f"Total organizations found: {len(orgs)}")
        
        # Organization table
        st.dataframe(df_orgs, height=400)
        
        # Filter by type
        ror_orgs = [o for o in orgs if 'ror.org' in o['uri']]
        wd_orgs = [o for o in orgs if 'wikidata' in o['uri']]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"ROR organizations: {len(ror_orgs)}")
        with col2:
            st.write(f"Wikidata organizations: {len(wd_orgs)}")
    else:
        st.warning("No organizations found in the knowledge graph.")