import streamlit as st
import pandas as pd
import os
import sys
from typing import cast

# Ajout de la racine du projet au PYTHONPATH pour gérer les imports correctement
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.langgraph_orchestrator import MultiAgentOrchestrator
from core.logger import Logger, MCP_LOG_FILE
from core.state import AgentState
from dotenv import load_dotenv

# Configuration de la page
st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🤖", layout="wide")
load_dotenv()

st.title("🤖 Multi-Agent Research Assistant")
st.markdown("### Orchestration par LangGraph & Communication via MCP")

# Sidebar pour les stats
with st.sidebar:
    st.header("📊 Observabilité (Agent Ops)")
    if st.button("Rafraîchir les logs"):
        pass # Le rerun rechargera les données
    
    if os.path.exists(MCP_LOG_FILE):
        logs = Logger.get_mcp_logs()
        if logs:
            df = pd.DataFrame(logs)
            st.metric("Total Appels MCP", len(df))
            st.metric("Temps moyen (ms)", round(df["latency_ms"].mean(), 2))
            
            st.subheader("Dernières erreurs")
            errors = df[df["status"] == "error"]
            if not errors.empty:
                st.error(f"{len(errors)} erreurs détectées")
                st.dataframe(errors[["timestamp", "agent_source", "error"]].tail(5))
            else:
                st.success("Aucune erreur récente")
        else:
            st.info("Aucun log disponible")

# Zone principale
mission = st.text_input("📝 Entrez votre mission de recherche :", "L'avenir des agents autonomes en 2025")

if st.button("🚀 Lancer la mission"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Clé API OpenAI manquante dans .env")
    else:
        orchestrator = MultiAgentOrchestrator()
        
        # Conteneurs pour l'affichage progressif
        status_container = st.container()
        
        with st.status("Exécution du workflow en cours...", expanded=True) as status:
            # On utilise stream pour voir les étapes
            initial_state = cast(AgentState, {
                "mission": mission,
                "research_data": [],
                "draft_report": "",
                "critique_feedback": None,
                "next_step": "manager",
                "iteration_count": 0
            })
            
            final_state = None
            
            # Stream des événements du graphe
            for event in orchestrator.workflow.stream(initial_state):
                for key, value in event.items():
                    st.write(f"👉 **Agent actif : {key.capitalize()}**")
                    
                    # Affichage contextuel selon l'agent
                    if key == "researcher":
                        st.info(f"🔍 Données trouvées : {len(value.get('research_data', []))} sources")
                    elif key == "writer":
                        st.markdown("✍️ **Brouillon généré**")
                    elif key == "critic":
                        feedback = value.get("critique_feedback", {})
                        status_code = feedback.get("status")
                        if status_code == "approved":
                            st.success("✅ Rapport approuvé par le critique")
                        else:
                            st.warning(f"⚠️ Révision demandée : {len(feedback.get('issues', []))} problèmes")
                    elif key == "manager":
                        next_step = value.get("next_step")
                        st.caption(f"🧠 Manager décide : {next_step}")
            
                # On garde le dernier état comme final
                final_state = list(event.values())[0]

            status.update(label="Mission terminée !", state="complete", expanded=False)

        # Affichage du résultat final
        if final_state and "draft_report" in final_state:
            st.divider()
            st.subheader("📄 Rapport Final")
            report = final_state["draft_report"]
            st.markdown(report)
            
            st.download_button(
                label="📥 Télécharger le rapport (Markdown)",
                data=report,
                file_name="rapport_recherche.md",
                mime="text/markdown"
            )
