from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, input_text: str) -> str:
        """Generate a candidate model output for gateway validation."""
