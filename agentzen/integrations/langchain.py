from typing import Any, Dict

from langchain.callbacks.base import AsyncCallbackHandler

from agentzen.tracing.tracer import Tracer
from agentzen.tracing.span import TraceSpan


class AgentZenLangChainCallback(AsyncCallbackHandler):
    """
    Async LangChain callback handler that emits clean,
    structured observability spans to agentzen Tracer.
    """

    def __init__(self, tracer: Tracer):
        self.tracer = tracer
        self._active_spans: Dict[str, TraceSpan] = {}

    # ============================================================
    # CHAINS
    # ============================================================

    async def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        run_id: str,
        **kwargs,
    ):
        span = self.tracer.start_span(
            name=f"chain:{serialized.get('name', 'unknown')}",
            attributes={"inputs": inputs},
        )
        self._active_spans[run_id] = span

    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
        run_id: str,
        **kwargs,
    ):
        span = self._active_spans.pop(run_id, None)
        if span:
            self.tracer.end_span(span, outputs)

    async def on_chain_error(
        self,
        error: BaseException,
        run_id: str,
        **kwargs,
    ):
        span = self._active_spans.pop(run_id, None)
        if span:
            self.tracer.record_exception(span, error)

    # ============================================================
    # LLM CALLS
    # ============================================================

    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: list,
        run_id: str,
        **kwargs,
    ):
        # IMPORTANT:
        # Do NOT put model info at span root.
        # LLM-specific metadata belongs in output only.
        span = self.tracer.start_span(
            name="llm:call",
            attributes={
                "prompts": prompts,
            },
        )
        self._active_spans[run_id] = span

    async def on_llm_end(
        self,
        response: Any,
        run_id: str,
        **kwargs,
    ):
        span = self._active_spans.pop(run_id, None)
        if not span:
            return

        # Stable, intentional LLM output schema
        output: Dict[str, Any] = {
            "text": None,
            "token_usage": None,
            "model": None,
        }

        try:
            # Chat models (most common case)
            if hasattr(response, "generations"):
                gen = response.generations[0][0]
                output["text"] = getattr(gen.message, "content", None)

            # Token usage + model name
            if hasattr(response, "llm_output") and isinstance(
                response.llm_output, dict
            ):
                output["token_usage"] = response.llm_output.get("token_usage")
                output["model"] = response.llm_output.get("model_name")

        except Exception:
            # Observability must never break execution
            output["raw"] = str(response)

        self.tracer.end_span(span, output)

    async def on_llm_error(
        self,
        error: BaseException,
        run_id: str,
        **kwargs,
    ):
        span = self._active_spans.pop(run_id, None)
        if span:
            self.tracer.record_exception(span, error)

    # ============================================================
    # TOOLS
    # ============================================================

    async def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        run_id: str,
        **kwargs,
    ):
        span = self.tracer.start_span(
            name=f"tool:{serialized.get('name', 'unknown')}",
            attributes={"input": input_str},
        )
        self._active_spans[run_id] = span

    async def on_tool_end(
        self,
        output: Any,
        run_id: str,
        **kwargs,
    ):
        span = self._active_spans.pop(run_id, None)
        if span:
            self.tracer.end_span(span, output)

    async def on_tool_error(
        self,
        error: BaseException,
        run_id: str,
        **kwargs,
    ):
        span = self._active_spans.pop(run_id, None)
        if span:
            self.tracer.record_exception(span, error)
