def sparkline(values: list[float], width: int = 24) -> str:
    if not values:
        return "(no data)"
    sample = values[-width:]
    ticks = "▁▂▃▄▅▆▇█"
    minimum = min(sample)
    maximum = max(sample)
    if minimum == maximum:
        return ticks[0] * len(sample)
    return "".join(
        ticks[int((value - minimum) / (maximum - minimum) * (len(ticks) - 1))]
        for value in sample
    )


def bar(label: str, value: int, total: int, width: int = 24) -> str:
    filled = int((value / total) * width) if total else 0
    return f"{label:<12} [{'#' * filled}{'.' * (width - filled)}] {value}"
