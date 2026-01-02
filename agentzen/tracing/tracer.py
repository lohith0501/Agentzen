import time
import uuid
from contextlib import contextmanager
from typing import Optional, Dict, Any


# ---------------------------------------------------------------------
# TRACE SPAN
# ---------------------------------------------------------------------

class TraceSpan:
    def __init__(
        self,
        name: str,
        trace_id: str,
        parent_id: Optional[str],
        attributes: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.trace_id = trace_id
        self.span_id = uuid.uuid4().hex
        self.parent_id = parent_id
        self.start_time = time.time()
        self.end_time = None
        self.output = None
        self.error = None
        self.attributes = attributes or {}

    def finish(self, output=None, error=None):
        self.end_time = time.time()
        self.output = output
        self.error = error


# ---------------------------------------------------------------------
# TRACER
# ---------------------------------------------------------------------

class Tracer:
    def __init__(self, exporter):
        """
        exporter must implement:
            export(span: TraceSpan)
        """
        self.exporter = exporter
        self._stack = []

        if not hasattr(exporter, "export"):
            raise RuntimeError(
                "Exporter must implement export(span)"
            )

    # --------------------------------------------------
    # CORE TRACE CONTEXT
    # --------------------------------------------------

    @contextmanager
    def trace(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ):
        trace_id = self._stack[0].trace_id if self._stack else uuid.uuid4().hex
        parent_id = self._stack[-1].span_id if self._stack else None

        span = TraceSpan(
            name=name,
            trace_id=trace_id,
            parent_id=parent_id,
            attributes=attributes,
        )

        self._stack.append(span)

        try:
            yield span
        except Exception as e:
            span.finish(error=str(e))
            raise
        else:
            span.finish()
        finally:
            self._stack.pop()
            self.exporter.export(span)

    # --------------------------------------------------
    # AGENT DECISION API
    # --------------------------------------------------

    @contextmanager
    def decision(
        self,
        name: str,
        options,
        chosen,
        confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Records a structured agent decision without exposing chain-of-thought.
        """

        attributes = {
            "type": "decision",
            "options": options,
            "chosen": chosen,
        }

        if confidence is not None:
            attributes["confidence"] = confidence

        if metadata:
            attributes.update(metadata)

        with self.trace(
            name=f"agent:decision:{name}",
            attributes=attributes,
        ):
            yield
