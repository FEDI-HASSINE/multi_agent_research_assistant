from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Literal
from core.state import AgentState
import os

from typing import Dict, Any, cast

# Modèle de sortie structurée pour le Manager
class ManagerDecision(BaseModel):
    next_agent: Literal["researcher", "writer", "critic", "finish"] = Field(
        description="Le prochain agent à appeler ou 'finish' si terminé."
    )
    reasoning: str = Field(description="La raison de cette décision.")

class ManagerAgent:
    def __init__(self):
        # On utilise un modèle léger pour l'orchestration
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def run(self, state: AgentState) -> Dict[str, Any]:
        print("--- MANAGER AGENT ---")
        
        mission = state["mission"]
        research_data = state.get("research_data", [])
        draft_report = state.get("draft_report", "")
        critique = state.get("critique_feedback", None)
        iteration = state.get("iteration_count", 0)

        # Logique de décision simple (peut être remplacée par le LLM si complexe)
        # Ici, on force un flux logique pour la démo, mais le LLM pourrait décider dynamiquement.
        
        system_prompt = """Tu es le Manager du projet. Ton rôle est d'orchestrer les agents.
        Flux standard : Researcher -> Writer -> Critic -> (Writer si révision nécessaire) -> Finish.
        
        État actuel :
        - Données recherche : {has_data}
        - Brouillon rapport : {has_draft}
        - Critique reçue : {has_critique}
        - Itération : {iteration}
        
        Décide de la prochaine étape.
        """
        
        has_data = "Oui" if research_data else "Non"
        has_draft = "Oui" if draft_report else "Non"
        has_critique = "Oui" if critique else "Non"

        prompt = system_prompt.format(
            has_data=has_data, 
            has_draft=has_draft, 
            has_critique=has_critique,
            iteration=iteration
        )

        # Appel au LLM avec sortie structurée
        structured_llm = self.llm.with_structured_output(ManagerDecision)
        decision = cast(ManagerDecision, structured_llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=f"Mission: {mission}")
        ]))

        print(f"Décision Manager : {decision.next_agent} ({decision.reasoning})")
        
        return {"next_step": decision.next_agent}
