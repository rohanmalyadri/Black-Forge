from typing import List, Callable, Dict, Any
from pydantic import BaseModel

class ToolSchema(BaseModel):
    name: str
    description: str

class ToolRegistry:
    """Manages the 43+ built-in and MCP dynamic tools."""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.schemas: Dict[str, ToolSchema] = {}

    def register_tool(self, schema: ToolSchema, func: Callable):
        self.schemas[schema.name] = schema
        self.tools[schema.name] = func

    def get_tool(self, name: str) -> Callable:
        return self.tools.get(name)

# Global registry
global_tool_registry = ToolRegistry()
