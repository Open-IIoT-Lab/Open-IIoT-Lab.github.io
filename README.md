# Open Industrial IoT Lab website

Website for Open Industrial IoT Lab at Zhejiang University, led by Chaojie Gu.

## Content and sources

The site's research directions, PI biography, contact details and recruitment text are based on:

- [Zhejiang University Chinese profile](https://person.zju.edu.cn/gucj)
- [Chaojie Gu's English homepage](https://chaojiegu.github.io/)
- [Complete publication list](https://chaojiegu.github.io/publications/)

The publication archive includes every entry in the PI's bibliography, including conference and journal versions, workshops, the book and the thesis. The homepage highlights four papers. Research themes connect a scientific question to a sequence of results, with direct links to the full archive and associated resources.

The resource catalog includes repositories linked from publications and verified author project pages. An unavailable repository is labeled explicitly and has no active code button. The catalog does not imply that every linked implementation is maintained by this lab.

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
- `assets/bibliography/publications.bib`: complete downloadable bibliography
- `_publications/<year>/*.md`: generated publication records
- `_data/publication_overrides.yml`: sourced metadata corrections and homepage selections
- `_data/research.yml`: research narratives, paper groupings and resource connections
- `_data/resources.yml`: verified code, tools and implementation guides
- `index.html`, `research.html`, `publications.html`, `resources.html`, `people.html`, `contact.html`: page content
- `assets/css/global.css`: visual styles

After updating the bibliography, run `python scripts/import_publications.py` (requires `bibtexparser` 1.x and `PyYAML`). It preserves existing record paths, checks unique keys and DOIs, and requires every paper to have a research theme. The website itself builds with Jekyll and needs no Python packages beyond the standard-library link checker.

The theme derives from [academic-homepage — Nostalgia 1990s](https://github.com/luost26/academic-homepage-nostalgia-1990s) under the MIT licence. Icon, cursor and font attributions appear in the site footer.
