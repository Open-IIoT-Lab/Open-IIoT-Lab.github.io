---
title: Open Edge Runtime
date: 2026-02-18 09:00:00 +0800
package: oil-edge-runtime
version: 0.9.2
license: Apache-2.0
stack: Go · Rust
status: stable
programme: Open Edge Runtime
summary: A portable control plane for running event-driven services beside production equipment.
links:
  Programme: /research/
  Report: /publications/#open-edge-orchestration-a-vendor-neutral-reference-architecture-for-services-beside-industrial-equipment
  Deployment notes: /publications/#observability-patterns-for-open-automation-logging-tracing-and-recovery-in-long-lived-deployments
---

What ships in the box: the runtime binary, the service manifest schema and validator, a reference
historian, and the replay tooling that Open Loop Bench builds on. The runtime keeps deadlines and
restart limits explicit, so a service that has stopped being useful stops being run.
