from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers in black_forge."""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class NullProvider(BaseLLMProvider):
    """Fallback provider when no config is detected."""
    def generate(self, prompt: str) -> str:
        return f"[NullProvider Echo]: {prompt}"
