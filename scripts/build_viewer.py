#!/usr/bin/env python3
"""Build self-contained viewer HTML files from Bilara JSONs.

Usage:
    python3 scripts/build_viewer.py sbh3.1 [sbh3.2 ...]
    python3 scripts/build_viewer.py --all       # builds every topic with a root file

For each topic, emits two pages:
  - docs/<uid>.html       — side-by-side Sanskrit / English (source view)
  - docs/<uid>-en.html    — English-only book view (clauses joined into paragraphs)

Plus docs/index.html listing all built topics with links to both views.
"""

import json
import re
import sys
import html
from pathlib import Path

EM_PATTERN = re.compile(r"\*([^*\n]+)\*")

REPO = Path(__file__).resolve().parent.parent
ROOT_DIR = REPO / "root" / "san" / "sastra" / "sbh"
TRANS_BASE = REPO / "translation" / "en"
COMMENT_BASE = REPO / "comment" / "en"
TRANS_NOTES_DIR = REPO / "notes" / "translation-notes"
DOCS_DIR = REPO / "docs"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Śrāvakabhūmi</title>
<style>
  :root {{
    --san-color: #2a2a2a;
    --en-color: #2a2a2a;
    --id-color: #999;
    --rule-color: #e6e1d8;
    --bg: #fbf8f1;
    --max-width: 1400px;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    font-family: "Charter", "Georgia", "Iowan Old Style", serif;
    color: var(--en-color);
    line-height: 1.55;
  }}
  header {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 2.5rem 2rem 1.5rem;
    border-bottom: 1px solid var(--rule-color);
  }}
  header h1 {{
    margin: 0 0 0.25rem;
    font-size: 1.6rem;
    font-weight: 600;
  }}
  header .sub {{
    color: #666;
    font-size: 0.95rem;
  }}
  header nav {{
    margin-top: 1rem;
    font-size: 0.9rem;
  }}
  header nav a {{
    color: #666;
    text-decoration: none;
    margin-right: 1rem;
  }}
  header nav a:hover {{ color: #000; text-decoration: underline; }}
  main {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 1.5rem 2rem 4rem;
  }}
  .col-headings {{
    display: grid;
    grid-template-columns: {grid_cols};
    gap: 1.5rem;
    padding: 0.5rem 0 0.75rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--rule-color);
    font-size: 0.78rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .col-headings .label-id {{ color: transparent; }}
  .row {{
    display: grid;
    grid-template-columns: {grid_cols};
    gap: 1.5rem;
    padding: 0.5rem 0;
    border-bottom: 1px dotted var(--rule-color);
  }}
  .row.heading {{
    margin-top: 1.5rem;
    border-bottom: none;
  }}
  .row.heading .san, .row.heading .en {{
    font-weight: 600;
    font-size: 1.1rem;
  }}
  .row:target {{
    background: #f4ecd8;
    border-left: 3px solid #c9a96e;
    margin-left: -1rem;
    padding-left: calc(1rem - 3px);
  }}
  .seg-id {{
    color: var(--id-color);
    font-family: "SF Mono", "Menlo", monospace;
    font-size: 0.75rem;
    padding-top: 0.25rem;
  }}
  .seg-id a {{
    color: inherit;
    text-decoration: none;
  }}
  .seg-id a:hover {{
    color: #2a2a2a;
    text-decoration: underline;
  }}
  .san {{
    color: var(--san-color);
    font-style: italic;
  }}
  .en {{
    color: var(--en-color);
  }}
  .en:empty::before {{
    content: "—";
    color: #ccc;
  }}
  .en-cell {{
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }}
  .comment {{
    font-size: 0.85rem;
    color: #6a6a6a;
    line-height: 1.5;
    padding-left: 0.6rem;
    border-left: 2px solid #e6e1d8;
  }}
  .intro {{
    max-width: 720px;
    margin: 0 auto 1.5rem;
    padding: 1rem 1.2rem;
    background: #f4ecd8;
    border-left: 3px solid #c9a96e;
    font-size: 0.95rem;
    line-height: 1.55;
    color: #3a3a3a;
  }}
  .intro p {{ margin: 0 0 0.6rem; }}
  .intro p:last-child {{ margin-bottom: 0; }}
  .intro em {{ font-style: italic; }}
  @media (max-width: 900px) {{
    .col-headings, .row {{
      grid-template-columns: 1fr;
      gap: 0.25rem;
    }}
    .row {{ padding: 0.75rem 0; }}
    .seg-id {{ font-size: 0.7rem; }}
    .col-headings {{ display: none; }}
  }}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <div class="sub">{subtitle}</div>
  <nav><a href="index.html">← All topics</a><a href="{uid}-en.html">View English only →</a></nav>
</header>
<main>
{intro}
<div class="col-headings">
  <div class="label-id">id</div>
  <div>Sanskrit</div>
  {column_labels}
</div>
{rows}
</main>
</body>
</html>
"""

PAGE_BOOK_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Śrāvakabhūmi (English)</title>
<style>
  :root {{
    --text: #2a2a2a;
    --muted: #888;
    --rule: #e6e1d8;
    --bg: #fbf8f1;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    font-family: "Charter", "Georgia", "Iowan Old Style", serif;
    color: var(--text);
    line-height: 1.7;
    font-size: 1.05rem;
  }}
  header {{
    max-width: 720px;
    margin: 0 auto;
    padding: 2.5rem 2rem 1.5rem;
    border-bottom: 1px solid var(--rule);
  }}
  header h1 {{ margin: 0 0 0.25rem; font-size: 1.7rem; font-weight: 600; }}
  header .sub {{ color: #666; font-size: 0.95rem; }}
  header nav {{ margin-top: 1rem; font-size: 0.9rem; }}
  header nav a {{ color: #666; text-decoration: none; margin-right: 1rem; }}
  header nav a:hover {{ color: #000; text-decoration: underline; }}
  main {{
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem 2rem 4rem;
  }}
  p {{
    margin: 0 0 1.1rem;
    text-align: justify;
    hyphens: auto;
  }}
  p:target {{
    background: #f4ecd8;
    border-left: 3px solid #c9a96e;
    padding-left: 0.75rem;
    margin-left: -0.75rem;
  }}
  h2 {{
    margin: 2rem 0 0.6rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: 0.01em;
  }}
  h2:first-of-type {{ margin-top: 0.5rem; }}
  .intro {{
    margin: 0 0 1.8rem;
    padding: 1rem 1.2rem;
    background: #f4ecd8;
    border-left: 3px solid #c9a96e;
    font-size: 0.95rem;
    line-height: 1.55;
    color: #3a3a3a;
  }}
  .intro p {{ margin: 0 0 0.6rem; text-align: left; }}
  .intro p:last-child {{ margin-bottom: 0; }}
  .intro em {{ font-style: italic; }}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <div class="sub">{subtitle}</div>
  <nav><a href="index.html">← All topics</a><a href="{uid}.html">View side-by-side ↔</a></nav>
</header>
<main>
{intro}
{paragraphs}
</main>
</body>
</html>
"""


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Śrāvakabhūmi — Working Bilingual Edition</title>
<style>
  body {{
    margin: 0;
    background: #fbf8f1;
    font-family: "Charter", "Georgia", "Iowan Old Style", serif;
    line-height: 1.6;
    color: #2a2a2a;
  }}
  .wrap {{ max-width: 760px; margin: 0 auto; padding: 3.5rem 2rem 4rem; }}
  h1 {{
    margin: 0 0 0.25rem;
    font-size: 1.9rem;
    font-weight: 600;
  }}
  .tagline {{
    color: #666;
    font-size: 1rem;
    margin-bottom: 2.5rem;
  }}
  h2 {{
    margin-top: 2.5rem;
    margin-bottom: 0.75rem;
    font-size: 1.15rem;
    font-weight: 600;
    color: #2a2a2a;
  }}
  p {{ margin: 0 0 1rem; }}
  .disclosure {{
    background: #f4ecd8;
    border-left: 3px solid #c9a96e;
    padding: 0.9rem 1.1rem;
    margin: 1.5rem 0 2rem;
    font-size: 0.95rem;
  }}
  .disclosure strong {{ display: block; margin-bottom: 0.25rem; }}
  ul.topics {{
    list-style: none;
    padding: 0;
    margin: 0;
    border-top: 1px solid #e6e1d8;
  }}
  ul.topics li {{
    padding: 0.7rem 0;
    border-bottom: 1px dotted #e6e1d8;
  }}
  ul.topics a {{
    color: #2a2a2a;
    text-decoration: none;
    display: flex;
    align-items: baseline;
  }}
  ul.topics a:hover {{ text-decoration: underline; }}
  ul.topics li {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
  }}
  ul.topics a.alt {{
    color: #888;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-left: auto;
  }}
  ul.topics a.alt:hover {{ color: #2a2a2a; }}
  .uid {{
    color: #999;
    font-family: "SF Mono", "Menlo", monospace;
    font-size: 0.85rem;
    margin-right: 0.9rem;
    flex-shrink: 0;
  }}
  dl.meta {{
    display: grid;
    grid-template-columns: 8rem 1fr;
    gap: 0.5rem 1rem;
    font-size: 0.95rem;
    margin: 0;
  }}
  dl.meta dt {{ color: #888; }}
  dl.meta dd {{ margin: 0; }}
  footer {{
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e6e1d8;
    font-size: 0.85rem;
    color: #888;
  }}
  a.link {{ color: #5a4a2a; }}
</style>
</head>
<body>
<div class="wrap">

<h1>Śrāvakabhūmi</h1>
<div class="tagline">A working bilingual edition of Asaṅga's Śrāvakabhūmi, in Sanskrit (Shukla 1973) and English.</div>

<h2>About</h2>
<p><em>Śrāvakabhūmi</em> means "The Stage of the Disciple" — from <em>śrāvaka</em>, literally "hearer," the term for those who heard the Buddha's teaching directly and trained for liberation as arhats, and <em>bhūmi</em>, "ground" or "stage." It is a section of the <em>Yogācārabhūmi-Śāstra</em>, the encyclopedic treatise on yogic practice traditionally ascribed to Asaṅga (4th century CE). Organized into four <em>yogasthānas</em> ("yogic foundations"), it lays out a detailed program of contemplative training: the nine stages of mental abiding (<em>śamatha</em>), the method of insight (<em>vipaśyanā</em>), the five temperament-matched practices (foulness, lovingkindness, dependent origination, elements, breath), and the seven attentions of the mundane path.</p>
<p>The Sanskrit original was long thought lost in India until 1938, when the explorer-scholar Rāhula Sāṅkṛtyāyana located and photographed a palm-leaf manuscript at Shalu Monastery in Tibet; those photographs are the basis for every modern Sanskrit edition, including the source text used here.</p>

<h2>Topics</h2>
<ul class="topics">
{items}
</ul>

<div class="disclosure">
<strong>This is an AI-assisted working translation.</strong>
Prepared from the Sanskrit with reference to standard Buddhist Sanskrit dictionaries and established technical terminology in the secondary literature. It is not a scholarly critical edition. Reports of errors or improvements welcome (see Contributing below).
</div>

<h2>Edition details</h2>
<dl class="meta">
<dt>Sanskrit source</dt><dd>Karunesha Shukla edition (1973), as hosted on <a class="link" href="https://suttacentral.net/sbh/san/shukla">SuttaCentral</a>.</dd>
<dt>Translator</dt><dd>Ryan Forsyth, AI-assisted, from the Shukla Sanskrit edition.</dd>
<dt>Format</dt><dd>Bilara-compatible segmented JSON (sources) rendered as side-by-side HTML.</dd>
<dt>License</dt><dd><a class="link" href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0 Universal</a> — dedicated to the public domain.</dd>
</dl>

<h2>Contributing</h2>
<p>Errors, alternative readings, and improvements are welcome via GitHub issues or pull requests on the source repository.</p>

<footer>
Cite as: Forsyth, R. (2026). <em>Śrāvakabhūmi (working bilingual edition)</em>. Translated from the Shukla (1973) Sanskrit, AI-assisted. CC0.
</footer>

</div>
</body>
</html>
"""


def extract_intro(uid: str) -> str:
    """Pull the first paragraph after the H1 from notes/translation-notes/<uid>.md
    and return as an HTML block. Convention: that paragraph is the website intro;
    subsequent paragraphs and sections stay file-only.

    *italic* spans are converted to <em>; backtick `code` spans to <code>.
    Returns empty string if the notes file is absent or has no intro paragraph."""
    path = TRANS_NOTES_DIR / f"{uid}.md"
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    intro_lines: list[str] = []
    seen_h1 = False
    for line in lines:
        if line.startswith("# "):
            seen_h1 = True
            continue
        if not seen_h1:
            continue
        if line.startswith("## "):
            break
        if not line.strip():
            if intro_lines:
                break  # blank line ends the first paragraph
            continue  # skip leading blank lines
        intro_lines.append(line.strip())
    if not intro_lines:
        return ""
    text = " ".join(intro_lines)
    escaped = html.escape(text)
    with_em = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", escaped)
    with_code = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", with_em)
    with_links = re.sub(
        r"\[([^\]\n]+)\]\(([^)\n]+)\)",
        r'<a href="\2">\1</a>',
        with_code,
    )
    return f'<div class="intro"><p>{with_links}</p></div>'


def discover_creators() -> list[str]:
    """Return creator_uids in publication order, then any unlisted alphabetically."""
    pub_file = REPO / "_publication-v2.json"
    listed = []
    if pub_file.exists():
        for entry in json.loads(pub_file.read_text(encoding="utf-8")):
            uid = entry.get("creator_uid")
            if uid and uid not in listed:
                listed.append(uid)
    on_disk = sorted(p.name for p in TRANS_BASE.iterdir() if p.is_dir())
    extras = [u for u in on_disk if u not in listed]
    return [u for u in listed if u in on_disk] + extras


def trans_path(creator: str, uid: str) -> Path:
    return TRANS_BASE / creator / "sastra" / "sbh" / f"{uid}_translation-en-{creator}.json"


def comment_path(creator: str, uid: str) -> Path:
    return COMMENT_BASE / creator / "sastra" / "sbh" / f"{uid}_comment-en-{creator}.json"


def _is_heading(seg_id: str) -> bool:
    last = seg_id.split(":")[-1]
    return seg_id.endswith(":0.1") or seg_id.endswith(":0.2") or last.endswith(".0")


def _en_cell(en: str, comment: str) -> str:
    en_html = f'<div class="en">{html.escape(en.rstrip())}</div>'
    if not comment:
        return en_html
    escaped = html.escape(comment.rstrip())
    with_em = EM_PATTERN.sub(r"<em>\1</em>", escaped)
    return f'<div class="en-cell">{en_html}<div class="comment">{with_em}</div></div>'


def render_row(seg_id: str, san: str, columns: list[tuple[str, str]]) -> str:
    """columns: list of (translation_text, comment_text) per creator."""
    cls = "row heading" if _is_heading(seg_id) else "row"
    esc_id = html.escape(seg_id, quote=True)
    cells = [
        f'<div class="seg-id"><a href="#{esc_id}">{html.escape(seg_id)}</a></div>',
        f'<div class="san">{html.escape(san.rstrip())}</div>',
    ]
    for en, comment in columns:
        cells.append(_en_cell(en, comment))
    return f'<div class="{cls}" id="{esc_id}">' + "".join(cells) + "</div>"


def render_book_paragraphs(translation: dict) -> str:
    """Group translation segments into paragraphs by the digit before the dot in
    the segment ID (which encodes the source's `||` paragraph boundary), and
    emit one <p> per paragraph. Segments ending in `.0` (e.g. `:1.0`, `:104.0`)
    are section headings and are emitted as <h2> before their paragraph body.
    Skips the 0.x title segments (the page-level title slots).
    """
    from itertools import groupby

    def para_key(seg_id: str) -> str:
        # "sbh2.0:3.1" → "3"
        return seg_id.split(":")[1].split(".")[0]

    def clause_idx(seg_id: str) -> str:
        # "sbh2.0:3.1" → "1"
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
                out.append(f'<h2 id="h-{html.escape(key, quote=True)}">{html.escape(heading_text)}</h2>')
        clauses = [translation[sid].strip() for sid in body_ids]
        text = " ".join(c for c in clauses if c)
        if not text:
            continue
        out.append(f'<p id="p-{html.escape(key, quote=True)}">{html.escape(text)}</p>')
    return "\n".join(out)


def build_topic(uid: str, creators: list[str]) -> tuple[str, str]:
    root_file = ROOT_DIR / f"{uid}_root-san-shukla.json"
    root = json.loads(root_file.read_text(encoding="utf-8"))

    available = []
    translations = []
    comments = []
    for c in creators:
        tp = trans_path(c, uid)
        if tp.exists():
            available.append(c)
            translations.append(json.loads(tp.read_text(encoding="utf-8")))
            cp = comment_path(c, uid)
            comments.append(json.loads(cp.read_text(encoding="utf-8")) if cp.exists() else {})

    title = uid
    for t in translations:
        if t.get(f"{uid}:0.2"):
            title = t[f"{uid}:0.2"].strip()
            break
    if title == uid and root.get(f"{uid}:0.2"):
        title = root[f"{uid}:0.2"].strip()

    rows = "\n".join(
        render_row(
            sid,
            root[sid],
            [(t.get(sid, ""), c.get(sid, "")) for t, c in zip(translations, comments)],
        )
        for sid in root.keys()
    )

    n_cols = 2 + len(translations)
    grid_cols = "4rem 1.4fr " + " ".join(["1fr"] * len(translations))
    column_labels = "\n  ".join(
        f'<div>{html.escape(label_for(c))}</div>' for c in available
    )

    intro_html = extract_intro(uid)

    page = PAGE_TEMPLATE.format(
        title=html.escape(title),
        subtitle=f"Śrāvakabhūmi · Sanskrit (Shukla 1973) ↔ English ({len(translations)} rendering{'s' if len(translations) != 1 else ''})",
        rows=rows,
        grid_cols=grid_cols,
        column_labels=column_labels,
        uid=html.escape(uid, quote=True),
        intro=intro_html,
    )

    out = DOCS_DIR / f"{uid}.html"
    out.write_text(page, encoding="utf-8")

    if translations:
        book_html = render_book_paragraphs(translations[0])
        book_page = PAGE_BOOK_TEMPLATE.format(
            title=html.escape(title),
            subtitle="Śrāvakabhūmi · English working translation",
            paragraphs=book_html,
            uid=html.escape(uid, quote=True),
            intro=intro_html,
        )
        (DOCS_DIR / f"{uid}-en.html").write_text(book_page, encoding="utf-8")

    return uid, title


def label_for(creator: str) -> str:
    """Display label for a creator_uid column header."""
    parts = creator.split("-")
    if len(parts) == 1:
        return "English"
    suffix = parts[-1]
    return f"English ({suffix})"


def build_index(topics: list[tuple[str, str]]) -> None:
    items = "\n".join(
        f'<li><a href="{uid}-en.html"><span class="uid">{uid}</span>{html.escape(title)}</a>'
        f'<a class="alt" href="{uid}.html">side-by-side</a></li>'
        for uid, title in topics
    )
    page = INDEX_TEMPLATE.format(items=items)
    (DOCS_DIR / "index.html").write_text(page, encoding="utf-8")


def main() -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    creators = discover_creators()
    if not creators:
        print("no translations found under translation/en/")
        sys.exit(1)

    if args == ["--all"]:
        def natural_key(uid: str) -> tuple:
            return tuple(int(p) if p.isdigit() else p for p in re.split(r"(\d+)", uid))
        uids = sorted(
            (p.stem.replace("_root-san-shukla", "") for p in ROOT_DIR.glob("*_root-san-shukla.json")),
            key=natural_key,
        )
    else:
        uids = args

    topics = []
    for uid in uids:
        topic = build_topic(uid, creators)
        topics.append(topic)
        print(f"built docs/{topic[0]}.html ({len(creators)} translation cols)")

    build_index(topics)
    print(f"built docs/index.html ({len(topics)} topics)")


if __name__ == "__main__":
    main()
