#!/usr/bin/env python3
"""Emit one markdown file per topic into markdown/.

Each file contains the English translation, with clauses joined into paragraphs
by the source's `||` boundary (encoded in the segment IDs). Filenames are
ordinal-prefixed so they sort in canonical reading order.

Output is a local build artifact, not committed to the repo (see .gitignore).

Usage:
    python3 scripts/build_markdown.py
"""

import json
import re
import unicodedata
from itertools import groupby
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT_DIR = REPO / "root" / "san" / "sastra" / "sbh"
TRANS_BASE = REPO / "translation" / "en"
OUT_DIR = REPO / "markdown"

CREATOR = "ryanforsyth"


def natural_key(uid: str) -> tuple:
    return tuple(int(p) if p.isdigit() else p for p in re.split(r"(\d+)", uid))


def slugify(text: str) -> str:
    # Strip diacritics, lowercase, replace non-alphanumeric with hyphens.
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "untitled"


def paragraphs(translation: dict) -> list[str]:
    """Group translation segments into paragraphs by the digit-before-dot
    in the segment ID. Segments ending in `.0` (e.g. `:1.0`, `:104.0`) are
    section headings and are emitted as `## ` markdown headings ahead of the
    paragraph body. Skips the 0.x title segments (the page-level title slots).
    """

    def para_key(seg_id: str) -> str:
        return seg_id.split(":")[1].split(".")[0]

    def clause_idx(seg_id: str) -> str:
        return seg_id.split(":")[1].split(".")[1]

    out = []
    for key, group in groupby(translation.keys(), key=para_key):
        if key == "0":
            continue
        seg_ids = list(group)
        headings = [sid for sid in seg_ids if clause_idx(sid) == "0"]
        body_ids = [sid for sid in seg_ids if clause_idx(sid) != "0"]
        for hid in headings:
            heading_text = translation[hid].strip()
            if heading_text:
                out.append(f"## {heading_text}")
        clauses = [translation[sid].strip() for sid in body_ids]
        text = " ".join(c for c in clauses if c)
        if text:
            out.append(text)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Clear stale outputs so renames/splits don't leave orphan files behind.
    for stale in OUT_DIR.glob("[0-9][0-9]-sbh*.md"):
        stale.unlink()

    uids = sorted(
        (p.stem.replace("_root-san-shukla", "") for p in ROOT_DIR.glob("*_root-san-shukla.json")),
        key=natural_key,
    )

    for ordinal, uid in enumerate(uids, start=1):
        trans_file = TRANS_BASE / CREATOR / "sastra" / "sbh" / f"{uid}_translation-en-{CREATOR}.json"
        if not trans_file.exists():
            print(f"  skipping {uid} (no translation)")
            continue

        translation = json.loads(trans_file.read_text(encoding="utf-8"))
        title = translation.get(f"{uid}:0.2", uid).strip()

        slug = slugify(title)
        filename = f"{ordinal:02d}-{uid}-{slug}.md"

        body = "\n\n".join(paragraphs(translation))
        content = f"# {title}\n\n*Śrāvakabhūmi · {uid}*\n\n{body}\n"

        out_path = OUT_DIR / filename
        out_path.write_text(content, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
