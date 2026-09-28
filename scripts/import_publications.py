"""Generate Jekyll records from the complete, downloadable BibTeX bibliography.

Run with: python scripts/import_publications.py
Requires bibtexparser 1.x and PyYAML; neither is needed for the Jekyll build.
Existing records are matched by bibliography key or DOI to preserve their paths.
"""
import calendar
import json
import re
from pathlib import Path
from urllib.parse import quote

import bibtexparser
from bibtexparser.customization import convert_to_unicode
import yaml

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "assets/bibliography/publications.bib"
PDF_BASE = "https://chaojiegu.github.io/assets/pdf/"


def clean(value):
    return re.sub(r"\s+", " ", str(value).replace("{", "").replace("}", "")).strip()


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def main():
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    database = bibtexparser.loads(BIB.read_text(encoding="utf-8"), parser=parser)
    overrides = yaml.safe_load((ROOT / "_data/publication_overrides.yml").read_text(encoding="utf-8"))
    themes = yaml.safe_load((ROOT / "_data/research.yml").read_text(encoding="utf-8"))
    figures = yaml.safe_load((ROOT / "_data/publication_figures.yml").read_text(encoding="utf-8"))
    selection = yaml.safe_load((ROOT / "_data/publication_selection.yml").read_text(encoding="utf-8"))
    keys = {e["ID"] for e in database.entries}
    assert len(keys) == len(database.entries), "Duplicate bibliography keys"
    assert set(overrides) <= keys, "Override refers to an unknown bibliography key"
    topics = {}
    for theme in themes:
        for key in theme["paper_keys"]:
            assert key in keys, f"Unknown research paper: {key}"
            topics.setdefault(key, []).append(theme["id"])
    assert keys == set(topics), f"Unclassified papers: {keys - set(topics)}"

    existing = {}
    for path in (ROOT / "_publications").glob("*/*.md"):
        data = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        key = data.get("bib_key") or data.get("links", {}).get("DOI", "").lower()
        existing[key] = (path, data)
    months = {name.lower(): i for i, name in enumerate(calendar.month_abbr) if name}
    seen_ids, seen_dois, generated = set(), set(), []
    for entry in database.entries:
        key = entry["ID"]
        extra = overrides.get(key, {})
        entry.update(extra.get("bib", {}))
        doi = entry.get("doi", "").strip()
        if doi:
            assert doi.lower() not in seen_dois, f"Duplicate DOI: {doi}"
            seen_dois.add(doi.lower())
        paper_id = "pub-" + slug(key)
        assert paper_id not in seen_ids, f"Duplicate ID: {paper_id}"
        seen_ids.add(paper_id)
        year = int(entry["year"])
        month = months.get(entry.get("month", "")[:3].lower(), 1)
        title = clean(entry["title"])
        authors = []
        for author in entry["author"].split(" and "):
            parts = [clean(p) for p in author.strip(" ,").split(",") if p.strip()]
            authors.append(" ".join(parts[1:] + parts[:1]) if len(parts) > 1 else parts[0])
        kind = extra.get("kind") or {"article": "Journal article", "inproceedings": "Conference paper", "phdthesis": "Thesis", "book": "Book"}.get(entry["ENTRYTYPE"], "Other")
        if "WKP" in entry.get("abbr", "") or any(s in entry.get("abbr", "") for s in ["Poster", "Demo"]):
            kind = "Workshop / demo"
        venue = clean(entry.get("journal") or entry.get("booktitle") or entry.get("school") or entry.get("publisher", ""))
        if extra.get("selected"):
            assert extra.get("selected_topic") in topics[key], f"Selected theme mismatch: {key}"
            assert extra.get("figure") in figures, f"Missing figure provenance: {key}"
            assert venue in selection[extra["selection_basis"]]["venues"], f"Unverified venue classification: {key}"
            assert figures[extra["figure"]]["source"].lower() == ("https://doi.org/" + doi).lower(), f"Figure source mismatch: {key}"
        links = {}
        if doi:
            links["DOI"] = "https://doi.org/" + doi
        for field, label in [("pdf", "PDF"), ("arxiv", "arXiv"), ("code", "Code"), ("website", "Project"), ("html", "Publisher"), ("slides", "Slides"), ("video", "Video"), ("supp", "Supplement")]:
            if entry.get(field):
                url = entry[field]
                if field == "pdf" and not url.startswith("https://"):
                    url = PDF_BASE + quote(url, safe="/")
                elif field == "arxiv" and not url.startswith("https://"):
                    url = "https://arxiv.org/abs/" + url
                links[label] = url
        record = {
            "bib_key": key, "paper_id": paper_id, "title": title,
            "date": f"{year}-{month:02d}-01", "year": year,
            "kind": kind, "topics": topics[key],
            "selected": bool(extra.get("selected", False)),
            "pub": venue, "pub_date": str(year), "venue_abbr": clean(entry.get("abbr", "")),
            "authors": authors, "links": links,
        }
        if extra.get("abstract"):
            record["abstract"] = extra["abstract"]
        for field in ["selected_order", "selected_topic", "selection_basis", "publication_status"]:
            if extra.get(field) is not None:
                record[field] = extra[field]
        if extra.get("figure"):
            figure = figures[extra["figure"]]
            record["cover"] = f"/assets/images/publications/{extra['figure']}.png"
            record["cover_alt"] = figure["alt"]
            record["cover_caption"] = figure["caption"]
            record["cover_figure"] = figure["figure"]
            record["cover_source"] = figure["source"]
            record["cover_width"] = round((figure["crop"][2] - figure["crop"][0]) * 3)
            record["cover_height"] = round((figure["crop"][3] - figure["crop"][1]) * 3)
        match = existing.get(key) or existing.get(("https://doi.org/" + doi).lower())
        if match:
            path, old = match
            if old.get("legacy_anchor"):
                record["legacy_anchor"] = old["legacy_anchor"]
            elif not old.get("bib_key"):
                record["legacy_anchor"] = slug(old["title"])
        else:
            path = ROOT / "_publications" / str(year) / (slug(key) + ".md")
        path.parent.mkdir(parents=True, exist_ok=True)
        content = "---\n" + yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=110) + "---\n"
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8", newline="\n")
        generated.append(path)
    assert set((ROOT / "_publications").glob("*/*.md")) == set(generated), "Stale publication files need review"
    BIB.write_text(bibtexparser.dumps(database).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"publications": len(generated), "years": sorted({int(e['year']) for e in database.entries}), "unique_dois": len(seen_dois)}))


if __name__ == "__main__":
    main()
