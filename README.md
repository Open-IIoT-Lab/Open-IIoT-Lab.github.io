# Open Industrial IoT Lab website

Website for Open Industrial IoT Lab at Zhejiang University, led by Chaojie Gu.

## Content and sources

The site's research directions, PI biography, contact details and recruitment text are based on:

- [Zhejiang University Chinese profile](https://person.zju.edu.cn/gucj)
- [Chaojie Gu's English homepage](https://chaojiegu.github.io/)
- [Complete publication list](https://chaojiegu.github.io/publications/)

The local publication list is deliberately selected, not exhaustive. Each entry links to a DOI; available research code links point to repositories listed on the PI's publication page. Verify changes against the official profiles before publishing. No student names or lab news are listed without a verified source.

## Build locally

The site uses Jekyll 3.x. With Ruby and Bundler installed:

    bundle install
    bundle exec jekyll build
    python scripts/check_links.py _site
    bundle exec jekyll serve

The site builds to `_site/`. A push to `main` triggers the GitHub Pages workflow; pull requests run the build and link check without deploying.

## Editing

- `_data/profile.yml`: lab name, affiliation, contact and profile links
- `_data/navigation.yml`: navigation
- `_publications/<year>/*.md`: selected publication entries
- `index.html`, `research.html`, `publications.html`, `resources.html`, `people.html`, `contact.html`: page content
- `assets/css/global.css`: visual styles

The theme derives from [academic-homepage — Nostalgia 1990s](https://github.com/luost26/academic-homepage-nostalgia-1990s) under the MIT licence. Icon, cursor and font attributions appear in the site footer.
