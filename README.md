# Open Industrial IoT Lab website

Website for Open Industrial IoT Lab at Zhejiang University, led by Chaojie Gu.

## Content and sources

The site's research directions, PI biography, contact details and recruitment text are based on:

- [Zhejiang University Chinese profile](https://person.zju.edu.cn/gucj)
- [Chaojie Gu's English homepage](https://chaojiegu.github.io/)
- [Complete publication list](https://chaojiegu.github.io/publications/)

The publication archive includes every entry in the PI's bibliography, including conference and journal versions, workshops, the book and the thesis. It is cross-checked against the author's paper collection; accepted work awaiting proceedings is labeled explicitly. The homepage highlights seven papers under Industrial Networks and Industrial Intelligence. Research narratives connect scientific questions to a sequence of results, with links to the full archive and associated resources.

Selected papers are drawn from CCF-A and CAA-A+ venues. Classification sources are recorded in `_data/publication_selection.yml`; the CAA source is the 2025 revision in CAST's fifth compilation. Each selected paper includes a figure extracted from its original PDF, with a descriptive caption, original figure number and a link to the paper. The website does not redistribute the source PDF collection.

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
- `_data/people.yml`: sourced student and alumni roster; add optional `photo` and `url` fields as profiles become available
- `_data/navigation.yml`: navigation
- `assets/bibliography/publications.bib`: complete downloadable bibliography
- `_publications/<year>/*.md`: generated publication records
- `_data/publication_overrides.yml`: sourced metadata corrections and homepage selections
- `_data/publication_figures.yml`: source filenames, page numbers, crop coordinates and figure captions
- `_data/publication_selection.yml`: official sources for venue classifications
- `_data/research.yml`: research narratives, paper groupings and resource connections
- `_data/resources.yml`: verified code, tools and implementation guides
- `index.html`, `research.html`, `publications.html`, `resources.html`, `people.html`, `contact.html`: page content
- `assets/css/global.css`: visual styles

After updating the bibliography, run `python scripts/import_publications.py` (requires `bibtexparser` 1.x and `PyYAML`). It preserves existing record paths, checks unique keys and DOIs, and requires every paper to have a research theme. The website itself builds with Jekyll and needs no Python packages beyond the standard-library link checker.

To re-extract the selected figures from an authorized local PDF collection, run `python scripts/extract_publication_figures.py --papers-dir PATH` (requires `PyMuPDF` and `PyYAML`), then rerun the publication importer. Crops are rendered directly from the original artwork at 216 dpi without changing their proportions.

The theme derives from [academic-homepage — Nostalgia 1990s](https://github.com/luost26/academic-homepage-nostalgia-1990s) under the MIT licence. Icon, cursor and font attributions appear in the site footer.
