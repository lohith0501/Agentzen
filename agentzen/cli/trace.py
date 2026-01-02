import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from agentzen.analysis.antipatterns import AntiPatternAnalyzer


def load_spans(path: Path) -> List[Dict[str, Any]]:
    with path.open() as f:
        return [json.loads(line) for line in f]


def group_by_trace(spans):
    traces = {}
    for s in spans:
        traces.setdefault(s["trace_id"], []).append(s)
    return traces


def print_trace(trace_id, spans):
    children = {}
    for s in spans:
        children.setdefault(s["parent_id"], []).append(s)

    def render(span, indent=0):
        dur = span["end_time"] - span["start_time"]
        print("│  " * indent + f"{span['name']} ({dur:.2f}s)")
        for k, v in span["attributes"].items():
            print("│  " * (indent + 1) + f"• {k}: {v}")
        for c in children.get(span["span_id"], []):
            render(c, indent + 1)

    root = children[None][0]
    print(f"\nTRACE {trace_id}")
    render(root)


def analyze(spans, fail=False):
    analyzer = AntiPatternAnalyzer(spans)
    result = analyzer.analyze()

    if result.is_empty():
        print("\nNO ANTI-PATTERNS DETECTED")
        return 0

    print("\nANTI-PATTERNS DETECTED")
    print("---------------------")
    for f in result.findings:
        print(f"• {f.message}")
        print(f"  ↳ Suggestion: {f.suggestion}")

    return 1 if fail else 0


def diff(a: Path, b: Path):
    a_spans = load_spans(a)
    b_spans = load_spans(b)

    def decisions(spans):
        return [
            s for s in spans
            if s["name"].startswith("agent:decision:")
        ]

    da, db = decisions(a_spans), decisions(b_spans)

    print("\nTRACE DIFF")
    print("----------")

    if len(da) != len(db):
        print(f"Decision count changed: {len(da)} → {len(db)}")
        return

    for i, (x, y) in enumerate(zip(da, db)):
        if x["attributes"]["chosen"] != y["attributes"]["chosen"]:
            print(f"Decision {i} changed:")
            print(f"  chosen: {x['attributes']['chosen']} → {y['attributes']['chosen']}")
            print(
                f"  confidence: "
                f"{x['attributes'].get('confidence')} → {y['attributes'].get('confidence')}"
            )


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  agentzen trace <trace.jsonl> [--analyze] [--fail]")
        print("  agentzen trace diff <a.jsonl> <b.jsonl>")
        sys.exit(1)

    if sys.argv[2] == "diff":
        diff(Path(sys.argv[3]), Path(sys.argv[4]))
        return

    path = Path(sys.argv[2])
    spans = load_spans(path)
    traces = group_by_trace(spans)

    analyze_flag = "--analyze" in sys.argv
    fail_flag = "--fail" in sys.argv

    exit_code = 0

    for trace_id, trace_spans in traces.items():
        print_trace(trace_id, trace_spans)
        if analyze_flag:
            exit_code = analyze(trace_spans, fail_flag)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
