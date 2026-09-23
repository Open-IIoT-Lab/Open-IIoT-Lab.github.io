---
layout: blog_post
title: 'Why industrial data models keep failing'
date: 2025-08-19 09:00:00 +0800
tags:
  - semantics
  - interoperability
  - field-notes
---

Every few years the industrial world adopts a new shared information model, and every few years
the same thing happens: the pilot works, the rollout stalls, and the model is quietly reduced to
a naming convention. It is rarely because the model was technically wrong.

## The failure is usually social, not formal

A shared model makes a claim about the plant: that a *pump* is a pump, that its *state* is one of
a known set of values, and that both mean the same thing in the control room, in maintenance, and
in the historian. Somewhere in the plant, someone's job depends on that claim being slightly
different.

We have seen a model rejected because it made two departments' work comparable for the first
time. Neither department was wrong to resist; the model had quietly become an organisational
decision wearing a schema.

## Three patterns that survive contact with a plant

### Map, do not migrate

The teams that succeed rarely replace existing tags. They add a mapping layer and keep the
original identifiers visible, so that anyone can trace a value back to the device it came from.
The mapping table becomes the artefact people argue about — a much healthier place for the
argument to live than in a steering committee.

### Publish the unknown

An empty field is a claim: "we know there is nothing here". If you do not know, say `unknown` and
let it be a distinct value from `not applicable`. Half of our mapping work is deciding which
flavour of missing we are looking at.

### Budget for review, not for tooling

The tooling is the cheap part. Reading 4,000 mappings with the people who own the equipment takes
weeks, and it is the only step that produces trust. Plan it as engineering work with names
attached.

## A small example

The same signal, described three ways. Only the third survived review:

| Description | Why it failed review |
| --- | --- |
| `line3.temp` | Nobody could say what it measures or in what unit. |
| `Line3_Pump_Temperature_Celsius` | Encodes the unit in the name, so a unit change becomes a rename. |
| `line3/pump-2/bearing-temperature` with `unit: degC`, `sensor: pt100`, `sampled_by: plc-7` | Survives, because every claim is separately checkable and separately wrong. |

The lesson is not that long identifiers are better. It is that each fact about the signal should
live in exactly one place, where it can be corrected by the person who knows it.

## What we do now

Before a mapping is allowed near a production line, we ask three questions:

1. Who can be wrong about this, and how would we find out?
2. What does the plant do today when this value is missing?
3. If the model changes next year, what breaks?

If the third answer is "everything", the mapping is not ready. The minimal ontology we ended up
with, and the failure modes we hit getting there, are documented in
[OIL-TR-2025-01]({{ '/publications/' | relative_url }}).
