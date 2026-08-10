# Skill Library

Сгенерировано автоматически (2026-08-10T07:44:30+00:00) — не редактировать руками.
Изменить: положить/поправить Skill в `skills/`, задать category/origin через `skillctl.py`, запустить `skillctl.py library`.

## Как пользоваться

- **Ищу Skill для задачи** — смотрю раздел по направлению ниже, читаю description.
- **Нашла новый Skill** — прошу добавить в библиотеку с указанием источника.
- **Skill отмечен ⚠ NEEDS REVIEW** — значит содержимое изменилось после последней проверки, старая проверка на него больше не распространяется.
- **Status `DRAFT`** — Skill в библиотеке, но ещё не проверен на реальных задачах. Можно использовать осторожно.
- **Нужен Skill, которого нет** — пока пишется вручную, как обычный SKILL.md, и добавляется тем же способом, что и остальные.

## CORE

### capability-creation-methodology
Использовать, когда Idea Calibration (Шаг 0) сработал и триггер — предложение нового агента/проекта, требующего экспертизы в целой незнакомой профессиональной области. Специализация Шага 2 (World Research) idea-calibration для случая целой профессии, не инструмента.

- источник: AI_OS (Мария) (own)
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

## DESIGN

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

### systematic-debugging
Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes

- источник: obra/superpowers (github, MIT license по репозиторию) (adapted)
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

### internal-comms
A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).

- источник: anthropics/skills (github, официальный репозиторий Anthropic) (adapted)
- статус: `DRAFT`
- использований: 0
