from agentzen.tracing.tracer import Tracer
from agentzen.exporters.jsonl import JSONLExporter

tracer = Tracer(JSONLExporter("decision_trace.jsonl"))

with tracer.trace("request"):
    with tracer.decision(
        name="choose_tool",
        options=["search", "calculate", "ask_user"],
        chosen="search",
        confidence=0.72,
    ):
        pass
