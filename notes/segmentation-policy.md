---
title: Segmentation policy
status: working note
created: 2026-05-18
---

# Segmentation policy

## Decision

The Śrāvakabhūmi is segmented into JSON files following Bilara conventions ([bilara-conventions.md](bilara-conventions.md)), with one file per topical chunk of body content. Framing material — yogasthāna headers, intermediate uddānas, closing colophons — attaches to whichever file sits next to it in linear source order. This produces an asymmetric file layout that mirrors the asymmetric structure of the source itself.

This document records the structural decisions, in parallel with [sanskrit-emendation-policy.md](sanskrit-emendation-policy.md) which records textual decisions.

## Yogasthāna-level architecture

The source attests four yogasthānas, each closed by an explicit colophon (`prathamaṁ/dvitīyaṁ/tṛtīyaṁ/caturthaṁ yogasthānam`). Within each yogasthāna, body content is divided into sub-topics that become individual files. The breakdown is:

| Yog | Files | Content |
|---|---|---|
| I | sbh1.1, sbh1.2, sbh1.3 | gotrabhūmi, avatārabhūmi, naiṣkramyabhūmi |
| II | sbh2.0, sbh2.1–sbh2.7 | framework topics + the seven ālambana chapters (vyāpī, aśubhā, maitrī, idaṁ-pratyayatā-pratītyasamutpāda, dhātu-prabheda, ānāpāna-smṛti, kauśalya) |
| III | sbh3.0, sbh3.1, sbh3.2 | preamble (approaching the teacher), śamatha (nine stages), vipaśyanā |
| IV | sbh4.1, sbh4.2, sbh4.3 | seven attentions, dhyāna/ārūpya samāpatti / abhijñā, rebirth + lokottara path + arhatship |

The result is asymmetric: only Yog II and Yog III have `.0` (preamble) files, because only those two yogasthānas carry substantive preamble material in the source. Yog I begins directly with `I. gotrabhūmiḥ`; Yog IV begins directly with `IV. caturthaṁ yogasthānam` followed by the seven-attentions content with no preamble.

## File-segmentation rule

Each `sbhN.M` file holds **one topical chunk** of body content. The chunk is determined by the source's own topical structure (the `tatra X katamaḥ?` definition blocks and their associated material). The current layout is:

- `sbh1.1` (gotrabhūmi): the stage of lineage as a unified topic.
- `sbh1.2` (avatārabhūmi): the stage of descent as a unified topic.
- `sbh1.3` (naiṣkramyabhūmi): the twelve requisites for going-forth.
- `sbh2.0`: the seventeen-question framework + framework topics that surround the ālambana chapters.
- `sbh2.1`: vyāpī-ālambana.
- `sbh2.2`–`sbh2.6`: the five carita-viśodhana practices, one per file.
- `sbh2.7`: kauśalya-ālambana.
- `sbh3.0`: preamble (approaching the teacher).
- `sbh3.1`: the nine stages of mental abiding + the śamatha framework.
- `sbh3.2`: vipaśyanā framework + per-ālambana vipaśyanā treatments.
- `sbh4.1`: the seven attentions.
- `sbh4.2`: dhyāna and ārūpya samāpattis + supernatural powers.
- `sbh4.3`: rebirth, the lokottara path, arhatship.

## Framing-marker placement

Framing markers (yogasthāna headers, intermediate uddānas, closing colophons) attach to whichever file sits next to them in linear source order — not to a hypothetical "frame file." The actual placements are:

| Marker | File | Position |
|---|---|---|
| Yog I closing colophon | sbh1.3 | tail |
| Yog II opening header | sbh2.0 | `:1.0` |
| Yog II closing colophon | sbh2.0 | tail |
| Yog III opening header | sbh3.0 | `:1.0` |
| Yog III piṇḍoddāna verses | sbh3.2 | tail (after vipaśyanā treatments) |
| Yog III closing colophon | sbh3.2 | tail (after the uddāna) |
| Yog IV opening header | sbh4.1 | `:1.0` |
| Yog IV uddāna verses | sbh4.3 | tail |
| Yog IV closing colophon | sbh4.3 | tail (after the uddāna) |
| Final śrāvakabhūmi colophon | sbh4.3 | tail (after the Yog IV closing) |

Note how the closing colophon for a yogasthāna does *not* go in the `.0` preamble file — it goes at the end of the last body-content file of the yogasthāna, because that is where it sits linearly in the source. The closing colophon for Yog II is at the end of sbh2.0 not because sbh2.0 is special but because sbh2.0's tail happens to contain the last body topic answered (`kathamārambho viphalo bhavati`) before the colophon.

## Why `.0` files exist for Yog II and Yog III but not Yog I or Yog IV

The source's asymmetry. Yog II opens with a long preamble (the seventeen-question framework, person-typology, ālambana setup) before reaching the carita-viśodhana chapters; this preamble takes a dedicated `.0` file. Yog III opens with a long preamble (approaching the teacher, daily routine, kāya-viveka, citta-viveka) before reaching the nine-stage śamatha; this preamble takes a dedicated `.0` file. Yog I and Yog IV have no such preamble: in the source, Yog I begins directly with `I. gotrabhūmiḥ` and Yog IV begins directly with `IV. caturthaṁ yogasthānam` continued by `tatra labdhamanaskārasya yoginaḥ…`, so a `.0` file would have no content.

## Segment-ID stability

Once published, segment IDs (`<work-uid>:<paragraph>.<clause>`) must remain stable to support cross-file references. When the segmentation rework needed to renumber paragraphs (because of merged-paragraph splits or content restoration), all cognate files were updated in sync, and all known internal and external references were chased. Notes:

- The sbh3.0 extraction and the corrections that followed (both 2026-05-18) involve substantial paragraph renumbering. These were applied **before** the corpus stabilized; future renumberings should be avoided.
- Cross-references should preferably name `paragraph:clause` rather than `paragraph` alone, so future merges or splits within a paragraph won't break them.

## Relationship to bilara-conventions.md

[bilara-conventions.md](bilara-conventions.md) covers the *format* (filename pattern, JSON structure, the `<paragraph>.<clause>` ID shape, the `.0` heading convention). This document covers the *content-level* decisions (which yogasthāna, which file, which framing marker goes where). They complement: bilara conventions are inherited from SuttaCentral; segmentation policy is project-specific to the Śrāvakabhūmi.
