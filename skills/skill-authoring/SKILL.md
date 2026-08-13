---
name: skill-authoring
description: Use when creating a new Skill, editing an existing one, or verifying that a Skill actually changes agent behavior before relying on it. Covers writing and testing as one cycle, not two separate tasks.
---

# Skill Authoring
## Writing and testing Skills as one discipline — TDD applied to process documentation

> Объединено 2026-08-12 (MERGE, Engineer, `DECISIONS.md` — «Финальное инженерное принятие capability-аудита») из `skill-creator` (anthropics/skills) и `writing-skills` (obra/superpowers) — два независимых источника, пришедших к одной идее: тестирование Skill'а не отдельный шаг после авторства, а тот же цикл, что и его создание. Тестовый пайплайн адаптирован под среду без внешнего eval-viewer/скриптов — см. раздел «Не перенесено» в конце. Заменяет `skill-creator` и `writing-skills` (оба — DEPRECATED, см. их evidence.json).

## Core principle

**Writing a Skill IS Test-Driven Development applied to process documentation.** Write a pressure/application scenario (test), watch a subagent fail it without the Skill (RED), write the Skill, watch a subagent pass with the Skill present (GREEN), close loopholes (REFACTOR).

**If you didn't watch an agent fail without the Skill, you don't know if the Skill teaches the right thing.**

## Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Applies to new Skills AND edits to existing ones. Wrote a Skill before testing it? Delete it, start over. No exceptions for "simple additions" or "just documentation."

## When to create a Skill

**Create when:** the technique wasn't intuitively obvious; you'd reference it again across tasks; the pattern applies broadly, not just to one project.

**Don't create for:** one-off solutions; standard practices documented elsewhere; project-specific conventions (belongs in that agent's own instructions); mechanical constraints better enforced by validation/script than by documentation.

## Skill types — test differently

| Type | Examples | Test with |
|---|---|---|
| Discipline-enforcing (rules) | test-driven-development, verification-before-completion | Pressure scenarios: complies under time/sunk-cost/authority pressure? |
| Technique (how-to) | systematic-debugging | Application scenarios: applies correctly to a new case? |
| Pattern (mental model) | tool-selection | Recognition scenarios: knows when to apply, and when not? |
| Reference (docs/API) | claude-api | Retrieval scenarios: finds and uses the right information? |

## The cycle

### 1. Capture intent
What should this Skill enable? When should it trigger — what words/situations? What's the expected output? Interview the owner if the scope isn't already obvious from the conversation.

### 2. RED — write the failing test first
Run the pressure/application scenario with a subagent that does **not** have the Skill. Document verbatim what it does — for discipline-enforcing Skills, the exact rationalizations it uses. A Skill written without seeing the baseline failure is a guess, not a fix.

### 3. Write the SKILL.md
Frontmatter — `name` (letters/numbers/hyphens only, matches folder) + `description`. **Description = when to use, never what it does or how.** A description that summarizes the workflow becomes a shortcut agents take instead of reading the body — tested finding from the source material: a description saying "review between tasks" made an agent do one review when the flowchart specified two. Start with "Use when...", third person, concrete triggers/symptoms, no workflow summary.

Match the guidance form to the failure type:

| Baseline failure | Right form |
|---|---|
| Skips a rule under pressure (knows better, does it anyway) | Prohibition + rationalization table + red flags |
| Complies, but wrong shape | Positive recipe: state what the output IS |
| Omits a required element | Structural: required field/slot in a template |
| Behavior should depend on a condition | Conditional keyed to an observable predicate |

No nuance clauses ("don't X unless it matters" reopens negotiation). No exemption clauses that don't structurally scope the rule away from what they claim to exempt.

For discipline-enforcing Skills — bulletproof against rationalization: close every named loophole explicitly ("don't keep it as reference", "don't look at it"), state that violating the letter is violating the spirit, build a rationalization table from what the baseline actually said, add a red-flags self-check list.

### 4. GREEN — verify with a subagent that has the Skill
Spawn both runs (with-Skill and baseline) in the same turn so they finish together, not sequentially. Compare: does the with-Skill agent now comply / apply correctly / recognize when to use it?

**Adapted for environments without `eval-viewer`/benchmark scripts**: read both transcripts directly, compare qualitatively. For 2-3 realistic test prompts this is fast enough without scripted aggregation; needing many more than that is itself a signal the Skill is trying to do too much.

### 5. REFACTOR — close loopholes
New rationalization found? Add an explicit counter, re-test until the agent can't find a way around it. Keep the Skill lean — remove anything not pulling its weight; read the transcript, not just the output, to see if the Skill made the model waste turns on something unproductive.

### 6. Discovery check (SDO)
Rich, trigger-only description; keyword coverage (error messages, symptoms, tool names an agent would actually search for); descriptive verb-first naming. Keep frequently-loaded parts lean — every token in a Skill that loads often is a token in every future conversation.

## Structure

```
skill-name/
├── SKILL.md (required — frontmatter + body, keep under 500 lines — confirmed against Anthropic's own current best-practices doc, not folklore: "Keep SKILL.md body under 500 lines for optimal performance. Split content into separate files when approaching this limit")
├── scripts/     — executable code for deterministic/repetitive tasks
├── references/  — docs loaded into context only as needed
└── assets/      — files used in output (templates, icons)
```

One excellent example beats several mediocre ones. Flowcharts only for genuinely non-obvious decision points — not for reference material, code, or linear steps.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Skill is obviously clear" | Clear to you ≠ clear to another agent. Test it. |
| "It's just a reference" | References have gaps too. Test retrieval. |
| "I'll test if problems emerge" | Problems = the Skill already failed someone. Test before deploying. |
| "Too tedious to test" | Debugging a bad Skill in production costs more than the test. |
| "No time to test" | Deploying untested wastes more time fixing it later. |

## Checklist

- [ ] Baseline (RED) run documented verbatim, not paraphrased
- [ ] `name`/`description` match format, description is trigger-only
- [ ] Guidance form matches the failure type (see table above)
- [ ] With-Skill (GREEN) run verified against the same scenario
- [ ] Rationalization table + red flags, if discipline-enforcing
- [ ] No dead references to infrastructure this environment doesn't have
- [ ] States explicitly when NOT to use it — not just when to use it (a Skill without this is easy to reach for on the wrong task)
- [ ] States explicitly what the next consumer of the result gets — a file, a decision, a specific field — not left implicit
- [ ] Installed, host agent's own Skill list/table updated

## Не перенесено из источников, и почему

`skill-creator` (Anthropic) в оригинале также включал: Python eval-viewer с браузерным ревью человеком, количественную агрегацию бенчмарков (`benchmark.json`/`aggregate_benchmark`), автоматизированный цикл оптимизации description (`run_loop.py` через `claude -p`), и flow упаковки `.skill`/`present_files`. Решения, которые они обслуживали (сравнить с/без Skill, оптимизировать триггер, упаковать для распространения), сохранены выше в адаптированном, ручном виде; конкретный тулинг — нет, если в среде агента его не установить: мёртвые ссылки на скрипты хуже, чем отсутствие шага вовсе.
