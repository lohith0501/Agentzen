from collections import defaultdict
from typing import List, Dict, Any


class Finding:
    def __init__(self, message: str, suggestion: str):
        self.message = message
        self.suggestion = suggestion


class AntiPatternResult:
    def __init__(self):
        self.findings: List[Finding] = []

    def add(self, message: str, suggestion: str):
        self.findings.append(Finding(message, suggestion))

    def is_empty(self) -> bool:
        return len(self.findings) == 0


class AntiPatternAnalyzer:
    def __init__(self, spans: List[Dict[str, Any]]):
        self.spans = spans

    def analyze(self) -> AntiPatternResult:
        result = AntiPatternResult()

        decisions = [
            s for s in self.spans
            if s["name"].startswith("agent:decision:")
        ]

        if not decisions:
            return result

        # --------------------------------------------------
        # Decision Loop
        # --------------------------------------------------
        counts = defaultdict(int)
        for d in decisions:
            counts[d["name"]] += 1

        for name, count in counts.items():
            if count >= 3:
                result.add(
                    f"Decision loop detected: '{name}' repeated {count} times",
                    "Add a stopping condition or max_iterations guard",
                )

        # --------------------------------------------------
        # Low Confidence
        # --------------------------------------------------
        confidences = [
            d["attributes"].get("confidence")
            for d in decisions
            if d["attributes"].get("confidence") is not None
        ]

        if confidences:
            avg = sum(confidences) / len(confidences)
            if avg < 0.5:
                result.add(
                    f"Low confidence decisions: average = {avg:.2f}",
                    "Improve prompt clarity or add more context",
                )

        # --------------------------------------------------
        # Oscillation
        # --------------------------------------------------
        last = None
        flips = 0

        for d in decisions:
            choice = d["attributes"].get("chosen")
            if last is not None and choice != last:
                flips += 1
            last = choice

        if flips >= 2:
            result.add(
                f"Decision oscillation detected: {flips} flips",
                "Introduce a preference bias or memory of past decisions",
            )

        # --------------------------------------------------
        # Excessive Decisions
        # --------------------------------------------------
        if len(decisions) > 5:
            result.add(
                f"Excessive decisions: {len(decisions)} in one trace",
                "Reduce planning depth or merge decisions",
            )

        return result
