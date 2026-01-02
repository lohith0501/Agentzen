from agentzen.tracing.tracer import Tracer
from agentzen.exporters.jsonl import JSONLExporter
from agentzen.tracing.decorators import trace_step

tracer = Tracer(JSONLExporter("trace.jsonl"))

@trace_step(tracer, "agent:plan")
def plan(goal):
    return f"Plan for {goal}"

@trace_step(tracer, "agent:execute")
def execute(plan):
    return f"Executed {plan}"

with tracer.trace("request"):
    p = plan("ship agentzen")
    execute(p)

print("Done")
