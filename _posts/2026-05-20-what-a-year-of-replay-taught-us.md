---
layout: blog_post
title: 'What a year of replay taught us'
date: 2026-05-20 09:00:00 +0800
tags:
  - replay
  - evaluation
  - operations
---

A year ago we started recording raw inputs next to every decision the runtime made. The original
motivation was narrow: when a model behaves differently on two shifts, we wanted evidence rather
than opinions. The replay corpus turned out to be useful for something else entirely — deciding
which changes are worth making at all.

## Replay is a budget, not a benchmark

Every traced hour is a claim about what matters in a plant, and traces are not free: they cost
storage, review time, and the attention of the people who have to trust them. We now treat the
corpus like a budget.

| Decision | What replay actually answered |
| --- | --- |
| Add a second model for anomaly scoring | No measurable gain on 94% of traces; 6% were worse. Rejected. |
| Move inference to a smaller runtime image | Same decisions, 40% less memory. Accepted. |
| Retrain weekly instead of monthly | Improved two traces, degraded one. Deferred pending more data. |
| Widen the deadline by 20ms | Removed 71% of late runs without changing outputs. Accepted. |

Two of those four decisions were "no". A benchmark that only produces "yes" is not measuring
anything; it is confirming a decision that has already been made.

## The disagreements are the deliverable

The most valuable output of the year was not a model improvement. It was the list of cases where
replay and the plant disagreed:

- **Stale inputs that the model handled gracefully in replay** and badly in the plant, because
  replay cannot reproduce the operator's reaction to a stale number appearing on screen.
- **Rare but legal input combinations** that the trace contained twice and the model had never
  been trained on, because training data was filtered by the same rules that produced the trace.
- **Timing-sensitive decisions** that replay reproduced exactly and the plant never did, because
  the plant's clock is shared with equipment that occasionally stalls.

The third one is still open, and we would rather publish it as open than paper over it with a
smoothing filter.

## What we would do differently

- Record context with the trace: who was on shift, what else was running, what the operator saw.
- Store the *rejected* outputs too. Half of the argument about a change is about what it stopped
  doing, and we did not keep that.
- Review traces in small batches with the people who own the equipment, not in a dashboard nobody
  opens. Twenty minutes with a maintenance engineer beats a week of aggregate statistics.

The comparison protocol, the replay format, and the three models that failed it are written up in
[OIL-TR-2026-01]({{ '/publications/' | relative_url }}).
