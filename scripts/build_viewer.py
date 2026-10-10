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
import shutil
from datetime import datetime
from pathlib import Path

_CODE_SPAN = re.compile(r"`([^`\n]+)`")
_STRONG_PATTERN = re.compile(r"\*\*([^*\n]+?)\*\*")
_EM_PATTERN = re.compile(r"\*([^*\n]+?)\*")
_CODE_PLACEHOLDER = re.compile(r"\x00CODE(\d+)\x00")


def inline_markup(text: str) -> str:
    """HTML-escape text and apply lightweight Markdown emphasis.

    Supports `code`, **strong**, *em* spans. Code spans are protected before
    escaping/emphasis so their contents are not interpreted. **strong** is
    matched before *em* so paired double-asterisks render as <strong>, not as
    nested broken <em>. Newlines terminate any span — this is intentional, to
    avoid runaway matches across paragraph boundaries."""
    stashed_code: list[str] = []

    def _stash(m: re.Match) -> str:
        stashed_code.append(m.group(1))
        return f"\x00CODE{len(stashed_code) - 1}\x00"

    with_placeholders = _CODE_SPAN.sub(_stash, text)
    escaped = html.escape(with_placeholders)
    with_strong = _STRONG_PATTERN.sub(r"<strong>\1</strong>", escaped)
    with_em = _EM_PATTERN.sub(r"<em>\1</em>", with_strong)

    def _unstash(m: re.Match) -> str:
        return f"<code>{html.escape(stashed_code[int(m.group(1))])}</code>"

    return _CODE_PLACEHOLDER.sub(_unstash, with_em)

REPO = Path(__file__).resolve().parent.parent
ROOT_DIR = REPO / "root" / "san" / "sastra" / "sbh"
TRANS_BASE = REPO / "translation" / "en"
COMMENT_BASE = REPO / "comment" / "en"
TRANS_NOTES_DIR = REPO / "notes" / "translation-notes"
SCRIPTS_DIR = REPO / "scripts"
DOCS_DIR = REPO / "docs"

# Canonical base URL of the published GitHub Pages site (no trailing slash).
SITE_BASE = "https://rforsyth.github.io/sravakabhumi-en"

SITE_DESCRIPTION = (
    "A working bilingual edition of the Śrāvakabhūmi (\"The Stage of the "
    "Disciple\") from the Yogācārabhūmi, in Sanskrit (Shukla 1973) and English."
)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_tags}
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
  footer.ai-note {{
    max-width: 720px;
    margin: 2.5rem auto 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e6e1d8;
    font-size: 0.85rem;
    color: #888;
    text-align: center;
  }}
  footer.ai-note a {{ color: #5a4a2a; }}
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
<footer class="ai-note">AI-assisted working translation, not yet reviewed by a Sanskritist. <a href="index.html#about">How it was made →</a></footer>
</body>
</html>
"""

PAGE_BOOK_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_tags}
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
  p:target, ul:target {{
    background: #f4ecd8;
    border-left: 3px solid #c9a96e;
    padding-left: 0.75rem;
    margin-left: -0.75rem;
  }}
  p.uddana {{
    text-align: left;
    color: #4a4a4a;
    margin: 1.5rem 0 1.1rem;
  }}
  ul.seg-list {{
    margin: 0 0 1.1rem;
    padding-left: 1.5rem;
  }}
  ul.seg-list li {{
    margin-bottom: 0.25rem;
  }}
  p.def-question {{
    text-align: left;
    color: #4a4a4a;
    margin-top: 1.3rem;
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
  footer.ai-note {{
    max-width: 720px;
    margin: 2.5rem auto 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e6e1d8;
    font-size: 0.85rem;
    color: #888;
    text-align: center;
  }}
  footer.ai-note a {{ color: #5a4a2a; }}
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
<footer class="ai-note">AI-assisted working translation, not yet reviewed by a Sanskritist. <a href="index.html#about">How it was made →</a></footer>
</body>
</html>
"""


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_tags}
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
  ul.topics li.yoggroup {{
    display: block;
    padding: 1.1rem 0 0.35rem;
    border-bottom: none;
    color: #8a7a4a;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }}
  ul.topics li.yoggroup:first-child {{ padding-top: 0.6rem; }}
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
<div class="tagline">A working bilingual edition of the Śrāvakabhūmi, in Sanskrit (Shukla 1973) and English.</div>

<h2>Introduction</h2>
<p><em>Śrāvakabhūmi</em> means "The Stage of the Disciple" — from <em>śrāvaka</em>, literally "hearer," the term for those who heard the Buddha's teaching directly and trained for liberation as arhats, and <em>bhūmi</em>, "ground" or "stage." It is a section of the <em>Yogācārabhūmi-Śāstra</em>, the encyclopedic treatise on yogic practice traditionally ascribed to Asaṅga (4th century CE). Organized into four <em>yogasthānas</em> ("yogic foundations"), it lays out a detailed program of contemplative training: the nine stages of mental abiding (<em>śamatha</em>), the method of insight (<em>vipaśyanā</em>), the five temperament-matched practices (unattractiveness, lovingkindness, dependent origination, elements, breath), and the seven attentions of the mundane path.</p>
<p>The Sanskrit original was long thought lost in India until 1938, when the Indian scholar Rāhula Sāṅkṛtyāyana located and photographed a palm-leaf manuscript at the Ri phug hermitage of Zhalu (Źa lu) monastery in Tibet. Shukla's edition rests on those photographs; the manuscript itself was reproduced in facsimile in 1994, and that facsimile underlies the later critical editions.</p>

<h2>Contents</h2>
<ul class="topics">
{items}
</ul>

<div class="disclosure" id="about">
<strong>This is an AI-assisted working translation.</strong>
The English was drafted with a large language model from Shukla's Sanskrit, cross-checked by a second model, and then reviewed section by section, also with AI assistance, against the Sanskrit, Xuanzang's Chinese translation (T1579), and, where available, the critical editions of Deleanu (2006) and the Taishō Śrāvakabhūmi Study Group. Ryan Forsyth, who does not read Sanskrit, directed the work, set the editorial policies, and is responsible for the result. It is not a scholarly critical edition. Reports of errors or improvements welcome (see Contributing below).
</div>

<h2>Edition details</h2>
<dl class="meta">
<dt>Sanskrit source</dt><dd>Karunesha Shukla, <em>Śrāvakabhūmi of Ācārya Asaṅga</em> (Patna: K.P. Jayaswal Research Institute, 1973; Tibetan Sanskrit Works Series 14), in the transcription hosted on <a class="link" href="https://suttacentral.net/sbh/san/shukla">SuttaCentral</a>.</dd>
<dt>Translator</dt><dd>Ryan Forsyth (see the note above).</dd>
<dt>Format</dt><dd>Bilara-compatible segmented JSON (sources) rendered as side-by-side HTML.</dd>
<dt>License</dt><dd><a class="link" href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0 Universal</a> for the English and apparatus. The Sanskrit is Shukla's 1973 edition, in SuttaCentral's transcription; the dedication does not cover it, and no license is claimed for it here.</dd>
</dl>

<h2>Textual status</h2>
<p>The Sanskrit layer is based on Shukla 1973 (via SuttaCentral) but is not a fully diplomatic transcription. Obvious PDF/OCR extraction artifacts — chiefly intra-word whitespace breaks — have been normalized; the policy is in the <a class="link" href="https://github.com/rforsyth/sravakabhumi-en/blob/main/notes/sanskrit-emendation-policy.md">emendation policy</a>. Where the English departs from Shukla's printed text it says so inline (<code>[Lacuna]</code>, <code>[Damaged]</code>, <code>[Conjectural: …]</code>, <code>[Restored: …]</code>) with a one-line note naming the witness; the markers are defined in the <a class="link" href="https://github.com/rforsyth/sravakabhumi-en/blob/main/notes/editorial-conventions.md">editorial conventions</a>. For close philological argument, cite the segment ID and check the Sanskrit against Shukla and, where available, against the Tibetan and Chinese witnesses.</p>

<h2 id="limitations">Known limitations</h2>
<p>No Sanskritist has yet reviewed this translation, and its director does not read Sanskrit. Every section except two has been read in full, segment by segment, against Shukla's Sanskrit and Xuanzang's Chinese; sbh4.1 and sbh4.2, and parts of sbh3.2 and sbh4.3, were also collated against the critical editions of Deleanu (2006) and the Taishō Śrāvakabhūmi Study Group, which are the only ones in hand. The two longest sections, sbh1.3 and sbh2.0, have so far been read in full only in one sampled stretch each. Shukla's text also has gaps, the largest about ten pages inside sbh3.2:55.16, which are marked and not filled. The section-by-section account, the critical-edition coverage, the sample results, and the gaps are set out under <a class="link" href="https://github.com/rforsyth/sravakabhumi-en#known-limitations">Known limitations</a> in the README.</p>

<h2>Contributing</h2>
<p>Errors, alternative readings, and improvements are welcome via GitHub issues or pull requests on the source repository.</p>

<footer>
Cite as: Forsyth, R. (2026). <em>Śrāvakabhūmi (working bilingual edition)</em>. Translated from the Shukla (1973) Sanskrit, AI-assisted. CC0.
</footer>

</div>
</body>
</html>
"""


_SBH_HTML_HREF = re.compile(r'^(sbh[0-9.]+)\.html(#.*)?$')


def _rewrite_href_for_en(href: str) -> str:
    """For the English-only book view, rewrite `sbhX.html[#anchor]` link targets
    to `sbhX-en.html[#anchor]` so readers stay in the en view when navigating
    between chapters. External and anchor-only hrefs are left untouched."""
    m = _SBH_HTML_HREF.match(href)
    if not m:
        return href
    return f"{m.group(1)}-en.html{m.group(2) or ''}"


def first_note_paragraph(uid: str) -> str:
    """Return the first paragraph after the H1 in notes/translation-notes/<uid>.md
    as raw Markdown text (the website-intro paragraph, by convention), or empty
    string if the notes file is absent or has no such paragraph."""
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
    return " ".join(intro_lines)


def extract_intro(uid: str, en_only: bool = False) -> str:
    """Render the first note paragraph (see first_note_paragraph) as an HTML
    intro block. Subsequent paragraphs and sections stay file-only.

    *italic* spans are converted to <em>; backtick `code` spans to <code>.
    When `en_only=True`, `sbhX.html` link targets are rewritten to `sbhX-en.html`
    so cross-chapter navigation stays in the English-only view.
    Returns empty string if there is no intro paragraph."""
    text = first_note_paragraph(uid)
    if not text:
        return ""

    # Extract markdown links first so their label/href don't get inline-markup'd
    # in conflicting ways. Stash each as a placeholder, then re-insert after
    # inline_markup has escaped & emphasized the surrounding prose.
    stashed_links: list[tuple[str, str]] = []

    def _stash_link(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        if en_only:
            href = _rewrite_href_for_en(href)
        stashed_links.append((label, href))
        return f"\x00LINK{len(stashed_links) - 1}\x00"

    text_with_link_holes = re.sub(r"\[([^\]\n]+)\]\(([^)\n]+)\)", _stash_link, text)
    rendered = inline_markup(text_with_link_holes)

    def _unstash_link(m: re.Match) -> str:
        label, href = stashed_links[int(m.group(1))]
        return f'<a href="{html.escape(href, quote=True)}">{inline_markup(label)}</a>'

    with_links = re.sub(r"\x00LINK(\d+)\x00", _unstash_link, rendered)
    return f'<div class="intro"><p>{with_links}</p></div>'


_MD_LINK = re.compile(r"\[([^\]\n]+)\]\([^)\n]+\)")


def _plain_text(md: str) -> str:
    """Reduce inline Markdown to plain text for use in a meta description:
    links -> their label, drop `code`/*emphasis* markers, collapse whitespace."""
    text = _MD_LINK.sub(r"\1", md)
    text = text.replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", text).strip()


def _truncate(text: str, limit: int = 155) -> str:
    """Trim to <=limit chars on a word boundary, appending an ellipsis."""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"


def extract_description(uid: str, title: str, en_only: bool) -> str:
    """Plain-text meta description for a topic page: the intro note's first
    paragraph when present, else a title-based fallback."""
    raw = first_note_paragraph(uid)
    if raw:
        return _truncate("AI-assisted translation. " + _plain_text(raw))
    view = "English working translation" if en_only else "Sanskrit (Shukla 1973) with English"
    return f"{title} — {view}, AI-assisted, from the Śrāvakabhūmi."


def head_tags(description: str, canonical_path: str) -> str:
    """Meta description + canonical link for a page's <head>. canonical_path is
    the page filename relative to the site root ('' for the homepage)."""
    desc = html.escape(description, quote=True)
    url = html.escape(f"{SITE_BASE}/{canonical_path}", quote=True)
    return (
        f'<meta name="description" content="{desc}">\n'
        f'<link rel="canonical" href="{url}">'
    )


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


def structure_path(creator: str, uid: str) -> Path:
    return TRANS_BASE / creator / "sastra" / "sbh" / f"{uid}_structure-en-{creator}.json"


def _is_heading(seg_id: str) -> bool:
    last = seg_id.split(":")[-1]
    return seg_id.endswith(":0.1") or seg_id.endswith(":0.2") or last.endswith(".0")


def _en_cell(en: str, comment: str) -> str:
    en_html = f'<div class="en">{inline_markup(en.rstrip())}</div>'
    if not comment:
        return en_html
    return f'<div class="en-cell">{en_html}<div class="comment">{inline_markup(comment.rstrip())}</div></div>'


def render_row(seg_id: str, san: str, columns: list[tuple[str, str]]) -> str:
    """columns: list of (translation_text, comment_text) per creator."""
    cls = "row heading" if _is_heading(seg_id) else "row"
    esc_id = html.escape(seg_id, quote=True)
    cells = [
        f'<div class="seg-id"><a href="#{esc_id}">{html.escape(seg_id)}</a></div>',
        f'<div class="san">{inline_markup(san.rstrip())}</div>',
    ]
    for en, comment in columns:
        cells.append(_en_cell(en, comment))
    return f'<div class="{cls}" id="{esc_id}">' + "".join(cells) + "</div>"


DEF_QUESTION_MAX_LEN = 200


def is_def_question(text: str) -> bool:
    """Short interrogative segment — the source's `katama-` definition-question
    opening. Each gets its own paragraph so Q&A pairs read distinctly."""
    t = text.strip()
    return t.endswith("?") and 0 < len(t) <= DEF_QUESTION_MAX_LEN


def render_book_paragraphs(translation: dict, structure: dict) -> str:
    """Group translation segments into paragraphs by the digit before the dot in
    the segment ID (which encodes the source's `||` paragraph boundary), and
    emit appropriate HTML blocks. Segments ending in `.0` (e.g. `:1.0`,
    `:104.0`) are section headings and are emitted as <h2>. Skips the 0.x title
    segments (the page-level title slots).

    `structure` maps segment-id -> role. Within each paragraph, consecutive
    segments are grouped by role and rendered per-role:
      - "uddana"          : italicised topic-line/list, joined into one <p><em>…</em></p>
      - "list", "question": <ul><li>…</li></ul>
      - (unset)           : default flowing prose joined into one <p>…</p>
    """
    from itertools import groupby

    def para_key(seg_id: str) -> str:
        return seg_id.split(":")[1].split(".")[0]

    def clause_idx(seg_id: str) -> str:
        return seg_id.split(":")[1].split(".")[1]

    def render_run(role: str, texts: list[str], key: str, run_idx: int) -> str:
        pid = html.escape(f"p-{key}-{run_idx}", quote=True)
        if role == "uddana":
            joined = inline_markup(" ".join(texts).rstrip(". "))
            return f'<p id="{pid}" class="uddana"><em>{joined}</em></p>'
        if role in ("list", "question"):
            items = "".join(f"<li>{inline_markup(t)}</li>" for t in texts)
            return f'<ul id="{pid}" class="seg-list">{items}</ul>'
        if role == "def-question":
            joined = inline_markup(" ".join(texts))
            return f'<p id="{pid}" class="def-question">{joined}</p>'
        joined = inline_markup(" ".join(texts))
        return f'<p id="{pid}">{joined}</p>'

    SPANNING_ROLES = {"list", "question", "uddana"}

    def ends_terminally(text: str) -> bool:
        s = text.rstrip()
        while len(s) > 1 and s[-1] in ")]\"'’”|":
            s = s[:-1].rstrip()
        return bool(s) and s[-1] in ".!?"

    out: list[str] = []
    run_role: str | None = None
    run_texts: list[str] = []
    run_start_key: str = ""
    key_run_counts: dict[str, int] = {}

    def flush():
        nonlocal run_role, run_texts
        if run_texts:
            idx = key_run_counts.get(run_start_key, 0)
            key_run_counts[run_start_key] = idx + 1
            out.append(render_run(run_role or "", run_texts, run_start_key, idx))
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
                out.append(f'<h2 id="h-{html.escape(key, quote=True)}">{inline_markup(heading_text)}</h2>')

        for sid in body_ids:
            text = translation[sid].strip()
            if not text:
                continue
            role = structure.get(sid, "")
            if not role and is_def_question(text) and (
                not run_texts or ends_terminally(run_texts[-1])
            ):
                role = "def-question"
            if run_texts and role != run_role:
                flush()
            if not run_texts:
                run_start_key = key
            run_role = role
            run_texts.append(text)
            if role == "def-question" and text.rstrip().endswith("?"):
                flush()

        if run_role not in SPANNING_ROLES and (
            not run_texts or ends_terminally(run_texts[-1])
        ):
            flush()

    flush()
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
        subtitle="Śrāvakabhūmi · Sanskrit (Shukla 1973) ↔ AI-assisted English",
        rows=rows,
        grid_cols=grid_cols,
        column_labels=column_labels,
        uid=html.escape(uid, quote=True),
        intro=intro_html,
        head_tags=head_tags(extract_description(uid, title, en_only=False), f"{uid}.html"),
    )

    out = DOCS_DIR / f"{uid}.html"
    out.write_text(page, encoding="utf-8")

    if translations:
        sp = structure_path(available[0], uid)
        structure = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
        book_html = render_book_paragraphs(translations[0], structure)
        book_page = PAGE_BOOK_TEMPLATE.format(
            title=html.escape(title),
            subtitle="Śrāvakabhūmi · AI-assisted English working translation",
            paragraphs=book_html,
            uid=html.escape(uid, quote=True),
            intro=extract_intro(uid, en_only=True),
            head_tags=head_tags(extract_description(uid, title, en_only=True), f"{uid}-en.html"),
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


YOG_GROUP_HEADERS = {
    "1": "Yogasthāna I — Gotrabhūmi, Avatārabhūmi, Naiṣkramyabhūmi",
    "2": "Yogasthāna II — Framework and the Seven Object-Supports",
    "3": "Yogasthāna III — Approaching the Teacher, Śamatha, Vipaśyanā",
    "4": "Yogasthāna IV — Seven Attentions, Samāpattis, Lokottara Path",
}


def _yog_of(uid: str) -> str:
    # uid looks like "sbh3.2"; return the major number as a string ("3").
    m = re.match(r"sbh(\d+)", uid)
    return m.group(1) if m else ""


def build_index(topics: list[tuple[str, str]]) -> None:
    rows: list[str] = []
    current_yog = ""
    for uid, title in topics:
        yog = _yog_of(uid)
        if yog and yog != current_yog:
            header = YOG_GROUP_HEADERS.get(yog)
            if header:
                rows.append(f'<li class="yoggroup">{html.escape(header)}</li>')
            current_yog = yog
        rows.append(
            f'<li><a href="{uid}-en.html"><span class="uid">{uid}</span>{html.escape(title)}</a>'
            f'<a class="alt" href="{uid}.html">side-by-side</a></li>'
        )
    items = "\n".join(rows)
    page = INDEX_TEMPLATE.format(items=items, head_tags=head_tags(SITE_DESCRIPTION, ""))
    (DOCS_DIR / "index.html").write_text(page, encoding="utf-8")


def _lastmod(path: Path) -> str:
    """File modification date as YYYY-MM-DD for the sitemap <lastmod>."""
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def build_sitemap(topics: list[tuple[str, str]]) -> None:
    """Write docs/sitemap.xml listing the homepage and every topic page.

    The English-only book views are the primary readable pages (priority 0.8);
    the side-by-side source views are secondary (0.5). The homepage is listed
    with its trailing-slash directory URL as the canonical entry point."""
    urls: list[tuple[str, str, str]] = []  # (loc, lastmod, priority)

    index_file = DOCS_DIR / "index.html"
    if index_file.exists():
        urls.append((f"{SITE_BASE}/", _lastmod(index_file), "1.0"))

    for uid, _title in topics:
        for suffix, priority in ((f"{uid}-en.html", "0.8"), (f"{uid}.html", "0.5")):
            page = DOCS_DIR / suffix
            if page.exists():
                urls.append((f"{SITE_BASE}/{suffix}", _lastmod(page), priority))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, priority in urls:
        lines.append(
            f"  <url><loc>{html.escape(loc, quote=True)}</loc>"
            f"<lastmod>{lastmod}</lastmod>"
            f"<priority>{priority}</priority></url>"
        )
    lines.append("</urlset>")
    (DOCS_DIR / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"built docs/sitemap.xml ({len(urls)} urls)")


def build_robots() -> None:
    """Write docs/robots.txt allowing all crawlers and pointing to the sitemap."""
    text = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_BASE}/sitemap.xml\n"
    )
    (DOCS_DIR / "robots.txt").write_text(text, encoding="utf-8")
    print("built docs/robots.txt")


def copy_verification_files() -> None:
    """Copy search-engine ownership-verification files staged in scripts/ into
    docs/ so they are served at the site root: Google Search Console
    (google*.html) and Bing Webmaster Tools (BingSiteAuth.xml). Kept under
    scripts/ in source and copied on build so a clean docs rebuild never drops
    them."""
    sources = list(SCRIPTS_DIR.glob("google*.html"))
    bing = SCRIPTS_DIR / "BingSiteAuth.xml"
    if bing.exists():
        sources.append(bing)
    for src in sources:
        shutil.copy2(src, DOCS_DIR / src.name)
        print(f"copied {src.name} -> docs/")


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

    build_all = args == ["--all"]
    if build_all:
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

    copy_verification_files()

    if build_all:
        build_index(topics)
        print(f"built docs/index.html ({len(topics)} topics)")
        build_sitemap(topics)
        build_robots()
    else:
        print("skipped docs/index.html, sitemap.xml (rebuild with --all to refresh)")


if __name__ == "__main__":
    main()
