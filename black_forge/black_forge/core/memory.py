import os

class MemoryManager:
    """Manages system memory, personas, and dynamic context injection."""
    
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.black_forge")
        self.soul_file = os.path.join(self.config_dir, "soul.md")
        self.user_file = os.path.join(self.config_dir, "user.md")
        self._ensure_files()
        
    def _ensure_files(self):
        """Creates dummy identity files if they do not exist."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        if not os.path.exists(self.soul_file):
            with open(self.soul_file, 'w') as f:
                f.write("You are Black Forge, a brilliant, concise, and highly effective terminal OS agent.\n")
                
        if not os.path.exists(self.user_file):
            with open(self.user_file, 'w') as f:
                f.write("User prefers Python, typing safety, and no unnecessary conversation blocks.\n")

    def _read_file_safe(self, filepath: str) -> str:
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return f.read()
        except:
            pass
        return ""

    def get_soul(self) -> str:
        return self._read_file_safe(self.soul_file)
        
    def get_user_preferences(self) -> str:
        return self._read_file_safe(self.user_file)
        
    def get_local_discovery(self, current_cwd: str) -> str:
        """Looks for a CLAUDE.md or BLACK_FORGE.md in the current execution path to inject context."""
        claude_path = os.path.join(current_cwd, "CLAUDE.md")
        black_forge_path = os.path.join(current_cwd, "BLACK_FORGE.md")
        
        context = ""
        if os.path.exists(claude_path):
            context += f"\n[Project Context from CLAUDE.md]:\n{self._read_file_safe(claude_path)}"
        if os.path.exists(black_forge_path):
            context += f"\n[Project Context from BLACK_FORGE.md]:\n{self._read_file_safe(black_forge_path)}"
            
        return context
        
    def assemble_system_prompt(self, cwd: str) -> str:
        """Dynamically builds the context window brain."""
        parts = []
        
        soul = self.get_soul()
        if soul:
            parts.append("--- AGENT PERSONA ---")
            parts.append(soul)
            
        user = self.get_user_preferences()
        if user:
            parts.append("--- USER PREFERENCES ---")
            parts.append(user)
            
        local = self.get_local_discovery(cwd)
        if local:
            parts.append("--- LOCAL PROJECT CONTEXT ---")
            parts.append(local)
            
        parts.append("You have access to a suite of terminal tools. NEVER guess file contents, explicitly read them using your tools when asked about a project.")
        
        return "\n\n".join(parts)
