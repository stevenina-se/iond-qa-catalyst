#!/usr/bin/env python3
"""E2E maestro de IOND: importación con IDs estables, cobertura y selección de suites.

Fuente editable: hoja "Iond Testing Plan" (exportada a CSV en resources/).
Configuración:   knowledge/test-suites/_config/{modules,rules,subcategory-map}.csv
Salida:          knowledge/test-suites/e2e-master.csv (no se edita a mano)

Uso (desde la raíz del repo, siempre con `python -I`):
  python -I scripts/e2e_master.py import
  python -I scripts/e2e_master.py export-sheet
  python -I scripts/e2e_master.py coverage
  python -I scripts/e2e_master.py select --layer 1 --subcategories "Boards,App Connectors" --risk Medio
  python -I scripts/e2e_master.py select --layer 2 --group G2 --exclude knowledge/releases/iond/v0.3.0/regression-matrix.csv

Solo usa la biblioteca estándar. No modifica bot-test: genera los comandos para ejecutarlo.
"""
import argparse
import csv
import difflib
import fnmatch
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUITES = os.path.join(ROOT, "knowledge", "test-suites")
CONFIG = os.path.join(SUITES, "_config")
DEFAULT_SHEET = os.path.join(ROOT, "resources", "Iond Testing Plan - Iond Automation Plan.csv")
DEFAULT_MASTER = os.path.join(SUITES, "e2e-master.csv")

SIDE_CODES = {"KC": "KC", "ADMIN": "ADM", "TENANT": "TEN", "ADMIN GATEWAY": "GTW"}
RUNNABLE = {"Ejecutable", "En PR"}
GROUPS = ["G1", "G2", "G3", "G4"]
BOT_TEST_BASE = "tests/IONFLOW/"
BOT_TEST_CONFIG = "tests/IONFLOW/playwright.ionflow.config.ts"

MASTER_COLS = [
    "ID", "SIDE", "MODULE", "FEATURE", "CASO", "PATH", "TEST_CASES", "PRIORITY",
    "STATUS_HOJA", "ASSIGNED", "BASELINE", "ROTACION", "PROD_SAFE", "CROSS_SYSTEM",
    "AUTOMATIZACION", "NOTA_AUTOMATIZACION", "BOT_TEST_SPEC", "BOT_TEST_TC",
    "TICKET_AUTOMATIZACION", "L2_MODULE", "IOND_SUBCATEGORY", "ESTADO_FILA", "OBSERVATION",
]
RULE_COLS = [
    "BASELINE", "PROD_SAFE", "CROSS_SYSTEM", "L2_MODULE", "BOT_TEST_SPEC", "BOT_TEST_TC",
    "AUTOMATIZACION", "NOTA_AUTOMATIZACION", "TICKET_AUTOMATIZACION",
]
# Columnas de ejecución de las matrices del release (sanity, smoke y regresión capa 1)
EXEC_COLS = ["ID", "PRIORIDAD", "SIDE", "MODULE", "FEATURE", "CASO", "RESULTADO ESPERADO", "QA ASIGNADO",
             "RESOLUCION", "OBSERVACION", "TICKET", "PRIORIDAD BUG"]
TIER_ORDER = {"urgent": 0, "high": 1, "normal": 2}
SHEET_STATUS_TO_AUTO = {"pending": "Pendiente", "manual for now": "Manual", "blocked": "Bloqueada"}


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, cols, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


# --------------------------------------------------------------------------- hoja

def parse_sheet(path):
    """Devuelve (filas_hoja, hojas). filas_hoja conserva el orden y los separadores."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        raw = list(csv.reader(fh))
    header = raw[0]
    upper = [h.strip().upper() for h in header]

    def col(name, default):
        return upper.index(name) if name in upper else default

    c_tc, c_asg, c_st, c_pr = col("TEST CASES", 6), col("ASSIGNED", 7), col("STATUS", 8), col("PRIORITY", 9)
    c_obs, c_ticket = col("OBSERVATION", 10), col("TICKET", 11)
    c_id = upper.index("ID") if "ID" in upper else None
    level_cols = list(range(1, c_tc))  # MODULE/FEATURE ocupa las columnas entre SIDE y TEST CASES

    side, levels = "", [""] * len(level_cols)
    rows, leaves = [], []
    for line_no, cells in enumerate(raw[1:], start=2):
        cells = cells + [""] * (len(header) - len(cells))
        if not any(c.strip() for c in cells):
            rows.append(None)
            continue
        if cells[0].strip():
            side = cells[0].strip()
            levels = [""] * len(level_cols)
        for i, c in enumerate(level_cols):
            if cells[c].strip():
                levels[i] = cells[c].strip()
                for j in range(i + 1, len(level_cols)):
                    levels[j] = ""
        status = cells[c_st].strip()
        if not status:
            rows.append(None)
            continue
        parts = [p for p in levels if p]
        leaf = {
            "line": line_no,
            "SIDE": side,
            "parts": parts,
            "PATH": " > ".join([side] + parts),
            "TEST_CASES": " / ".join(x.strip() for x in cells[c_tc].splitlines() if x.strip()),
            "ASSIGNED": cells[c_asg].strip(),
            "STATUS_HOJA": status,
            "PRIORITY": cells[c_pr].strip(),
            "OBSERVATION": " · ".join(x.strip() for x in [cells[c_obs]] + cells[c_ticket + 1:] if x.strip()),
            "SHEET_TICKET": cells[c_ticket].strip(),
            "SHEET_ID": cells[c_id].strip() if c_id is not None else "",
        }
        rows.append(leaf)
        leaves.append(leaf)
    return rows, leaves


# --------------------------------------------------------------------------- config

def load_modules():
    mods = {}
    for r in read_csv(os.path.join(CONFIG, "modules.csv")):
        mods[(norm(r["SIDE"]), norm(r["MODULE"]))] = r
    return mods


def load_rules():
    return [r for r in read_csv(os.path.join(CONFIG, "rules.csv")) if not r["MATCH"].startswith("#")]


def load_subcategories():
    path = os.path.join(CONFIG, "subcategory-map.csv")
    return read_csv(path) if os.path.exists(path) else []


def module_of(leaf, modules):
    side = norm(leaf["SIDE"])
    first = norm(leaf["parts"][0]) if leaf["parts"] else ""
    return modules.get((side, first)) or modules.get((side, "*"))


def apply_rules(path, rules):
    out = {}
    target = norm(path)
    for rule in rules:
        if fnmatch.fnmatchcase(target, norm(rule["MATCH"])):
            for c in RULE_COLS:
                if rule.get(c, "").strip():
                    out[c] = rule[c].strip()
    return out


# --------------------------------------------------------------------------- import

def cmd_import(args):
    modules, rules, subcats = load_modules(), load_rules(), load_subcategories()
    _, leaves = parse_sheet(args.sheet)
    old = read_csv(args.master) if os.path.exists(args.master) else []
    old_by_id = {r["ID"]: r for r in old}
    old_by_path = {norm(r["PATH"]): r for r in old}

    counters = defaultdict(int)
    for r in old:
        m = re.match(r"E2E-([A-Z]+-[A-Z]+)-(\d+)$", r["ID"])
        if m:
            counters[m.group(1)] = max(counters[m.group(1)], int(m.group(2)))

    rev_sub = defaultdict(list)
    for s in subcats:
        for code in s.get("E2E_MODULES", "").split():
            rev_sub[code].append(s["IOND_SUBCATEGORY"])

    missing, out, seen = [], [], set()
    for leaf in leaves:
        mod = module_of(leaf, modules)
        if not mod:
            missing.append(leaf["PATH"])
            continue
        prefix = f"{SIDE_CODES.get(leaf['SIDE'].upper(), 'XXX')}-{mod['CODE']}"
        prev = old_by_id.get(leaf["SHEET_ID"]) or old_by_path.get(norm(leaf["PATH"]))
        if prev:
            row_id = prev["ID"]
        else:
            counters[prefix] += 1
            row_id = f"E2E-{prefix}-{counters[prefix]:03d}"
        if row_id in seen:
            raise SystemExit(f"ID duplicado {row_id} en la línea {leaf['line']}")
        seen.add(row_id)

        derived = apply_rules(leaf["PATH"], rules)
        auto = derived.get("AUTOMATIZACION") or SHEET_STATUS_TO_AUTO.get(norm(leaf["STATUS_HOJA"]), "Pendiente")
        out.append(OrderedDict(
            ID=row_id,
            SIDE=leaf["SIDE"],
            MODULE=leaf["parts"][0] if leaf["parts"] else "",
            FEATURE=leaf["parts"][1] if len(leaf["parts"]) > 1 else "",
            CASO=" > ".join(leaf["parts"][2:]),
            PATH=leaf["PATH"],
            TEST_CASES=leaf["TEST_CASES"],
            PRIORITY=leaf["PRIORITY"],
            STATUS_HOJA=leaf["STATUS_HOJA"],
            ASSIGNED=leaf["ASSIGNED"],
            BASELINE=derived.get("BASELINE", "no"),
            ROTACION=prev.get("ROTACION", "") if prev else "",
            PROD_SAFE=derived.get("PROD_SAFE", "no"),
            CROSS_SYSTEM=derived.get("CROSS_SYSTEM", ""),
            AUTOMATIZACION=auto,
            NOTA_AUTOMATIZACION=derived.get("NOTA_AUTOMATIZACION", ""),
            BOT_TEST_SPEC=derived.get("BOT_TEST_SPEC", ""),
            BOT_TEST_TC=derived.get("BOT_TEST_TC", ""),
            TICKET_AUTOMATIZACION=leaf["SHEET_TICKET"] or derived.get("TICKET_AUTOMATIZACION", ""),
            L2_MODULE=derived.get("L2_MODULE") or mod.get("L2_MODULE", ""),
            IOND_SUBCATEGORY="; ".join(sorted(set(rev_sub.get(prefix, [])))),
            ESTADO_FILA="Vigente",
            OBSERVATION=leaf["OBSERVATION"],
        ))

    if missing:
        print("Filas sin módulo en _config/modules.csv (agregar y reimportar):", file=sys.stderr)
        for p in missing:
            print("  -", p, file=sys.stderr)
        raise SystemExit(1)

    for r in old:  # filas que salieron de la hoja: nunca se borran ni se renumeran
        if r["ID"] not in seen:
            r = dict(r)
            r["ESTADO_FILA"] = "Retirada"
            out.append(r)

    assign_rotation(out)
    write_csv(args.master, MASTER_COLS, out)
    vig = [r for r in out if r["ESTADO_FILA"] == "Vigente"]
    print(f"{rel(args.master)}: {len(vig)} filas vigentes, "
          f"{len(out) - len(vig)} retiradas, {len({r['ID'] for r in out})} IDs únicos")


MAX_UNIT_LOAD = 15  # filas manuales por unidad de rotación antes de dividirla


def path_parts(row):
    return [p.strip() for p in row["PATH"].split(" > ")]


def manual_load(row):
    return 0 if row["AUTOMATIZACION"] in RUNNABLE | {"Bloqueada"} or row["ESTADO_FILA"] != "Vigente" else 1


def rotation_units(rows):
    """Unidad = módulo completo; si su carga manual supera MAX_UNIT_LOAD se divide por el nivel siguiente."""
    units = OrderedDict()

    def split(members, depth):
        load = sum(manual_load(m) for m in members)
        if load <= MAX_UNIT_LOAD or all(len(path_parts(m)) <= depth for m in members):
            units[" > ".join(path_parts(members[0])[:depth])] = members
            return
        children = OrderedDict()
        for m in members:
            children.setdefault(tuple(path_parts(m)[:depth + 1]), []).append(m)
        for child in children.values():
            split(child, depth + 1)

    modules = OrderedDict()
    for r in rows:
        modules.setdefault(tuple(path_parts(r)[:2]), []).append(r)
    for members in modules.values():
        split(members, 2)
    return units


def assign_rotation(rows):
    """Asigna G1–G4 por unidad de rotación. Una fila que ya tiene grupo no cambia de grupo."""
    load = Counter({g: 0 for g in GROUPS})
    pending = []
    for members in rotation_units(rows).values():
        known = Counter(m["ROTACION"] for m in members if m.get("ROTACION") in GROUPS)
        if known:
            group = known.most_common(1)[0][0]
            for m in members:
                m["ROTACION"] = m.get("ROTACION") if m.get("ROTACION") in GROUPS else group
                load[m["ROTACION"]] += manual_load(m)
        else:
            pending.append(members)
    pending.sort(key=lambda ms: -sum(manual_load(m) for m in ms))
    for members in pending:
        group = min(GROUPS, key=lambda g: (load[g], GROUPS.index(g)))
        for m in members:
            m["ROTACION"] = group
        load[group] += sum(manual_load(m) for m in members)


# --------------------------------------------------------------------------- export

def cmd_export_sheet(args):
    master = {norm(r["PATH"]): r for r in read_csv(args.master) if r["ESTADO_FILA"] == "Vigente"}
    rows, _ = parse_sheet(args.sheet)
    out = []
    for leaf in rows:
        r = master.get(norm(leaf["PATH"])) if leaf else None
        spec = ""
        if r and r["BOT_TEST_SPEC"]:
            spec = f"{r['BOT_TEST_SPEC']} [{r['BOT_TEST_TC']}]" if r["BOT_TEST_TC"] else r["BOT_TEST_SPEC"]
        out.append({"ID": r["ID"] if r else "", "TICKET": r["TICKET_AUTOMATIZACION"] if r else "", "SPEC": spec})
    write_csv(args.out, ["ID", "TICKET", "SPEC"], out)
    print(f"{rel(args.out)}: {len(out)} filas alineadas con la hoja desde la fila 2 "
          f"({sum(1 for o in out if o['ID'])} con ID)")


# --------------------------------------------------------------------------- coverage

def pct(a, b):
    return f"{(100 * a / b):.0f} %" if b else "—"


def cmd_coverage(args):
    rows = [r for r in read_csv(args.master) if r["ESTADO_FILA"] == "Vigente"]
    sides = OrderedDict()
    for r in rows:
        sides.setdefault(r["SIDE"], []).append(r)

    def stats(group):
        n = len(group)
        auto = sum(1 for r in group if r["AUTOMATIZACION"] in RUNNABLE | {"Rota"})
        run = sum(1 for r in group if r["AUTOMATIZACION"] in RUNNABLE)
        pend = [r for r in group if norm(r["STATUS_HOJA"]) == "pending"]
        pend_auto = sum(1 for r in pend if r["AUTOMATIZACION"] in RUNNABLE | {"Rota"})
        return n, auto, run, len(pend), pend_auto

    lines = [
        "# Cobertura de automatización del E2E maestro",
        "",
        "> Archivo generado por `python -I scripts/e2e_master.py coverage`. No se edita a mano.",
        "",
        "**Automatizada** = existe una spec en bot-test (`En PR`, `Ejecutable` o `Rota`). "
        "**Ejecutable** = la spec corre hoy (`En PR` o `Ejecutable`). "
        "La columna *Pending* considera solo las filas que la hoja marca como `Pending`.",
        "",
        "## Resumen por SIDE",
        "",
        "| SIDE | Filas | Automatizadas | % | Ejecutables | % | Pending automatizadas |",
        "|---|---|---|---|---|---|---|",
    ]
    tot = [0, 0, 0, 0, 0]
    for side, group in sides.items():
        n, auto, run, pn, pa = stats(group)
        tot = [a + b for a, b in zip(tot, [n, auto, run, pn, pa])]
        lines.append(f"| {side} | {n} | {auto} | {pct(auto, n)} | {run} | {pct(run, n)} | {pa}/{pn} ({pct(pa, pn)}) |")
    n, auto, run, pn, pa = tot
    lines.append(f"| **Total** | **{n}** | **{auto}** | **{pct(auto, n)}** | **{run}** | **{pct(run, n)}** | **{pa}/{pn} ({pct(pa, pn)})** |")

    lines += ["", "## Estado de automatización", "", "| Estado | Filas |", "|---|---|"]
    for state, count in Counter(r["AUTOMATIZACION"] for r in rows).most_common():
        lines.append(f"| {state} | {count} |")

    lines += ["", "## Por módulo", "",
              "| SIDE | Módulo | Prefijo | Filas | Automatizadas | Ejecutables | Baseline | Rotación | Ticket(s) de automatización |",
              "|---|---|---|---|---|---|---|---|---|"]
    mods = OrderedDict()
    for r in rows:
        mods.setdefault((r["SIDE"], r["MODULE"]), []).append(r)
    for (side, module), group in mods.items():
        n, auto, run, _, _ = stats(group)
        prefix = group[0]["ID"].rsplit("-", 1)[0]
        base = sum(1 for r in group if r["BASELINE"] == "sí")
        rot = ", ".join(sorted({r["ROTACION"] for r in group}))
        tickets = ", ".join(sorted({t.strip() for r in group for t in r["TICKET_AUTOMATIZACION"].split(";") if t.strip()}))
        lines.append(f"| {side} | {module} | `{prefix}` | {n} | {auto} | {run} | {base} | {rot} | {tickets or '—'} |")

    lines += ["", "## Carga de la rotación manual (capa 2)", "",
              "Filas vigentes, no ejecutables y no bloqueadas que corresponden a cada grupo.", "",
              "| Grupo | Filas manuales | Módulos |", "|---|---|---|"]
    for g in GROUPS:
        members = [r for r in rows if r["ROTACION"] == g and manual_load(r)]
        mod_names = sorted({f"{r['SIDE']} › {r['MODULE']}" for r in members})
        lines.append(f"| {g} | {len(members)} | {', '.join(mod_names) or '—'} |")

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    n, auto, run = tot[0], tot[1], tot[2]
    print(f"{rel(args.out)}: {n} filas · automatizadas {auto} ({pct(auto, n)}) · ejecutables {run} ({pct(run, n)})")


# --------------------------------------------------------------------------- select

NODE_PREFIXES = ("tenant > boards > list > create board > all tools > ",
                 "tenant > boards > list > create board > storage > ",
                 "tenant > boards > list > create board > ion pdf > ",
                 "tenant > boards > list > create board > tenant app > ")
PRIORITY_BY_RISK = {"Bajo": {"urgent"}, "Medio": {"urgent", "high"}, "Alto": None}
PRIORITY_ORDER = {"urgent": 0, "high": 1, "normal": 2, "low": 3}


def grep_escape(text):
    return re.sub(r"([.^$*+?()\[\]{}|\\])", r"\\\1", text)


def run_command(rows):
    by_spec = OrderedDict()
    for r in rows:
        if r["AUTOMATIZACION"] in RUNNABLE and r["BOT_TEST_SPEC"]:
            by_spec.setdefault(r["BOT_TEST_SPEC"], set()).update(
                t.strip() for t in r["BOT_TEST_TC"].split(";") if t.strip())
    if not by_spec:
        return ""
    specs = " ".join(BOT_TEST_BASE + s for s in by_spec)
    tcs = sorted({t for ts in by_spec.values() for t in ts})
    grep = "|".join(grep_escape(t) for t in tcs)
    return f'npx playwright test {specs} --config={BOT_TEST_CONFIG} --project=ionflow-chromium -g "{grep}"'


def node_rows(rows, name):
    """Filas del nodo del canvas que más se parecen a `name` (tolera errores de tipeo de la hoja)."""
    leaves = {}
    for r in rows:
        p = norm(r["PATH"])
        for prefix in NODE_PREFIXES:
            if p.startswith(prefix):
                leaves.setdefault(p[len(prefix):], []).append(r)
    hits = difflib.get_close_matches(norm(name), list(leaves), n=1, cutoff=0.6)
    return leaves[hits[0]] if hits else []


def code_of(row):
    return row["ID"][4:].rsplit("-", 1)[0]


def cmd_select(args):
    rows = [r for r in read_csv(args.master) if r["ESTADO_FILA"] == "Vigente"]
    subcats = load_subcategories()
    wanted = [s.strip() for s in (args.subcategories or "").split(",") if s.strip()]
    impacted, excludes, node_ids, systems, unknown = set(), [], set(), set(), []
    for s in wanted:
        match = next((x for x in subcats if norm(x["IOND_SUBCATEGORY"]) == norm(s)), None)
        if match is None and norm(s).startswith("nodo "):
            hits = node_rows(rows, norm(s)[5:])
            if hits:
                node_ids.update(r["ID"] for r in hits)
                continue
        if match is None:
            unknown.append(s)
            continue
        impacted.update(match["E2E_MODULES"].split())
        excludes += [g.strip() for g in match.get("E2E_EXCLUDE", "").split(";") if g.strip()]
        systems.update(norm(x) for x in match.get("CROSS_SYSTEM", "").split(";") if x.strip())
    impacted.update(m.strip() for m in (args.modules or "").split(",") if m.strip())
    if args.cross_system == "sí":
        systems = {norm(r["CROSS_SYSTEM"]) for r in rows if r["CROSS_SYSTEM"]}
    elif args.cross_system == "no":
        systems = set()
    allowed = PRIORITY_BY_RISK[args.risk]

    def in_scope(r):
        if r["ID"] in node_ids:
            return True
        if code_of(r) not in impacted:
            return False
        p = norm(r["PATH"])
        if any(fnmatch.fnmatchcase(p, norm(g)) for g in excludes):
            return False
        return allowed is None or norm(r["PRIORITY"]) in allowed

    focus = {}
    if getattr(args, "focus", None):
        with open(args.focus, encoding="utf-8-sig", newline="") as fh:
            sample = fh.read()
        if sample.lstrip().upper().startswith("ID"):
            for fr in csv.DictReader(sample.splitlines()):
                if fr.get("ID"):
                    focus[fr["ID"].strip()] = (fr.get("TICKETS") or "").strip()
        else:
            focus = {line.strip(): "" for line in sample.splitlines() if line.strip()}
        unknown_focus = sorted(set(focus) - {r["ID"] for r in rows})
        if unknown_focus:
            print("IDs del foco que no existen en el maestro:", ", ".join(unknown_focus))
    urgent_high = {"urgent", "high"}

    def tier(r, why):
        """urgent = obligatoria · high = importante · normal = pasa a la capa 2 (doc 05 §6.3, regla de recorte)."""
        if r["BASELINE"] == "sí" or r["ID"] in focus or r["ID"] in node_ids:
            return "urgent"
        hot = norm(r["PRIORITY"]) in urgent_high
        if hot and ("módulo impactado" in why or "cross-system" in why):
            return "urgent" if not focus and "módulo impactado" in why and norm(r["PRIORITY"]) == "urgent" else "high"
        return "normal"

    selected = []
    if args.layer == "1":
        for r in rows:
            reasons = []
            if r["BASELINE"] == "sí":
                reasons.append("baseline")
            if r["ID"] in focus:
                reasons.append("foco del release")
            if in_scope(r):
                reasons.append("módulo impactado")
            if norm(r["CROSS_SYSTEM"]) in systems and (allowed is None or norm(r["PRIORITY"]) in allowed):
                reasons.append(f"cross-system {r['CROSS_SYSTEM']}")
            if args.risk == "Alto" and not reasons:
                reasons.append("extendida")
            # Una fila bloqueada en la hoja entra si el release la desbloquea (está en el foco).
            if reasons and (r["AUTOMATIZACION"] != "Bloqueada" or r["ID"] in focus):
                selected.append((r, ", ".join(reasons)))
        title = f"Regression capa 1 — riesgo {args.risk}"
    else:
        excluded = set()
        if args.exclude and os.path.exists(args.exclude):
            # Las filas normal de la capa 1 se cubren en la capa 2: solo se excluyen las urgent y high.
            excluded = {r.get("ID", "") for r in read_csv(args.exclude)
                        if r.get("PRIORIDAD", "urgent") in ("urgent", "high", "P1", "P2")}
        for r in rows:
            if r["AUTOMATIZACION"] in RUNNABLE:
                selected.append((r, "automatizada"))
            elif (r["ROTACION"] == args.group and r["AUTOMATIZACION"] != "Bloqueada"
                  and r["ID"] not in excluded):
                selected.append((r, f"rotación {args.group}"))
        title = f"E2E maestro capa 2 — automatizado + rotación {args.group}"

    def prio(item):
        return tier(*item) if args.layer == "1" else ""

    def sort_key(item):
        r, why = item
        manual = r["AUTOMATIZACION"] not in RUNNABLE
        return (TIER_ORDER.get(prio(item), 9), manual, "baseline" not in why, PRIORITY_ORDER.get(norm(r["PRIORITY"]), 9))

    selected.sort(key=sort_key)
    def observation(r, why):
        notes = [r["OBSERVATION"]] if r.get("OBSERVATION") else []
        if args.layer == "1" and r["AUTOMATIZACION"] == "Bloqueada":
            notes.append("Bloqueada en la hoja: entra porque el release toca la feature")
        if args.layer == "1" and prio((r, why)) == "normal":
            notes.append("No se ejecuta en la capa 1: la cubre la capa 2")
        return " · ".join(notes)

    out_rows = [dict(r, PRIORIDAD=prio((r, why)), MOTIVO=why, TICKETS_RELEASE=focus.get(r["ID"], ""),
                     EJECUCION="Automática" if r["AUTOMATIZACION"] in RUNNABLE else "Manual",
                     RESULTADO="", **{
                         "RESULTADO ESPERADO": r.get("TEST_CASES") or "Sin regresión: el flujo funciona como en la versión anterior",
                         "QA ASIGNADO": "", "RESOLUCION": "", "OBSERVACION": observation(r, why),
                         "TICKET": "", "PRIORIDAD BUG": ""}) for r, why in selected]
    if args.layer == "1":
        # Capa 1: columnas de ejecución + contexto de la selección + automatización (se ocultan en la hoja)
        cols = EXEC_COLS + ["MOTIVO", "TICKETS_RELEASE", "CROSS_SYSTEM",
                            "EJECUCION", "AUTOMATIZACION", "BOT_TEST_SPEC", "BOT_TEST_TC"]
    else:
        cols = ["ID", "SIDE", "MODULE", "FEATURE", "CASO", "PRIORITY", "MOTIVO",
                "EJECUCION", "AUTOMATIZACION", "BOT_TEST_SPEC", "BOT_TEST_TC", "CROSS_SYSTEM", "RESULTADO"]
    if args.out:
        write_csv(args.out, cols, out_rows)
    auto = sum(1 for r in out_rows if r["EJECUCION"] == "Automática")
    print(f"## {title}")
    print(f"Filas: {len(out_rows)} · automáticas {auto} · manuales {len(out_rows) - auto}")
    if args.layer == "1":
        for t in ("urgent", "high", "normal"):
            group = [r for r in out_rows if r["PRIORIDAD"] == t]
            a = sum(1 for r in group if r["EJECUCION"] == "Automática")
            print(f"  {t}: {len(group)} filas · automáticas {a} · manuales {len(group) - a}")
    if impacted or node_ids:
        print("Alcance impactado:", ", ".join(sorted(impacted | node_ids)))
    if systems:
        print("Sistemas cruzados:", ", ".join(sorted(systems)))
    if unknown:
        print("Subcategorías sin mapa (agregar a _config/subcategory-map.csv):", ", ".join(unknown))
    cmd = run_command([r for r, _ in selected])
    if cmd:
        print("\nComando (desde apps/bot-test, con el perfil del ambiente cargado):")
        print(cmd)
    if args.out:
        print(f"\nMatriz: {rel(args.out)}")


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", default=DEFAULT_SHEET)
    ap.add_argument("--master", default=DEFAULT_MASTER)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("import")
    p_exp = sub.add_parser("export-sheet")
    p_exp.add_argument("--out", default=os.path.join(SUITES, "exports", "sheet-id-ticket-spec.csv"))
    p_cov = sub.add_parser("coverage")
    p_cov.add_argument("--out", default=os.path.join(SUITES, "coverage.md"))
    p_sel = sub.add_parser("select")
    p_sel.add_argument("--layer", choices=["1", "2"], required=True)
    p_sel.add_argument("--subcategories", help="Iond Subcategory de los tickets, separadas por coma")
    p_sel.add_argument("--modules", help="Prefijos adicionales, p. ej. TEN-BRD,TEN-PDF")
    p_sel.add_argument("--risk", choices=["Alto", "Medio", "Bajo"], default="Medio")
    p_sel.add_argument("--cross-system", choices=["sí", "no"],
                       help="sí = todos los flujos cross-system (p. ej. la corrida mensual completa); no = ninguno")
    p_sel.add_argument("--group", choices=GROUPS, help="Grupo de rotación de la capa 2")
    p_sel.add_argument("--exclude", help="CSV de la capa 1 (sus IDs urgent/high no se repiten en la rotación)")
    p_sel.add_argument("--focus", help="CSV (columna ID) o lista de IDs E2E tocados por los tickets del release: van como urgent")
    p_sel.add_argument("--out", help="CSV de salida con la matriz seleccionada")
    args = ap.parse_args()
    if args.cmd == "select" and args.layer == "2" and not args.group:
        ap.error("--group es obligatorio en la capa 2")
    {"import": cmd_import, "export-sheet": cmd_export_sheet,
     "coverage": cmd_coverage, "select": cmd_select}[args.cmd](args)


if __name__ == "__main__":
    main()
