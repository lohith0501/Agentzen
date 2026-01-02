import asyncio

from agentzen.tracing.tracer import Tracer
from agentzen.exporters.jsonl import JSONLExporter
from agentzen.tracing.decorators import trace_async_step

tracer = Tracer(JSONLExporter("trace_async.jsonl"))

@trace_async_step(tracer, "agent:plan")
async def plan(goal):
    await asyncio.sleep(0.1)
    return f"Plan for {goal}"

@trace_async_step(tracer, "agent:execute")
async def execute(plan):
    await asyncio.sleep(0.1)
    return f"Executed {plan}"

async def main():
    async with tracer.trace_async("request"):
        p = await plan("ship async agentzen")
        await execute(p)

asyncio.run(main())
