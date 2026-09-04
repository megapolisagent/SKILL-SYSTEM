---
name: tldraw-offline
description: Drive and script tldraw offline canvases with an agent — read open canvases, make edits, write document scripts (JS embedded in .tldraw files) for durable reactive shapes/buttons/animations.
license: MIT
---

> Перенесено 2026-09-04 (владелец → ENGINEER) из каталога Hermes Agent
> (https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-tldraw-offline)
> — не GitHub-репозиторий (страница не называет исходный код отдельно), содержимое взято
> дословно со страницы каталога через WebFetch, не сочинено. Автор: Teknium + Hermes Agent,
> MIT license.

# Tldraw Offline

Подключает агента к открытому локальному холсту tldraw через локальный HTTP API
(`localhost:7236`, `curl`-команды, без кликов мышью и без прямого редактирования файла).
Аутентификация — bearer-токен из `server.json`.

Два режима:
1. **Разовые правки** (`/exec`) — живые изменения холста (layout, генерация фигур).
2. **Долговечное поведение** (`script/main.js`) — персистентные скрипты, переживающие
   перезагрузку файла, через file-watcher.

Контракт скрипта документа:
```
export default function ({ editor, helpers, signal }) {
  editor.run(() => { /* batch changes */ })
  const stop = editor.store.listen(() => { /* react */ })
  signal.addEventListener('abort', () => stop())
}
```
`editor` — манипуляция фигурами, `helpers` — идемпотентное создание объектов, `signal` —
очистка при отмене.

Требования: tldraw offline установлен и запущен с открытым документом; Agent Skills
установлены через `Develop → Install Agent Skills`; порт/токен читаются из `server.json` при
каждом вызове; скрипты идемпотентны (стабильные ID фигур). Платформы: Linux/macOS/Windows.
