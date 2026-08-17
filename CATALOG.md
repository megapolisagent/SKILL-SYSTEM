# Skill Catalog

Сгенерировано автоматически (2026-08-17T09:33:51+00:00) — не редактировать руками.
Производный индекс для выбора ресурса под задачу. Источник истины — SKILL.md каждого Skill, не этот файл.
Обновить: `skillctl.py catalog`.

## architecture-review

- description: Чеклист архитектурной фазы сборки нового агента — Reliability Architecture, AI Reasoning Boundaries, capability map по Skills/MCP/моделям. Используй после того, как задача и профессия агента понятны (эталон от Researcher есть), и до того как проходить чек-лист «репозиторий готов».
- when: —
- what: —
- not_when: Раздел Reliability Architecture — не для простых utility-агентов, только для client-facing/decision-making/аналитики/финансово-чувствительных систем.
- examples: «Задача и профессия нового агента понятны, эталон от Researcher получен — нужно закрыть архитектурную фазу перед сборкой репозитория» → architecture-review; «Обычный багфикс в уже существующем агенте» → architecture-review не нужен
- related: capability-creation-methodology (предшествующий шаг, если агент строится под целую незнакомую профессию — architecture-review закрывает его результат); repository-design (следующий шаг после architecture-review — чек-лист «репозиторий готов»)
- status: DRAFT
- origin: AI_OS (Мария) (own)
- usage: 0

## brainstorming

- description: You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.
- when: —
- what: —
- not_when: Когда решение уже принято и требуется исполнение, а не исследование вариантов.
- examples: «Придумать новую функцию продукта или агента» → brainstorming; «Исправить уже известный баг» → brainstorming не нужен; «Решение уже принято, нужно его реализовать» → brainstorming не нужен, нужен Skill для реализации
- related: idea-calibration (если из брейншторма рождается архитектурное решение); writing-plans (когда решение уже принято и начинается планирование реализации)
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## brand-guidelines

- description: Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
- when: —
- what: To access Anthropic's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design
- not_when: Не для брендинга любой компании — конкретно фирменный стиль Anthropic (их цвета/типографика), не переносимый шаблон.
- examples: «Нужно оформить артефакт в фирменном стиле Anthropic (их цвета/шрифты)» → brand-guidelines; «Нужен брендинг произвольной компании, не Anthropic» → brand-guidelines не нужен — это конкретно фирменный стиль Anthropic, не универсальный шаблон
- related: pptx (обычно применяется поверх уже готовой презентации/документа)
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## capability-creation-methodology

- description: Воспроизводимый путь от «нужна экспертиза в незнакомой профессии» до спроектированного набора способностей нового агента — обязательный Open Source Research, Legacy-first Alarm, take/reject-лог по источникам. Используй когда задача — построить агента для целой незнакомой профессиональной области, не точечный инструмент.
- when: «Вход в задачу» из устава агента сработал (Impact/Uncertainty/Complexity, хотя бы одна high), и триггер конкретно — «нужен агент для X», где X — целая профессиональная область (маркетинг, продажи, финансы, обучение, юриспруденция), не точечный инструмент.
- what: —
- not_when: - Точечное расширение уже понятной области — решается напрямую, без этого Skill.
- Область, где уже есть собранный и используемый агент — это пересмотр существующего, не новое создание.
- Задача не прошла «Вход в задачу» — этот Skill не подменяет его.
- examples: «Нужен целый новый профессиональный агент (например, Маркетолог), которого в системе ещё нет» → capability-creation-methodology; «Нужен точечный инструмент внутри уже существующего агента» → не нужен
- related: architecture-review (следующий шаг после проектирования capability — закрытие архитектурной фазы)
- status: DRAFT
- origin: AI_OS (Мария) (own)
- usage: 0

## capability-recommend

- description: Используй, когда пользователь формулирует рабочую задачу и хочет понять, какие Skills/MCP/инструменты помогут её решить — прежде чем начинать работу над задачей вручную. Не запускается, если пользователь уже прямо назвал конкретный Skill/инструмент, который использовать, или если это правка/продолжение уже начатой в этой сессии работы.
- when: —
- what: —
- not_when: —
- examples: —
- related: —
- status: DRAFT
- origin: Claude Code, эта сессия (own)
- usage: 0

## claude-api

- description: |-
- when: Use WebFetch to get the latest documentation when:

- User asks for "latest" or "current" information
- Cached data seems incorrect
- User asks about features not covered here

Live documentation URLs are in `shared/live-sources.md`.
- what: —
- not_when: Явно не для OpenAI/Gemini/Llama/Mistral/Cohere/Ollama — при этих маркерах skill сам требует остановиться и спросить пользователя.
- examples: «Пишем код, вызывающий Claude/Anthropic API» → claude-api; «Работаем с OpenAI/Gemini/другим провайдером» → claude-api не нужен — сам skill явно требует остановиться и уточнить
- related: mcp-builder (если поверх Claude API строится ещё и MCP-сервер)
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## conversion-method

- description: Use when пишешь текст, который должен убедить конкретного человека совершить одно конкретное действие в течение одной сессии чтения — лендинг, объявление, короткое коммерческое предложение. Статус: рабочая гипотеза, не подтверждённая универсальная методология.
- when: Лендинг, объявление, короткое коммерческое предложение — разовое, быстрое
убеждение.

**Not for:** длинные доказательные документы (грант, RFP, формальное
предложение с проверкой множества критериев) — отдельная, ещё не построенная
гипотеза; визуальное оформление — нет capability генерации изображений.
- what: Пишет текст, который убеждает конкретного человека совершить одно конкретное
действие в течение одной сессии чтения.
- not_when: —
- examples: «Нужен текст лендинга, убеждающий читателя сделать одно конкретное действие» → conversion-method; «Нужен длинный доказательный документ (грант, RFP)» → conversion-method не нужен — отдельная, ещё не построенная гипотеза
- related: —
- status: EVALUATED
- origin: AI_OS (Мария) (own)
- usage: 0

## decision-documentation

- description: Документирует значимое решение агента в формате Foundation (Статус / Что решается / Обоснование / Отклонённые альтернативы / Источник) — контекст и причина, не только сам факт решения. Используй, когда решение переживёт текущий диалог, меняет правила работы, или владелец спрашивает «что мы решили по X».
- when: —
- what: —
- not_when: —
- examples: «Приняли решение, которое переживёт этот диалог или меняет правила работы» → decision-documentation; «Рядовая задача, не проходящая фильтр по значимости» → не нужен
- related: —
- status: VERIFIED · LIVE
- origin: Foundation/04_REPOSITORY/DECISIONS.md (уже существующий формат) (own)
- usage: 1

## dispatching-parallel-agents

- description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
- when: **Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other
- what: You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need.…
- not_when: **Related failures:** Fixing one might fix others - investigate together first
**Need full context:** Understanding requires seeing entire system
**Exploratory debugging:** You don't know what's broken yet
**Shared state:** Agents would interfere (editing same files, using same resources)
- examples: «3+ независимых теста падают по разным причинам» → dispatching-parallel-agents; «Непонятно, что вообще сломано (exploratory debugging)» → не нужен
- related: subagent-driven-development (оба про делегирование подзадач фоновым агентам, разный акцент (параллельность vs план))
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## doc-coauthoring

- description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
- when: —
- what: —
- not_when: —
- examples: «Нужно написать техническую спецификацию/proposal/decision doc с нуля» → doc-coauthoring; «Нужно быстро поправить пару предложений в готовом документе» → doc-coauthoring не нужен — это тяжеловесный процесс для существенной, не точечной работы
- related: brainstorming
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## docx

- description: Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
- when: —
- what: —
- not_when: —
- examples: «Нужно создать/отредактировать Word-документ (.docx)» → docx; «Нужен PDF или презентация, не Word» → docx не нужен, соответственно pdf/pptx
- related: pdf (соседний Skill для другого формата документа)
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## executing-plans

- description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
- when: —
- what: Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell your human partner that Superpowers works much better with access to subagents (Claude Code, Codex CLI, Codex App, Copilot CLI, and Gemini CLI all qualify; see the per-platform tool refs in `../using-superpowers/references/`).…
- not_when: —
- examples: «Есть письменный план реализации, нужно выполнить в отдельной сессии с точками ревью» → executing-plans; «Плана ещё нет» → нужен writing-plans, не executing-plans
- related: writing-plans (естественный предшественник — сначала план пишется, потом выполняется); subagent-driven-development (альтернативный способ выполнения плана с независимыми задачами)
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## final-quality-gate

- description: Чеклист перед тем, как считать ответ завершённым — не 'достаточно ли хорош ответ', а есть ли действие, которое заметно улучшит результат без непропорционального роста времени/сложности. Семь проверок: Coverage, Evidence, Opportunity, Simplification, Future Problems, Completion, System Opportunity.
- when: —
- what: —
- not_when: —
- examples: «Собираюсь заявить, что ответ готов» → final-quality-gate — обязательная проверка перед завершением почти любого содержательного ответа
- related: generalization-ladder (оба — универсальная дисциплина проверки качества рассуждения); independent-validation (более тяжёлая независимая проверка для решений с высокой ценой ошибки — следующий уровень строгости)
- status: DRAFT
- origin: AI_OS (Мария) (own)
- usage: 0

## generalization-ladder

- description: Дисциплина обобщения субъективных наблюдений и утверждений: свободная формулировка не становится правилом сразу — Raw Observation → Hypothesis → Recurring Pattern, статус повышается только при независимом повторении (≥2-3 случая), не потому что показалось важным.
- when: —
- what: —
- not_when: —
- examples: «Человек высказал субъективное впечатление один раз» → фиксируется как Hypothesis, не сразу как Pattern; «То же наблюдение повторилось независимо 2-3 раза» → можно поднять до Recurring Pattern
- related: final-quality-gate (часть той же универсальной дисциплины проверки собственных выводов)
- status: DRAFT
- origin: AI_OS (Мария) (own)
- usage: 0

## idea-calibration

- description: Use when "Вход в задачу" (HOME.md) flagged a genuinely large decision — new agent, change to Engineer's own methodology, or a redesign touching more than two modules — not for ordinary uncertainty a few clarifying questions already resolve.
- when: «Вход в задачу» уже сработал (хотя бы одна ось high), и решение конкретно про: новый агент/проект; изменение собственной методологии работы Engineer; редизайн, затрагивающий больше двух модулей/файлов устава.
- what: —
- not_when: - Обычная неопределённость, которую снимают 2-3 уточняющих вопроса — для этого «Вход в задачу» уже достаточен, этот Skill не подменяет его.
- Разовая задача без долгосрочных последствий, даже если Uncertainty high.
- examples: «Решение про новый агент, смену методологии, редизайн больше двух модулей» → idea-calibration — обязательный глубокий путь; «Обычная неопределённость, снимается 2-3 вопросами» → не нужен, входного гейта достаточно
- related: architecture-review (следующий шаг после Decision: Yes); capability-creation-methodology (используется, если цель — целая незнакомая профессия, не точечный инструмент)
- status: DRAFT
- origin: AI_OS (Мария) (own)
- usage: 0

## independent-validation

- description: Независимая проверка итогового решения (не тем же ходом рассуждений, что его породил) при новом агенте, высокой цене ошибки, сложном архитектурном анализе или изменении самой методологии. Проверяет Correctness, Necessity, Reuse, Problem Fidelity.
- when: —
- what: —
- not_when: —
- examples: «Новый агент, высокая цена ошибки, меняется сама методология» → independent-validation обязательна; «Обычный рефакторинг, короткий ответ, простая автоматизация» → не нужна
- related: generalization-ladder (не применяется к Raw Observation/Hypothesis — только к уже зафиксированному решению); final-quality-gate (более лёгкая, всегда применяемая проверка — independent-validation про решения с высокой ценой ошибки)
- status: DRAFT
- origin: AI_OS (Мария) (own)
- usage: 0

## internal-comms

- description: A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).
- when: To write internal communications, use this skill for:
- 3P updates (Progress, Plans, Problems)
- Company newsletters
- FAQ responses
- Status reports
- Leadership updates
- Project updates
- Incident reports
- what: —
- not_when: Не для внешних/публичных материалов — только внутренние коммуникации компании (само название это ограничивает).
- examples: «Нужен статус-репорт/апдейт для руководства/новостная рассылка компании» → internal-comms; «Нужна внешняя публичная коммуникация (клиенты, пресса)» → internal-comms не нужен — только внутренние форматы
- related: —
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## legacy-repository-audit

- description: Use when the owner points at an old/external agent repository (previous version of an agent, abandoned system, a repo built by someone else) and asks to check it before building something new. Covers identification, full inventory, and owner-confirmed classification — not a general code review.
- when: Владелец называет конкретный старый/внешний репозиторий агента и просит проверить его — обычно перед тем, как строить новых агентов, чтобы не переизобретать то, что уже сделано или уже решено не делать.
- what: —
- not_when: - Разбор текущего, живого репозитория самого Engineer/Researcher — для этого есть `architecture-review`/`repository-design`, не этот Skill.
- Ревью кода перед доставкой — не про это.
- Задача не про целый репозиторий, а про один конкретный файл/вопрос — избыточно, читай файл напрямую.
- examples: —
- related: architecture-review, repository-design
- status: DRAFT
- origin: Engineer — собран из практики этой сессии (MAIN_ENGINEER, AI_OS) (own)
- usage: 0

## mcp-builder

- description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
- when: —
- what: Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.
- not_when: Не для выбора/использования уже существующего MCP — только для постройки нового сервера с нуля.
- examples: «Нужно построить MCP-сервер для интеграции внешнего API» → mcp-builder; «Нужно просто вызвать уже существующий MCP, ничего не строить» → mcp-builder не нужен, см. tool-selection
- related: tool-selection (соседняя, но обратная задача — выбор среди готовых инструментов, не постройка нового)
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## opportunity-discovery

- description: Использовать, когда пользователь делится новой технологией, моделью, инструментом, статьёй, видео, GitHub-проектом, MCP, SDK, API или стартапом — материалом, меняющим пространство возможностей экосистемы. Не запускается на багфиксах, рефакторинге, локальной автоматизации или точечных технических вопросах.
- when: —
- what: —
- not_when: —
- examples: «Пользователь поделился новой технологией/видео/GitHub-проектом для экосистемы» → opportunity-discovery; «Обычный багфикс внутри уже выбранной архитектуры» → не запускается
- related: youtube-analysis (частый источник триггера — видео, после которого автоматически передаётся сюда)
- status: VERIFIED · LIVE
- origin: AI_OS (Мария) (own)
- usage: 1

## pdf

- description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
- when: —
- what: This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see REFERENCE.md. If you need to fill out a PDF form, read FORMS.md and follow its instructions.
- not_when: —
- examples: «Нужно прочитать/объединить/подписать PDF-файл» → pdf; «Нужна таблица (.xlsx) или Word-документ, не PDF» → pdf не нужен
- related: xlsx (соседний Skill для другого формата документа)
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## pptx

- description: Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. If a .pptx or .potx file needs to be opened, created, or touched, use this skill.
- when: —
- what: —
- not_when: —
- examples: «Нужна презентация/питч-дек (.pptx)» → pptx; «Нужен обычный текстовый документ, не слайды» → pptx не нужен, см. docx
- related: pdf (соседний Skill для другого формата документа); brand-guidelines (применяется поверх, если нужен именно фирменный стиль Anthropic)
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## repository-design

- description: Проектирует и проверяет структуру репозитория нового AI-агента, собранного поверх Foundation — что обязательно, что заполняет специализация, что нельзя трогать. Используй, когда нужно спроектировать структуру нового агента, проверить уже собранный репозиторий или объяснить, зачем нужен тот или иной файл дома.
- when: —
- what: —
- not_when: —
- examples: «Собираем нового агента поверх Foundation, нужно спроектировать структуру репозитория» → repository-design; «Репозиторий уже спроектирован, выполняется обычная задача внутри него» → не нужен
- related: architecture-review (architecture-review — про архитектурную фазу проекта в целом; repository-design — конкретно про файлы/структуру Foundation)
- status: VERIFIED · LIVE
- origin: Foundation/03_ARCHITECTURE/FOUNDATION_ARCHITECTURE.md (внутренний источник проекта, не внешний) (own)
- usage: 1

## reverse-engineering

- description: Реверс-инженерит реальную мировую практику для заданной цели (агент/система/продукт/компания/профессиональный домен/идея будущего агента) и превращает это в Intelligence Report с evidence — не мнение, не пересказ документации. Используй, когда нужно узнать, как что-то реально делается лучшими практиками в мире, для одной цели за раз.
- when: —
- what: —
- not_when: —
- examples: —
- related: —
- status: DRAFT
- origin: AI Intelligence, оригинальная методология (own)
- usage: 0

## skill-authoring

- description: Use when creating a new Skill, editing an existing one, or verifying that a Skill actually changes agent behavior before relying on it. Covers writing and testing as one cycle, not two separate tasks.
- when: —
- what: —
- not_when: —
- examples: «Нужно создать новый Skill с нуля, отредактировать существующий, или проверить, что Skill реально меняет поведение агента» → skill-authoring; «Skill уже написан и просто используется, менять его не нужно» → не нужен
- related: skill-creator (один из двух источников, объединённых в этот Skill — в архиве, заменён этим); writing-skills (второй из двух источников, объединённых в этот Skill — в архиве, заменён этим)
- status: DRAFT
- origin: Engineer — MERGE skill-creator (anthropics/skills) + writing-skills (obra/superpowers) (own)
- usage: 0

## subagent-driven-development

- description: Use when executing implementation plans with independent tasks in the current session
- when: **vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Review after each task (spec compliance + code quality), broad review at the end
- Faster iteration (no human-in-loop between tasks)
- what: —
- not_when: —
- examples: «Выполняется план реализации с независимыми задачами в текущей сессии» → subagent-driven-development; «Задачи зависят друг от друга последовательно» → не нужен
- related: executing-plans (оба про выполнение уже готового плана, разный акцент на делегирование подзадач); dispatching-parallel-agents (похожий принцип параллельного делегирования для независимых задач)
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## systematic-debugging

- description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- when: Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simpl…
- what: **Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**
- not_when: —
- examples: «Баг, падающий тест или неожиданное поведение — до предложения фикса» → systematic-debugging; «Root cause уже найден, нужно просто написать исправление» → не нужен, переходим к реализации
- related: test-driven-development (systematic-debugging — расследование причины; TDD — как потом писать сам фикс); verification-before-completion (после фикса — проверка, что он реально работает)
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## taste-capture

- description: Использовать, когда нужно определить эстетическое, творческое или брендовое направление, а готового брендбука или явно сформулированных предпочтений нет — вкус нужно обнаружить через реакцию человека, а не изобрести за него.
- when: Нужно определить эстетическое, творческое или брендовое направление, и нет
готового брендбука или явно сформулированных предпочтений — вкус нужно
обнаружить, а не изобрести за человека.
- what: —
- not_when: —
- examples: «Нужно определить эстетическое/брендовое направление, а готового брендбука нет» → taste-capture; «Брендбук/стиль уже чётко определён» → не нужен
- related: —
- status: DRAFT
- origin: AI_OS (Мария) (own)
- usage: 0

## test-driven-development

- description: Use when implementing any feature or bugfix, before writing implementation code
- when: **Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.
- what: Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**
- not_when: —
- examples: «Реализуем новую фичу или багфикс, код ещё не написан» → test-driven-development; «Одноразовый прототип или конфигурационный файл» → можно не применять, по согласованию
- related: systematic-debugging (после расследования причины бага — TDD про то, как писать сам фикс); verification-before-completion (после написания кода — проверка, что тесты реально проходят)
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## tool-selection

- description: Правила выбора инструмента под задачу Engineer — какая категория работы требует какой категории инструмента, и что делать, если подходящего инструмента нет. Используй перед тем, как начать искать информацию, менять репозиторий или задавать вопрос владельцу.
- when: —
- what: —
- not_when: —
- examples: «Перед тем как искать информацию/менять репозиторий/спрашивать владельца — неясно, какой инструмент нужен» → tool-selection; «Инструмент уже очевиден и однозначен» → не нужен, не создавай лишний шаг
- related: mcp-builder (соседняя, но обратная задача — постройка нового MCP, не выбор среди готовых)
- status: DRAFT
- origin: Инвентаризация реальной среды Claude Code, AI Intelligence проект (own)
- usage: 1

## verification-before-completion

- description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
- when: **ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness
- what: **Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**
- not_when: —
- examples: «Собираюсь заявить, что работа исправлена/готова/тесты проходят» → verification-before-completion — обязательно прогнать проверочные команды; «Работа явно не завершена, ничего пока не заявляется» → неприменимо ещё
- related: test-driven-development (TDD пишет тест заранее; verification-before-completion проверяет результат перед тем, как заявить об успехе); final-quality-gate (более общая универсальная проверка качества ответа)
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## visual

- description: Генерация фото, видео и аудио через VelsVisual CLI и KIE API (kie.ai). Используй, когда пользователь просит «сгенерируй картинку/изображение/фото/видео/музыку/песню/озвучку/голос/саунд-эффект», text-to-image, image-to-video, TTS или апскейл изображения.
- when: —
- what: —
- not_when: —
- examples: «Нужно сгенерировать картинку/видео/озвучку через API» → visual; «Нужен обычный текстовый ответ» → не нужен
- related: —
- status: DRAFT
- origin: nick-vels/VelsVisual (github, MIT license) (adapted)
- usage: 0

## writing-plans

- description: Use when you have a spec or requirements for a multi-step task, before touching code
- when: —
- what: Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD.…
- not_when: —
- examples: «Есть спецификация для многошаговой задачи, код ещё не тронут» → writing-plans; «Задача тривиальная, план избыточен» → не нужен
- related: executing-plans (естественное продолжение — план пишется здесь, выполняется там); brainstorming (предшествует, если решение ещё не выбрано — сначала исследовать варианты, потом планировать)
- status: DRAFT
- origin: obra/superpowers (github, MIT license по репозиторию) (adapted)
- usage: 0

## xlsx

- description: Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
- when: —
- what: —
- not_when: —
- examples: «Таблица — основной вход/выход задачи (.xlsx/.csv)» → xlsx; «Результат должен быть Word-документом или HTML-отчётом» → xlsx не нужен
- related: pdf (соседний Skill для другого формата документа)
- status: DRAFT
- origin: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- usage: 0

## youtube-analysis

- description: Использовать, когда пользователь прислал ссылку на YouTube-видео. Последовательно пробует субтитры, транскрипцию и кадры, прежде чем сообщать об ограничении; после анализа автоматически передаёт результат в opportunity-discovery.
- when: —
- what: —
- not_when: —
- examples: «Пользователь прислал ссылку на YouTube-видео» → youtube-analysis; «Нужно исследовать текстовую статью или GitHub-репозиторий, не видео» → youtube-analysis не нужен
- related: opportunity-discovery (автоматический переход после анализа — подтверждено реальным использованием)
- status: VERIFIED · LIVE
- origin: AI_OS (Мария) (own)
- usage: 1
