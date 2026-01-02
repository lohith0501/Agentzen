import json
from pathlib import Path
from typing import Any


class JSONLExporter:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def export(self, span: Any):
        """
        Export a single TraceSpan as JSONL.
        """

        record = {
            "name": span.name,
            "span_id": span.span_id,
            "parent_id": span.parent_id,
            "trace_id": span.trace_id,
            "start_time": span.start_time,
            "end_time": span.end_time,
            "output": span.output,
            "error": span.error,
            "attributes": span.attributes,
        }

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
