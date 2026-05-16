# Śrāvakabhūmi — Working Bilingual Edition

A working bilingual edition of Asaṅga's *Śrāvakabhūmi* (4th century CE) — Sanskrit (Shukla 1973) alongside English, segment-by-segment.  First complete English translation.

**Rendered site:** [rforsyth.github.io/sravakabhumi-en](https://rforsyth.github.io/sravakabhumi-en/)

## Introduction

*Śrāvakabhūmi* means "The Stage of the Disciple" — from *śrāvaka*, literally "hearer," the term for those who heard the Buddha's teaching directly and trained for liberation as arhats, and *bhūmi*, "ground" or "stage." It is a section of the *Yogācārabhūmi-Śāstra*, the encyclopedic treatise on yogic practice traditionally ascribed to Asaṅga (4th century CE). Organized into four *yogasthāna*s ("yogic foundations"), it lays out a detailed program of contemplative training: the nine stages of mental abiding (*śamatha*), the method of insight (*vipaśyanā*), the five temperament-matched practices (unattractiveness, lovingkindness, dependent origination, elements, breath), and the seven attentions of the mundane path.

The Sanskrit original was long thought lost in India until 1938, when the explorer-scholar Rāhula Sāṅkṛtyāyana located and photographed a palm-leaf manuscript at Shalu Monastery in Tibet; those photographs are the basis for every modern Sanskrit edition, including the source text used here.

The full Sanskrit text is present, segmented at the clause level, with English translation and translator's notes inline.

## About

This is an **AI-assisted working translation**, prepared from the Sanskrit with reference to standard Buddhist Sanskrit dictionaries and the established technical terminology found in the secondary literature. It is not a scholarly critical edition — no manuscript collation, no apparatus criticus — and is a personal publication not associated with any institution. Citations and downstream use should preserve the AI-assisted disclosure.

### Sources

- **Sanskrit text:** Karunesha Shukla edition (1973), as hosted on [SuttaCentral](https://suttacentral.net/sbh/san/shukla).
- **Format:** [Bilara](https://github.com/suttacentral/bilara-data)-compatible segmented JSON for the source data; static HTML site rendered from it.
- **Segmentation:** Established for this edition; no segmentation hosted by SuttaCentral exists for this text. Segmentation rules approximate clause-level units, with paragraph clusters under topic UIDs (e.g. `sbh3.1:6.4`).

### Textual status

The Sanskrit layer in `root/` is based on Shukla 1973 as hosted by SuttaCentral, but it is **not a fully diplomatic transcription**. Obvious PDF/OCR extraction artifacts — chiefly intra-word whitespace breaks around ligature characters — have been normalized in the root JSONs. A small number of clearly documented restorations and supplements are recorded in [notes/sanskrit-emendation-policy.md](notes/sanskrit-emendation-policy.md). The English translation marks damaged or conjecturally reconstructed passages inline (e.g. `[Damaged]`, `[Damaged/Conjectural: …]`, bracketed supplied words).

For close philological argument, cite the segment ID and verify the Sanskrit against Shukla directly and, where available, against the Tibetan and Chinese witnesses. For general reading and reference, this is intended as a working bilingual edition.

## Format

```
sravakabhumi-en/
├── root/san/sastra/sbh/                  # Sanskrit segments (Bilara format)
├── translation/en/ryanforsyth/sastra/sbh/  # English segments
├── comment/en/ryanforsyth/sastra/sbh/      # Translator's notes (per-segment, optional)
├── docs/                                 # Generated static site (GitHub Pages)
└── scripts/build_viewer.py               # Build script (Python 3, no deps)
```

To rebuild the site locally:

```sh
python3 scripts/build_viewer.py --all
```

This regenerates `docs/index.html` and one `docs/<uid>.html` per topic. Output is self-contained — no JS, no external CSS, no build dependencies.

## Contributing

Errors, alternative readings, terminology suggestions, and segmentation refinements are welcome via GitHub issues or pull requests. Please include the segment ID in question and a short rationale.

## License

[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) — dedicated to the public domain. The Sanskrit text is itself in the public domain (the Shukla edition reconstruction is decades old and hosted CC0 on SuttaCentral); the English renderings and apparatus are released CC0 to match.

### Citation

See [CITATION.cff](CITATION.cff). Suggested form:

> Forsyth, R. (2026). *Śrāvakabhūmi (working bilingual edition)*. Translated from the Shukla (1973) Sanskrit, AI-assisted. CC0.

When citing a specific segment, include the segment ID and link directly:

> ...as Asaṅga puts it ([sbh3.1:9.2](https://rforsyth.github.io/sravakabhumi-en/sbh3.1.html#sbh3.1:9.2)).

## Editorial policies

- **Sanskrit text:** The source file extracted from SuttaCentral contains intra-word whitespace artifacts from PDF→text extraction. These are silently rejoined in the root JSONs; the policy and audit trail live in [notes/sanskrit-emendation-policy.md](notes/sanskrit-emendation-policy.md).
- **Translator's notes:** Notes accompanying a translation appear inline below the relevant English cell in the rendered site. They are sparse by default and focused on Sanskrit-grounded observations (terminology, sandhi, syntax) rather than practice-instruction.
