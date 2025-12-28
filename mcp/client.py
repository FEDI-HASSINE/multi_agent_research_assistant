from typing import Dict, Any
from mcp.server import MCPServer
from mcp.types import MCPRequest, MCPResponse

class MCPClient:
    def __init__(self, server: MCPServer):
        self.server = server

    def call(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Envoie une requête au serveur MCP et retourne les données ou lève une erreur.
        Gère automatiquement le logging de l'appel.
        """
        request = MCPRequest(tool_name=tool_name, params=params)
        
        print(f"📡 MCP Call -> {self.server.agent_name}.{tool_name}")
        
        response: MCPResponse = self.server.execute(request)
        
        # Observabilité simple (Logs)
        if response.status == "success":
            print(f"✅ MCP Success [{response.meta.latency_ms}ms]")
            return response.data
        else:
            print(f"❌ MCP Failed: {response.error_message}")
            raise RuntimeError(f"MCP Error in {self.server.agent_name}: {response.error_message}")
