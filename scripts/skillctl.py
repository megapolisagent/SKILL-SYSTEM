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
        return json.loads(p.read_text(encoding="utf-8"))
    return {
        "skill": name,
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

def registry(write: bool = True):
    rows = []
    if not SKILLS_DIR.exists():
        print("[warn] skills/ ещё не существует")
        return []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        ok, _ = validate(name, quiet=True)
        data = load_evidence(name)
        rows.append({
            "name": name,
            "valid": ok,
            "status": compute_status(name) if ok else "INVALID",
            "evaluations": len(data["evaluations"]),
            "usage_count": data["usage"]["count"],
            "last_used": data["usage"]["last_used"],
            "deprecated": data["deprecated"],
        })
    if write:
        REGISTRY_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    width = max((len(r["name"]) for r in rows), default=4)
    print(f"{'skill'.ljust(width)}  status")
    print("-" * (width + 30))
    for r in rows:
        print(f"{r['name'].ljust(width)}  {r['status']}")
    return rows


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

    sub.add_parser("registry")

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
    elif args.cmd == "registry":
        registry()


if __name__ == "__main__":
    main()
