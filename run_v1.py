from agentzen.tracing.tracer import Tracer
from agentzen.exporters.jsonl import JSONLExporter

tracer = Tracer(JSONLExporter("run_v1.jsonl"))

with tracer.trace("request"):
    with tracer.decision(
        name="choose_tool",
        options=["search", "calculate"],
        chosen="search",
        confidence=0.6,
    ):
        pass
