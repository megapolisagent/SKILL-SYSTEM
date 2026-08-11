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
  Explorer          — `explorer`: генерирует explorer.html — один статический файл,
                       открывается в браузере (file://), без сервера. Основной интерфейс
                       для человека: поиск, фильтр по category/статусу, карточки, деталь по клику.
  Library           — `library`: генерирует LIBRARY.md — текстовый/машиночитаемый
                       спутник каталога (для агентов и grep). registry.json/evidence.json —
                       внутренние механизмы под капотом, не для прямого чтения человеком.

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


def undeprecate(name, reason):
    """Вернуть Skill из DEPRECATED — например, когда отложенный ('архивный') Skill снова понадобился.
    Не перезаписывает историю: причина возврата добавляется отдельной пометкой, старая причина ухода не стирается."""
    data = load_evidence(name)
    if not data.get("deprecated"):
        print(f"[warn] {name}: не был DEPRECATED, ничего не делаю")
        return
    data["deprecated"] = False
    data.setdefault("reactivations", []).append({
        "date": now(), "reason": reason, "was_deprecated_reason": data.get("deprecated_reason"),
    })
    save_evidence(name, data)
    print(f"[ok] {name}: возвращён из DEPRECATED (статус пересчитается из evidence, см. status)")


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


def status_bucket(status: str) -> str:
    """Статус без скобок-уточнений — для фильтрации по крупной категории."""
    return status.split(" (")[0]


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


# ---------- Explorer (визуальный интерфейс — основной для человека) ----------

# Заголовки в теле SKILL.md, по которым механически (без анализа смысла)
# вытаскивается контекст для карточки. Если такого заголовка в конкретном
# Skill нет — соответствующее поле остаётся пустым, ничего не придумываем.
_HIGHLIGHT_HEADINGS = {
    "when": ["когда использовать", "когда нанимают", "когда нельзя",
             "use when", "when to use", "when to apply", "when should"],
    "what": ["purpose", "назначение", "overview", "что делает"],
    "output": ["output", "result", "результат", "deliverable",
               "что на выходе", "выходные данные"],
}


def _trim(text: str, limit: int = 420) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text.rfind(". ", 0, limit)
    if cut < limit * 0.4:
        cut = limit
    return text[:cut + 1].strip() + "…"


def extract_highlights(body: str) -> dict:
    """Ищет в теле SKILL.md разделы с заголовками из _HIGHLIGHT_HEADINGS.
    Механическое совпадение по заголовку, не суммаризация и не анализ смысла —
    если заголовка нет, соответствующее поле остаётся None. Строки внутри
    ```code``` игнорируются при поиске заголовков — иначе `# комментарий`
    в примере кода ошибочно читается как markdown-заголовок."""
    sections = []
    heading, buf, in_fence = None, [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            if heading is not None:
                buf.append(line)
            continue
        if not in_fence:
            m = re.match(r"^#{1,6}\s+(.*)$", line)
            if m:
                if heading is not None:
                    sections.append((heading, buf))
                heading, buf = m.group(1).strip(), []
                continue
        if heading is not None:
            buf.append(line)
    if heading is not None:
        sections.append((heading, buf))

    result = {"when": None, "what": None, "output": None}
    for heading, buf in sections:
        h_low = heading.lower()
        text = re.sub(r"```.*?```", "", "\n".join(buf), flags=re.DOTALL)
        text = re.sub(r"(?m)^\s*---\s*$", "", text).strip()
        if not text:
            continue
        for bucket, keywords in _HIGHLIGHT_HEADINGS.items():
            if result[bucket] is None and any(kw in h_low for kw in keywords):
                result[bucket] = _trim(text)
    return result


def list_skill_files(name: str):
    """Все настоящие файлы Skill'а (пути от корня репозитория), SKILL.md первым,
    evidence.json скрыт — это внутренние данные, не часть самого Skill."""
    d = skill_dir(name)
    if not d.exists():
        return []
    files = [p for p in sorted(d.rglob("*")) if p.is_file() and p.name != "evidence.json"]
    rels = [str(p.relative_to(ROOT)).replace("\\", "/") for p in files]
    skill_md_rel = f"skills/{name}/SKILL.md"
    rest = sorted(r for r in rels if r != skill_md_rel)
    return ([skill_md_rel] if skill_md_rel in rels else []) + rest


def collect_full():
    """Как collect_rows(), но с полным evidence — для Explorer/детального просмотра."""
    rows = []
    if not SKILLS_DIR.exists():
        return rows
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        ok, errors = validate(name, quiet=True)
        data = load_evidence(name)
        fm, body = {}, ""
        if skill_md_path(name).exists():
            fm, body = parse_frontmatter(skill_md_path(name))
        status = compute_status(name) if ok else "INVALID"
        rows.append({
            "name": name,
            "valid": ok,
            "errors": errors,
            "status": status,
            "statusBucket": status_bucket(status),
            "category": data.get("category") or "БЕЗ КАТЕГОРИИ",
            "origin": data.get("origin"),
            "description": fm.get("description", ""),
            "highlights": extract_highlights(body),
            "hasComparison": (skill_dir(name) / "comparison.md").exists(),
            "files": list_skill_files(name),
            "reactivations": data.get("reactivations", []),
            "evaluations": data["evaluations"],
            "usage": data["usage"],
            "review": data["review"],
            "deprecated": data["deprecated"],
            "deprecatedReason": data.get("deprecated_reason"),
        })
    return rows


EXPLORER_TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Skill System</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {
    --bg: #f7f7f5; --panel: #ffffff; --text: #1c1c1a; --muted: #6b6b66;
    --border: #e3e2dd; --accent: #2f5fa8; --accent-soft: #eef2fb;
    --draft: #8a8a85; --evaluated: #2f6fb8; --verified: #1f8f5b; --live: #0f9e5e;
    --review: #c17a12; --deprecated: #a33a3a; --invalid: #a33a3a;
    --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#15161a; --panel:#1e2024; --text:#eceae4; --muted:#9a9a94; --border:#31333a; --accent-soft:#1b2534;
      --draft:#8f8f8a; --evaluated:#4d84d6; --verified:#33ab74; --live:#22c07e; --review:#dd9a35; --deprecated:#d16060; }
  }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font:15px/1.6 var(--sans); -webkit-font-smoothing:antialiased; }
  header { position:sticky; top:0; background:var(--bg); padding:20px 24px 0; border-bottom:1px solid var(--border); z-index:10; }
  h1 { font-size:21px; margin:0 0 8px; font-weight:700; letter-spacing:-.01em; }
  .statbar { display:flex; flex-wrap:wrap; gap:6px 16px; align-items:baseline; margin-bottom:12px; font-size:13px; color:var(--muted); }
  .statbar b { color:var(--text); font-weight:600; }
  .statbar .stat-dot { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:5px; vertical-align:middle; }
  .sub { color:var(--muted); font-size:12px; margin-bottom:14px; }
  nav.tabs { display:flex; gap:4px; }
  nav.tabs button { border:none; background:none; padding:10px 14px; font-size:14px; color:var(--muted);
    cursor:pointer; border-bottom:2px solid transparent; font-family:var(--sans); }
  nav.tabs button.active { color:var(--text); border-bottom-color:var(--accent); font-weight:600; }
  .toolbar { display:none; padding:14px 0 12px; }
  .toolbar.show { display:flex; align-items:center; gap:14px; }
  #search { flex:1; max-width:460px; padding:9px 12px; border:1px solid var(--border); border-radius:8px;
            background:var(--panel); color:var(--text); font-size:14px; font-family:var(--sans); }
  #search:focus { outline:2px solid var(--accent); outline-offset:1px; }
  .kbd { font-family:var(--mono); font-size:11px; border:1px solid var(--border); border-radius:4px; padding:0 5px;
         color:var(--muted); margin-left:6px; }
  .toolbar-count { color:var(--muted); font-size:12.5px; white-space:nowrap; }
  .chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:10px; }
  .chip { padding:5px 11px; border-radius:999px; border:1px solid var(--border); background:var(--panel);
          color:var(--text); font-size:12.5px; cursor:pointer; user-select:none; }
  .chip.active { background:var(--accent); border-color:var(--accent); color:#fff; }
  main { padding:20px 24px 60px; max-width:1180px; margin:0 auto; }
  .view { display:none; }
  .view.show { display:block; }
  .count { color:var(--muted); font-size:13px; margin:4px 0 16px; }
  .banner { display:none; align-items:center; justify-content:space-between; gap:14px; background:var(--accent-soft);
            border:1px solid var(--review); border-left:3px solid var(--review); border-radius:10px;
            padding:12px 16px; margin:16px 0; font-size:13.5px; }
  .banner.show { display:flex; }
  .banner button { border:none; background:var(--review); color:#fff; padding:7px 13px; border-radius:7px;
                   font-size:12.5px; cursor:pointer; font-family:var(--sans); white-space:nowrap; }
  .layout { display:flex; align-items:flex-start; gap:26px; }
  .sidebar { flex:0 0 216px; position:sticky; top:132px; display:flex; flex-direction:column; gap:20px; }
  .sidebar-title { font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:0 0 8px; }
  .sidebar-list { display:flex; flex-direction:column; gap:2px; }
  .sidebar-row { display:flex; align-items:center; gap:8px; padding:6px 8px; border-radius:7px; cursor:pointer;
                 font-size:13px; border-left:3px solid transparent; user-select:none; }
  .sidebar-row:hover { background:var(--accent-soft); }
  .sidebar-row.active { background:var(--accent-soft); border-left-color:var(--accent); font-weight:600; }
  .sidebar-row .dot { width:8px; height:8px; border-radius:50%; flex:none; }
  .sidebar-row .lbl { flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .sidebar-row .cnt { color:var(--muted); font-size:12px; }
  .sidebar-reset { font-size:12px; color:var(--accent); cursor:pointer; background:none; border:none; padding:2px 8px;
                   text-align:left; font-family:var(--sans); }
  .content { flex:1; min-width:0; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:12px; }
  .card { background:var(--panel); border:1px solid var(--border); border-radius:10px;
          padding:14px 14px 12px; cursor:pointer; transition:border-color .12s ease, box-shadow .12s ease; position:relative; }
  .card:hover { box-shadow:0 2px 10px rgba(0,0,0,.06); }
  .card .top { display:flex; align-items:flex-start; justify-content:space-between; gap:8px; margin-bottom:6px; }
  .card h3 { margin:0; font-size:15px; font-weight:650; }
  .card .stateIcon { font-size:14px; flex:none; }
  .card p { margin:0 0 10px; color:var(--text); font-size:13px; display:-webkit-box;
            -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }
  .card .meta { font-size:11.5px; color:var(--muted); border-top:1px solid var(--border); margin-top:8px; padding-top:8px;
                display:flex; flex-wrap:wrap; gap:4px 10px; }
  .evline { font-size:11.5px; color:var(--muted); margin:2px 0 8px; font-family:var(--mono); }
  .row { display:flex; gap:6px; flex-wrap:wrap; align-items:center; }
  .badge { font-size:11px; padding:2px 8px; border-radius:999px; border:1px solid var(--border); color:var(--muted); }
  .status { font-size:11px; padding:2px 8px; border-radius:999px; color:#fff; font-family:var(--mono); }
  .st-DRAFT{background:var(--draft)} .st-EVALUATED{background:var(--evaluated)}
  .st-VERIFIED{background:var(--verified)} .st-LIVE{background:var(--live)}
  .st-NEEDS{background:var(--review)} .st-DEPRECATED{background:var(--deprecated)} .st-INVALID{background:var(--invalid)}
  @media (max-width: 780px) {
    .layout { flex-direction:column; }
    .sidebar { position:static; width:100%; flex-direction:row; flex-wrap:wrap; gap:14px; }
    .sidebar-list { flex-direction:row; flex-wrap:wrap; }
    .sidebar-row { border-left:none; border-bottom:2px solid transparent; }
    .sidebar-row.active { border-left:none; border-bottom-color:var(--accent); }
  }
  @media (max-width: 640px) {
    header { padding:14px 16px 0; }
    main { padding:16px 16px 60px; }
    h1 { font-size:18px; }
    nav.tabs button { padding:9px 8px; font-size:13px; }
    .grid { grid-template-columns:1fr; }
    #detail { width:100vw; }
    .statbar { font-size:12px; gap:5px 10px; }
    .toolbar.show { flex-wrap:wrap; }
  }
  #overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,.45); z-index:20; }
  #detail { position:fixed; right:0; top:0; bottom:0; width:min(480px,92vw); background:var(--panel);
            border-left:1px solid var(--border); z-index:21; padding:22px; overflow-y:auto; transform:translateX(100%);
            transition:transform .18s ease; }
  #detail.open { transform:translateX(0); }
  #overlay.open { display:block; }
  #detail h2 { margin-top:0; margin-bottom:8px; }
  .detailWhat { font-size:14.5px; line-height:1.55; margin-bottom:14px; }
  .highlights { display:flex; flex-direction:column; gap:8px; margin:0 0 16px; padding:12px 14px; background:var(--accent-soft);
                border-radius:8px; font-size:13px; line-height:1.5; }
  .highlights .hl b { color:var(--text); }
  .techDetails { margin-top:18px; border-top:1px solid var(--border); padding-top:6px; }
  .techDetails summary { cursor:pointer; font-size:12px; color:var(--accent); padding:6px 0; user-select:none; }
  .techDetails[open] summary { margin-bottom:4px; }
  .openbtn { display:inline-block; padding:8px 14px; border-radius:8px; background:var(--accent);
             color:#fff; text-decoration:none; font-size:13.5px; font-weight:600; }
  .openbtn:hover { opacity:.9; }
  .statusLine { display:flex; align-items:center; gap:8px; margin-top:14px; font-size:12px; color:var(--muted); }
  .moreTitle { font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted);
               margin:22px 0 4px; padding-top:14px; border-top:1px solid var(--border); }
  .filelist { margin:2px 0 0; padding-left:0; list-style:none; font-family:var(--mono); font-size:12px; }
  .filelist li { margin:2px 0; }
  .filelist a { color:var(--accent); text-decoration:none; }
  .filelist a:hover { text-decoration:underline; }
  #detail .close { float:right; cursor:pointer; color:var(--muted); font-size:20px; }
  #detail dt { color:var(--muted); font-size:12px; margin-top:12px; }
  #detail dd { margin:2px 0 0; }
  #detail table { width:100%; border-collapse:collapse; font-size:13px; margin-top:6px; }
  #detail td, #detail th { border-top:1px solid var(--border); padding:5px 4px; text-align:left; vertical-align:top; }
  section.cat { margin-top:26px; }
  section.cat h2 { font-size:14px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); margin:0 0 10px; }
  .empty { color:var(--muted); padding:40px 0; text-align:center; }
  .about { line-height:1.65; }
  .about h2 { font-size:16px; margin:28px 0 8px; }
  .about h2:first-child { margin-top:0; }
  .about code, .about pre { background:var(--panel); border:1px solid var(--border); border-radius:6px; }
  .about pre { padding:12px; overflow-x:auto; font-size:13px; }
  .about code { padding:1px 5px; font-size:13px; }
  .zone { border:1px solid var(--border); border-radius:8px; padding:10px 14px; margin:8px 0; background:var(--panel); }
  .zone b { display:block; margin-bottom:2px; }
  .catlist { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
</style>
</head>
<body>
<header>
  <h1>Skill System</h1>
  <div class="statbar" id="statbar"></div>
  <div class="sub">__GENERATED__ · не редактировать этот файл — он сгенерирован из skills/</div>
  <nav class="tabs">
    <button data-tab="about" class="active">🏠 Как всё устроено</button>
    <button data-tab="library">📚 Библиотека</button>
    <button data-tab="archive">📦 Архив</button>
  </nav>
  <div class="toolbar" id="toolbar">
    <input id="search" placeholder="Искать по имени или описанию… ( / )">
    <span class="toolbar-count" id="toolbarCount"></span>
  </div>
</header>
<main>
  <div class="banner" id="banner">
    <span id="bannerText"></span>
    <button onclick="showReview()">показать →</button>
  </div>
  <section id="view-about" class="view show about">
    <h2>Что это</h2>
    <p>Библиотека профессиональных Skills — не папка случайных файлов, а система, которая помнит: что есть, для чего, откуда взято, что реально проверено, а что отправлено в архив.</p>

    <h2>Как устроена</h2>
    <pre>Новый Skill
     │
     ▼
Исследование ─── что делает, откуда, какие есть альтернативы в мире
     │
     ▼
Сравнение с тем, что уже в библиотеке
     │
     ▼
        Решение владельца библиотеки
        /                          \\
   не нужен сейчас              нужен
        │                          │
        ▼                          ▼
    📦 Archive                📚 Active Library
   (не удалён,                     │
    можно вернуть)                 ▼
                          используется, следим за изменениями
                                    │
                                    ▼
                     изменился/устарел → пересмотр</pre>

    <h2>Три роли — не смешиваются</h2>
    <div class="zone"><b>Исследователь</b> — изучает мир, сравнивает найденный Skill с тем, что уже есть, и с альтернативами снаружи, приносит факты. Не решает и не кладёт Skill в библиотеку сам.</div>
    <div class="zone"><b>Skill System</b> (то, что перед вами) — хранит библиотеку, проверяет структуру каждого Skill, следит за изменениями, показывает, что есть.</div>
    <div class="zone"><b>Будущие агенты</b> — берут готовые Skills из библиотеки. Пока не построены — отдельный, следующий этап.</div>

    <h2>Что такое Skill у нас</h2>
    <p>Стандартный формат <code>SKILL.md</code> (папка + YAML frontmatter <code>name</code>/<code>description</code> + markdown-тело, опционально <code>scripts/</code>, <code>references/</code>, <code>assets/</code>) — открытый стандарт, тот же, что использует Anthropic, Cursor, Google и другие. Свой формат не изобретаем — совместимость важнее.</p>

    <h2>Направления</h2>
    <div class="catlist" id="aboutCats"></div>

    <h2>Что дальше почитать</h2>
    <p><a href="https://github.com/megapolisagent/SKILL-SYSTEM/blob/main/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a> — как добавить и проверить Skill. <a href="https://github.com/megapolisagent/SKILL-SYSTEM/blob/main/SKILL-SYSTEM.md" target="_blank">SKILL-SYSTEM.md</a> — полная архитектура (evidence, статусы, зоны ответственности) для тех, кому нужны детали.</p>
  </section>

  <section id="view-library" class="view">
    <div class="layout">
      <aside class="sidebar" id="sidebar-library"></aside>
      <div class="content">
        <div class="count" id="count-library"></div>
        <div id="lib-library"></div>
      </div>
    </div>
  </section>

  <section id="view-archive" class="view">
    <div class="layout">
      <aside class="sidebar" id="sidebar-archive"></aside>
      <div class="content">
        <div class="count" id="count-archive"></div>
        <div id="lib-archive"></div>
      </div>
    </div>
  </section>
</main>
<div id="overlay" onclick="closeDetail()"></div>
<aside id="detail"></aside>
<script>
const SKILLS = __DATA__;
const ACTIVE = SKILLS.filter(s => s.statusBucket !== 'DEPRECATED');
const ARCHIVED = SKILLS.filter(s => s.statusBucket === 'DEPRECATED');

function originLabel(origin){
  if (!origin) return 'источник не указан';
  return origin.type === 'own' ? 'наш' : 'взят снаружи';
}

// Человеческая версия origin.note. Это НЕ анализ смысла — просто: если текст
// заметки не содержит признаков реальной зависимости (требует установки/доступа),
// считаем её служебной пометкой о переносе и показываем один стандартный текст;
// если признаки есть — показываем текст заметки как есть (не сокращаем факты).
function noteDisplay(origin){
  if (!origin || !origin.note) return null;
  const clean = origin.note.replace(/\\(см\\.[^)]*\\)/gi, '').replace(/\\s{2,}/g, ' ').trim();
  const isDependency = /завис|требует установ|требует доступ/i.test(clean);
  if (isDependency) return { label: 'Зависимости', text: clean };
  return { label: 'Примечание', text: 'Перенесён из существующего Skill без изменения основной логики.' };
}

function statusClass(bucket){
  if (bucket === 'VERIFIED · LIVE') return 'st-LIVE';
  if (bucket === 'VERIFIED') return 'st-VERIFIED';
  if (bucket === 'NEEDS REVIEW') return 'st-NEEDS';
  if (bucket === 'DEPRECATED') return 'st-DEPRECATED';
  if (bucket === 'INVALID') return 'st-INVALID';
  if (bucket === 'EVALUATED') return 'st-EVALUATED';
  return 'st-DRAFT';
}
function statusColorVar(bucket){
  const cls = statusClass(bucket).replace('st-', '');
  const map = {DRAFT:'--draft', EVALUATED:'--evaluated', VERIFIED:'--verified', LIVE:'--live', NEEDS:'--review', DEPRECATED:'--deprecated', INVALID:'--invalid'};
  return map[cls] || '--draft';
}

const CAT_META = {
  CORE:        { color:'#5b6b8c', icon:'🧩' },
  RESEARCH:    { color:'#1f8f8f', icon:'🔍' },
  WRITING:     { color:'#b8860f', icon:'✍️' },
  STRATEGY:    { color:'#7a4fb0', icon:'🎯' },
  ENGINEERING: { color:'#2f6fb8', icon:'🛠️' },
  DESIGN:      { color:'#c23b7a', icon:'🎨' },
};
function catMeta(c){ return CAT_META[c] || { color:'#8a8a85', icon:'📁' }; }

// Русские подписи интерфейса. Внутренние ключи (CORE, DRAFT, tested, …) не меняются —
// это данные и логика; переводится только то, что видит человек.
const RU_CAT = {
  CORE:'Базовые', RESEARCH:'Исследование', STRATEGY:'Стратегия',
  WRITING:'Письмо и контент', ENGINEERING:'Инженерия', DESIGN:'Дизайн',
};
function catLabel(c){ return RU_CAT[c] || c; }

const RU_STATUS = {
  DRAFT:'В библиотеке', EVALUATED:'Проверен', VERIFIED:'Подтверждён',
  'VERIFIED · LIVE':'Подтверждён · в использовании', 'NEEDS REVIEW':'Требует пересмотра',
  DEPRECATED:'В архиве', INVALID:'Ошибка структуры',
};
const RU_STATUS_ICON = {
  DRAFT:'⚪', EVALUATED:'🟢', VERIFIED:'✅', 'VERIFIED · LIVE':'✅',
  'NEEDS REVIEW':'⚠️', DEPRECATED:'📦', INVALID:'⛔',
};
const RU_STATUS_EXPLAIN = {
  DRAFT: 'Добавлен в библиотеку, отдельной проверки в нашей работе пока не было.',
  EVALUATED: 'Прошёл проверку на задаче, но пока без итогового одобрения человека.',
  VERIFIED: 'Проверка пройдена и одобрена человеком.',
  'VERIFIED · LIVE': 'Одобрен и реально используется.',
  'NEEDS REVIEW': 'Изменился после проверки или пересмотр запрошен явно — прежняя проверка больше не считается действующей.',
  DEPRECATED: 'Признан не нужным сейчас. Не удалён — может быть возвращён.',
  INVALID: 'Не проходит структурную проверку — см. ошибки ниже.',
};
function statusLabel(bucket){ return RU_STATUS[bucket] || bucket; }
function statusDisplay(fullStatus, bucket){
  const detail = fullStatus.includes('(') ? ' ' + fullStatus.slice(fullStatus.indexOf('(')).replace('Evaluation', 'проверки') : '';
  const icon = RU_STATUS_ICON[bucket] ? RU_STATUS_ICON[bucket] + ' ' : '';
  return icon + statusLabel(bucket) + detail;
}

const RU_MODE = { tested:'тест', observed:'наблюдение' };
const RU_DECISION = { approved:'одобрено', rejected:'отклонено', pending:'в ожидании' };
const RU_PROVENANCE = { measured:'измерено', inferred:'предположительно' };

let currentTab = 'about';
let activeCats = new Set();
let activeStatuses = new Set();

function uniq(arr){ return [...new Set(arr)].sort(); }

// ---- URL state (hash-based: tab, search, category/status filters) ----
function readState(){
  const p = new URLSearchParams(location.hash.slice(1));
  currentTab = p.get('tab') || 'about';
  activeCats = new Set((p.get('cat') || '').split(',').filter(Boolean));
  activeStatuses = new Set((p.get('status') || '').split(',').filter(Boolean));
  return p.get('q') || '';
}
function writeState(){
  const p = new URLSearchParams();
  if (currentTab !== 'about') p.set('tab', currentTab);
  const q = (document.getElementById('search').value || '').trim();
  if (q) p.set('q', q);
  if (activeCats.size) p.set('cat', [...activeCats].join(','));
  if (activeStatuses.size) p.set('status', [...activeStatuses].join(','));
  const s = p.toString();
  history.replaceState(null, '', s ? '#' + s : location.pathname + location.search);
}

function switchTab(tab){
  currentTab = tab;
  document.querySelectorAll('nav.tabs button').forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
  document.querySelectorAll('.view').forEach(v => v.classList.toggle('show', v.id === 'view-' + tab));
  document.getElementById('toolbar').classList.toggle('show', tab === 'library' || tab === 'archive');
  if (tab === 'library' || tab === 'archive') { render(); }
  writeState();
}
document.querySelectorAll('nav.tabs button').forEach(b => b.onclick = () => switchTab(b.dataset.tab));

function poolFor(tab){ return tab === 'archive' ? ARCHIVED : ACTIVE; }

function renderStatbar(){
  const byStatus = {};
  ACTIVE.forEach(s => { byStatus[s.statusBucket] = (byStatus[s.statusBucket] || 0) + 1; });
  const order = ['VERIFIED · LIVE', 'VERIFIED', 'EVALUATED', 'NEEDS REVIEW', 'DRAFT'];
  const parts = [`<span><b>${SKILLS.length}</b> Skills</span>`, `<span><b>${uniq(ACTIVE.map(s=>s.category)).length}</b> направлений</span>`];
  order.filter(k => byStatus[k]).forEach(k => {
    parts.push(`<span><span class="stat-dot" style="background:var(${statusColorVar(k)})"></span><b>${byStatus[k]}</b> ${statusLabel(k)}</span>`);
  });
  parts.push(`<span>📦 <b>${ARCHIVED.length}</b> в архиве</span>`);
  document.getElementById('statbar').innerHTML = parts.join('');
}

function renderBanner(){
  const needsReview = ACTIVE.filter(s => s.statusBucket === 'NEEDS REVIEW');
  const banner = document.getElementById('banner');
  if (!needsReview.length) { banner.classList.remove('show'); return; }
  document.getElementById('bannerText').textContent =
    `⚠ Требует пересмотра: ${needsReview.length}. Содержимое изменилось после проверки или пересмотр запрошен явно — прежняя проверка на такой Skill больше не распространяется.`;
  banner.classList.add('show');
}
function showReview(){
  switchTab('library');
  activeStatuses = new Set(['NEEDS REVIEW']);
  render();
}

function toggleCat(c){
  activeCats.has(c) ? activeCats.delete(c) : activeCats.add(c);
  render();
}
function toggleStatus(s){
  activeStatuses.has(s) ? activeStatuses.delete(s) : activeStatuses.add(s);
  render();
}
function resetFilters(){
  activeCats = new Set(); activeStatuses = new Set();
  render();
}

function sidebarSection(title, rows){
  if (!rows.length) return '';
  return `<div><div class="sidebar-title">${title}</div><div class="sidebar-list">${rows.join('')}</div></div>`;
}

function buildSidebar(pool, targetId){
  const catCounts = {};
  pool.forEach(s => { catCounts[s.category] = (catCounts[s.category] || 0) + 1; });
  const catRows = Object.keys(catCounts).sort().map(c => `
    <div class="sidebar-row${activeCats.has(c)?' active':''}" onclick="toggleCat('${c}')">
      <span class="dot" style="background:${catMeta(c).color}"></span>
      <span class="lbl">${catMeta(c).icon} ${catLabel(c)}</span>
      <span class="cnt">${catCounts[c]}</span>
    </div>`);

  let statusRows = [];
  if (targetId !== 'sidebar-archive') {
    const stCounts = {};
    pool.forEach(s => { stCounts[s.statusBucket] = (stCounts[s.statusBucket] || 0) + 1; });
    const order = ['VERIFIED · LIVE', 'VERIFIED', 'EVALUATED', 'NEEDS REVIEW', 'DRAFT', 'INVALID'];
    statusRows = order.filter(s => stCounts[s]).map(s => `
      <div class="sidebar-row${activeStatuses.has(s)?' active':''}" onclick="toggleStatus('${s}')">
        <span class="dot" style="background:var(${statusColorVar(s)})"></span>
        <span class="lbl">${statusLabel(s)}</span>
        <span class="cnt">${stCounts[s]}</span>
      </div>`);
  }

  const resetBtn = (activeCats.size || activeStatuses.size)
    ? '<button class="sidebar-reset" onclick="resetFilters()">✕ сбросить фильтры</button>' : '';

  document.getElementById(targetId).innerHTML =
    sidebarSection('Направления', catRows) + sidebarSection('Статус', statusRows) + resetBtn;
}

function matches(s, q){
  if (activeCats.size && !activeCats.has(s.category)) return false;
  if (activeStatuses.size && !activeStatuses.has(s.statusBucket)) return false;
  if (q) {
    const hay = (s.name + ' ' + s.description).toLowerCase();
    if (!hay.includes(q)) return false;
  }
  return true;
}

function cardHtml(s){
  const meta = [
    statusLabel(s.statusBucket),
    originLabel(s.origin),
    `${s.evaluations.length} проверок · ${s.usage.count} использований`,
  ];
  if (s.hasComparison) meta.push('📄 сравнение');
  return `
    <div class="card" onclick="openDetail('${s.name}')">
      <div class="top">
        <h3>${s.name}</h3>
        <span class="stateIcon" title="${statusLabel(s.statusBucket)}">${RU_STATUS_ICON[s.statusBucket] || ''}</span>
      </div>
      <p>${(s.description || 'без description').replace(/</g,'&lt;')}</p>
      <div class="meta">${meta.map(m => `<span>${m}</span>`).join('')}</div>
    </div>`;
}

function render(){
  const q = document.getElementById('search').value.trim().toLowerCase();
  const pool = poolFor(currentTab);
  const shown = pool.filter(s => matches(s, q));
  const countEl = document.getElementById('count-' + currentTab);
  const libEl = document.getElementById('lib-' + currentTab);
  countEl.textContent = shown.length + ' из ' + pool.length;
  document.getElementById('toolbarCount').textContent = pool.length + ' Skills';
  buildSidebar(pool, 'sidebar-' + currentTab);
  writeState();
  if (!shown.length) {
    libEl.innerHTML = currentTab === 'archive'
      ? '<div class="empty">Архив пуст — сюда попадают Skills, которые изучены и признаны неактуальными сейчас, но не удаляются.</div>'
      : '<div class="empty">Ничего не найдено</div>';
    return;
  }
  const byCat = {};
  shown.forEach(s => { (byCat[s.category] = byCat[s.category] || []).push(s); });
  const cats = Object.keys(byCat).sort();
  libEl.innerHTML = cats.map(cat => `
    <section class="cat">
      <h2 style="border-left:3px solid ${catMeta(cat).color};padding-left:8px;">${catMeta(cat).icon} ${catLabel(cat)} (${byCat[cat].length})</h2>
      <div class="grid">${byCat[cat].map(cardHtml).join('')}</div>
    </section>`).join('');
}

function openDetail(name){
  const s = SKILLS.find(x => x.name === name);
  const d = document.getElementById('detail');
  const evalRows = s.evaluations.map(e =>
    `<tr><td>${e.date.slice(0,10)}</td><td>${RU_MODE[e.mode]||e.mode}</td><td>${RU_DECISION[e.decision]||e.decision}</td><td>${RU_PROVENANCE[e.provenance]||e.provenance}</td></tr>`
  ).join('') || '<tr><td colspan="4">пока не проверялся</td></tr>';
  const reactRows = (s.reactivations || []).map(r =>
    `<li>${r.date.slice(0,10)}: ${r.reason} (была причина ухода: ${r.was_deprecated_reason || '—'})</li>`
  ).join('');
  const files = s.files || [];
  const skillMdHref = files[0] || ('skills/' + s.name + '/SKILL.md');
  const restFiles = files.slice(1);
  const filesHtml = !restFiles.length ? '' :
    restFiles.length <= 8
      ? '<dt>Остальные файлы Skill</dt><dd><ul class="filelist">' +
        restFiles.map(f => `<li><a href="${f}" target="_blank">${f.slice(('skills/'+s.name+'/').length)}</a></li>`).join('') +
        '</ul></dd>'
      : `<dt>Остальные файлы Skill</dt><dd>${restFiles.length} файлов — <a href="skills/${s.name}/" target="_blank">открыть папку целиком</a></dd>`;
  const hl = s.highlights || {};
  const hlRows = [
    hl.when   ? ['Когда использовать', hl.when] : null,
    hl.what   ? ['Что делает (подробнее)', hl.what] : null,
    hl.output ? ['Результат', hl.output] : null,
  ].filter(Boolean);
  const highlightsHtml = hlRows.length ? '<div class="highlights">' + hlRows.map(([label, text]) =>
    `<div class="hl"><b>${label}:</b> ${text.replace(/</g,'&lt;')}</div>`
  ).join('') + '</div>' : '';
  const sourceShort = !s.origin ? 'не указан' : (s.origin.type === 'own' ? 'Наш Skill' : (s.origin.source || '').split(' (')[0]);
  const note = noteDisplay(s.origin);
  const noteRow = note ? `<dt>${note.label}</dt><dd>${note.text.replace(/</g,'&lt;')}</dd>` : '';
  const usageRow = s.usage.count > 0
    ? `<dt>Использование</dt><dd>${s.usage.count} вызовов${s.usage.last_used ? ', последний ' + s.usage.last_used.slice(0,10) : ''} (учтено в Skill System)</dd>`
    : '';
  d.innerHTML = `
    <span class="close" onclick="closeDetail()">&times;</span>
    <h2>${s.name}</h2>
    <div class="detailWhat">${(s.description || '—').replace(/</g,'&lt;')}</div>
    ${highlightsHtml}
    <a class="openbtn" href="${skillMdHref}" target="_blank">📄 Открыть Skill</a>
    <div class="statusLine">${RU_STATUS_ICON[s.statusBucket] || ''} ${statusDisplay(s.status, s.statusBucket)} — ${RU_STATUS_EXPLAIN[s.statusBucket] || ''}</div>
    <div class="moreTitle">Подробнее</div>
    <dl>
      <dt>Направление</dt><dd>${catMeta(s.category).icon} ${catLabel(s.category)}</dd>
      <dt>Источник</dt><dd>${sourceShort}</dd>
      ${noteRow}
      ${usageRow}
      ${s.hasComparison ? '<dt>Сравнение с альтернативами</dt><dd>см. <a href="skills/' + s.name + '/comparison.md" target="_blank">comparison.md</a></dd>' : ''}
      ${s.deprecated ? '<dt>Почему в архиве</dt><dd>' + (s.deprecatedReason || '') + '</dd>' : ''}
      ${!s.valid ? '<dt>Ошибки проверки</dt><dd>' + s.errors.join('; ') + '</dd>' : ''}
    </dl>
    <details class="techDetails">
      <summary>Технические сведения</summary>
      <dl>
        <dt>Путь у источника</dt><dd>${s.origin ? (s.origin.source_path || '—') : '—'}</dd>
        <dt>Источник (полностью)</dt><dd>${s.origin ? s.origin.source + ' (' + originLabel(s.origin) + ')' : 'не указан'}</dd>
        <dt>Примечание к происхождению (полный текст)</dt><dd>${s.origin ? (s.origin.note || '—') : '—'}</dd>
        ${filesHtml}
        ${reactRows ? '<dt>Возвращён из архива</dt><dd><ul style="margin:4px 0 0;padding-left:16px;">' + reactRows + '</ul></dd>' : ''}
      </dl>
      <dt style="color:var(--muted);font-size:12px;margin-top:14px;">История проверок</dt>
      <table><tr><th>дата</th><th>режим</th><th>решение</th><th>основание</th></tr>${evalRows}</table>
    </details>
  `;
  d.classList.add('open');
  document.getElementById('overlay').classList.add('open');
}
function closeDetail(){
  document.getElementById('detail').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
}

document.getElementById('search').addEventListener('input', render);

document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement !== document.getElementById('search')) {
    e.preventDefault();
    document.getElementById('search').focus();
  }
  if (e.key === 'Escape') { closeDetail(); }
});

// ---- init: restore state from URL, then render ----
function goToCategory(c){
  switchTab('library');
  activeCats = new Set([c]);
  render();
}

renderStatbar();
renderBanner();
document.getElementById('aboutCats').innerHTML = uniq(ACTIVE.map(s => s.category))
  .map(c => `<span class="chip" style="border-color:${catMeta(c).color}" onclick="goToCategory('${c}')">${catMeta(c).icon} ${catLabel(c)}</span>`).join('');

const initialQ = readState();
document.getElementById('search').value = initialQ;
switchTab(currentTab);
</script>
</body>
</html>
"""


def explorer():
    """Пишет index.html — так GitHub Pages отдаёт интерфейс прямо с корневого URL,
    без редиректа и без дублирования с explorer.html."""
    rows = collect_full()
    active_n = sum(1 for r in rows if r["statusBucket"] != "DEPRECATED")
    payload = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    html = (EXPLORER_TEMPLATE
            .replace("__DATA__", payload)
            .replace("__GENERATED__", now()))
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"[ok] index.html обновлён ({len(rows)} skills, {active_n} активных, {len(rows) - active_n} в архиве)")


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

    sp = sub.add_parser("undeprecate")
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
    sub.add_parser("explorer")

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
    elif args.cmd == "undeprecate":
        undeprecate(args.name, args.reason)
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
    elif args.cmd == "explorer":
        explorer()


if __name__ == "__main__":
    main()
