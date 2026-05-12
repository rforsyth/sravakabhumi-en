---
title: Sanskrit emendation policy
status: working note (pre-METHOD.md)
created: 2026-05-11
---

# Sanskrit emendation policy

## Decision

The Sanskrit source file extracted from SuttaCentral's Shukla edition contains intra-word whitespace artifacts, almost certainly introduced by PDF→text extraction (or upstream OCR). They split single Sanskrit words across spaces in places no Sanskrit reader would accept — typically around ligature characters (`cch`, `ścch`, `ñch`).

These are **silently rejoined** in the root JSONs. No per-correction apparatus; the general policy is documented here and will move to METHOD.md when that file is written.

## Scope

The emendation policy covers only:

- Intra-word whitespace splits that produce non-words (e.g. `tadba la maudārikam` → `tadbalamaudārikam`)
- Ligature-splitting (e.g. `nicchi śchi draṁ` → `niścchidraṁ`)
- Sandhi-boundary mis-splits (e.g. `tā madhipatiṁ` → `tāmadhipatiṁ`)

Not covered (left as-is, treated as Shukla's reading):

- Edition-level variants like `upanibaghnāti` for `upanibadhnāti`
- Edition-level spellings like `cittasaṁtathau` for `cittasaṁtatau`
- Manuscript-level features in Shukla's text (he reconstructed from manuscripts; what he printed is the source of truth)

## Editorial supplements

A category beyond the whitespace policy: occasionally the source omits a word that context requires (e.g., a member of a canonical list). These are supplied silently in the JSON; the literal translation flags them with brackets. Each supplement is listed in the per-topic audit trail under "Supplements."

## Audit trail — sbh3.1

Fixes applied to `root/san/sastra/sbh/sbh3.1_root-san-shukla.json`:

| Segment | Source (glitched) | Emended |
|---|---|---|
| `sbh3.1:4.2` | `tadba la maudārikam` | `tadbalamaudārikam` |
| `sbh3.1:7.4` | `kāma c chandanivaraṇādibhiḥ` | `kāmacchandanivaraṇādibhiḥ` |
| `sbh3.1:8.2` | `samudācāra re saty` | `samudācāre saty` |
| `sbh3.1:9.2` | `nicchi śchi draṁ` | `niścchidraṁ` |
| `sbh3.1:9.2` | `samādhipravāhamā ma vasthāpayatyeva mekotīkaroti` | `samādhipravāhamavasthāpayatyevamekotīkaroti` |
| `sbh3.1:10.5` | `yenānabhisaṁskāra re vā ṇā nābhogenāsya` | `yenānabhisaṁskāreṇānābhogenāsya` |
| `sbh3.1:12.2` | `tā madhipatiṁ` | `tāmadhipatiṁ` |
| `sbh3.1:12.12` | `paricaya balena` | `paricayabalena` |
| `sbh3.1:13.2` | `sa c chidravāhano nichi śchi dravāhanaḥ` | `sacchidravāhano niścchidravāhanaḥ` |
| `sbh3.1:14.3` | `nichi śchi dravāhano` | `niścchidravāhano` |

## Audit trail — sbh2.1, sbh2.6 (Vyāpī, Ānāpānasmṛti)

Whitespace rejoins and minor restorations applied to the root JSONs for these two topics follow the recurring patterns established earlier: intra-word whitespace splits, anusvāra-`m` artifacts, dittographies, and ligature splits. Both passages are typographically noisier than sbh3.1 but cleaner than sbh2.5/sbh2.2. No semantic emendation. The Sanskrit-level corruptions in the sixteen-aspect list (sbh2.6:13.10–13.16) are preserved as-is and flagged in the comment file.

## Audit trail — sbh2.2 (Aśubhā)

Whitespace rejoins and minor restorations applied to `root/san/sastra/sbh/sbh2.2_root-san-shukla.json` follow the same patterns:

- Intra-word whitespace splits and anusvāra-`m` artifacts (recurring throughout)
- Compound-list normalization (commas and spacing in long body-parts and cemetery-aspect enumerations)
- The unusual `vibhadrātmaka` reading is preserved as-is (Asanga's reading; possibly a variant of *vipadumaka*)
- `gūtha-kaṭhilla` ('dung-clod' / 'dung-heap') preserved despite being a hapax legomenon

The passage is among the noisier in the source (the body-parts and cemetery enumerations accumulate small errors). No semantic emendation.

## Audit trail — sbh2.5 (Dhātu-prabheda)

Whitespace rejoins and minor restorations applied to `root/san/sastra/sbh/sbh2.5_root-san-shukla.json` follow the recurring patterns:

- Intra-word whitespace splits (e.g. `snāyu ḥ` → `snāyuḥ`, `vṛkkā kkaṁ` → `vṛkkaṁ`, `kā ya` → `kāya`)
- Anusvāra-`m` artifacts (e.g. `tvaṅmānsam` → `tvaṅmāṁsam`)
- Anusvāra mis-spelling (e.g. `mastakaluṁgaṁ` → `mastakaluṅgaṁ`)
- Dittography / OCR-insertion patterns (e.g. `praśrāvoya srāvo 'ya mucyate` → `prasrāvaḥ ayamucyate`; `kāṣṭhā ni vā,loṣṭhā ni vā` → `kāṣṭhāni vā, loṣṭhāni vā`)
- `b`/`v` normalizations where the standard reading requires (e.g. `basā` → `vasā`)
- Spurious initial-syllable artifacts (`kop dhātuḥ bdhātuḥ` → `'bdhātuḥ`)

The passage is one of the noisier sections in the source; no individual emendation departs from the standard Shukla reading attested in other digitizations. None changes the semantic content.

## Audit trail — sbh2.4 (Idaṁ-pratyayatā)

Whitespace rejoins applied to `root/san/sastra/sbh/sbh2.4_root-san-shukla.json`:

| Segment | Source (glitched) | Emended |
|---|---|---|
| `sbh2.4:1.2` | `apekṣā yuktyā` | `apekṣāyuktyā` |
| `sbh2.4:2.3` | `moha caritāccittaṁ` | `mohacaritāccittaṁ` |

## Audit trail — sbh2.3 (Maitrī)

Whitespace rejoins applied to `root/san/sastra/sbh/sbh2.3_root-san-shukla.json`:

| Segment | Source (glitched) | Emended |
|---|---|---|
| `sbh2.3:1.4` | `hitā dhyā śayam` | `hitādhyāśayam` |
| `sbh2.3:2.1` | `amitra pakṣe` | `amitrapakṣe` |
| `sbh2.3:2.4` | `ākhyātā ḥ` | `ākhyātāḥ` |
| `sbh2.3:2.5` | `avyābādhata yā ca` | `avyābādhatayā ca` |
| `sbh2.3:2.7` | `avyābādhyatā avyābādhatā` | `avyābādhatā` (dittographic; removed first form) |

Note: `sbh2.3:3.5` contains a known corrupt phrase (`adhimucyasyānirvo-`) preserved as-is; reading uncertain. See comment file.

## Audit trail — sbh2.7

Whitespace rejoins applied to `root/san/sastra/sbh/sbh2.7_root-san-shukla.json`:

| Segment | Source (glitched) | Emended |
|---|---|---|
| `sbh2.7:1.1` | `ka tamat` | `katamat` |
| `sbh2.7:3.3` | `audāri kamvā, sūkṣmvā, hīnamvā, praṇītamvā` | `audārikaṁ vā, sūkṣmaṁ vā, hīnaṁ vā, praṇītaṁ vā` (anusvāra-`mv` recurring pattern) |
| `sbh2.7:5.7` | `cakṣuḥsaṁsparśa jā saṁjñā` | `cakṣuḥsaṁsparśajā saṁjñā` |
| `sbh2.7:6.1` | `saṁskāra skandhaḥ` | `saṁskāraskandhaḥ` |
| `sbh2.7:6.2` | `ṣaṭcetanā kāyāḥ cakṣuḥ saṁsparśajā` | `ṣaṭ cetanākāyāḥ cakṣuḥsaṁsparśajā` |
| `sbh2.7:7.4` | `śrotraghrāṇajihvkāyamanovijñānaṁ` | `śrotraghrāṇajihvākāyamanovijñānaṁ` (missing macron) |
| `sbh2.7:11.3` | `skandhavyatirekeṇāhvā tmā namupalabhate` | `skandhavyatirekeṇātmānamupalabhate` |
| `sbh2.7:12.12` | `jihvdhātū` | `jihvādhātū` (missing macron) |
| `sbh2.7:12.13` | `jihvavijñānadhātuḥ` | `jihvāvijñānadhātuḥ` (missing macron) |
| `sbh2.7:12.14` | `mano vijñānadhātur` | `manovijñānadhātur` |
| `sbh2.7:13.5` | `svarusvakāddhātoḥ` | `svakasvakāddhātoḥ` |
| `sbh2.7:13.6` | `hetupratyakauśalyam` | `hetupratyayakauśalyam` (missing `ya`) |
| `sbh2.7:14.3` | `dvādaśayatanāni` | `dvādaśāyatanāni` (missing macron) |
| `sbh2.7:14.12` | `spraṣṭavyāya tanaṁ` | `spraṣṭavyāyatanaṁ` |
| `sbh2.7:15.3` | `samana ntara niruddhaṁ` | `samanantaraniruddhaṁ` |
| `sbh2.7:15.7` | `sa saṁprayogasyotpattaye` | `sasaṁprayogasyotpattaye` |
| `sbh2.7:15.11` | `sasaṁprayogānā ṇā miti` | `sasaṁprayogāṇāmiti` |
| `sbh2.7:16.1` | `katamaḥ mat pratītyasamutpādakauśalyaṁ` | `katamat pratītyasamutpādakauśalyaṁ` (extra `ḥ`/dittographic `katamaḥ` artifact) |
| `sbh2.7:16.3` | `saṁskārapratyayamvijñānaṁ` | `saṁskārapratyayaṁ vijñānaṁ` |
| `sbh2.7:17.1` | `yatpurardharmā` | `yatpunardharmā` |
| `sbh2.7:17.1` | `dharmānabhiṣpandayati nti` | `dharmānabhiṣpandayanti` |
| `sbh2.7:17.2` | `pratītyasamutpannatvātvādabhūtvā` | `pratītyasamutpannatvāt vā abhūtvā` |
| `sbh2.7:17.4` | `jarāṁdharmāṇo` | `jarādharmāṇo` (spurious anusvāra) |
| `sbh2.7:17.8` | `pratītatyasamutpādakauśalyam` | `pratītyasamutpādakauśalyam` (dittographic `ta`) |
| `sbh2.7:18.3` | `sthānāsthānakauśalyenā` | `sthānāsthānakauśalyena` (spurious vowel-lengthening) |

Note: also normalized many `paṁca` → `pañca` (anusvāra-`m` artifact recurring across the passage).

Supplements applied to `root/san/sastra/sbh/sbh2.7_root-san-shukla.json`:

| Segment | Source (manuscript) | Supplied |
|---|---|---|
| `sbh2.7:2.4` | `rūpaskandho vedanāskandhaḥ saṁskāraskandho vijñānaskandhaśca` (4 aggregates listed) | `rūpaskandho vedanāskandhaḥ saṁjñāskandhaḥ saṁskāraskandho vijñānaskandhaśca` (5 aggregates — *saṁjñāskandhaḥ* supplied by context) |

The 5-aggregate doctrine is universally attested; *saṁjñāskandha* is supplied because the per-aggregate definitions immediately following cover all five, and a missing-aggregate reading would be incoherent. Literal English translation flags the supplement with brackets: `[perception-aggregate,]`.

## Workflow for future topics

When a new topic is segmented from the source file:

1. After initial segmentation, scan the new root JSON for the same patterns: spaces inside what should be single words, ligature-character splits (`cch`, `ścch`, `ñch`), and isolated single consonants/syllables (`re`, `vā`, `ṇā`, `la`, `ma`, `c`) standing between recognizable Sanskrit fragments.
2. Apply rejoins. Add each correction to this audit trail.
3. If a glitch is ambiguous (multiple plausible rejoins), leave the source reading and flag in this note for review.

## Section-heading re-segmentation (2026-05-15)

Four chapters had Roman-numeral section headings embedded in or merged with body segments. To render headings as headings rather than as the opening sentence of body prose, these segments were split into a heading slot (`:N.0`) and a body slot (`:N.1`). The `.0` suffix is the project's existing heading convention (recognized by `_is_heading()` in `build_viewer.py`); the splits add new `:N.0` IDs without renaming any existing body-segment IDs — except `sbh1.1:1.1`, which was pure heading text and was simply renamed to `:1.0`.

Changes (applied symmetrically to both `root/san/.../*.json` and `translation/en/.../*.json`; affected comment entries also moved):

| Chapter | Before | After |
|---|---|---|
| `sbh1.1:1.1` (pure heading) | `:1.1` = "I. gotrabhūmiḥ // \|" | renamed to `:1.0` |
| `sbh1.2:1.1` (heading + body merged) | `:1.1` = "............................. II. avatārabhūmiḥ ........... yaiḥ ṣaḍbhir..." | split: `:1.0` = "............................. II. avatārabhūmiḥ ........... "; `:1.1` = "yaiḥ ṣaḍbhir..." |
| `sbh1.3:1.1` (doubled term) | `:1.1` = "naiṣkramyabhūmiḥ naiṣkramyabhūmiḥ katamā \|" | split: `:1.0` = "[III.] naiṣkramyabhūmiḥ "; `:1.1` = "naiṣkramyabhūmiḥ katamā \|" |
| `sbh2.0:1.1` (heading + body merged) | `:1.1` = "II. dvitīyaṁ yogasthānam laukikaṁ caiva..." | split: `:1.0` = "II. dvitīyaṁ yogasthānam "; `:1.1` = "laukikaṁ caiva..." |
| `sbh2.0:104.1` (mid-text Yogasthāna boundary) | `:104.1` = "III. tṛtīyaṁ yogasthānam evaṁ kṛte..." | split: `:104.0` = "III. tṛtīyaṁ yogasthānam "; `:104.1` = "evaṁ kṛte..." |

These are structural splits at recognizable section boundaries in the source — not semantic emendations. The 12 Category B chapters (sbh2.1–2.7, sbh3.1–3.2, sbh4.1–4.3) were not modified; they don't have embedded body-text headings, and their chapter title is displayed via the page H1 sourced from `:0.2`.

**Restoration in sbh1.3**: the Sanskrit source at this point has *naiṣkramyabhūmiḥ naiṣkramyabhūmiḥ katamā* — the bhūmi name doubled, with no Roman-numeral marker. The doubling is anomalous and most plausibly preserves a scribal error covering a lost *III.* (the previous two sub-bhūmis of Yogasthāna I, sbh1.1 and sbh1.2, carry explicit *I.* and *II.* markers). Bracketed *III.* has been editorially restored in both Sanskrit (`[III.]`) and English (`[III.]`) — the brackets signal the editorial nature of the restoration.

