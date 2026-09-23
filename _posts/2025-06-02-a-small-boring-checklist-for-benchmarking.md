---
layout: blog_post
title: 'A small, boring checklist for benchmarking industrial AI'
date: 2025-06-02 09:00:00 +0800
tags:
  - benchmarks
  - evaluation
  - edge
---

Most benchmark tables in industrial AI are answering a question nobody asked: how well does this
model do on data from the same distribution it was trained on, on hardware nobody deploys? The
numbers are not wrong. They are just not about the plant.

## Measure the thing that fails

Start from the failure you are afraid of, then measure the distance to it. In our experience the
list is short and unglamorous:

| What to measure | Why it is on the list |
| --- | --- |
| p99 latency under load, not mean latency | The mean is fine right up until the shift changes. |
| Behaviour when the input is stale | Sensor dropout is normal, not exceptional. |
| Behaviour when the input is out of range | Clamping silently is a decision; make it visible. |
| Recovery time after a restart | Includes model load, not just process start. |
| Agreement between repeated runs | If two identical inputs disagree, nothing else matters. |
| Cost of being wrong, per hour | The only number a plant manager will remember. |

## Hold the right things fixed

A benchmark is only a comparison if two things are true: the workload is identical, and the
hardware is boring. We record the workload as a replayable trace rather than a script, so that a
slow run cannot quietly change the sequence of inputs.

```python
# harness.py — the whole idea, in fifteen lines
def run_once(service, trace, deadline_ms):
    results = []
    for event in trace:                      # deterministic replay, fixed order
        started = time.perf_counter_ns()
        out = service.handle(event.payload)
        elapsed_ms = (time.perf_counter_ns() - started) / 1e6
        results.append({
            "event_id": event.id,
            "elapsed_ms": elapsed_ms,
            "late": elapsed_ms > deadline_ms,  # silence past the deadline is a failure
            "out": out,
            "input_hash": event.hash,          # so a rerun can be compared honestly
        })
    return summarise(results)
```

Two details matter more than they look. `late` is recorded rather than the run being aborted,
because a system that degrades predictably is often better than one that fails cleanly. And
`input_hash` makes it possible to notice that the "same" benchmark was not the same benchmark.

## Report the boring things

- How many runs, and what was excluded. If a run was excluded, say why in the same table.
- The hardware, including firmware version and ambient temperature if the workload is thermal.
- Which numbers you do not trust, and what would change your mind.

> A benchmark without a stated failure mode is a marketing document with decimal places.

## What we stopped trusting

- Single-run comparisons on shared hardware. The variance was larger than the effect.
- Latency measured without the input pipeline. The model was never the bottleneck.
- Any accuracy figure produced on data collected after the model was deployed.

The checklist, with the reasoning behind each item and the measurements that failed to convince
us, is in [OIL-WP-2025-01]({{ '/publications' | relative_url }}).
