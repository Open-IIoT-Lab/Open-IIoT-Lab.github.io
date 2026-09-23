---
layout: blog_post
title: 'Notes from building an open edge runtime'
date: 2025-11-04 09:00:00 +0800
tags:
  - edge
  - runtime
  - architecture
---

We have spent the last year building a runtime that runs beside industrial equipment, and the
most useful thing we can publish is not the architecture diagram. It is the list of assumptions
that turned out to be wrong.

## What we wanted

The goal was modest: a control plane small enough that a plant engineer can read the whole thing
in an afternoon, and boring enough that it can stay running for years without a maintainer who
remembers why a line of code exists.

That constraint rules out a surprising amount of modern infrastructure. No cluster scheduler. No
service mesh. A single binary, a text manifest, and a filesystem layout that a person can inspect
with `ls`.

## What the manifest looks like

The deployment manifest is the part of the system most likely to be read by someone who did not
write it, so it is the part we spent the most time on:

```yaml
# edge-manifest.yml — one service, one machine, no surprises
service: vibration-watch
image: /var/lib/oil/services/vibration-watch-1.4.2
schedule:
  mode: interval
  every: 250ms
  deadline: 180ms          # if we miss this, the previous result is stale
resources:
  cpu: 0.5                 # shares, not cores
  memory: 256Mi
restart:
  policy: on-failure
  backoff: [1s, 5s, 30s]
  give_up_after: 5
observability:
  log: /var/log/oil/vibration-watch.log
  trace_sample: 0.05       # 5% of runs, always including failures
```

Two decisions are visible in those eleven lines. The first is `deadline`: a service declares the
point after which its output stops being useful, which lets the runtime discard work instead of
queueing it behind a slow model. The second is `give_up_after`: a service is allowed to stop
being restarted. An edge node that keeps restarting a broken analyser forever is not resilient,
it is noisy.

> The most expensive failures we saw were not crashes. They were services that kept running and
> kept being wrong, politely, for eleven days.

## Three assumptions we got wrong

### 1. "The network is unreliable, so buffer everything"

Buffering is the obvious answer to a flaky link, and it is the wrong default for control paths.
A buffered command that arrives after the process has moved on is worse than a dropped one. We
now separate *observational* data, which may be buffered and replayed, from *actionable* data,
which expires. The manifest above has one deadline because the service only produces actionable
data; our historian path has none, and buffers for days.

### 2. "Operators will read the dashboard"

They read the machine, then the dashboard, in that order, and only when something already looks
wrong. Anything that has to be watched continuously will not be watched. The runtime now writes a
single line per hour into the plant's existing shift log, in the format the plant already uses.

### 3. "Determinism is a testing concern"

It is an operational concern. When a model update changed behaviour on one line but not another,
the difference was temperature drift in the sensor, not the model. We could only see that because
we had recorded raw inputs alongside decisions. Replay is now a first-class feature rather than a
debugging trick — see [Open Loop Bench]({{ '/research/' | relative_url }}).

## What we would tell the next team

- Write the manifest for the person who inherits it, not for the person writing the parser.
- Separate data that expires from data that accumulates, and make the distinction explicit in
  configuration rather than in a comment.
- Record inputs with decisions, or you will spend the next incident arguing about hardware.
- Let things stop. Restart loops hide more than they fix.

The reference architecture, including the parts we have not solved, is written up in
[OIL-TR-2025-02]({{ '/publications/' | relative_url }}). If you run something similar in a plant and
disagree with any of this, we would like to hear about it.
