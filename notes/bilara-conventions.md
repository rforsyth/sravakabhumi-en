# Bilara conventions

This repo follows the file-layout conventions of SuttaCentral's [`bilara-data`](https://github.com/suttacentral/bilara-data) — the segmented-JSON format used to source the SuttaCentral website. Shaped this way so the content can be rebased into `bilara-data/root/san/sastra/sbh/...` someday with minimal restructuring.

## What Bilara stores

For one work, several **cognate** files in parallel directory trees. Each file is a flat JSON object keyed by segment ID:

```json
{ "<segment-id>": "<string>", ... }
```

The segment ID is the join key across categories. Filenames are convenience; the segment IDs are the contract — they must remain stable once published.

Categories used here:

- `root/` — the Sanskrit source (Shukla 1973)
- `translation/` — English rendering
- `comment/` — translator's notes, sparse (only commented segments present)

Categories defined by Bilara but not used here: `html/`, `variant/`, `reference/`.

## Path shape

```
<category>/<lang>/<edition-or-translator>/<basket>/<collection>/<file>.json
```

Concrete: `root/san/sastra/sbh/sbh1.1_root-san-shukla.json` and its translation cognate at `translation/en/ryanforsyth/sastra/sbh/sbh1.1_translation-en-ryanforsyth.json`.

`sastra` (treatise) is a new basket not currently used in `bilara-data` — SuttaCentral has `sutta`, `vinaya`, `abhidhamma` only. The Yogācārabhūmi is a śāstra, so a fourth basket is appropriate; on migration SC would either accept the new basket or rename.

## Segment IDs

Format: `<work-uid>:<paragraph>.<clause>`. Examples: `sbh1.1:1.1`, `sbh3.1:9.2`.

- The `<paragraph>` number tracks the source's `||` boundaries.
- The `<clause>` number tracks the source's `|` boundaries within a paragraph.
- `<clause>` of `0` (e.g. `sbh1.1:1.0`) marks a section heading inside the body. `<paragraph>` of `0` (e.g. `sbh1.1:0.1`, `sbh1.1:0.2`) holds the page-level title slots. The `_is_heading()` function in `scripts/build_viewer.py` encodes both conventions.

## Edition and translator UIDs

- Edition UID `shukla` (the 1973 Sanskrit edition) appears in root filenames as `_root-san-shukla.json`. Being explicit about edition is more useful than SC's elision in single-edition collections.
- Translator UID `ryanforsyth`. Matches the github-handle-style convention SC uses.

## Authoritative references

- **Bilara data repo**: <https://github.com/suttacentral/bilara-data> — the canonical convention; this repo mirrors its layout.
- **Bilara editor**: <https://github.com/suttacentral/bilara> — the editing tool, useful for understanding what conventions exist.
- **SuttaCentral**: <https://suttacentral.net/> — the rendered site Bilara feeds into.
- **Community**: <https://discourse.suttacentral.net/> — for questions about migrating content upstream.
