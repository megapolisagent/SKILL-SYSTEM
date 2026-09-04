---
name: oh-my-openagent
description: Reference note only — this is a full CLI/harness overlay (`bunx oh-my-openagent install`), not an installable Agent Skill. Reconfigures the whole Codex/OpenCode CLI (models per role, discipline agents, LSP/ast-grep tools, tmux team mode).
---

> Перенесено 2026-09-04 (владелец → ENGINEER) из `code-yeongyu/oh-my-openagent` (GitHub) —
> **честно, не как рабочий Skill**: проверка репозитория показала, что папка `.agents/skills/`
> внутри него — это внутренние skills для обслуживания самого проекта (`publish`,
> `work-with-pr`, `tech-debt-audit`, `github-triage`) — не то, что методичка описывает
> (дисциплинарные агенты Sisyphus/Hephaestus/Prometheus, Team Mode, LSP/ast-grep). Эта
> функциональность реализована как отдельный CLI-инструмент, ставится целиком через
> `bunx oh-my-openagent install` и переконфигурирует весь харнесс — не Skill в формате
> Agent Skills. Кодекс (аудит 15 скиллов) уже отметил риск vendor lock-in при 40 агентах на
> разных рантаймах. Оставлен здесь как справочная запись-указатель на инструмент, не как
> установимый скилл — не подключать через `installer` без отдельного решения владельца.

# oh-my-openagent — что это реально

Плагин-надстройка над агентными харнессами (OpenCode, Codex CLI). Идеи, которые могут быть
адаптированы отдельно, без установки всего инструмента: discipline-режимы (агент не
останавливается до конца задачи), LSP-интеграция (rename/diagnostics/goto вместо угадывания по
тексту), ast-grep (поиск/замена по AST). Источник:
https://github.com/code-yeongyu/oh-my-openagent
