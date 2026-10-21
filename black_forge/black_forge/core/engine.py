from typing import List, Any
from .gateway import Session
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from black_forge.tools.registry import global_tool_registry
from black_forge.tools.permissions import PermissionChecker
# Make sure builtins are registered
import black_forge.tools.builtins
import black_forge.tools.sandbox

class QueryEngine:
    """The central Agent Loop engine evaluating streams and tool-use."""

    def __init__(self, session: Session):
        self.session = session
        self.messages: List[Any] = []
        
        # Load Provider dynamically mapping to config later, hardcoding Gemini for Phase 2
        from black_forge.providers.gemini import GeminiProvider
        self.provider = GeminiProvider()
        
        from black_forge.core.memory import MemoryManager
        self.memory = MemoryManager()
        
        # System prompt now handled dynamically by memory, but baseline identity is 'black_forge'
        self.baseline_name = "Black Forge"

    # Hard stop so a model that keeps requesting tools can't loop forever.
    MAX_TOOL_ROUNDS = 15
        
    def execute_loop(self, prompt: str) -> str:
        """
        Runs the stream -> tool_use -> execute -> loop cycle until final answer.
        """
        import os
        current_cwd = os.getcwd()
        system_prompt = self.memory.assemble_system_prompt(current_cwd)
        
        self.messages.append(HumanMessage(content=prompt))
        
        for _ in range(self.MAX_TOOL_ROUNDS):
            # 1. Ask LLM
            response_msg = self.provider.interact(self.messages, system_prompt)
            self.messages.append(response_msg)
            
            # 2. Check if Tool Call is requested
            if not getattr(response_msg, "tool_calls", None):
                # No tool calls, finish loop. `.text` flattens Gemini's list-of-blocks content.
                return response_msg.text
                
            # 3. Execute Tool
            for tool_call in response_msg.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_call_id = tool_call["id"]
                
                # Check permissions
                if not PermissionChecker.is_authorized(self.session.session_id, tool_name):
                    self.messages.append(ToolMessage(
                        content=f"Error: Permission denied for tool {tool_name}", 
                        tool_call_id=tool_call_id
                    ))
                    continue
                
                func = global_tool_registry.get_tool(tool_name)
                if func:
                    try:
                        result = func(**tool_args)
                        self.messages.append(ToolMessage(content=str(result), tool_call_id=tool_call_id))
                    except Exception as e:
                        self.messages.append(ToolMessage(content=f"Error executing {tool_name}: {e}", tool_call_id=tool_call_id))
                else:
                    self.messages.append(ToolMessage(content=f"Error: Tool {tool_name} not found.", tool_call_id=tool_call_id))
            
            # Loop runs again with the ToolMessage appended!

        return f"Stopped after {self.MAX_TOOL_ROUNDS} tool rounds without a final answer."
