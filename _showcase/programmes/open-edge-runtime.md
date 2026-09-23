---
show: true
width: 6
date: 2025-10-02 09:00:00 +0800
group: Programmes
---

<div class="p-4">
    <h3>Open Edge Runtime</h3>
    <p><strong>Status:</strong> reference implementation · <strong>Started:</strong> 2024</p>
    <p>
        A portable control plane for running event-driven services beside production equipment:
        one binary, one text manifest, and a filesystem layout a plant engineer can read end to
        end. The runtime is deliberately small so that its assumptions stay visible.
    </p>
    <ul>
        <li>Declarative service manifests with explicit deadlines and restart limits.</li>
        <li>Deterministic replay of recorded inputs next to the decisions they produced.</li>
        <li>Failure domains documented per pattern, including the ones we accept on purpose.</li>
    </ul>
    <p>
        <a class="classic-button" href="{{ '/publications' | relative_url }}">Read OIL-TR-2025-02</a>
        <a class="classic-button" href="{{ '/blog/2025/11/04/notes-from-building-an-open-edge-runtime/' | relative_url }}">Build notes</a>
    </p>
</div>
