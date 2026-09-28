"""Extract selected figures without redrawing or changing the paper artwork.

Usage: python scripts/extract_publication_figures.py --papers-dir PATH
Requires PyMuPDF and PyYAML. Original PDFs are not copied into the website.
"""
import argparse
from pathlib import Path

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--papers-dir", required=True, type=Path)
    args = parser.parse_args()
    figures = yaml.safe_load((ROOT / "_data/publication_figures.yml").read_text("utf-8"))
    output = ROOT / "assets/images/publications"
    output.mkdir(parents=True, exist_ok=True)
    for name, figure in figures.items():
        with fitz.open(args.papers_dir / figure["file"]) as document:
            page = document[figure["page"] - 1]
            clip = fitz.Rect(figure["crop"])
            assert page.rect.contains(clip), f"Figure crop outside page: {name}"
            # Render vector text and diagrams at 216 dpi; preserve the original aspect ratio.
            page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip, alpha=False).save(output / f"{name}.png")
        print(f"{name}: figure {figure['figure']}, page {figure['page']}")


if __name__ == "__main__":
    main()
