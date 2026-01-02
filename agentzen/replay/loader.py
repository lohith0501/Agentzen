import json
from pathlib import Path
from agentzen.tracing.span import TraceSpan


def load_trace(path: str) -> list[TraceSpan]:
    spans = []
    for line in Path(path).read_text().splitlines():
        spans.append(TraceSpan(**json.loads(line)))
    return spans
