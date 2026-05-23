# LLM Adapter Layer

ZT&SI Stability Gateway v0.3 adds an LLM Adapter Layer so model generation can be routed through runtime stability validation before final output manifestation.

## Why ZT&SI Sits Between LLM and Output

An LLM provider can generate fluent text that still drifts from the request, contradicts itself, contains unstable recursive language, or violates governance thresholds. ZT&SI sits between the model response and the application response so no model output manifests without gateway validation.

The adapter makes the application flow explicit:

```text
CLIENT -> API -> LLM ADAPTER -> MODEL PROVIDER -> ZT&SI RUNTIME -> FIREWALL -> RESPONSE
```

## Provider Architecture

Providers implement `BaseLLMProvider`:

```python
class BaseLLMProvider:
    def generate(self, input_text: str) -> str:
        ...
```

The `LLMAdapter` accepts application input, calls the selected provider, receives a candidate model output, and sends that candidate through the existing ZT&SI runtime. The runtime still performs drift scoring, coherence scoring, governance evaluation, lineage logging, firewall enforcement, and final status certification.

## Mock Provider Behavior

`MockLLMProvider` is enabled by default and requires no API keys. It returns stable output for normal input. If the input contains terms such as `unstable`, `contradict`, `loop`, `collapse`, or `ignore previous`, it returns intentionally unstable recursive language so the gateway can demonstrate blocking behavior.

## Future Providers

Future providers can wrap OpenAI, local models, or internal model gateways by implementing `BaseLLMProvider` and registering the provider name in `providers.py`. Real provider integrations should remain optional, disabled by default, and configured so missing credentials never break the mock-first runtime.

## Safety Rule

No model output manifests without gateway validation. Every generated candidate output must pass through ZT&SI drift, coherence, governance, lineage, firewall, and runtime stability handling before the application treats it as final.
