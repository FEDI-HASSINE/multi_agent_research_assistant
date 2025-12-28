from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any, cast
from mcp.server import MCPServer
from mcp.client import MCPClient

# Modèles Pydantic
class CritiqueOutput(BaseModel):
    status: Literal["approved", "needs_revision"] = Field(description="Statut du rapport")
    issues: List[str] = Field(description="Liste des problèmes identifiés")
    suggestions: List[str] = Field(description="Suggestions d'amélioration")

# 1. Serveur MCP Critic
critic_server = MCPServer("CriticAgent")

@critic_server.tool()
def review_report(mission: str, draft: str) -> Dict[str, Any]:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = f"""Tu es un critique sévère. Analyse ce rapport sur : {mission}.
    Vérifie la clarté, la structure et si les sources sont citées.
    
    Rapport :
    {draft}
    """

    structured_llm = llm.with_structured_output(CritiqueOutput)
    feedback = cast(CritiqueOutput, structured_llm.invoke([HumanMessage(content=prompt)]))
    
    return feedback.model_dump()

# 2. Client LangGraph
class CriticAgent:
    def __init__(self):
        self.client = MCPClient(critic_server)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("--- CRITIC AGENT (via MCP) ---")
        draft = state["draft_report"]
        mission = state["mission"]
        iteration = state.get("iteration_count", 0)

        if iteration > 2:
            print("Limite d'itérations atteinte. Approbation forcée.")
            return {
                "critique_feedback": {"status": "approved", "issues": [], "suggestions": []},
                "iteration_count": iteration + 1
            }

        # Appel MCP
        feedback_dict = self.client.call("review_report", {
            "mission": mission,
            "draft": draft
        })
        
        print(f"Critique Status: {feedback_dict['status']}")
        
        return {
            "critique_feedback": feedback_dict,
            "iteration_count": iteration + 1
        }
