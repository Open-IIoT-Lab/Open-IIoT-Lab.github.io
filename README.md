# Open Industrial IoT Lab — website

The website of **Open Industrial IoT Lab** (Open IIoT), a research lab working on edge-native
industrial systems, interoperability, and trustworthy automation.

**Live: <https://open-iiot-lab.github.io/>**

![The lab homepage](assets/images/screenshots/homepage.png)

## Preview locally

```bash
bundle install
bundle exec jekyll serve     # http://127.0.0.1:4000/
```

`bundle exec jekyll build` writes the site to `_site/`.

## Editing

Almost everything lives in data files and Markdown; the layouts and theme in `_layouts/`,
`_includes/`, and `assets/` rarely need to change.

| Path | What it holds |
| --- | --- |
| `_data/profile.yml` | Lab name, eyebrow, contact links, about text, focus areas, programmes, milestones |
| `_data/navigation.yml` | The navigation tabs |
| `_data/display.yml` | Which homepage sections appear, how many news items, footer text |
| `_data/authors.yml` | Author names used (and highlighted) in publication lists |
| `_data/people.yml` | Lab members, grouped by role for the People page |
| `_data/gallery.yml` | Photo sets for the Gallery page |
| `_news/*.md` | One file per news line on the homepage |
| `_publications/<year>/*.md` | One file per report; set `programme:` to list it under a programme |
| `_resources/*.md` | One file per open-source project on the Resources page |
| `_posts/*.md` | Blog articles |
| `_research/<group>/*.md` | Research cards: programme cards and the "how we work" cards |
| `index.html`, `research.html`, `publications.html`, `resources.html`, `people.html`, `blog.html`, `gallery.html`, `contact.html` | Page shells |

A resource entry uses front matter for its metadata and the file body for its description:

```yaml
---
title: Open Edge Runtime
date: 2026-02-18 09:00:00 +0800
package: oil-edge-runtime      # shown in the monospace metadata line
version: 0.9.2
license: Apache-2.0
stack: Go · Rust
status: stable                 # stable -> "Stable releases"; anything else -> "In development"
summary: One line about what it is.
links:
  Programme: /research/        # internal links keep the site free of dead ends
  Report: /publications/#<report-title-slug>
---

A paragraph or two about what the project contains and where it fails.
```

Each page's front matter carries a `navbar_title` that must match the `name` of its entry in
`_data/navigation.yml` so the right tab is highlighted. Internal links use the canonical
trailing-slash form (`/publications/`); `scripts/check_links.py` fails the build if a link or an
in-page anchor points at something that does not exist.

## Deployment

Every push to `main` builds the site and publishes it with GitHub Pages through
`.github/workflows/pages.yml`; pull requests only build, so a broken page is caught first.

After a deploy, hard-refresh (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>) if a page still looks
like the previous version: GitHub Pages caches HTML for ten minutes. The footer shows the build id
it was generated from, so a stale page is easy to spot.

## Content status

The reports, news lines, blog articles, and research cards describe the kind of work the lab does;
they are sample content, and every date, identifier, and number in them is illustrative. The People
and Gallery pages stay empty until members are added to `_data/people.yml` and photos to
`_data/gallery.yml` — both pages explain that state rather than showing a broken layout.

## Credits

The theme is adapted from [academic-homepage — Nostalgia 1990s](https://github.com/luost26/academic-homepage-nostalgia-1990s)
by [luost26](https://github.com/luost26), released under the MIT licence (see `LICENSE`). The
bundled icons and font keep their own provenance and licence notices:
`assets/images/classic/NOTICE.md` and `assets/fonts/classic/NOTICE.md`. Artwork credits also appear
in the collapsed *Artwork credits* section of the site footer.
