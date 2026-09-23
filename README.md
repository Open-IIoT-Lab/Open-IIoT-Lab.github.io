# Open IIoT Lab — homepage

The website for **Open IIoT Lab**, an open research collective working on industrial
intelligence, edge-native systems, and trustworthy automation.

The site is built with Jekyll on top of the
[Nostalgia 1990s academic homepage template](https://github.com/luost26/academic-homepage-nostalgia-1990s)
by [luost26](https://github.com/luost26), which is itself a variant of
[academic-homepage](https://github.com/luost26/academic-homepage). The late-1990s desktop design
language — teal backdrop, beveled silver chrome, navy masthead, tabbed navigation, classic icons —
comes from that template; the content, the lab mark, and the section structure are the lab's own.

![The Open IIoT Lab homepage: navy masthead, tabbed navigation, profile rail, and the lab's focus areas, programmes, milestones, and news](assets/images/screenshots/homepage.png)

> **The repository is private.** That is fine for development and for a private preview, but
> GitHub Pages is only available for private repositories on paid plans (see
> [Publishing](#publishing)).

## Preview locally

The site is plain Jekyll; there is no build step for the content itself.

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://127.0.0.1:4000/>. With the default `baseurl: ""` in `_config.yml` the site is
served from the root of the local server, so internal links work as written.

`bundle exec jekyll build` writes the generated site to `_site/`.

## What is in the repository

| Path | What it holds |
| --- | --- |
| `_data/profile.yml` | Lab name, strapline, contact links, about text, focus areas, programmes, milestones |
| `_data/navigation.yml` | The four navigation tabs, in order |
| `_data/display.yml` | Which homepage sections are shown, how many news items, footer text |
| `_data/authors.yml` | Author names used (and highlighted) in publication lists |
| `_news/*.md` | One file per news line on the homepage |
| `_publications/<year>/*.md` | One file per report, paper, or working paper |
| `_posts/*.md` | Blog articles (the lab notebook) |
| `_showcase/<group>/*.md` | Showcase cards, grouped by their `group:` field |
| `index.html`, `publications.html`, `blog.html`, `showcase.html`, `404.html` | Page shells; they mostly assemble the widgets below |
| `_layouts/`, `_includes/` | Template engine: page layouts and the widgets each page uses |
| `assets/` | Theme CSS and JS, the Windows 95-style font, and the classic icon set |
| `.github/workflows/jekyll-build.yml` | CI that builds the site and uploads the generated `_site` as an artifact |

Content lives in data files and Markdown; you should not need to touch `_layouts/`, `_includes/`,
or `assets/` to keep the site up to date.

## Editing content

**Lab identity and homepage background** — `_data/profile.yml`. The three background groups reuse
the template's `education`, `experience`, and `awards` keys; the headings shown on the page are
renamed to *Focus areas*, *Programmes*, and *Milestones* through the `section_headings` map in the
same file, so the widget itself stays untouched.

**A news line** — add `_news/YYYY-MM-DD-short-title.md`:

```yaml
---
title: >-
    What happened, in one sentence. <a href="publications">Optional link <i class="fas fa-angle-double-right"></i></a>
date: 2026-01-15 09:00:00 +0800
---
```

**A publication** — add `_publications/<year>/<year>-short-title.md`. Set `selected: true` to show
it on the homepage. Fields: `title`, `date`, `selected`, `pub_pre`, `pub`, `pub_date`, `pub_last`
(trailing badges), `abstract`, `authors` (keys from `_data/authors.yml`), `links`, and optionally
`cover` (an image path; without it the template draws a deterministic dithered cover from the
title) and `semantic_scholar_id` (adds a live citation count).

**A blog article** — add `_posts/YYYY-MM-DD-short-title.md` with `layout: blog_post`, `title`,
`date`, and `tags`. Articles are published under `/blog/YYYY/MM/DD/slug/`; headings in the article
become the "On this page" list automatically.

**A showcase card** — add `_showcase/<group>/<name>.md`:

```yaml
---
show: true
width: 6          # 1-12; 6 is half width, 12 is full width
date: 2026-01-15 09:00:00 +0800
group: Programmes
---

<div class="p-4">
    <h3>Card title</h3>
    <p>Plain HTML, styled by the theme's classic card look.</p>
</div>
```

Cards are ordered by `date` (newest first) and grouped by `group` (the newest card's group appears
first).

## Publishing

The generated site is a normal Jekyll site, so it can be served by GitHub Pages, an internal web
server, or any static host.

- **GitHub Pages, private repository:** Pages on a private repository requires a paid GitHub plan.
  If the account has one, enable Pages with "Deploy from a branch" and select the branch root.
- **GitHub Pages, free plan:** the repository has to be public. Make it public only after checking
  the content in `_data/`, `_news/`, and `_publications/` — nothing in this repository is secret,
  but the placeholder text should be replaced first.
- **Any static host:** run `bundle exec jekyll build` and upload `_site/`.

When the site is served from a subpath (for example `https://<user>.github.io/open-iiot-lab-homepage/`),
set `baseurl` in `_config.yml` to that subpath — `/open-iiot-lab-homepage` — and rebuild. The
template's debugging widgets on the homepage will show a warning whenever `baseurl` does not match
the path the site is actually served from.

## Replace before publishing

The site ships with coherent but **sample** content so the design can be judged in context:

- `hello@openiiotlab.org` and the `github:` entry in `_data/profile.yml` are placeholders.
- The reports in `_publications/`, the news lines, the blog articles, and the showcase cards
  describe the kind of work the lab does; they are not claims about real projects, and every date,
  identifier, and number in them is illustrative.
- `assets/images/open-iiot-mark.svg` and `assets/images/favicon.svg` are the lab mark and its
  favicon; replace them if the lab has its own artwork.

## Credits and licence

The theme is adapted from [luost26/academic-homepage-nostalgia-1990s](https://github.com/luost26/academic-homepage-nostalgia-1990s),
released under the MIT licence — see [`LICENSE`](LICENSE), which is kept unchanged. The Windows 98
icon set, the W95FA and MS Sans Serif fonts, and the other artwork keep their own licences and
provenance records; those notices ship with the assets (`assets/images/classic/NOTICE.md`,
`assets/fonts/classic/NOTICE.md`) and are repeated in the collapsed *Artwork credits* section in
the site footer. Please keep those credits and licence files in place when reusing the theme.
