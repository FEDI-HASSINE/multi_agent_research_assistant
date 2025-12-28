import json
import os
from datetime import datetime
from typing import Any, Dict

# Utilisation de chemins absolus pour garantir que les logs sont toujours à la racine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
MCP_LOG_FILE = os.path.join(LOG_DIR, "mcp_logs.jsonl")
TRACE_LOG_FILE = os.path.join(LOG_DIR, "trace_logs.jsonl")

class Logger:
    @staticmethod
    def _write_jsonl(file_path: str, data: Dict[str, Any]):
        """Écrit une ligne JSON dans le fichier spécifié."""
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    @staticmethod
    def log_mcp_event(agent_name: str, tool_name: str, params: Dict[str, Any], result: Any, latency_ms: float, status: str, error: str | None = None):
        """Enregistre un événement MCP."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_source": agent_name,
            "tool_name": tool_name,
            "input_context": params,
            "output_result": str(result)[:500] + "..." if result and len(str(result)) > 500 else str(result), # Tronquer pour lisibilité
            "latency_ms": latency_ms,
            "status": status,
            "error": error
        }
        Logger._write_jsonl(MCP_LOG_FILE, entry)

    @staticmethod
    def log_trace_event(node: str, action: str, details: Dict[str, Any]):
        """Enregistre une trace d'exécution du graphe."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "node": node,
            "action": action,
            "details": details
        }
        Logger._write_jsonl(TRACE_LOG_FILE, entry)

    @staticmethod
    def get_mcp_logs():
        """Lit les logs MCP."""
        if not os.path.exists(MCP_LOG_FILE):
            return []
        with open(MCP_LOG_FILE, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]
