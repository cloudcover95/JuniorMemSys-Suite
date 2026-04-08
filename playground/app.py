# junior-memsys-suite/playground/app.py
import streamlit as st
from junior_memsys_suite.core.palace import MemoryPalace
from junior_memsys_suite.core.knowledge_graph import TopologicalKnowledgeGraph

st.set_page_config(page_title="JCLLC Mem Sys — TDA Sandbox", layout="wide")
st.title("JCLLC Topological Memory Palace")

palace = MemoryPalace()
kg = TopologicalKnowledgeGraph()

tab1, tab2, tab3 = st.tabs(["Ingest Tensors", "Gamma Signal Search", "Knowledge Graph Protocol"])

with tab1:
    content = st.text_area("Raw Context String")
    if st.button("Etch into TDA Mesh"):
        success = palace.store("alpha", "playground", "sandbox", content)
        if success:
            st.success("State etched successfully. Q-Mark validated.")
        else:
            st.error("Signal rejected. Sub-threshold Q-Mark.")

with tab2:
    query = st.text_input("Semantic Vector Query")
    if st.button("Execute Bit Drift Inference"):
        results = palace.semantic_search(query, "alpha")
        st.write(f"Yield: {len(results)} active nodes.")
        for r in results:
            st.json(r)