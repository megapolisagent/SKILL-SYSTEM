# Skill Library

Сгенерировано автоматически (2026-08-10T11:03:07+00:00) — не редактировать руками.
Изменить: положить/поправить Skill в `skills/`, задать category/origin через `skillctl.py`, запустить `skillctl.py library`.

## Как пользоваться

- **Ищу Skill для задачи** — смотрю раздел по направлению ниже, читаю description.
- **Нашла новый Skill** — прошу добавить в библиотеку с указанием источника.
- **Skill отмечен ⚠ NEEDS REVIEW** — значит содержимое изменилось после последней проверки, старая проверка на него больше не распространяется.
- **Status `DRAFT`** — Skill в библиотеке, но ещё не проверен на реальных задачах. Можно использовать осторожно.
- **Нужен Skill, которого нет** — пока пишется вручную, как обычный SKILL.md, и добавляется тем же способом, что и остальные.

## CORE

### brainstorming
You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### capability-creation-methodology
Использовать, когда Idea Calibration (Шаг 0) сработал и триггер — предложение нового агента/проекта, требующего экспертизы в целой незнакомой профессиональной области. Специализация Шага 2 (World Research) idea-calibration для случая целой профессии, не инструмента.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### docx
Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### executing-plans
Use when you have a written implementation plan to execute in a separate session with review checkpoints

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### idea-calibration
Обязательный gate перед любым архитектурным решением — использовать, когда меняется способ решения задачи (новый агент/проект, крупное архитектурное изменение >2 модулей, масштабирование), не при точечных правках внутри уже выбранной архитектуры.

- источник: AI_OS (Мария) (own)
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

### skill-creator
Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### visual
Генерация фото, видео и аудио через VelsVisual CLI и KIE API (kie.ai). Используй, когда пользователь просит «сгенерируй картинку/изображение/фото/видео/музыку/песню/озвучку/голос/саунд-эффект», text-to-image, image-to-video, TTS или апскейл изображения.

- источник: nick-vels/VelsVisual (github, MIT license) (adapted)
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
- статус: `DRAFT`
- использований: 0

### xlsx
Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
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

## ENGINEERING

### architecture-review
Чеклист архитектурной фазы — использовать после Idea Calibration (шаг 7: Yes) и до Bootstrap Sequence, чтобы закрыть архитектурную фазу нового агента/проекта: workflow, capabilities map, naming, reliability architecture, AI reasoning boundaries.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

### claude-api
|-

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

### dispatching-parallel-agents
Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### mcp-builder
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
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

### verification-before-completion
Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
- статус: `DRAFT`
- использований: 0

### webapp-testing
Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0

## RESEARCH

### youtube-analysis
Использовать, когда пользователь прислал ссылку на YouTube-видео. Последовательно пробует субтитры, транскрипцию и кадры, прежде чем сообщать об ограничении; после анализа автоматически передаёт результат в opportunity-discovery.

- источник: AI_OS (Мария) (own)
- статус: `DRAFT`
- использований: 0

## STRATEGY

### opportunity-discovery
Использовать, когда пользователь делится новой технологией, моделью, инструментом, статьёй, видео, GitHub-проектом, MCP, SDK, API или стартапом — материалом, меняющим пространство возможностей экосистемы. Не запускается на багфиксах, рефакторинге, локальной автоматизации или точечных технических вопросах.

- источник: AI_OS (Мария) (own)
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

### internal-comms
A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0
