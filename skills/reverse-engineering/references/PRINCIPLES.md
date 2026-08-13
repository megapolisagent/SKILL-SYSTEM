# Reverse Engineering — Principles

Provenance: every principle below is adapted from an existing, cited discipline — origin and evidence-level are stated inline, per rule.

This document answers: *why do we investigate this way*. It does not describe the process (see [METHODOLOGY.md](METHODOLOGY.md)) or how the process evolves (see [REVIEW_LOOP.md](REVIEW_LOOP.md)).

## P0 — Prove non-existence before inventing

Before creating any new mechanism, document, or process — not only a methodology rule — first search for an existing practice that already solves the problem. A new construct may be proposed only after that search comes up genuinely empty, and the search itself is recorded, not skipped.

**Origin**: prior art search discipline in patent law and engineering design (USPTO's own 7-step search guidance; Stanford OTL; CASRAI) — a mandatory, decades-old, cross-domain norm requiring a documented search of existing patents and non-patent literature before committing to build or file, specifically to avoid duplicating what already exists.
**Evidence level**: established (a universal professional norm, not specific to this project or to AI systems).
**Governs**: every other principle and every mechanism in `METHODOLOGY.md`/`REVIEW_LOOP.md` was, or should have been, produced this way. This project's own history recorded violations of this principle — a tool-selection rule written before checking for an existing analog, and an initial "Self-Audit" design written before checking whether Double-Loop Learning (see [REVIEW_LOOP.md](REVIEW_LOOP.md)) already covered the same gap. Both were caught by external correction, not self-caught in the moment — which is itself the evidence for why this principle is numbered first, not sixth.

## P1 — Facts before conclusions

Conclusions are drawn only after evidence is collected and laid out, never before. A conclusion formed first and then supported with selectively chosen evidence is a failure of this principle, not a variant of it.

**Origin**: Analysis of Competing Hypotheses (Heuer) — evidence is listed and matrixed against *all* hypotheses before any hypothesis is favored; International Fact-Checking Network Code of Principles — "follow the same process for every fact check and let the evidence dictate the conclusions."
**Evidence level**: established (two independent disciplines converge on the same rule).

## P2 — Mechanism before behavior

An investigation is not complete when it can describe *what* a system does. It is complete only when it can describe *how* the system produces that behavior internally. Surface description is the beginning of the work, not the end.

**Origin**: malware reverse engineering practice — static analysis (structure/mechanism) is established before dynamic analysis (observed behavior) is trusted as an explanation; Anthropic's mechanistic interpretability program — explicitly framed as reverse-engineering the internal algorithm instead of treating a model as a black box judged only on input/output behavior.
**Evidence level**: established (a security-research discipline and an AI-research discipline independently converge on treating behavior as insufficient evidence of mechanism).

## P3 — Multiple independent sources, triangulated

No claim is accepted on the strength of a single source. Where a claim is contested or load-bearing for a conclusion, it must be corroborated by at least one further, independent source before it is treated as fact.

**Origin**: Bellingcat OSINT methodology — a distinctive feature is identified, then triangulated against secondary, independent features before a location/claim is accepted; IFCN Code of Principles — signatories commit to "accessing multiple sources for contested points of evidence."
**Evidence level**: established (independently converged on by open-source investigation practice and fact-checking practice).

## P4 — Evidence over marketing

A claim made by the subject of investigation about itself (an announcement, a marketing page, a pitch) is a data point about what is claimed, never a data point about what is true. It is downgraded automatically, regardless of how credible the speaker appears.

**Origin**: IFCN Code of Principles — transparency-of-funding commitment exists specifically so that "funders have no influence over conclusions," i.e. the source of a claim is separated from its truth-value; intelligence tradecraft (Kent School) — source evaluation is a standing, explicit step separate from evaluating the content of what the source reports.
**Evidence level**: established.

## P5 — Every judgment carries an explicit confidence level

A conclusion is stated together with how well-supported it is, not as a flat assertion. Ambiguous language ("likely," "seems to") is banned unless it is anchored to a defined confidence tier.

**Origin**: Sherman Kent, "Words of Estimative Probability" (1964) — the founding document of the practice of attaching calibrated probability language to intelligence judgments, adopted because ambiguous confidence language was found to cause analysts and decision-makers to misunderstand each other even when they agreed on the facts.
**Evidence level**: established (single origin, but foundational and durable — in continuous use across intelligence and cyber-threat-intel disciplines since 1964).
**Adaptation for this skill**: Kent's numeric scale (0–100%) is replaced with a four-tier evidence-level taxonomy suited to methodology rules and investigation claims, not probabilistic forecasts. Tag: **original** (adapted framing — no existing discipline defines confidence tiers for *methodology rules themselves*).

## P6 — Stop collecting once a source stops adding new information

Depth is not measured by how much was read, but by whether the last thing read taught something new. Once a category of source repeatedly fails to surface a mechanism not already captured, that category is closed.

**Origin**: Grounded theory (Glaser & Strauss, 1967) — theoretical saturation: sampling stops when further data yields no new properties of the category under study.
**Evidence level**: established.
**Applies to**: the Collection stage of every individual case (see METHODOLOGY.md).
