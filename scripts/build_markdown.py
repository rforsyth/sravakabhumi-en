#!/usr/bin/env python3
"""Emit one markdown file per topic into markdown/.

Each file contains the English translation, with clauses joined into paragraphs
by the source's `||` boundary (encoded in the segment IDs). Filenames are
ordinal-prefixed so they sort in canonical reading order.

Output is committed: it is the published plain-text edition that downstream
users vendor at a pinned commit, so rebuild it in the same commit as any
translation change.

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


DEF_QUESTION_MAX_LEN = 200


def is_def_question(text: str) -> bool:
    """Short interrogative segment, e.g. 'What is X?' / 'How many māras?' —
    the source's `katama-` definition-question opening. Each gets its own
    paragraph so Q&A pairs are visually distinct."""
    t = text.strip()
    return t.endswith("?") and 0 < len(t) <= DEF_QUESTION_MAX_LEN


def paragraphs(translation: dict, structure: dict) -> list[str]:
    """Group translation segments into paragraphs by the digit-before-dot
    in the segment ID. Segments ending in `.0` (e.g. `:1.0`, `:104.0`) are
    section headings and are emitted as `## ` markdown headings ahead of the
    paragraph body. Skips the 0.x title segments (the page-level title slots).

    `structure` maps segment-id -> role. Roles change how a run of consecutive
    segments is rendered:
      - "uddana"       : italicised topic-line/list, joined with spaces, own paragraph
      - "list"         : bullet list, one bullet per segment
      - "question"     : bullet list of questions, one bullet per segment
      - "def-question" : single interrogative segment, own paragraph (auto-detected
                          for short `?`-ending segments unless overridden)
      - (unset)        : default flowing prose, joined with spaces
    """

    def para_key(seg_id: str) -> str:
        return seg_id.split(":")[1].split(".")[0]

    def clause_idx(seg_id: str) -> str:
        return seg_id.split(":")[1].split(".")[1]

    def render_run(role: str, texts: list[str]) -> str:
        if role == "uddana":
            return "*" + " ".join(texts).rstrip(". ") + "*"
        if role in ("list", "question"):
            return "\n".join(f"- {t}" for t in texts)
        return " ".join(texts)

    # Runs of these roles bridge paragraph-key boundaries so a list/uddana
    # that the source split across `||` boundaries renders as one block.
    SPANNING_ROLES = {"list", "question", "uddana"}

    out: list[str] = []
    run_role: str | None = None
    run_texts: list[str] = []

    def flush():
        nonlocal run_role, run_texts
        if run_texts:
            out.append(render_run(run_role or "", run_texts))
            run_texts = []
            run_role = None

    for key, group in groupby(translation.keys(), key=para_key):
        if key == "0":
            continue
        seg_ids = list(group)
        headings = [sid for sid in seg_ids if clause_idx(sid) == "0"]
        body_ids = [sid for sid in seg_ids if clause_idx(sid) != "0"]

        if headings:
            flush()
        for hid in headings:
            heading_text = translation[hid].strip()
            if heading_text:
                out.append(f"## {heading_text}")

        for sid in body_ids:
            text = translation[sid].strip()
            if not text:
                continue
            role = structure.get(sid, "")
            if not role and is_def_question(text):
                role = "def-question"
            if run_texts and role != run_role:
                flush()
            run_role = role
            run_texts.append(text)
            # A def-question segment ending in `?` closes the paragraph; a
            # subsequent def-question segment that doesn't end in `?` (e.g.
            # `katamā |` followed by `smṛtiḥ |`) keeps the run open until the
            # closing `?` lands.
            if role == "def-question" and text.rstrip().endswith("?"):
                flush()

        if run_role not in SPANNING_ROLES:
            flush()

    flush()
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
        struct_file = TRANS_BASE / CREATOR / "sastra" / "sbh" / f"{uid}_structure-en-{CREATOR}.json"
        structure = json.loads(struct_file.read_text(encoding="utf-8")) if struct_file.exists() else {}
        title = translation.get(f"{uid}:0.2", uid).strip()

        slug = slugify(title)
        filename = f"{ordinal:02d}-{uid}-{slug}.md"

        body = "\n\n".join(paragraphs(translation, structure))
        content = f"# {title}\n\n*Śrāvakabhūmi · {uid}*\n\n{body}\n"

        out_path = OUT_DIR / filename
        out_path.write_text(content, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
