# Śrāvakabhūmi — Working Bilingual Edition

A working bilingual edition of the *Śrāvakabhūmi* — Sanskrit (Shukla 1973) alongside English, segment by segment.

**Rendered site:** [rforsyth.github.io/sravakabhumi-en](https://rforsyth.github.io/sravakabhumi-en/)

## Introduction

*Śrāvakabhūmi* means "The Stage of the Disciple" — from *śrāvaka*, literally "hearer," the term for those who heard the Buddha's teaching directly and trained for liberation as arhats, and *bhūmi*, "ground" or "stage." It is a section of the *Yogācārabhūmi-Śāstra*, the encyclopedic treatise on yogic practice traditionally ascribed to Asaṅga (4th century CE). Organized into four *yogasthāna*s ("yogic foundations"), it lays out a detailed program of contemplative training: the nine stages of mental abiding (*śamatha*), the method of insight (*vipaśyanā*), the five temperament-matched practices (unattractiveness, lovingkindness, dependent origination, elements, breath), and the seven attentions of the mundane path.

The Sanskrit original was long thought lost in India until 1938, when the Indian scholar Rāhula Sāṅkṛtyāyana located and photographed a palm-leaf manuscript at the Ri phug hermitage of Zhalu (Źa lu) monastery in Tibet. Shukla's edition rests on those photographs; the manuscript itself was reproduced in facsimile in 1994, and that facsimile underlies the later critical editions.

The full Sanskrit text is present, segmented at the clause level, with English translation and translator's notes inline.

## About

This is an **AI-assisted working translation**. The English was drafted with a large language model from Shukla's Sanskrit, cross-checked by a second model, and then reviewed section by section, also with AI assistance, against the Sanskrit, Xuanzang's Chinese translation (T1579), and, where available, the critical editions of Deleanu (2006) and the Taishō Śrāvakabhūmi Study Group. Ryan Forsyth, who does not read Sanskrit, directed the work, set the editorial policies, and is responsible for the result.

It is not a scholarly critical edition, and it is a personal publication not associated with any institution. No new collation of the manuscript was made; readings were checked against Deleanu (2006) and the Taishō Śrāvakabhūmi Study Group's edition where held, and the known-limitations statement below says which sections. Citations and downstream use are asked to keep the AI-assisted disclosure.

### Sources

- **Sanskrit text:** Karunesha Shukla, *Śrāvakabhūmi of Ācārya Asaṅga* (Patna: K.P. Jayaswal Research Institute, 1973; Tibetan Sanskrit Works Series 14), in the transcription hosted on [SuttaCentral](https://suttacentral.net/sbh/san/shukla).
- **Format:** [Bilara](https://github.com/suttacentral/bilara-data)-compatible segmented JSON for the source data; static HTML site rendered from it.
- **Segmentation:** Established for this edition; no segmentation hosted by SuttaCentral exists for this text. Segmentation rules approximate clause-level units, with paragraph clusters under topic UIDs (e.g. `sbh3.1:6.4`).

### Textual status

The Sanskrit layer in `root/` is based on Shukla 1973 as hosted by SuttaCentral, but it is **not a fully diplomatic transcription**. Obvious PDF/OCR extraction artifacts — chiefly intra-word whitespace breaks around ligature characters — have been normalized in the root JSONs; the policy is in [notes/sanskrit-emendation-policy.md](notes/sanskrit-emendation-policy.md). Where the English departs from Shukla's printed text it says so inline (`[Lacuna]`, `[Damaged]`, `[Conjectural: …]`, `[Restored: …]`) with a one-line note naming the witness; the markers are defined in [notes/editorial-conventions.md](notes/editorial-conventions.md) §2.

For close philological argument, cite the segment ID and verify the Sanskrit against Shukla directly and, where available, against the Tibetan and Chinese witnesses. For general reading and reference, this is intended as a working bilingual edition.

## Known limitations

**No Sanskritist has yet reviewed this translation, and its director does not read Sanskrit.** The statement under About says how the English was made; this section says how far each part of it has been checked, so that a reader can calibrate rather than guess. A reader who does know Sanskrit and is willing to check even a few segments is what this edition most needs; see Contributing.

### How each section was read

In the sections marked "in full" below, every segment's English was read against Shukla's Sanskrit and against Xuanzang's Chinese translation (T1579), and corrected wherever the two disagreed with it. Where a critical edition is in hand, the section was also collated against it: its apparatus was read for manuscript readings that differ from Shukla's print, and those readings are adopted and marked `[Restored: …]`. The translator's notes and the section introductions were read in full for every section.

| Section | Segments | Read against the Sanskrit and Xuanzang | Collated against a critical edition |
|---|---|---|---|
| sbh1.1, sbh1.2 | 195, 122 | in full | none in hand |
| sbh1.3 | 2,071 | in full | none in hand |
| sbh2.0 | 2,066 | in full | none in hand |
| sbh2.1–2.7 | 755 | in full | none in hand |
| sbh3.0, sbh3.1 | 214, 72 | in full | none in hand |
| sbh3.2 | 782 | in full | ŚBh-Gr III-(6), for 55.9–58.1 only |
| sbh4.1, sbh4.2 | 221, 228 | in full | Deleanu 2006, throughout |
| sbh4.3 | 561 | in full | Deleanu 2006 for ¶1–2; ŚBh-Gr IV(1)–IV(2) for 3.1–18.5; none exists for 18.6 to the end |

sbh1.3 and sbh2.0, 57% of the text, were read in full last, after a sampled stretch of each. About 8 segments per hundred in sbh1.3 and 10 per hundred in sbh2.0 needed a correction of sense (wrong or misleading, not style), close to what the samples had predicted; most often the English had rendered a corrupt printed word as if it were sound. All have been corrected.

### The Sanskrit text against Shukla's print

The Sanskrit shown here is SuttaCentral's transcription of Shukla's edition. It was collated against an OCR of Shukla's printed pages for the whole text, and every place where the two differed by more than a few letters was checked on the scan. At 25 places the transcription had dropped a printed phrase or sentence, spliced in text from elsewhere, or duplicated a line; each was brought back to the print, and the English translates the print. Shukla's own corrections and queried readings are left as he printed them.

### Critical editions: what exists, what is in hand

| Our files | Critical edition | In hand? |
|---|---|---|
| sbh1.1–1.3 (yogasthāna I) | ŚBh-Gr, *Śrāvakabhūmi* I, bound volume, 1998 | no |
| sbh2.0–2.7 (yogasthāna II) | ŚBh-Gr, *Śrāvakabhūmi* II, bound volume, 2006 | no |
| sbh3.0–3.2 (yogasthāna III) | ŚBh-Gr, *Śrāvakabhūmi* III, bound volume, 2018, superseding the serial installments III-(1)–(6) | no; of the installments, only III-(6) (TSN 35, 2013), covering sbh3.2:55.9–58.1 |
| sbh4.1, sbh4.2, sbh4.3:1–2 (the mundane path) | Deleanu 2006 | yes |
| sbh4.3:3.1–18.5 (Shukla pp. 470,7–482,2) | ŚBh-Gr IV(1), TSN 46, 2024; IV(2), TSN 47, 2025 | yes |
| sbh4.3:18.6 to the end (Shukla p. 482,2 onward) | none published | — |

ŚBh-Gr is the Śrāvakabhūmi Study Group, Taishō University; TSN is the *Annual of the Institute for Comprehensive Studies of Buddhism, Taishō University*, whose installments are open access at tais.repo.nii.ac.jp. Where no edition was in hand, a misreading in Shukla's print that leaves no trace in Xuanzang's Chinese remains undetected. The bound volumes are being sought, and the sections they cover will be collated when they arrive.

### Gaps in Shukla's text

Shukla's edition has gaps where the manuscript photographs were damaged or a passage was skipped. They are marked `[Lacuna]` in the English and nothing is supplied for them. The largest is at Shukla p. 432 line 4, inside sbh3.2:55.16: about ten pages are missing, from the resolve on the space-element, through the whole beginner's instruction in mindfulness of breathing (*ānāpānasmṛti*), to the opening of the section's summary. ŚBh-Gr III-(6) (2013, pp. (78)–(88)) supplies the passage from two manuscripts, and Xuanzang has it at T1579 juan 32 (463c27–464c06); it is not translated here. The other gaps are shorter: the opening of sbh1.1 (the manuscript begins mid-list), the end of sbh1.1 ¶26, a manuscript break at sbh1.3:52.2 (the close of the account of full awareness and the opening of the account of good friends, which Xuanzang preserves), the closing block of sbh4.3 (29.44–29.65, where the leaf is damaged), and a number of lost clauses and list items that Xuanzang preserves.

### What the markers mean

Every departure from Shukla's printed text is marked inline with one of four markers, `[Lacuna]`, `[Damaged]`, `[Conjectural: …]`, `[Restored: …]`, and carries a one-line note naming its witness; the markers are defined in [notes/editorial-conventions.md](notes/editorial-conventions.md) §2. In brief: `[Restored]` means a Sanskrit reading attested in a critical edition; `[Conjectural]` means a reading supplied from the context or from Xuanzang's Chinese alone, with no Sanskrit witness. At the time of writing about 350 segments carry a `[Conjectural]` reading, 90 a `[Restored]` one, 55 a `[Lacuna]`, and 22 a `[Damaged]`. The `[Conjectural]` readings, and among them the ones that add or remove a negative, are the first thing a reader of Sanskrit should check.


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

[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). The English translation, the translator's notes, the section introductions, the segmentation, the scripts and the rest of the apparatus made for this edition are dedicated to the public domain. The Sanskrit in `root/` is the text of Karunesha Shukla's edition (Patna: K.P. Jayaswal Research Institute, 1973), taken from the transcription hosted on [SuttaCentral](https://suttacentral.net/sbh/san/shukla), which treats the original texts of Buddhism as public domain. The CC0 dedication does not extend to the Sanskrit, and no license is claimed for it here.

### Citation

See [CITATION.cff](CITATION.cff). Suggested form:

> Forsyth, R. (2026). *Śrāvakabhūmi (working bilingual edition)*. Translated from the Shukla (1973) Sanskrit, AI-assisted. CC0.

When citing a specific segment, include the segment ID and link directly:

> ...as the text puts it ([sbh3.1:9.2](https://rforsyth.github.io/sravakabhumi-en/sbh3.1.html#sbh3.1:9.2)).

## Editorial policies

- **Sanskrit text:** The source file extracted from SuttaCentral contains intra-word whitespace artifacts from PDF→text extraction. These are silently rejoined in the root JSONs; the policy and audit trail live in [notes/sanskrit-emendation-policy.md](notes/sanskrit-emendation-policy.md).
- **Translator's notes:** Notes accompanying a translation appear inline below the relevant English cell in the rendered site. They are sparse by default and focused on Sanskrit-grounded observations (terminology, sandhi, syntax) rather than practice-instruction.
