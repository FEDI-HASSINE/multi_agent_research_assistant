from typing import TypedDict, List, Optional, Dict, Any

class AgentState(TypedDict):
    mission: str                # La mission initiale de l'utilisateur
    research_data: List[str]    # Liste des informations trouvées
    draft_report: str           # Le rapport en cours de rédaction
    critique_feedback: Optional[Dict[str, Any]] # Le retour du critique
    next_step: str              # La prochaine étape décidée par le Manager
    iteration_count: int        # Pour éviter les boucles infinies
