from langgraph.graph import StateGraph, END
from core.state import AgentState
from core.logger import Logger
from agents.manager_agent import ManagerAgent
from agents.researcher_agent import ResearcherAgent
from agents.writer_agent import WriterAgent
from agents.critic_agent import CriticAgent
from typing import cast

class MultiAgentOrchestrator:
    def __init__(self):
        self.manager = ManagerAgent()
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.critic = CriticAgent()
        
        self.workflow = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Wrappers pour le tracing
        def trace_node(node_name, func):
            def wrapper(state):
                Logger.log_trace_event(node_name, "start", {"iteration": state.get("iteration_count")})
                result = func(state)
                Logger.log_trace_event(node_name, "end", {"result_keys": list(result.keys())})
                return result
            return wrapper

        # 1. Ajouter les noeuds avec tracing
        workflow.add_node("manager", trace_node("ManagerAgent", self.manager.run))
        workflow.add_node("researcher", trace_node("ResearcherAgent", self.researcher.run))
        workflow.add_node("writer", trace_node("WriterAgent", self.writer.run))
        workflow.add_node("critic", trace_node("CriticAgent", self.critic.run))

        # 2. Définir le point d'entrée
        workflow.set_entry_point("manager")

        # 3. Définir les arêtes conditionnelles (Logique du Manager)
        workflow.add_conditional_edges(
            "manager",
            lambda state: state["next_step"],
            {
                "researcher": "researcher",
                "writer": "writer",
                "critic": "critic",
                "finish": END
            }
        )

        # 4. Définir les retours vers le Manager
        workflow.add_edge("researcher", "manager")
        workflow.add_edge("writer", "manager")
        workflow.add_edge("critic", "manager")

        return workflow.compile()

    def run(self, mission: str):
        initial_state = cast(AgentState, {
            "mission": mission,
            "research_data": [],
            "draft_report": "",
            "critique_feedback": None,
            "next_step": "manager",
            "iteration_count": 0
        })
        
        return self.workflow.invoke(initial_state)
