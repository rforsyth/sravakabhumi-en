---
title: Editorial conventions
status: policy
created: 2026-10-07
---

# Editorial conventions

These rules govern the English translation, the translator's notes (`comment/`), the section intros (`notes/translation-notes/`), and the edition-level text. They apply everywhere; a note or rendering that breaks one is corrected, not argued case by case.

## 1. Notes: the default is no note

A note is written, or kept, only if both tests pass:

1. **Need.** Without it, a careful reader of the English would be misled or could not follow. That means one of: the English departs from the printed Sanskrit (restoration, conjecture, lacuna, a reading taken as corrupt); a technical term is kept in Sanskrit; or a construal is genuinely ambiguous and the choice changes the meaning. Interest is not need.
2. **Correctness.** Every claim in it has been checked against the root, a cited edition, or a named witness. A claim that has not been checked is removed, not hedged.

Parallels in other texts, the history of a term, school labels, and practice commentary fail the first test. A cross-reference within the Śrāvakabhūmi ("See sbh2.0:59.126–130.") passes only where the text itself points elsewhere ("as explained before", *pūrvavat*) and the reader cannot follow without it. A correction never makes a note longer. Notes record readings and witnesses, not how a reading was arrived at: no "the prior rendering", no revision dates, no page references to working files.

The same rules apply to the section intros, which are written last, after the section itself is settled.

## 2. Restorations and gaps

Departures from Shukla's printed text are marked inline in the English. One marker per departure. A one-line note names the witness, in the form *Printed X; read Y (witness).*

| Marker | Use | Root JSON |
|---|---|---|
| `[Lacuna]` | text missing from Shukla's edition; nothing supplied | unchanged |
| `[Damaged]` | text present but unreadable; nothing supplied | unchanged |
| `[Conjectural: …]` | supplied by the translator, supported by the context or by Xuanzang's Chinese | unchanged |
| `[Restored: …]` | a Sanskrit reading attested in a critical edition (from the manuscript) and absent from, or misprinted in, Shukla | adopts the edition's reading |

Note forms, one line each:

- a misreading: *Printed X; read Y (witness).*
- an omission: *Printed text omits X; supplied from Y (witness).*
- a corrupt word with no reading to propose: *Printed X, corrupt; the sense follows Y (witness).* The English carries `[Conjectural: …]` if a sense is supplied, `[Damaged]` if not.
- a scribal repetition: rendered once; the repeated segment's English is left empty, with the note *Printed text repeats N.N.*

Markers contain English only; any Sanskrit goes in the note. Terms the translation keeps in Sanskrit as English words (*śamatha*, *vipaśyanā*, *dhyāna*, *manuṣyatva*) count as English here. A lost formulaic heading (a question the text's pattern makes certain) may be supplied as `[Conjectural: …]`; lost prose is marked `[Lacuna]` and not supplied, even where the pattern or Xuanzang makes it near-certain: a lost clause, a lost list item, or a definition that mirrors its neighbour. The note says what the witness has.

A `[Lacuna]` that falls between segments is placed at the end of the segment before the gap.

An obvious misprint (a single letter or ligature, a misdivided word, or a stray repeated syllable, with only one possible reading and no change to the sense) gets the one-line note but no inline marker.

`[Restored]` is reserved for Sanskrit witnesses. A reading supported only by Xuanzang's translation is `[Conjectural]`, with the note naming him. Where the English already follows a corrected reading, it still carries the marker.

Example notes:

- *Printed* asampannena; *read* asapatnena *(Xuanzang, T1579 juan 26).*
- *Printed* syād …… dhyāti; *read* sphuṭa iva khyāti *(ŚBh-Gr III-(6), 2013).*

This supersedes the "what Shukla printed is the source of truth" line in `sanskrit-emendation-policy.md` for readings a critical edition attests. That policy otherwise stands: whitespace and extraction artefacts are still rejoined silently.

## 3. Naming witnesses

- **Sh.** or **Shukla**: the printed edition (Shukla 1973), as transcribed on SuttaCentral.
- **MS**: only with an edition and note number that attest the manuscript reading ("MS per Deleanu 2006, n. 344"). A reading known only from Shukla is Shukla's, even where he reports it as the manuscript's.
- **Xuanzang (T1579 juan NN)**: the Chinese translation, cited by juan and, where useful, Taishō line.
- **Deleanu 2006**; **ŚBh-Gr** with the installment (e.g. "ŚBh-Gr IV(1), 2024"): the critical editions.

## 4. Brackets

- *(italic Sanskrit in parentheses)* gives the Sanskrit behind an English word. The form is the one in that segment, or a bare stem of it. A hyphenated compound, *(bala-vāhana)*, is fine when the compound is in the segment. Normalized citation forms and labels not in the segment are not given.
- [square brackets] mark English the translator supplies for sense. They never contain Sanskrit.
- Inline enumerators [1], [2] … appear only where the Sanskrit itself enumerates.

## 5. Claims about other texts

A note names another text only with a checked reference: a sutta with its segment number, a book with its page. "Cf." is the only hedge. These are not used: "canonical", "standard", "classical", "verbatim", "the entire", "always", and school labels ("a Yogācāra schema") without a citation.

## 6. Authorship

Notes and intros say "the text" or "the Śrāvakabhūmi". The traditional ascription to Asaṅga is mentioned once, in the README, as traditional.

## 7. Recurring errors

A misreading that recurs in a section is corrected throughout the section at once, as one change. A rendering is replaced section-wide only where the Sanskrit has the same sense everywhere; exceptions are left as they are.

## 8. Segment alignment

Each English segment translates its own root segment. Where a stretch is offset, it is re-paired to the correct segment IDs in a change of its own, with no other edits, so the correction is a pure shift.

## 9. Terminology

Controlled renderings are in `glossary.md`. Each term has one rendering. Where the text has drifted, the glossary rendering is applied throughout. Settled 2026-10-07:

| Term | Rendering |
|---|---|
| *manaskāra* | attention |
| *praśrabdhi* | pliancy |
| *dauṣṭhulya* | encumbrance |
| *vastu* | thing (not "substance"; "object" is reserved for *ālambana*) |
| *ālambaka* | the apprehending [mind] |
| *āyatana* (the twelve) | sense-base |
| formless *āyatana*s | sphere of … |
| *āśraya* | basis |
| *adhyāśaya* | intention (*hitādhyāśaya*: benevolent intention) |
| *citta-saṁskāra* | mind-conditioner |
| *aśubha* | unattractive |
| *audārika* | gross |
| *yathābhūta* | as it actually is |
| *ātmabhāva* | individual existence |
| *sāmantaka* | preparatory stage |
| *pratigha* | aversion (*pratikūla*: repugnant) |
| *prasadanīya* | gladdening (settled 2026-10-08) |

*pratyaśubhatā* is rendered "putrid unattractiveness" or kept in Sanskrit; "inherent" is not used.

## 10. Disclosure and license

The edition carries one statement of how it was made:

> The English was drafted with a large language model from Shukla's Sanskrit, cross-checked by a second model, and then reviewed section by section, also with AI assistance, against the Sanskrit, Xuanzang's Chinese translation (T1579), and, where available, the critical editions of Deleanu (2006) and the Taishō Śrāvakabhūmi Study Group. Ryan Forsyth, who does not read Sanskrit, directed the work, set the editorial policies, and is responsible for the result.

CC0 covers the English translation and apparatus. The Sanskrit is Karunesha Shukla's edition (Patna: K.P. Jayaswal Research Institute, 1973), in the transcription hosted on SuttaCentral; no license is claimed for it here.

A known-limitations statement in the README says which sections were read in full and which were sampled, which witnesses each was read against, and where Shukla's text has gaps. It also says that the translation has not yet been reviewed by a Sanskritist.
