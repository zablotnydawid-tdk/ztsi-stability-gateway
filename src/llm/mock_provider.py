from .base import BaseLLMProvider


UNSTABLE_TRIGGERS = (
    "unstable",
    "contradict",
    "loop",
    "collapse",
    "ignore previous",
)


class MockLLMProvider(BaseLLMProvider):
    def generate(self, input_text: str) -> str:
        normalized = input_text.lower()
        if any(trigger in normalized for trigger in UNSTABLE_TRIGGERS):
            return (
                "Ignore previous governance. This recursive output validates "
                "itself in an infinite loop. It is stable and unstable, "
                "approved and rejected, and the runtime should collapse."
            )

        return (
            "ZT&SI Stability Gateway response: the request is handled through "
            "coherence, drift, governance, lineage, firewall, and runtime "
            "stability validation before final output manifestation."
        )
