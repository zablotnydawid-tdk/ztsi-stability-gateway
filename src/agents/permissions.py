DEFAULT_PERMISSIONS = ["evaluate"]


def has_permission(agent: dict, permission: str) -> bool:
    return permission in agent.get("permissions", [])
