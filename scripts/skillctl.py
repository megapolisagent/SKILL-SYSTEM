#!/usr/bin/env python3
"""
skillctl.py — минимальный CLI для Skill System v0.

Реализует ответственности из SKILL-SYSTEM.md, ничего сверх них:
  Artifact          — не код; сам формат SKILL.md (папка + YAML frontmatter
                       name/description + markdown-тело), см. §3.
  Registry          — `registry`: сканирует skills/, пишет registry.json.
  Validation        — `validate <skill>`: структурная проверка SKILL.md.
  Evaluation        — `evaluate <skill>`: записывает событие оценки в evidence.json.
  Usage             — `record-usage <skill>`: фиксирует факт вызова.
  Review/Deprecate  — `request-review`, `deprecate`: ручные, человеком инициируемые события.
  Lifecycle/Status  — `status`/`registry`: статус ВСЕГДА вычисляется из evidence,
                       нигде не хранится и не выставляется вручную (§5).
  Классификация     — `set-category`, `set-origin`: минимальные поля, выведенные
                       из реального материала библиотеки, не придуманная заранее таксономия.
  Library           — `library`: генерирует LIBRARY.md — человеческий интерфейс
                       к библиотеке (не JSON и не CLI). Это конечная точка для человека;
                       registry.json/evidence.json — внутренние механизмы под капотом.

Явно НЕ реализовано (см. SKILL-SYSTEM.md §8): composition, usage-freshness
auto-trigger для Review (usage — только информационное поле, см. §7), dependency
management, marketplace, собственная БД, интеграция с Foundation.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REGISTRY_PATH = ROOT / "registry.json"

# Правило имени — из открытого стандарта SKILL.md (agentskills.io), не наше изобретение.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_frontmatter(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end]
    fm = {}
    for line in fm_block.splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm, text[end + 4:]


def skill_dir(name: str) -> Path:
    return SKILLS_DIR / name


def skill_md_path(name: str) -> Path:
    return skill_dir(name) / "SKILL.md"


def evidence_path(name: str) -> Path:
    return skill_dir(name) / "evidence.json"


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load_evidence(name: str) -> dict:
    p = evidence_path(name)
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
        data.setdefault("category", None)
        data.setdefault("origin", None)
        return data
    return {
        "skill": name,
        "category": None,
        "origin": None,   # {"source", "source_path", "type": "own"|"adapted", "note"}
        "evaluations": [],
        "usage": {"count": 0, "last_used": None, "log": []},
        "review": {"requested": False, "requested_date": None, "reason": None},
        "deprecated": False,
        "deprecated_reason": None,
    }


def save_evidence(name: str, data: dict) -> None:
    evidence_path(name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------- Validation ----------

def validate(name: str, quiet: bool = False):
    """Структурная проверка Artifact. Возвращает (ok, errors)."""
    errors = []
    if not skill_dir(name).exists():
        return False, [f"папка skills/{name}/ не существует"]
    md = skill_md_path(name)
    if not md.exists():
        return False, [f"skills/{name}/SKILL.md не существует"]
    fm, _ = parse_frontmatter(md)
    if "name" not in fm:
        errors.append("frontmatter: нет поля 'name'")
    else:
        if fm["name"] != name:
            errors.append(f"frontmatter name='{fm['name']}' не совпадает с именем папки '{name}'")
        if not NAME_RE.match(fm["name"]):
            errors.append(f"name '{fm['name']}' не соответствует формату a-z0-9- (SKILL.md spec)")
    if "description" not in fm or not fm["description"].strip():
        errors.append("frontmatter: нет непустого поля 'description'")
    ok = not errors
    if not quiet:
        if ok:
            print(f"[ok] {name}: валиден")
        else:
            print(f"[fail] {name}:")
            for e in errors:
                print(f"  - {e}")
    return ok, errors


# ---------- Evaluation ----------

def evaluate(name, mode, result, decision, test_cases, provenance):
    ok, errors = validate(name, quiet=True)
    if not ok:
        print(f"[stop] {name} не прошёл Validation — Evaluation не записана:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    data = load_evidence(name)
    entry = {
        "date": now(),
        "mode": mode,               # tested | observed
        "test_cases": test_cases,
        "result": result,
        "decision": decision,       # approved | rejected | pending — человеческое решение
        "provenance": provenance,   # measured | inferred
        "artifact_hash": content_hash(skill_md_path(name)),
    }
    data["evaluations"].append(entry)  # append-only, история не перезаписывается
    save_evidence(name, data)
    print(f"[ok] {name}: evaluation записана (mode={mode}, decision={decision})")
    print(f"     статус теперь: {compute_status(name)}")


# ---------- Usage ----------

def record_usage(name):
    data = load_evidence(name)
    ts = now()
    data["usage"]["count"] += 1
    data["usage"]["last_used"] = ts
    data["usage"]["log"].append(ts)
    save_evidence(name, data)
    print(f"[ok] {name}: usage записан ({data['usage']['count']} всего)")


# ---------- Category / Origin (минимальная классификация и происхождение) ----------

def set_category(name, category):
    data = load_evidence(name)
    data["category"] = category
    save_evidence(name, data)
    print(f"[ok] {name}: category = {category}")


def set_origin(name, source, source_path, otype, note):
    data = load_evidence(name)
    data["origin"] = {
        "source": source,
        "source_path": source_path,
        "type": otype,       # own | adapted
        "note": note,
        "recorded": now(),
    }
    save_evidence(name, data)
    print(f"[ok] {name}: origin записан ({otype}, {source})")


# ---------- Review / Deprecate ----------

def request_review(name, reason):
    data = load_evidence(name)
    data["review"] = {"requested": True, "requested_date": now(), "reason": reason}
    save_evidence(name, data)
    print(f"[ok] {name}: review запрошен")


def deprecate(name, reason):
    data = load_evidence(name)
    data["deprecated"] = True
    data["deprecated_reason"] = reason
    data["deprecated_date"] = now()
    save_evidence(name, data)  # не удаляется, только помечается — SKILL-SYSTEM.md §5
    print(f"[ok] {name}: помечен DEPRECATED (файлы и история сохранены)")


# ---------- Status (Lifecycle) — вычисляется, не хранится ----------

def compute_status(name: str) -> str:
    if not skill_md_path(name).exists():
        return "UNKNOWN"
    data = load_evidence(name)
    if data.get("deprecated"):
        return "DEPRECATED"
    evals = data["evaluations"]
    if not evals:
        return "DRAFT"
    latest_approved = next((e for e in reversed(evals) if e["decision"] == "approved"), None)
    if latest_approved is None:
        return "EVALUATED"
    current_hash = content_hash(skill_md_path(name))
    if current_hash != latest_approved["artifact_hash"]:
        return "NEEDS REVIEW (изменился после Evaluation)"
    if data["review"]["requested"]:
        return "NEEDS REVIEW (запрошен человеком)"
    if data["usage"]["count"] > 0:
        return "VERIFIED · LIVE"
    return "VERIFIED"
    # Примечание: usage=0 сознательно НЕ переводит в NEEDS REVIEW — правило
    # ещё не принято (SKILL-SYSTEM.md §7). usage виден в registry как поле,
    # не как триггер статуса.


# ---------- Registry ----------

def collect_rows():
    rows = []
    if not SKILLS_DIR.exists():
        return rows
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        ok, errors = validate(name, quiet=True)
        data = load_evidence(name)
        fm = {}
        if skill_md_path(name).exists():
            fm, _ = parse_frontmatter(skill_md_path(name))
        rows.append({
            "name": name,
            "valid": ok,
            "errors": errors,
            "status": compute_status(name) if ok else "INVALID",
            "category": data.get("category"),
            "origin": data.get("origin"),
            "description": fm.get("description", ""),
            "evaluations": len(data["evaluations"]),
            "usage_count": data["usage"]["count"],
            "last_used": data["usage"]["last_used"],
            "deprecated": data["deprecated"],
        })
    return rows


def registry(status_filter=None, category_filter=None, write: bool = True):
    rows = collect_rows()
    if write:
        REGISTRY_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    shown = rows
    if status_filter:
        shown = [r for r in shown if status_filter.lower() in r["status"].lower()]
    if category_filter:
        shown = [r for r in shown if (r["category"] or "").lower() == category_filter.lower()]
    width = max((len(r["name"]) for r in shown), default=4)
    print(f"{'skill'.ljust(width)}  {'category'.ljust(10)}  status")
    print("-" * (width + 40))
    for r in shown:
        print(f"{r['name'].ljust(width)}  {(r['category'] or '—').ljust(10)}  {r['status']}")
    return shown


# ---------- Library (человеко-читаемый каталог — основной интерфейс) ----------

def library():
    rows = collect_rows()
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"] or "БЕЗ КАТЕГОРИИ", []).append(r)

    lines = []
    lines.append("# Skill Library")
    lines.append("")
    lines.append(f"Сгенерировано автоматически ({now()}) — не редактировать руками.")
    lines.append("Изменить: положить/поправить Skill в `skills/`, задать category/origin через `skillctl.py`, запустить `skillctl.py library`.")
    lines.append("")
    lines.append("## Как пользоваться")
    lines.append("")
    lines.append("- **Ищу Skill для задачи** — смотрю раздел по направлению ниже, читаю description.")
    lines.append("- **Нашла новый Skill** — прошу добавить в библиотеку с указанием источника.")
    lines.append("- **Skill отмечен ⚠ NEEDS REVIEW** — значит содержимое изменилось после последней проверки, старая проверка на него больше не распространяется.")
    lines.append("- **Status `DRAFT`** — Skill в библиотеке, но ещё не проверен на реальных задачах. Можно использовать осторожно.")
    lines.append("- **Нужен Skill, которого нет** — пока пишется вручную, как обычный SKILL.md, и добавляется тем же способом, что и остальные.")
    lines.append("")

    for cat in sorted(by_cat):
        items = by_cat[cat]
        lines.append(f"## {cat}")
        lines.append("")
        for r in sorted(items, key=lambda x: x["name"]):
            flag = " ⚠" if "NEEDS REVIEW" in r["status"] else ""
            lines.append(f"### {r['name']}{flag}")
            if r["description"]:
                lines.append(f"{r['description']}")
            origin = r["origin"] or {}
            src = origin.get("source", "не указан")
            otype = origin.get("type", "?")
            lines.append("")
            lines.append(f"- источник: {src} ({otype})")
            lines.append(f"- статус: `{r['status']}`")
            lines.append(f"- использований: {r['usage_count']}" + (f", последний раз {r['last_used']}" if r["last_used"] else ""))
            if not r["valid"]:
                lines.append(f"- ⚠ не прошёл validation: {'; '.join(r['errors'])}")
            lines.append("")

    (ROOT / "LIBRARY.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[ok] LIBRARY.md обновлён ({len(rows)} skills, {len(by_cat)} категорий)")


# ---------- CLI ----------

def main():
    p = argparse.ArgumentParser(description="skillctl — минимальный CLI Skill System v0")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("validate"); sp.add_argument("name")

    sp = sub.add_parser("evaluate")
    sp.add_argument("name")
    sp.add_argument("--mode", choices=["tested", "observed"], required=True)
    sp.add_argument("--result", required=True)
    sp.add_argument("--decision", choices=["approved", "rejected", "pending"], required=True)
    sp.add_argument("--test-case", action="append", default=[], dest="test_cases")
    sp.add_argument("--provenance", choices=["measured", "inferred"], default="measured")

    sp = sub.add_parser("record-usage"); sp.add_argument("name")

    sp = sub.add_parser("request-review")
    sp.add_argument("name"); sp.add_argument("--reason", required=True)

    sp = sub.add_parser("deprecate")
    sp.add_argument("name"); sp.add_argument("--reason", required=True)

    sp = sub.add_parser("status"); sp.add_argument("name")

    sp = sub.add_parser("set-category")
    sp.add_argument("name"); sp.add_argument("category")

    sp = sub.add_parser("set-origin")
    sp.add_argument("name")
    sp.add_argument("--source", required=True)
    sp.add_argument("--source-path", default="")
    sp.add_argument("--type", choices=["own", "adapted"], required=True, dest="otype")
    sp.add_argument("--note", default="")

    sp = sub.add_parser("registry")
    sp.add_argument("--status", default=None)
    sp.add_argument("--category", default=None)

    sub.add_parser("library")

    args = p.parse_args()

    if args.cmd == "validate":
        validate(args.name)
    elif args.cmd == "evaluate":
        evaluate(args.name, args.mode, args.result, args.decision, args.test_cases, args.provenance)
    elif args.cmd == "record-usage":
        record_usage(args.name)
    elif args.cmd == "request-review":
        request_review(args.name, args.reason)
    elif args.cmd == "deprecate":
        deprecate(args.name, args.reason)
    elif args.cmd == "status":
        print(compute_status(args.name))
    elif args.cmd == "set-category":
        set_category(args.name, args.category)
    elif args.cmd == "set-origin":
        set_origin(args.name, args.source, args.source_path, args.otype, args.note)
    elif args.cmd == "registry":
        registry(status_filter=args.status, category_filter=args.category)
    elif args.cmd == "library":
        library()


if __name__ == "__main__":
    main()
