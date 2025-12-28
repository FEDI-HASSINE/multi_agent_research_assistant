import time
import traceback
from typing import Callable, Dict, Any, Optional
from mcp.types import MCPRequest, MCPResponse, MCPResponseMeta
from core.logger import Logger
import time
import traceback

class MCPServer:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.tools: Dict[str, Callable] = {}

    def tool(self):
        """Décorateur pour enregistrer une fonction comme outil MCP."""
        def decorator(func: Callable):
            self.tools[func.__name__] = func
            return func
        return decorator

    def execute(self, request: MCPRequest) -> MCPResponse:
        """Exécute une requête MCP et retourne une réponse standardisée."""
        start_time = time.time()
        
        try:
            if request.tool_name not in self.tools:
                raise ValueError(f"Outil '{request.tool_name}' inconnu pour l'agent {self.agent_name}")

            # Exécution de la fonction
            func = self.tools[request.tool_name]
            result = func(**request.params)
            
            status = "success"
            error_msg = None

        except Exception as e:
            result = None
            status = "error"
            error_msg = str(e)
            print(f"❌ MCP Error [{self.agent_name}]: {traceback.format_exc()}")

        end_time = time.time()
        latency = (end_time - start_time) * 1000

        meta = MCPResponseMeta(
            agent_name=self.agent_name,
            latency_ms=round(latency, 2),
            status=status
        )
        
        # LOGGING CENTRALISÉ (PHASE 4)
        Logger.log_mcp_event(
            agent_name=self.agent_name,
            tool_name=request.tool_name,
            params=request.params,
            result=result,
            latency_ms=round(latency, 2),
            status=status,
            error=error_msg
        )

        return MCPResponse(
            status=status,
            data=result,
            meta=meta,
            error_message=error_msg
        )
