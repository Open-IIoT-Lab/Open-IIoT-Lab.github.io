#!/usr/bin/env python3
"""Check every internal link in the generated site.

Run after `bundle exec jekyll build`:

    python3 scripts/check_links.py _site

It verifies that
  * every internal href/src points at a file that the build actually produced, and
  * every in-page fragment (href="/publications/#some-report") resolves to an element
    with that id on the target page.

CI runs this so a renamed page or a removed section cannot leave dead links behind
(the Showcase -> Research rename did exactly that once).
"""

import html
import os
import re
import sys

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
ID_RE = re.compile(r'\sid="([^"]+)"')
SKIP_PREFIXES = ("http://", "https://", "//", "mailto:", "data:", "javascript:", "#")


def target_path(root, url):
    """Return (file, fragment) for an internal URL, or None if it is external."""
    if url.startswith(SKIP_PREFIXES) and not url.startswith("#"):
        return None
    path, _, fragment = url.partition("#")
    path = path.split("?")[0]
    if not path:
        return None
    candidate = os.path.join(root, path.lstrip("/"))
    if path.endswith("/"):
        candidate = os.path.join(candidate, "index.html")
    elif not os.path.isfile(candidate):
        index = os.path.join(candidate, "index.html")
        if os.path.isfile(index):
            candidate = index
    return candidate, fragment


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "_site"
    if not os.path.isdir(root):
        print("no such directory: {}".format(root))
        return 1

    pages = {}
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".html"):
                full = os.path.join(dirpath, filename)
                with open(full, encoding="utf-8", errors="replace") as handle:
                    text = handle.read()
                pages[full] = (text, set(ID_RE.findall(text)))

    problems = []
    checked = 0
    for source, (text, _) in sorted(pages.items()):
        for raw in LINK_RE.findall(text):
            url = html.unescape(raw)
            if url.startswith("#"):
                fragment = url[1:]
                checked += 1
                if fragment and fragment not in pages[source][1]:
                    problems.append(
                        "{}: {} -> no element with id '{}'".format(
                            os.path.relpath(source, root), url, fragment
                        )
                    )
                continue
            resolved = target_path(root, url)
            if resolved is None:
                continue
            target, fragment = resolved
            checked += 1
            relative_source = os.path.relpath(source, root)
            if not os.path.isfile(target):
                problems.append("{}: {} -> missing file".format(relative_source, url))
                continue
            if fragment and target in pages:
                if fragment not in pages[target][1]:
                    problems.append(
                        "{}: {} -> no element with id '{}' on {}".format(
                            relative_source, url, fragment, os.path.relpath(target, root)
                        )
                    )

    print("checked {} internal links across {} pages".format(checked, len(pages)))
    for problem in problems:
        print("BROKEN  " + problem)
    if problems:
        print("{} broken link(s)".format(len(problems)))
        return 1
    print("no broken internal links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
