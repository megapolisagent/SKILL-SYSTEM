# Reverse Engineering — Review Loop

Defines how this methodology itself is allowed to change. The methodology is not edited directly; it evolves through a fixed loop, and every change is traceable to a reason.

## The loop

```
Methodology vX.Y
      ↓
Run on real cases (see knowledge/cases/)
      ↓
Evidence Review  (mandatory — a version bump may not skip this)
      ↓
Decision Log entry per changed rule (adopted / kept / dropped, tagged with reason)
      ↓
Methodology vX.(Y+1)
```

## Evidence Review

After a batch of cases (recommended: 5 before a minor revision), produce an Evidence Review answering, rule by rule:

- **Confirmed** — the rule held; cite which case(s) confirmed it.
- **Disconfirmed** — the rule produced a wrong or unusable result; cite the case.
- **Useless** — the rule never mattered to the outcome across the batch (true regardless of whether it was followed).
- **Missing** — a pattern was observed across cases that no current rule covers.
- **False positive** — the rule fired / was satisfied, but the resulting recommendation was wrong in hindsight.

An Evidence Review with no disconfirmed or missing entries after only 1–2 cases is treated as insufficient evidence, not as a sign of a finished methodology — absence of failure this early is more likely under-testing than correctness.

**Origin**: Google SRE postmortem culture — the review is treated as a learning opportunity for the practice, not a verdict on whoever wrote the rule (blameless framing applies to methodology review, not only incident review).
**Evidence level**: established (direct transfer of postmortem culture from incidents to methodology rules).

**Addition — Contract compliance check (2026-08-05, unvalidated)**: before starting new case work, check whether this document's own declared transitions — Evidence Review due after N cases, a Decision Log entry required for a changed rule, human sign-off required before v1.0 — have already come due and not yet occurred. A transition that fired without its required action is a contract violation, not a deferred task: it is stated plainly (which condition, what triggered it, why it hasn't happened) rather than folded silently into the next Evidence Review as if nothing was overdue. Findings are recorded per checked condition; a clean result on one condition is not evidence about conditions not checked.

**Origin**: original — no practice cited elsewhere in this skill checks whether the practice's own declared triggers have actually fired. Prompted by a near-miss in this same session: an initial file count over `knowledge/cases/` suggested five cases and an overdue Evidence Review; a corrected count found four distinct cases, meaning the recommended threshold had not actually been reached and no violation had occurred. The check itself is warranted independently of that specific instance — nothing in this document's own process would catch a real miss automatically, whether or not this particular one turned out to be real.
**Evidence level**: unvalidated — first candidate for its own Evidence Review once checked against real elapsed cadence.

## Decision Log

There is no separate decision-log file. Every rule added, changed, or removed is recorded directly in the document that changed (`PRINCIPLES.md`, `METHODOLOGY.md`, or `knowledge/CAPABILITY_MAP.md`), using the same inline `Origin:` / `Evidence level:` format already used throughout those files — what changed, which case triggered it, and whether it's `adapted from <cited practice>` or `original`. A project this size keeping the same fact in two files (an inline note plus a mirrored ledger entry) is exactly the "two sources of truth quietly disagreeing" failure this skill itself has flagged when studying other systems; one inline note per rule is the whole record.

**Origin**: Architecture Decision Records (Nygard format: Context / Decision / Consequences) and IFCN's "open and honest corrections" commitment — a change to a public claim/standard is documented, not silently made.
**Evidence level**: established.

## Versioning

- `v0.x` — draft, may be revised by the agent itself between Evidence Reviews.
- `v1.0` ("stable standard") — requires explicit human sign-off. The agent may propose that v1.0 is ready; it may not declare it. Until sign-off, the version stays `v0.x` regardless of how many cases have run.
- Post-v1.0 changes (`v1.0 → v1.1`, etc.) follow the same Evidence Review discipline — stability is not a reason to skip the loop, only a reason the loop should trigger less often.

(An earlier draft of this gate also required "10 diverse cases" and "no critical change in the last 3 studies" as numeric pre-conditions. Dropped: both numbers were arrived at by feel, not by evidence, and the project's own principles (P1, facts before conclusions) don't support gating a real decision — human sign-off — behind a threshold nobody had actually tested. Sign-off is the one part of this gate that is genuinely load-bearing; it is kept, and the un-evidenced numbers are not.)

## Double-Loop Review

Evidence Review, above, is **single-loop**: it checks whether a rule held on real cases and adjusts within the existing framework — confirmed, disconfirmed, useless, missing, false positive. By Argyris & Schön's exact distinction (1974/1978), that is only half of a complete learning cycle. Double-loop learning corrects error by first examining and revising the *governing variables themselves* — here, whether `PRINCIPLES.md`'s principles and `METHODOLOGY.md`'s stage definitions are still the right framework — not only the actions taken inside them.

**Trigger**: on the same cadence as Evidence Review (after a batch of cases, or at the close of a major research unit) — scheduled as part of the cadence itself, not invoked only when asked. This follows the After Action Review discipline of being built into the event's own rhythm, rather than depending on an external party to request it.

**Procedure, compressed to the essential move**: before a unit of work, state which principle/stage is expected to govern it and what outcome that implies (OODA's prediction-before-outcome tracking). After, compare expectation to what actually happened. A gap is either closed by a different *action* under the existing rules (single-loop, feeds Evidence Review) or requires changing a *principle or stage itself* (double-loop). If double-loop, apply P0 first — search for an existing practice before proposing a change. Record the result inline in the changed document either way, including "no change needed": an unchanged rule for a long stretch is a thing to check, not a comfort (Toyota's standard-work discipline), and a finding specific to one object rather than the method itself belongs entirely in that object's own case file, not here.

**Known limit, stated honestly**: the scientific self-correction literature (Allchin, 2024; Merton) finds that self-correction is not a guaranteed mechanism even in science, and depends on conditions this project cannot fully supply alone — chiefly, *diversity of perspective*. A single agent reviewing its own governing framework is structurally weaker than a review involving a genuinely different vantage point. Double-Loop Review is a supplement to external review, not a replacement for it — every double-loop instance to date in this project's history was still triggered by an external party noticing first, and that is expected to remain a real, ongoing limit, not a temporary immaturity to be engineered away entirely. **Confirmed again, 2026-08-11**: the AI Engineering / Engineering Agent investigation drifted from research into design across roughly a dozen turns with no internal checkpoint catching it; the project owner named the drift during a requested post-mortem, which produced `METHODOLOGY.md`'s new Responsibility Boundary Gate and Internal-context-first rule. The mechanism worked exactly as this section predicts — the review happened, but only because an external party asked for it.

**Origin**: adapted from Argyris & Schön's single-loop/double-loop distinction (organizational learning theory), After Action Review's built-into-cadence discipline (US Army FM 7-0), OODA's explicit prediction-vs-outcome tracking (Boyd), and Toyota's "an unchanged standard is a signal, not a comfort" rule — combined with an explicit, cited limitation from Mertonian scientific self-correction literature. Tag: adapted (combination) — every component is cited; none is original to this project. Full source detail: `knowledge/evidence/2026-08-03-meta-review-existing-practices.md`.
**Evidence level**: established per component; the combination is this project's own synthesis.
