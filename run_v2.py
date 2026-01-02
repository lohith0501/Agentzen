# run_v2.py
from agentzen.tracing.tracer import Tracer
from agentzen.exporters.jsonl import JSONLExporter

tracer = Tracer(JSONLExporter("decision_v2.jsonl"))

with tracer.trace("request"):
    with tracer.decision(
        name="choose_tool",
        options=["search", "calculate", "ask_user"],
        chosen="calculate",
        confidence=0.91,
    ):
        pass
