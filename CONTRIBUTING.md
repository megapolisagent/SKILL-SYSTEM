# Как пользоваться Skill System

Практическое руководство. «Почему так устроено» — в [`SKILL-SYSTEM.md`](SKILL-SYSTEM.md), здесь только «что делать».

## Формат Skill

Папка `skills/<имя>/`, обязателен `SKILL.md`:

```markdown
---
name: имя-совпадает-с-папкой
description: Что делает и когда использовать — по этому полю Skill находят.
---

Тело — обычный markdown, инструкция для агента.
```

`name` — строчные латинские буквы, цифры, дефис, без ведущего/двойного дефиса, обязано совпадать с именем папки. Опционально рядом: `scripts/`, `references/`, `assets/` — что реально нужно Skill'у для работы.

Свой формат не придумываем — это открытый стандарт (agentskills.io), тот же, что у Anthropic, Cursor, Google.

## Добавить новый Skill

```bash
# 1. Положить папку с SKILL.md в skills/<имя>/

# 2. Проверить структуру
python3 scripts/skillctl.py validate <имя>

# 3. Указать источник
python3 scripts/skillctl.py set-origin <имя> \
  --source "откуда взят (репозиторий/автор/AI_OS/и т.п.)" \
  --source-path "путь у источника, если применимо" \
  --type own|adapted \
  --note "зависимости, что изменено при переносе, что нужно знать"

# 4. Указать направление
python3 scripts/skillctl.py set-category <имя> CORE|RESEARCH|WRITING|STRATEGY|ENGINEERING|DESIGN

# 5. Пересобрать интерфейс
python3 scripts/skillctl.py explorer
python3 scripts/skillctl.py library
```

Список направлений не фиксирован — новое направление появляется, когда для него реально есть Skill, не заранее.

Если Skill взят из внешнего мира (не написан нами) и есть на рынке похожие решения — стоит сравнить его с альтернативами и сохранить результат в `skills/<имя>/comparison.md`. Формального шаблона нет, ориентир — уже существующий `skills/visual/comparison.md`.

## Проверить (Evaluation)

Структурная проверка (`validate`) — не то же самое, что «Skill реально полезен». Чтобы записать проверку на реальной задаче:

```bash
python3 scripts/skillctl.py evaluate <имя> \
  --mode tested|observed \
  --result "что получилось, с чем сравнивали" \
  --decision approved|rejected|pending \
  --provenance measured|inferred \
  --test-case "описание тест-кейса"   # можно несколько раз
```

`tested` — спланированный прогон/сравнение. `observed` — заранее заявленный критерий, который подтверждается или опровергается реальным будущим использованием, не постановочным тестом. `decision: approved` — единственный способ продвинуть Skill дальше `EVALUATED`, и это всегда решение человека, не системы. Не фабриковать Evaluation ради красивого статуса — статус `DRAFT` для непроверенного Skill честнее.

## Статус

Вычисляется всегда заново из `evidence.json`, не хранится и не редактируется вручную:

```text
DRAFT → EVALUATED → VERIFIED → VERIFIED·LIVE → NEEDS REVIEW → VERIFIED·LIVE / DEPRECATED
```

```bash
python3 scripts/skillctl.py status <имя>
```

## Usage (реальное использование)

```bash
python3 scripts/skillctl.py record-usage <имя>
```

Не доказательство качества — это evidence актуальности, отдельно от Evaluation.

## Review / Архив

```bash
python3 scripts/skillctl.py request-review <имя> --reason "почему пересматриваем"
python3 scripts/skillctl.py deprecate <имя> --reason "почему не нужен сейчас"
python3 scripts/skillctl.py undeprecate <имя> --reason "почему снова понадобился"
```

`deprecate` не удаляет файлы и историю — Skill просто перестаёт быть «активным», в интерфейсе показывается как «Архив». Обратимо в любой момент.

## Обновить интерфейс

```bash
python3 scripts/skillctl.py explorer   # index.html — основной интерфейс (и локально, и на GitHub Pages)
python3 scripts/skillctl.py library    # LIBRARY.md — текстовый спутник
python3 scripts/skillctl.py registry   # таблица в терминал + registry.json
```

Все три — генерируются из `skills/`, не редактируются руками. Запускать после любого изменения библиотеки.

## Commit

Обычный git — история хранится как есть, ничего специального не изобретаем:

```bash
git add -A
git commit -m "что изменилось и почему"
git push
```

## Требования

Python 3.8+, ничего кроме стандартной библиотеки — `skillctl.py` не тянет никаких зависимостей.
