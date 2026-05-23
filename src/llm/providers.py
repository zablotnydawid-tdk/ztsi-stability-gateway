from .base import BaseLLMProvider
from .mock_provider import MockLLMProvider


class UnknownProviderError(ValueError):
    pass


PROVIDERS: dict[str, type[BaseLLMProvider]] = {
    "mock": MockLLMProvider,
}


def get_provider(provider_name: str = "mock") -> BaseLLMProvider:
    normalized = provider_name.strip().lower() or "mock"
    provider_class = PROVIDERS.get(normalized)
    if provider_class is None:
        supported = ", ".join(sorted(PROVIDERS))
        raise UnknownProviderError(
            f"Unknown LLM provider '{provider_name}'. Supported providers: {supported}."
        )
    return provider_class()
