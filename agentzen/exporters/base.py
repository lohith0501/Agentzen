from abc import ABC, abstractmethod
from agentzen.tracing.span import TraceSpan


class SpanExporter(ABC):
    @abstractmethod
    def on_span_start(self, span: TraceSpan):
        ...

    @abstractmethod
    def on_span_end(self, span: TraceSpan):
        ...
