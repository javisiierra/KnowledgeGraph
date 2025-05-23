import streamlit as st
import pandas as pd
import kg_utils

# Nuevas librerías para la visualización del grafo
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

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
    [
        "Papers by Topic",
        "Paper Explorer",
        "Similar Papers",
        "Organizations",
        "Knowledge Graph Visualization"  # Nueva sección
    ]
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

elif section == "Knowledge Graph Visualization":
    st.header("Knowledge Graph Visualization")
    st.write("Visualización interactiva de tópicos conectados con artículos del grafo.")

    # Obtener datos del grafo
    df_topics = kg_utils.get_papers_by_topic(g)

    if not df_topics.empty:
        # Filtro opcional por tópico
        unique_topics = df_topics['topic'].unique()
        selected_topic = st.selectbox("Selecciona un tópico para enfocar", ["Todos"] + list(unique_topics))

        if selected_topic != "Todos":
            df_topics = df_topics[df_topics['topic'] == selected_topic]

        G = nx.Graph()

        for _, row in df_topics.iterrows():
            topic = row['topic']
            title = row['title']
            paper_uri = row['paper']  # Añadido para obtener info extendida

            # Añadir nodo del tópico (caja)
            G.add_node(topic,
                       label=topic,
                       color='#ffcc00',
                       shape='box',
                       title=f'Tópico: {topic}',
                       value=1)

            # Obtener personas y organizaciones reconocidas para el paper
            people = kg_utils.get_people_by_paper(g, paper_uri)
            orgs = kg_utils.get_organizations_by_paper(g, paper_uri)

            people_names = ", ".join([p['name'] for p in people]) if people else "Ninguna"
            org_names = ", ".join([o['name'] for o in orgs]) if orgs else "Ninguna"

            # Construir tooltip con saltos de línea (no HTML)
            tooltip = (
                f"Artículo: {title}\n"
                f"Personas reconocidas: {people_names}\n"
                f"Organizaciones reconocidas: {org_names}"
            )

            # Añadir nodo del artículo (óvalo) con tooltip enriquecido
            G.add_node(title,
                       label=title,
                       color='#00ccff',
                       shape='ellipse',
                       title=tooltip,
                       value=1)

            G.add_edge(topic, title)

        # Ajustar tamaño de nodos según grado
        for node in G.nodes():
            G.nodes[node]['value'] = G.degree[node] * 2

        # Visualización con PyVis
        net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black", notebook=False)
        net.from_nx(G)

        # Mejorar física del grafo
        net.set_options("""
        const options = {
          "nodes": {
            "borderWidth": 2,
            "size": 25,
            "font": {"size": 14}
          },
          "edges": {
            "color": {"inherit": true},
            "smooth": false
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -8000,
              "centralGravity": 0.3,
              "springLength": 100,
              "springConstant": 0.04,
              "damping": 0.09
            },
            "minVelocity": 0.75
          }
        }
        """)

        # Exportar y mostrar en Streamlit
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            net.save_graph(tmp_file.name)
            html_path = tmp_file.name

        components.html(open(html_path, 'r', encoding='utf-8').read(), height=600)
        os.unlink(html_path)

    else:
        st.warning("No hay datos de tópicos y artículos para visualizar.")