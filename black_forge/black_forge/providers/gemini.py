import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from typing import List, Callable, Any
from .llm import BaseLLMProvider
from black_forge.tools.registry import global_tool_registry

class GeminiProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "gemini-1.5-flash", temperature: float = 0.5):
        from dotenv import load_dotenv
        load_dotenv()
        
        self.model_name = model_name
        self.temperature = temperature
        
        # Will fail if GOOGLE_API_KEY is not in env
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        
    def _convert_to_lc_tools(self) -> List[Any]:
        from langchain_core.tools import StructuredTool
        lc_tools = []
        for name, func in global_tool_registry.tools.items():
            description = global_tool_registry.schemas[name].description
            # Use StructuredTool to handle dynamic naming and descriptions reliably
            st_tool = StructuredTool.from_function(
                func=func,
                name=name,
                description=description
            )
            lc_tools.append(st_tool)
        return lc_tools

    def generate(self, prompt: str) -> str:
        # Default mock if no full loop is running
        return f"[Gemini Echo]: {prompt}"

    def interact(self, messages: List[Any], system_prompt: str) -> Any:
        lc_tools = self._convert_to_lc_tools()
        llm_with_tools = self.llm.bind_tools(lc_tools)
        
        full_conversation = [SystemMessage(content=system_prompt)] + messages
        return llm_with_tools.invoke(full_conversation)
