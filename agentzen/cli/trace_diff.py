import json
from pathlib import Path
from collections import Counter


def load_spans(path: Path):
    with path.open() as f:
        return [json.loads(l) for l in f if l.strip()]


def summarize(spans):
    summary = Counter()
    prompt_tokens = 0
    completion_tokens = 0
    latency = 0.0
    decisions = []

    for s in spans:
        summary["spans"] += 1
        latency += (s.get("end_time", 0) - s.get("start_time", 0))

        if s["name"] == "llm:call":
            summary["llm_calls"] += 1
            usage = (s.get("output") or {}).get("token_usage") or {}
            prompt_tokens += usage.get("prompt_tokens", 0)
            completion_tokens += usage.get("completion_tokens", 0)

        if s["name"].startswith("tool:"):
            summary["tool_calls"] += 1

        if s["name"].startswith("agent:decision"):
            decisions.append(s.get("attributes", {}))

    return {
        "summary": summary,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "latency": round(latency, 2),
        "decisions": decisions,
    }


def diff(a, b):
    print("\nTRACE DIFF")
    print("----------")

    print(f"LLM calls:         {b['summary']['llm_calls'] - a['summary']['llm_calls']:+}")
    print(f"Tool calls:        {b['summary']['tool_calls'] - a['summary']['tool_calls']:+}")

    decision_changed = a["decisions"] != b["decisions"]
    print(f"Decision changes:  {'YES' if decision_changed else 'NO'}")

    print(f"Latency delta:     {b['latency'] - a['latency']:+.2f}s")
    print(f"Prompt tokens:     {b['prompt_tokens'] - a['prompt_tokens']:+}")
    print(f"Completion tokens: {b['completion_tokens'] - a['completion_tokens']:+}")

    def eff(x):
        if x["prompt_tokens"] == 0:
            return 0
        return round(x["completion_tokens"] / x["prompt_tokens"], 3)

    print(f"Efficiency:        {eff(a)} → {eff(b)}")


def main(path_a: str, path_b: str):
    a = summarize(load_spans(Path(path_a)))
    b = summarize(load_spans(Path(path_b)))
    diff(a, b)
