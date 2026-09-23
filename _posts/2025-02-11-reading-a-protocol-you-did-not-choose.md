---
layout: blog_post
title: 'Reading a protocol you did not choose'
date: 2025-02-11 09:00:00 +0800
tags:
  - protocols
  - legacy
  - field-notes
---

Sooner or later every industrial project inherits an interface that nobody documented, on
equipment that cannot be stopped, speaking a protocol that is *almost* the standard one. The
temptation is to write code until something moves. The method below is slower for the first day
and much faster for the next six months.

## 1. Capture before you guess

Write down what is actually on the wire, with timestamps, before forming any theory about it.
Theory is cheap and it contaminates observation.

```bash
# Capture the conversation without joining it.
# -s 0 keeps whole frames; -w writes a file we can re-read later, repeatedly.
tcpdump -i eth1 -s 0 -w captures/line3-2025-02-11.pcap 'tcp port 502 or tcp port 44818'
```

Then record the *context* of the capture: what the machine was doing, what the operator did, and
when. A capture without context is a list of numbers.

## 2. Find the invariants

Look for the parts that never change: the header, the length field, the unit identifier, the
sequence number. Invariants are the skeleton of the protocol, and they are usually visible within
a few hundred frames.

## 3. Find the safety envelope

Before the first write, answer these questions in writing:

- What is the worst thing a malformed write can do to the process?
- What happens if the connection drops mid-write?
- Which values are physically impossible, and will the equipment reject them or accept them?
- Who is allowed to authorise a write, by name?

> The first write is an operational event, not a debugging step. Treat it like one: announce it,
> schedule it, and have the rollback ready before you need it.

## 4. Write down what you still do not know

This is the step teams skip, and it is the one that prevents the next incident. A short,
honest list — "the meaning of byte 7 is unknown; it is 0x00 in all captures so far" — is worth
more than a confident parser that hides the uncertainty.

## 5. Build the smallest possible reader

Read-only first. A reader that logs every field, including the ones you do not understand, gives
you the data to understand them later without touching the machine again.

## The artefact that matters

The output of this work is not a driver. It is a short document: the frame layout as understood,
the invariants, the safety envelope, the open questions, and the date. Anyone who follows you
should be able to disagree with your conclusions without re-doing your observations.

We keep the full method, including the field checklist and the mistakes that produced it, in
[OIL-TR-2024-01]({{ '/publications' | relative_url }}). The companion notes on integrating what
you find are on the [blog index]({{ '/blog' | relative_url }}).
