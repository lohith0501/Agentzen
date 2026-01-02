from .base import SpanExporter
from agentzen.tracing.span import TraceSpan


class MemoryExporter(SpanExporter):
    def __init__(self):
        self.spans = []

    def on_span_start(self, span: TraceSpan):
        pass

    def on_span_end(self, span: TraceSpan):
        self.spans.append(span)
