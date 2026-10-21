import uuid
import os
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel

class Session(BaseModel):
    session_id: str
    metadata: Dict[str, Any] = {}
    is_active: bool = True

class SessionPool:
    """Manages the lifecycle of multiple agent sessions with disk persistence."""
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.config_dir = os.path.expanduser("~/.black_forge")
        self.gateway_file = os.path.join(self.config_dir, "gateway.json")
        self._ensure_config_dir()
        self.load_sessions()

    def _ensure_config_dir(self):
        os.makedirs(self.config_dir, exist_ok=True)

    def load_sessions(self):
        if os.path.exists(self.gateway_file):
            try:
                with open(self.gateway_file, 'r') as f:
                    data = json.load(f)
                    for sid, s_data in data.items():
                        self.sessions[sid] = Session(**s_data)
            except Exception as e:
                print(f"Warning: Failed to load existing sessions: {e}")

    def save_sessions(self):
        try:
            with open(self.gateway_file, 'w') as f:
                json.dump({sid: s.model_dump() for sid, s in self.sessions.items()}, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save sessions: {e}")

    def create_session(self, metadata: Optional[Dict[str, Any]] = None) -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id, metadata=metadata or {})
        self.sessions[session_id] = session
        self.save_sessions()
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)

    def close_session(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id].is_active = False
            self.save_sessions()

# Global gateway session pool for the CLI
global_session_pool = SessionPool()
