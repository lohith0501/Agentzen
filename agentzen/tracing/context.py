from contextvars import ContextVar
from typing import Optional

_current_trace_id: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)
_current_span_id: ContextVar[Optional[str]] = ContextVar("span_id", default=None)


def get_trace_id() -> Optional[str]:
    return _current_trace_id.get()


def set_trace_id(trace_id: str):
    _current_trace_id.set(trace_id)


def get_span_id() -> Optional[str]:
    return _current_span_id.get()


def set_span_id(span_id: Optional[str]):
    _current_span_id.set(span_id)
