# Reverse Engineering — Methodology

Version: 0.2 (bootstrap, unvalidated — see [REVIEW_LOOP.md](REVIEW_LOOP.md) for the path to v1.0). Revised 2026-08-11: Responsibility Boundary Gate and the Internal-context-first rule added below, both single-case/unvalidated — see inline Origin/Evidence level entries.
Applies to any object of investigation: an existing AI agent or system, an AI product, an AI company, a professional domain, or an idea for a future agent. Does not define what the output looks like — see `MISSION.md` for that.

This is a five-stage pipeline. Each stage has a defined exit condition; a stage is not "done enough," it is done or not done.

## Scope Sufficiency Gate (precondition to Stage 1)

Before Collection begins, check whether the target/finding as given is sufficient to investigate responsibly. Infer everything inferable from what's already been said. Ask only if the answer would change what gets investigated or how the report reads — never a generic "tell me more." One question at a time, scoped to a real fork, not a business interview. If nothing would change on any plausible answer, proceed without asking.

**Origin**: adapted from the Context Sufficiency Gate observed in Chief Design Officer (this project's own research) and from `mattpocock/skills`'s `grilling` skill. **Correction (2026-08-05)**: previously marked "the actual question-generation mechanism there isn't public, so this is the principle only, not a ported implementation" — that was wrong, caught when the requester asked how to install it. The mechanism (`skills/productivity/grilling/SKILL.md`, fetched and read directly) is public: interview the user as a "design tree," ask every currently-answerable question (the "frontier") in one numbered round with a recommended answer per question, wait for answers, recompute the frontier, repeat until nothing is left unasked — facts are the agent's job to find (dispatch a sub-agent, don't ask the user), decisions are the user's to make.
**Evidence level**: established (Chief Design Officer's gate, read in full) + established (grilling's mechanism, verified directly against its own `SKILL.md`, not inferred as before).

## Responsibility Boundary Gate (checked at every stage transition, not only before Stage 1)

Before moving from one stage to the next — and explicitly before any work that follows a completed Stage 5 — state out loud which of four modes governs what happens next: continuing collection/verification (**research**), synthesizing what has already been collected (**synthesis**), designing the consuming project's own solution (**design**), or a decision that belongs to the owner alone (**owner decision**). Silently sliding from one mode into another — most commonly research into design — is not permitted; the transition is named, not assumed. A mode-change that hasn't been named out loud has not happened yet, no matter how small the step looks from inside it.

**Origin**: 2026-08-11, AI Engineering / future Engineering Agent investigation (`research/AI-Engineering/`) — a real case, not bootstrap literature. Over roughly a dozen turns, "describe the AI Engineering profession" (research) progressively became "write this project's own Engineering Rules, Workflow, Checklist, Tool Stack, and Skill Map" (design), with no explicit checkpoint marking the switch anywhere in between. The switch was named by the project owner during a requested post-mortem, not caught by the process itself in the moment — the post-mortem's own findings are logged as evidence, not just this gate's justification. This is a further confirming instance of the limit `REVIEW_LOOP.md`'s Double-Loop Review section already states honestly: every double-loop instance to date has been triggered by an external party noticing first.
**Evidence level**: unvalidated — single case, first time this specific failure mode has been named as a gate rather than caught after the fact. First candidate for the next Evidence Review; should be tested against at least one more investigation with a design-facing consumer before being trusted as a stable rule.
**Relationship to the Scope Sufficiency Gate above**: that gate checks whether the *target* is well-defined before Stage 1 starts. This gate checks which *mode of work* is currently authorized, at every later transition — including the ones after Stage 5, which the Scope Sufficiency Gate does not cover at all.

## Stage 1 — Collection

**Internal-context-first rule (added 2026-08-11)**: before any external search opens, the internal context of the project that the investigation's findings are meant to serve must be read in full — not sampled reactively once a downstream question makes it unavoidable. Concretely: who is this research for, what does that project already have, what has it already decided. Only once that is done does external, world-practice search open.

**Origin**: same 2026-08-11 case as the Responsibility Boundary Gate above. The investigation's own brief named its consumer up front (a future Engineering Agent that composes agents from this project's own Foundation) — yet Foundation's own architecture documents (`Foundation/03_ARCHITECTURE/FOUNDATION_ARCHITECTURE.md`, `Foundation/04_REPOSITORY/README.md`), which turned out to already answer several questions the external market search had been tasked with (repository structure and its rationale, most concretely), went unread until several turns later, reactively, once "repository rules" was explicitly requested. The gap was never specific to Foundation — the general failure is that any internal-consumer-context document can be skipped this way whenever reading it isn't a named, required step before external search opens.
**Evidence level**: unvalidated — single case. Generalizes what had been an informal, project-specific habit into a standing Stage 1 requirement for any investigation with a defined internal consumer.
**Relationship to P0**: distinct from Principle P0 (`PRINCIPLES.md` — prove non-existence before inventing a new *mechanism*). This rule is about understanding the *consumer* before searching the *world*, not about avoiding duplicate invention.

Gather raw evidence about the object before forming any view of it. Evidence includes: source code (if available), primary documentation, changelogs/commit history, and observable behavior. Record what was found, verbatim or close to it — not an initial interpretation.

**Exit condition**: the collected evidence is written down in a form a second analyst could review without re-doing the collection.

**Origin**: Bellingcat OSINT practice — evidence (images, metadata, records) is gathered and logged before any claim is built on it; Google SRE postmortems — the timeline is drafted from raw facts *before* anyone walks into the review room, specifically to prevent the discussion from starting with an interpretation.
**Evidence level**: established.

*(Working default, not a rule: semantic/neural search has tended to surface primary sources faster than keyword search for initial discovery; keyword search remains useful for verification and confirming canonical/official domains. Not rigorously A/B tested — treat as a starting point, not a requirement.)*

**Source-type checklist**: check each of the following categories explicitly for the object under investigation — GitHub, official documentation, `CLAUDE.md`/`AGENTS.md`, README, Issues, Discussions, Releases/changelog, blog posts by the author(s), X/Twitter, YouTube, Reddit, Hacker News, papers, benchmarks, Discord (if open), demo videos. For each, record one of: found and read, found but not reachable, or not investigated. A category is never silently skipped — "not investigated" is a valid, honest state; silence about it is not. Video sources (YouTube, demo videos) are a known weak point: transcripts are not reliably fetched by default, so prefer a written companion artifact (blog post, thread, README) when one exists, and mark the video itself "not directly accessed, written companion used" rather than treating it as covered.

**Evidence level**: Inferred — this is a direct extension of the Document Inventory table already used ad hoc in individual case files (`knowledge/cases/`), generalized into a named, standing checklist rather than a per-case improvisation.

**Addition — Tool router (2026-08-05, unvalidated)**: which concrete tool is opened for a given source-type is not decided ad hoc each time; it follows a fixed check order:

1. The object's own artifact already exists locally (in-repo)? → read it directly (`Read`/`Grep`/`Glob`). Never search externally for something already on disk.
2. A URL is already known? → fetch it directly — the raw file if it's a GitHub path, `WebFetch`/a page-scrape tool otherwise (reach for a rendering-capable scraper only if the plain fetch can't get the structure needed) — rather than searching for it again.
3. No URL known, target still needs discovering → semantic/neural search first (per the working default above — it tends to surface primary sources faster for discovery), keyword search second, once a candidate is found, to confirm it's the canonical/official source.
4. The source type found through discovery selects what's opened next: a video → a transcript tool if one is reachable, else the written-companion rule above applies unchanged; a forum/discussion thread (Reddit, Hacker News) → general web search filtered to that domain — no dedicated per-forum tool assumed to exist, and content from it stays at hierarchy level 3–5 regardless of how it's fetched; an academic paper → a paper-search tool if the environment has one; a named library/SDK/framework → its documentation tool if the environment has one, in preference to general web search, since a docs-specific tool is typically more current and structured than search results.

Point 4 depends on what the current environment actually provides — the check is "does a tool for this source-type exist here," not an assumption that every category has a dedicated tool (it may not; general web search is the fallback for any category without one).

**Exit condition**: none of its own — this is a routing check inside Stage 1's Collection loop, consulted every time a source is needed and none is already open, not a stage with its own completion state.
**Origin**: original — no practice cited elsewhere in this skill specifies which tool serves which source category; the ordering itself (local > known-URL > discovery, semantic-before-keyword, dedicated-tool-if-one-exists) is a direct application of this stage's own semantic/keyword working default and Stage 2's source hierarchy to a new question, not borrowed from an outside discipline.
**Evidence level**: unvalidated — produced in a design discussion about this methodology's own process, not derived from running it on a real case. First candidate for the next Evidence Review (`REVIEW_LOOP.md`) once real cases exercise it.

## Stage 2 — Verification

Check the collected evidence against the source hierarchy before trusting it:

1. Primary artifact (source code, the system prompt itself, the actual configuration) — highest trust.
2. Official technical documentation.
3. Independent practitioner analysis / technical write-ups.
4. Official announcements/blog posts from the subject itself.
5. Media, marketing, hype — not trusted as evidence of mechanism, only as evidence that a claim exists (see [PRINCIPLES.md](PRINCIPLES.md) — P4).

When the object under investigation has a reachable primary artifact — a public GitHub repository, open documentation, an accessible README/`CLAUDE.md`/`SKILL.md`, source code — it must actually be opened and read before any conclusion is drawn about what it does. Reconstructing a mechanism from its name, from a secondary article's gloss, or from a README-level summary is not permitted when the primary artifact itself is one fetch away. This applies to any moment a specific mechanism gets described as fact, not only to a final report — a quick read partway through a conversation is not exempt.

Any claim resting only on levels 4–5 is marked unverified and cannot support a conclusion above the "watch" confidence tier (see Definition of Done, condition 7, and the confidence tiers below).

**Exit condition**: every load-bearing claim has a source-hierarchy level attached; claims from levels 4–5 alone are flagged, not silently promoted. In the final report, attribution is at the sentence level, not the paragraph or section level — a reader must be able to tell which specific source backs which specific claim without re-deriving the mapping themselves.

**Origin**: intelligence tradecraft source evaluation (Kent School) — evaluating the reliability of a source is a distinct, explicit step, separate from evaluating its content; IFCN — multiple independent sources required for contested claims.
**Evidence level**: established.

**Addition, confirmed on two independent cases (2026-08-03 — agentic-ceo, os-tack/ostk.ai)**: when a document claims a specific mechanism, behavior, or term (a threshold, a metric, a license, an agent's existence) and a corresponding primary implementation artifact is reachable (source code, a LICENSE file, a config file, an independent classifier), that artifact must be checked directly before the claim is credited as verified — not "the project says X," but "the project's own code/file does X." Where the artifact is unreachable, the claim stays at the Unverified tier regardless of how detailed the surrounding prose is. (Both confirming instances: a documented quantitative Critic behavior that did not exist anywhere in the actual source, and a README license claim contradicted by the project's own LICENSE file.)

**Addition — explicit report when a primary artifact is unreachable (2026-08-05)**: when this stage requires a primary artifact (a `SKILL.md`, a `CLAUDE.md`/`AGENTS.md`, an ADR, a PDF, a gated file, a video's actual content) and it cannot be reached, this is never silently absorbed by continuing on secondary sources alone. A request to the user for the document is a last resort, not a first move: it is written only after a real attempt to fetch the artifact has actually been made and failed — never issued preemptively as a shortcut around trying. Once that attempt has genuinely failed, it is reported in this shape:

> Для завершения анализа не хватает первичного артефакта:
> [конкретный путь/файл, а не «документы» вообще]
> Причина: [почему не удалось получить — приватный репозиторий, платный доступ, сеть не отдаёт файл, и т.п.]
> Прошу предоставить его вручную — самостоятельно получить не удалось.

The artifact named is always specific — a path, filename, or exact document type (e.g. "`skills/productivity/grill-me/SKILL.md`", "the PDF", "a transcript of the linked video") — never a generic request to "send documents." The reason line is required, not optional: it is what distinguishes a genuine last resort from a shortcut. If the artifact is later provided, it becomes the new top of the source hierarchy for that claim, and any prior conclusion that depended on the secondary source is re-checked and revised if it changes — not left standing beside a now-better source. This is the same non-destructive-revision discipline `REVIEW_LOOP.md` already applies to the methodology's own rules, applied here to a specific finding within one investigation. **Origin**: direct extension of Definition of Done condition 8 (explicit abstention) and the source hierarchy above, prompted by a real instance — reading a secondary description of a skill instead of its `SKILL.md` when the repository was fully public and one fetch away — caught during this project's own work, not hypothetical.

**Addition — independence of the check (2026-08-04)**: this check must not be satisfied from memory or from an earlier read in the same session. It is a fresh, separate fetch of the primary artifact, performed specifically to verify the claim — not reused reasoning from Stage 1 Collection. The report names which specific fetch performed the check for each Confirmed-tier claim that depended on it, so a second reader can see the check happened rather than take it on trust. **Origin**: adapted from the deny-by-default separation between the process that writes a claim and the process that checks it (scout-ci, OpenOSINT: "no model can fake a citation, because the code that checks provenance shares nothing with the code that writes the claim"). This project has no separate verification code — the same agent still performs the check — so independence here means a distinct, fresh, targeted action, not a distinct system; a genuinely separate, code-level check remains a larger step this rule does not itself take. **Evidence level**: established (the underlying separation principle), adapted (the weaker, same-agent form used here).

**Addition — Counting-unit check (2026-08-05)**: when a claim rests on a count (files, cases, sources), verify the counting unit actually matches the unit the claim is about before trusting the number as evidence — a file count is not automatically an object count.
**Origin**: adapted from measurement validity theory (Microsoft Research), already logged in `knowledge/CAPABILITY_MAP.md` (Capability 10 — checking whether a metric actually measures the claimed construct, distinct from checking where evidence came from); reinforced by a live instance this session (a file count over `knowledge/cases/` was briefly mistaken for the number of distinct cases).
**Evidence level**: established external practice, confirmed once in-project — not yet a repeated in-project pattern.

## Stage 3 — Decomposition

Break the object down to the mechanism that produces its behavior — not the behavior itself. For software/agent objects this typically means: what triggers it, what it actually does step by step, what constraints or guardrails shape it, and why it was built that way rather than another way.

Do not stop at "it does X." Continue until the answer is "it does X because of mechanism Y," where Y is falsifiable — a second analyst could check Y directly (in code, in config, in logs) rather than take it on faith.

**Exit condition**: the description names a mechanism, not just an observed behavior (see [PRINCIPLES.md](PRINCIPLES.md) — P2).

**Origin**: malware reverse engineering — static analysis (structure) is established as the foundation before dynamic (behavioral) analysis is trusted to explain anything; Anthropic mechanistic interpretability — the explicit goal is identifying the internal circuit responsible for a behavior, not describing the behavior.
**Evidence level**: established.

## Stage 4 — Contextualization

Place the mechanism in the context it exists within: what constraints (technical, commercial, organizational) shaped this design, and what does it cost — i.e. what alternative was given up by choosing this mechanism. Then place it against the current state of the receiving system (AI_OS / the consuming agent's own domain): what already exists there that is similar, absent, or in tension with it.

**Exit condition**: the mechanism is explained in terms of the constraints that produced it (not treated as a decision made in a vacuum) and a comparison to the receiving system's current state is stated explicitly.

**Origin**: Architecture Decision Records (Nygard) — the "Context" field exists specifically to capture the forces that led to a decision, not just the decision; Google SRE postmortems — modern practice favors "contributing factors" (the system context an incident occurred within) over a single isolated root cause.
**Evidence level**: established.

## Stage 5 — Judgment

State a conclusion, arrived at by elimination, not by confirmation-seeking: which explanation survives attempts to disprove it, not which explanation was found first or is most appealing. The conclusion must convert into something actionable — a recommendation, not an open-ended observation.

**Exit condition**: the conclusion names what should be adopted, what should be rejected, and what trade-off is accepted either way; it is attached to a confidence tier (see below).

**Origin**: Analysis of Competing Hypotheses (Heuer) — the surviving hypothesis is the one *least* disproven by the evidence, not the one most confirmed (which inverts the intuitive, confirmation-seeking default); Google SRE postmortems — conclusions are required to produce corrective action items with named owners, i.e. judgment that does not convert into an action is treated as incomplete.
**Evidence level**: established.

## Confidence tiers (used throughout, per Principle P5)

Adapted from Kent's Words of Estimative Probability, re-scaled from forecasting language to methodology/investigation claims:

- **Confirmed** — corroborated by 2+ independent sources at hierarchy level 1–2.
- **Established, single-source** — one strong level 1–2 source, not yet cross-corroborated.
- **Inferred** — pattern extrapolated by combining multiple sources, not stated outright by any one of them.
- **Unverified** — rests only on level 4–5 sources (announcement/marketing/media); may be reported, never used to justify "adopt."

## Definition of Done

An investigation is not complete when a report has been written. It is complete only when all eight conditions below hold, across two independent axes — a report can satisfy one axis and fail the other, and both are required. This is the exit gate for Stage 5, and the acceptance test applied during the validation cases in Stage 0 (see [REVIEW_LOOP.md](REVIEW_LOOP.md)).

**Synthesis axis** — does the report say something worth knowing:

1. A mechanism was identified, not just a description of behavior. *(Stage 3, P2)*
2. The cause of the advantage/design choice is identified — why it works, not only what it does.
3. Trade-offs are explicitly stated — what is given up by this design. *(adapted from ADR "Consequences")*
4. A transferable capability is identified, if one exists.
5. What should **not** be transferred is explicitly stated, if applicable.
5a. **Integration, one card per significant, reusable finding** — added 2026-08-11, refined same day, mandatory, not a separate artifact from the Report (it is `MISSION.md`'s existing "what transfers / what explicitly doesn't" output section, given a fixed structure instead of being left as free-text paragraphs). Placement: immediately after the lead synthesis (Stage 5 Judgment / profession model, where one exists) — not at the end of the document — since it is what a reader opens the report to act on. "Reusable" is the filter, not just "significant": a true, significant fact about one object (e.g. "OpenHands migrated its skill mechanism") is not itself a card; the reusable lesson it supports (e.g. "a bespoke local convention carries a real, paid-later migration cost once the field converges on a standard") is. For every such finding, the report states, in the same fixed shape every time:
- **Назначение** — what it is.
- **Почему интересен** — why it earned a place in the report.
- **Наш вывод** — one of *использовать полностью / адаптировать / объединить / отложить / отвергнуть*.
- **Если адаптируем/объединяем — с чем.**
- **Куда идёт** — which part of the receiving system (e.g. Foundation / Skill System / a specific consuming agent / stays a Research finding only).
- **Приоритет.**
- **Почему именно так** — the reason, stated concretely enough that it is still legible in three months without re-deriving it from the surrounding prose.
- **Что конкретно переносим** — added 2026-08-11, second pass: a ✔/✘ breakdown of exactly which part of the finding is taken and which part is explicitly left behind (e.g. "✔ progressive disclosure, ✔ the `name`/`description` contract; ✘ the specific example directory layout"). Without this field a card answers *what to do* but not *what to do it with*, which left the reader still needing to re-open the primary source before any actual building could start — the exact gap this whole section exists to close.

A report is not complete while a reader still has to ask "so what do we do with this, and with which specific part of it" after reading it — both questions are answered inline, per finding, not left as an exercise for whoever reads the report next.
**Origin**: 2026-08-11, AI Engineering / Engineering Agent investigation, two passes in the same session. First pass: three consecutive documents (`02-evidence.md`, `03-full-report.md`, `04-profession-model.md`) each did real, correctly-scoped work — collect, verify, synthesize into a profession model — and none of them, individually or together, ever answered "what do we take, what do we adapt, what do we merge, what do we reject, and where does it go." Verified against this project's own locked decision (`MISSION.md`'s Output contract, "product is the Intelligence Report — not open for re-discussion") before adopting: the fix strengthens the Report's own existing, chronically under-specified output section rather than introducing a new artifact next to it, which is what the lock's own test ("does this make the Report better, or just make the system more complex") requires. Second pass, same day: the first version of this section (applied to `research/AI-Engineering/03-full-report.md`) still ended each card at "adapt" without saying which part — caught immediately on first real use, prompting the "Что конкретно переносим" field and the "reusable, not just significant" filter.
**Evidence level**: unvalidated — single case, revised once already within that one case. First candidate for the next Evidence Review.

**Grounding axis** — is what it says actually supported:

6. The conclusion is reproducible — a second analyst applying this methodology to the same object would arrive at the same mechanism and trade-offs, even if worded differently. *(adapted from IFCN transparency-of-methodology — "readers can verify findings themselves")*
7. No conclusion rests solely on an Unverified-tier claim. *(Stage 2, P4)*
8. Where evidence was genuinely insufficient to support a finding in a required section, this is stated explicitly — not silently omitted, and not softened into a vague claim that reads as a finding. Abstaining correctly is a visible, checkable act, not an invisible non-event.

Neither axis substitutes for the other: a well-argued, well-organized report built on ungrounded claims fails this gate exactly as much as a well-cited report that never identifies a real mechanism.

**Provenance of this gate**: conditions 1, 2, 3, 6, 7 are each adapted from a specific cited practice above. Conditions 4 and 5 are tagged **original** — no reviewed discipline judges its object of study for the purpose of transplanting a capability into a separate, different system; intelligence analysis, SRE, and ADR practice all reason about and within their *own* system, not across systems. This is the one place bootstrap research did not find an existing rule to adapt, and the gap is filled deliberately rather than silently — flagged as the highest-risk pair in this methodology, first candidates for revision if real cases show them producing false positives. Condition 8 is tagged **adapted** — the 2026 deep-research-agent literature explicitly names confident fabrication under insufficient evidence as the worst failure mode of the category (worse than an honest "cannot verify"), and names held-out abstention testing as the direct check against it; this condition is that check applied to this methodology's own conclusions rather than to a benchmark question set.
