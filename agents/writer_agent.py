from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
from mcp.server import MCPServer
from mcp.client import MCPClient

# 1. Serveur MCP Writer
writer_server = MCPServer("WriterAgent")

@writer_server.tool()
def write_report(mission: str, data: List[str], critique: Dict[str, Any], current_draft: str) -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    prompt = f"""Tu es un rédacteur expert. Rédige un rapport structuré en Markdown.
    
    Sujet : {mission}
    
    Sources disponibles :
    {data}
    """

    if critique and critique.get("status") == "needs_revision":
        prompt += f"\n\nATTENTION : Tu dois corriger le rapport précédent en suivant ces remarques :\n{critique.get('issues')}\nSuggestions: {critique.get('suggestions')}"
        prompt += f"\n\nAncien brouillon :\n{current_draft}"

    response = llm.invoke([HumanMessage(content=prompt)])
    return str(response.content)

# 2. Client LangGraph
class WriterAgent:
    def __init__(self):
        self.client = MCPClient(writer_server)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("--- WRITER AGENT (via MCP) ---")
        
        # Appel MCP
        draft = self.client.call("write_report", {
            "mission": state["mission"],
            "data": state["research_data"],
            "critique": state.get("critique_feedback", {}),
            "current_draft": state.get("draft_report", "")
        })
        
        return {"draft_report": draft}
