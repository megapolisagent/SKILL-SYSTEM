# Skill Library

Сгенерировано автоматически (2026-09-04T15:47:55+00:00) — не редактировать руками.
Изменить: положить/поправить Skill в `skills/`, задать category/origin через `skillctl.py`, запустить `skillctl.py library`.

## Как пользоваться

- **Ищу Skill для задачи** — смотрю раздел по направлению ниже, читаю description.
- **Нашла новый Skill** — прошу добавить в библиотеку с указанием источника.
- **Skill отмечен ⚠ NEEDS REVIEW** — значит содержимое изменилось после последней проверки, старая проверка на него больше не распространяется.
- **Status `DRAFT`** — Skill в библиотеке, но ещё не проверен на реальных задачах. Можно использовать осторожно.
- **Нужен Skill, которого нет** — пока пишется вручную, как обычный SKILL.md, и добавляется тем же способом, что и остальные.

## CORE

### capability-recommend
Используй, когда пользователь формулирует рабочую задачу и хочет понять, какие Skills/MCP/инструменты помогут её решить — прежде чем начинать работу над задачей вручную. Не запускается, если пользователь уже прямо назвал конкретный Skill/инструмент, который использовать, или если это правка/продолжение уже начатой в этой сессии работы.

- источник: Claude Code, эта сессия (own)
- статус: `DRAFT`
- использований: 0

### final-quality-gate
Чеклист перед тем, как считать ответ завершённым — не 'достаточно ли хорош ответ', а есть ли действие, которое заметно улучшит результат без непропорционального роста времени/сложности. Семь проверок: Coverage, Evidence, Opportunity, Simplification, Future Problems, Completion, System Opportunity.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### generalization-ladder
Дисциплина обобщения субъективных наблюдений и утверждений: свободная формулировка не становится правилом сразу — Raw Observation → Hypothesis → Recurring Pattern, статус повышается только при независимом повторении (≥2-3 случая), не потому что показалось важным.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### grilling
Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### independent-validation
Независимая проверка итогового решения (не тем же ходом рассуждений, что его породил) при новом агенте, высокой цене ошибки, сложном архитектурном анализе или изменении самой методологии. Проверяет Correctness, Necessity, Reuse, Problem Fidelity.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### to-questionnaire
Turn a decision you can't fully answer into a questionnaire for someone else to fill in.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

## DESIGN

### brand-guidelines
Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### taste-capture
Использовать, когда нужно определить эстетическое, творческое или брендовое направление, а готового брендбука или явно сформулированных предпочтений нет — вкус нужно обнаружить через реакцию человека, а не изобрести за него.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### visual
Генерация фото, видео и аудио через VelsVisual CLI и KIE API (kie.ai). Используй, когда пользователь просит «сгенерируй картинку/изображение/фото/видео/музыку/песню/озвучку/голос/саунд-эффект», text-to-image, image-to-video, TTS или апскейл изображения.

- источник: nick-vels/VelsVisual (github, MIT license) (adapted)
- статус: `DRAFT`
- использований: 0

## ENGINEERING

### architecture-review
Чеклист архитектурной фазы сборки нового агента — Reliability Architecture, AI Reasoning Boundaries, capability map по Skills/MCP/моделям. Используй после того, как задача и профессия агента понятны (эталон от Researcher есть), и до того как проходить чек-лист «репозиторий готов».

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### capability-creation-methodology
Воспроизводимый путь от «нужна экспертиза в незнакомой профессии» до спроектированного набора способностей нового агента — обязательный Open Source Research, Legacy-first Alarm, take/reject-лог по источникам. Используй когда задача — построить агента для целой незнакомой профессиональной области, не точечный инструмент.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### claude-api
|-

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### claude-md-improver
Audit and improve CLAUDE.md files in repositories. Use when user asks to check, audit, update, improve, or fix CLAUDE.md files. Scans for all CLAUDE.md files, evaluates quality against templates, outputs quality report, then makes targeted updates. Also use when the user mentions "CLAUDE.md maintenance" or "project memory optimization".

- источник: anthropics/claude-plugins-official (github.com/anthropics/claude-plugins-official) (adapted)
- статус: `DRAFT`
- использований: 0

### codebase-design
Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### decision-documentation
Документирует значимое решение агента в формате Foundation (Статус / Что решается / Обоснование / Отклонённые альтернативы / Источник) — контекст и причина, не только сам факт решения. Используй, когда решение переживёт текущий диалог, меняет правила работы, или владелец спрашивает «что мы решили по X».

- источник: Foundation/04_REPOSITORY/DECISIONS.md (уже существующий формат) (own)
- статус: `VERIFIED · LIVE`
- использований: 1, последний раз 2026-08-11T17:52:03+00:00

### dispatching-parallel-agents
Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### domain-modeling
Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### executing-plans
Use when you have a written implementation plan to execute in a separate session with review checkpoints

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### git-guardrails-claude-code
Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### idea-calibration
Use when "Вход в задачу" (HOME.md) flagged a genuinely large decision — new agent, change to Engineer's own methodology, or a redesign touching more than two modules — not for ordinary uncertainty a few clarifying questions already resolve.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### legacy-repository-audit
Use when the owner points at an old/external agent repository (previous version of an agent, abandoned system, a repo built by someone else) and asks to check it before building something new. Covers identification, full inventory, and owner-confirmed classification — not a general code review.

- источник: Engineer — собран из практики этой сессии (MAIN_ENGINEER, AI_OS) (own)
- статус: `DRAFT`
- использований: 0

### mcp-builder
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### prototype
Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### repository-design
Проектирует и проверяет структуру репозитория нового AI-агента, собранного поверх Foundation — что обязательно, что заполняет специализация, что нельзя трогать. Используй, когда нужно спроектировать структуру нового агента, проверить уже собранный репозиторий или объяснить, зачем нужен тот или иной файл дома.

- источник: Foundation/03_ARCHITECTURE/FOUNDATION_ARCHITECTURE.md (внутренний источник проекта, не внешний) (own)
- статус: `VERIFIED · LIVE`
- использований: 1, последний раз 2026-08-11T17:52:03+00:00

### resolving-merge-conflicts
Use when you need to resolve an in-progress git merge/rebase conflict.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### skill-authoring
Use when creating a new Skill, editing an existing one, or verifying that a Skill actually changes agent behavior before relying on it. Covers writing and testing as one cycle, not two separate tasks.

- источник: Engineer — MERGE skill-creator (anthropics/skills) + writing-skills (obra/superpowers) (own)
- статус: `DRAFT`
- использований: 0

### skill-creator
Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DEPRECATED`
- использований: 0

### subagent-driven-development
Use when executing implementation plans with independent tasks in the current session

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### systematic-debugging
Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### test-driven-development
Use when implementing any feature or bugfix, before writing implementation code

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### tool-selection
Правила выбора инструмента под задачу Engineer — какая категория работы требует какой категории инструмента, и что делать, если подходящего инструмента нет. Используй перед тем, как начать искать информацию, менять репозиторий или задавать вопрос владельцу.

- источник: Инвентаризация реальной среды Claude Code, AI Intelligence проект (own)
- статус: `DRAFT`
- использований: 1, последний раз 2026-08-11T17:52:03+00:00

### triage
Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### verification-before-completion
Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### webapp-testing
Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DEPRECATED`
- использований: 0

### wizard
Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### writing-for-agents
Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.

- источник: mattpocock/skills (github.com/mattpocock/skills) (adapted)
- статус: `DRAFT`
- использований: 0

### writing-plans
Use when you have a spec or requirements for a multi-step task, before touching code

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### writing-skills
Use when creating new skills, editing existing skills, or verifying skills work before deployment

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DEPRECATED`
- использований: 0

## RESEARCH

### reverse-engineering
Реверс-инженерит реальную мировую практику для заданной цели (агент/система/продукт/компания/профессиональный домен/идея будущего агента) и превращает это в Intelligence Report с evidence — не мнение, не пересказ документации. Используй, когда нужно узнать, как что-то реально делается лучшими практиками в мире, для одной цели за раз.

- источник: AI Intelligence, оригинальная методология (own)
- статус: `DRAFT`
- использований: 0

### youtube-analysis
Использовать, когда пользователь прислал ссылку на YouTube-видео. Последовательно пробует субтитры, транскрипцию и кадры, прежде чем сообщать об ограничении; после анализа автоматически передаёт результат в opportunity-discovery.

- источник: AI_OS (Мария) (own)
- статус: `VERIFIED · LIVE`
- использований: 1, последний раз 2026-08-11T14:20:57+00:00

## STRATEGY

### brainstorming
You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### opportunity-discovery
Использовать, когда пользователь делится новой технологией, моделью, инструментом, статьёй, видео, GitHub-проектом, MCP, SDK, API или стартапом — материалом, меняющим пространство возможностей экосистемы. Не запускается на багфиксах, рефакторинге, локальной автоматизации или точечных технических вопросах.

- источник: AI_OS (Мария) (own)
- статус: `VERIFIED · LIVE`
- использований: 1, последний раз 2026-08-11T14:20:57+00:00

### outcome-gate
Use before starting or saving any artifact that claims an external, observable result for its addressee (a decision, a structure to act on, a metric to move) — not for artifacts whose only claim is that they exist. Triggers on business/strategy teardown outputs, recommendation documents, plans presented as ready to act on.

- источник: github.com/megapolisagent/AI_OS (CLAUDE.md, Outcome Gate / Outcome Over Output) (adapted)
- статус: `DRAFT`
- использований: 0

### pricing
Экспертная методика ценообразования и монетизации (SaaS-фокус, но применимо шире) — модели ценообразования, структура тарифов, аудит цен/pricing-страницы, willingness-to-pay. Используй, когда нужно понять, что взять за основу для решения по цене/пакетированию — не как готовое решение самой, а как справочный материал для агента-специалиста или для совета владельцу бизнеса без прямого исполнения.

- источник: coreyhaines31/marketingskills (GitHub, MIT license) (adapted)
- статус: `DRAFT`
- использований: 0

### revops
Экспертная методика revenue operations — жизненный цикл лида, скоринг/роутинг, стадии пайплайна, гигиена данных CRM, передача маркетинг→продажи. Используй, когда нужен справочный материал по устройству CRM/лид-процессов — не как готовое решение самой, а как база для агента-специалиста или для совета владельцу бизнеса без прямого исполнения.

- источник: coreyhaines31/marketingskills (GitHub, MIT license) (adapted)
- статус: `DRAFT`
- использований: 0

## WRITING

### conversion-method
Use when пишешь текст, который должен убедить конкретного человека совершить одно конкретное действие в течение одной сессии чтения — лендинг, объявление, короткое коммерческое предложение. Статус: рабочая гипотеза, не подтверждённая универсальная методология.

- источник: AI_OS (Мария) (own)
- статус: `EVALUATED`
- использований: 0

### doc-coauthoring
Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### docx
Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### humanizer
|

- источник: blader/humanizer (adapted)
- статус: `DRAFT`
- использований: 0

### internal-comms
A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### pdf
Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### pptx
Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. If a .pptx or .potx file needs to be opened, created, or touched, use this skill.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### xlsx
Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0
