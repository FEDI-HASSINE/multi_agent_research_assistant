from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
from mcp.server import MCPServer
from mcp.client import MCPClient
from tools.search_tool import search_web

# 1. Création du Serveur MCP pour le Researcher
researcher_server = MCPServer("ResearcherAgent")

@researcher_server.tool()
def perform_research(mission: str) -> List[str]:
    """Logique interne de recherche encapsulée dans un outil MCP"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Analyser la mission
    prompt = f"Extrais 3 mots-clés de recherche pour cette mission : {mission}"
    response = llm.invoke([HumanMessage(content=prompt)])
    keywords = str(response.content)
    
    # Exécuter la recherche
    return search_web(keywords)

# 2. L'Agent LangGraph devient un Client MCP
class ResearcherAgent:
    def __init__(self):
        self.client = MCPClient(researcher_server)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("--- RESEARCHER AGENT (via MCP) ---")
        mission = state["mission"]
        
        # Appel via le protocole MCP
        results = self.client.call("perform_research", {"mission": mission})
        
        return {"research_data": results}
