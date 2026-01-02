
<p align="center">
  <img src="https://trialogueknowledgehub.co.za/wp-content/uploads/2019/08/monitoring-impact.jpg" width="1500" alt="AgentZen Logo">
</p>

<h1 align="center">AgentZen</h1>

<p align="center">
  Observe how agents behave, not what they think.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-success.svg" />
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" />
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" />
  <img src="https://img.shields.io/badge/agent-observability-purple.svg" />
  <img src="https://img.shields.io/badge/ci-ready-brightgreen.svg" />
</p>

---

## Overview

AgentZen is a toolkit for observing and understanding how AI agents act.

It helps developers see what an agent did, why it made certain decisions, how confident it was, and how its actions change from run to run—without recording prompts, chain-of-thought, or internal model details.

AgentZen focuses on actions and outcomes, not generated text.

---

## Why AgentZen

Modern AI agents often fail silently.

Small changes such as:
- prompt edits
- model upgrades
- tool-routing logic changes

can subtly alter agent behavior in ways that are difficult to detect.

Traditional logging shows outputs but not intent.  
Logging chain-of-thought introduces privacy, safety, and policy risks.

AgentZen solves this by recording **structured decision events instead of reasoning text**, making agent behavior observable and safe for production.

---

## Design Goals

- Behavior over text
- Explainability without reasoning leakage
- Deterministic, structured traces
- Production-safe and policy-compliant
- CLI-first workflows
- Minimal dependencies
- CI compatibility

AgentZen is intentionally **not**:
- an agent framework
- a prompt manager
- a monitoring dashboard

---

## Core Concepts

### Traces

A trace represents a single execution of an agent.

Each trace:
- corresponds to one run
- contains multiple spans
- is written incrementally during execution
- is exported as structured JSONL

---

### Spans

A span represents a unit of agent behavior.

Examples:
- planning phases
- tool calls
- retries
- sub-task execution
- decisions

Spans may be nested to reflect execution structure.

---

### Decision Spans

A decision span captures a single agent choice.

Each decision span records:
- decision name
- available options
- chosen option
- confidence score (0.0–1.0)

Decision spans explicitly do **not** capture:
- prompts
- chain-of-thought
- model internals
- hidden state

This ensures safety, determinism, and production readiness.

---

## Installation

### Requirements

- Python 3.9 or newer
- pip

### Install from PyPI

```bash
pip install agentzen
````

### Verify Installation

```bash
agentzen --help
```

Expected output:

```
AgentZen CLI
Usage:
  agentzen trace <trace.jsonl> [--analyze] [--fail]
  agentzen trace diff <old.jsonl> <new.jsonl>
```

---

## Basic Usage

### Initializing the Tracer

```python
from agentzen.tracing.tracer import Tracer
from agentzen.exporters.jsonl import JSONLExporter

tracer = Tracer(JSONLExporter("trace.jsonl"))
```

---

### Creating a Trace

```python
with tracer.trace("request"):
    ...
```

All spans created inside this block belong to the same execution.

---

### Instrumenting Decisions

```python
with tracer.decision(
    name="choose_tool",
    options=["search", "calculate"],
    chosen="search",
    confidence=0.72,
):
    pass
```

Guidelines:

* options should enumerate all meaningful alternatives
* chosen must be one of the options
* confidence should reflect internal certainty

---

Each run produces a structured JSONL trace describing agent behavior.

---

## CLI Reference

All CLI commands operate on JSONL trace files.

---

## Command: trace (View Execution)

```bash
agentzen trace trace.jsonl
```

Example output:

```
Trace: request
└── Decision: choose_tool
    ├── Options: [search, calculate]
    ├── Chosen: search
    └── Confidence: 0.72
```

---

## Command: trace --analyze (Behavioral Analysis)

```bash
agentzen trace trace.jsonl --analyze
```

Healthy trace output:

```
Behavioral Analysis Summary
---------------------------
✔ No critical issues detected

Observations:
- All decisions exceeded confidence threshold (0.60)
- No oscillation detected
- No repeated decision loops
```

Problematic trace output:

```
Behavioral Analysis Summary
---------------------------
⚠ Issues Detected: 2

1. Decision Loop Detected
   - Decision: choose_tool
   - Repeated 4 times
   - Recommendation: Add stopping condition

2. Low Confidence Decisions
   - Decision: select_action
   - Confidence below 0.40
   - Recommendation: Improve context or constrain options
```

---

## Command: trace --analyze --fail (CI Enforcement)

```bash
agentzen trace trace.jsonl --analyze --fail
```

Example output:

```
Behavioral Analysis Summary
---------------------------
✖ Blocking Issues Detected

- Decision loop detected
- Confidence regression detected

Exiting with status code 1
```

Exit codes:

* 0 → acceptable behavior
* 1 → regression detected

---

## Command: trace diff (Behavioral Diffing)

```bash
agentzen trace diff run_v1.jsonl run_v2.jsonl
```

Example output:

```
Behavioral Diff Summary
-----------------------
⚠ Behavior Changes Detected

Decision: choose_tool
- Previous: search (0.81)
- New: calculate (0.62)

Decision: plan_steps
- Confidence dropped by 0.27

Overall Assessment:
- Behavior materially changed
```

---

## Command Summary

```bash
agentzen trace <trace.jsonl>
agentzen trace <trace.jsonl> --analyze
agentzen trace <trace.jsonl> --analyze --fail
agentzen trace diff <old.jsonl> <new.jsonl>
```

---

## Production Usage

### Feature Flagging

AgentZen is typically:

* initialized once
* guarded behind a feature flag
* disabled in latency-sensitive paths

When disabled, overhead is near zero.

---

### SDK Integration

SDK authors typically:

* embed AgentZen internally
* instrument key control-flow decisions
* expose observability as an opt-in feature

---

### Storage and Retention

Traces contain:

* no prompts
* no chain-of-thought
* no sensitive model state

They are safe to store, share, and retain.

---

## What AgentZen Does Not Do

AgentZen does not:

* generate prompts
* orchestrate agents
* manage tools
* provide dashboards
* log reasoning or model internals

---

## License

MIT License.

---

## Who This Is For

AgentZen is built for:

* developers building production AI agents
* teams operating agent-based systems
* SDK and platform engineers
* organizations requiring behavioral guarantees over time

```
