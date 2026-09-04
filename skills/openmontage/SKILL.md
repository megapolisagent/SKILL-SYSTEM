---
name: openmontage
description: Full video-production pipeline agent — researches a brief, builds concept/script, plans scenes, sources/generates assets, edits timeline, renders final video. Reference only, not a lightweight Agent Skill.
---

> Перенесено 2026-09-04 (владелец → ENGINEER) из `calesthio/OpenMontage` (GitHub, MIT license).
> Честно: это не один установимый SKILL.md — это целый продукт (Backlot-сториборд, десятки
> внутренних markdown-справок в `skills/{core,creative,meta,pipelines}/`, requirements.txt на
> GPU-стек). Полный обзорный README сохранён как справка в `references/README-original.md`.
> Не подключён ни одному агенту — паркуется до появления видео-агента, которому реально нужен
> полный пайплайн, не только рендер (для рендера — см. `hyperframes`).

# OpenMontage — обзор возможностей

Превращает бриф (текст, YouTube-ссылка, Short/Reel/TikTok, локальный клип) в готовое видео:
ресерч → концепция/сценарий → планирование сцен → подбор/генерация ассетов → монтаж таймлайна →
рендер. Backlot показывает производство как живой сториборд (сценарий, сцены, ассеты, решения
по провайдерам, расходы). Полный текст оригинального README — `references/README-original.md`.
