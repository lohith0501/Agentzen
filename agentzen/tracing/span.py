from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from time import time
import uuid


@dataclass
class TraceSpan:
    """
    Represents a single tracing span.

    This object is intentionally minimal and uses
    explicit serialization via to_dict() to avoid
    leaking internal or accidental attributes.
    """

    # ---- Identity ----
    name: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    parent_id: Optional[str] = None
    trace_id: Optional[str] = None

    # ---- Timing ----
    start_time: float = field(default_factory=time)
    end_time: Optional[float] = None

    # ---- Data ----
    input: Optional[Any] = None
    output: Optional[Any] = None
    error: Optional[str] = None

    # ---- Metadata ----
    attributes: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def finish(self, output: Any = None):
        """
        Mark the span as completed successfully.
        """
        self.output = output
        self.end_time = time()

    def fail(self, exc: Exception):
        """
        Mark the span as failed with an exception.
        """
        self.error = repr(exc)
        self.end_time = time()

    # ------------------------------------------------------------------
    # Serialization (STRICT, WHITELISTED)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize the span using a strict whitelist.

        This prevents accidental leakage of internal
        or dynamically-attached attributes.
        """
        return {
            "name": self.name,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "trace_id": self.trace_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "input": self.input,
            "output": self.output,
            "error": self.error,
            "attributes": self.attributes,
        }
