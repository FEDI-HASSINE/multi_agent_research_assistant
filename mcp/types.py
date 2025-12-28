from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Literal
from datetime import datetime

class MCPRequest(BaseModel):
    tool_name: str = Field(description="Nom de l'outil à appeler")
    params: Dict[str, Any] = Field(default_factory=dict, description="Paramètres de la fonction")

class MCPResponseMeta(BaseModel):
    agent_name: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    latency_ms: float
    status: Literal["success", "error"]

class MCPResponse(BaseModel):
    status: Literal["success", "error"]
    data: Any
    meta: MCPResponseMeta
    error_message: Optional[str] = None
