---
title: Edge Historian Lite
date: 2026-05-14 09:00:00 +0800
package: oil-historian-lite
version: 0.5.0
license: MPL-2.0
stack: Rust
status: beta
programme: Open Edge Runtime
summary: A small time-series historian that survives a plant network being unavailable for days.
links:
  Programme: /research/
  Report: /publications/#observability-patterns-for-open-automation-logging-tracing-and-recovery-in-long-lived-deployments
---

Buffers observational data locally with a bounded disk budget, replays it when the link returns,
and keeps actionable data out of the buffer entirely — a command that arrives after the process has
moved on is worse than one that was dropped.
