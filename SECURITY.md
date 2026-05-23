# Security Policy

## Supported Versions

This public repository is currently preparing the v1.0 release candidate line. Security updates and documentation corrections apply to the current public branch.

## No Secrets Policy

Do not commit secrets, API keys, provider credentials, private certificates, tokens, `.env` files, runtime logs, runtime memory, or local machine configuration. The public runtime uses a mock LLM provider by default and does not require real provider credentials.

The following generated or sensitive files must remain untracked:

- `runtime_logs/`
- `runtime_memory/`
- `.venv/`
- `__pycache__/`
- `*.pyc`
- `.env`
- `*.key`
- `*.pem`
- `*.crt`
- `secrets.*`
- local configuration files

## Responsible Disclosure

For responsible disclosure, open a GitHub security advisory if available for the repository, or contact the repository maintainer through the public GitHub profile associated with the project. Do not publish exploit details in a public issue before the maintainer has had time to review.

## Public And Private Boundary

This repository is a public demonstrator for ZT&SI Cognitive Stability Infrastructure. It contains public examples of runtime governance, semantic drift checks, bounded projection, memory, telemetry, policy evaluation, and multi-agent mesh behavior.

Advanced sovereign-core mechanisms, proprietary stabilization methods, production calibration, internal strategic doctrine, and private deployment hardening are intentionally outside this repository.

## Production Warning

This repository is not production security software. It is a public proof-of-work and research demonstrator. Do not treat it as a complete production firewall, compliance layer, or safety enforcement system without independent review, threat modeling, deployment hardening, monitoring, and security testing.
