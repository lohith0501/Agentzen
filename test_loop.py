# test_loop.py
from agentzen.tracing.tracer import Tracer
from agentzen.exporters.jsonl import JSONLExporter

tracer = Tracer(JSONLExporter("loop.jsonl"))

with tracer.trace("request"):
    for _ in range(3):
        with tracer.decision(
            name="choose_tool",
            options=["search", "calculate"],
            chosen="search",
            confidence=0.4,
        ):
            pass
