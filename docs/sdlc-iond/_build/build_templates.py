"""Genera las plantillas de comentario C-01 ... C-33 del QA Catalyst desde la fuente canónica.

Fuente:  knowledge/L1-project/sdlc-consolidation.md, §14 (bloque entre
         <!-- BEGIN:comentarios --> y <!-- END:comentarios -->).
Salida:  templates/comments/C-xx.md (una por comentario) + templates/comments/README.md.

Uso (desde la raíz del repo):
    python -I docs/sdlc-iond/_build/build_templates.py

Solo biblioteca estándar. Escribe UTF-8 sin BOM con fin de línea LF.
Falla (exit 1) si el bloque no existe, si un comentario no tiene bloque de código
o si encuentra menos de 33 IDs (o falta alguno entre C-01 y C-33).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "knowledge" / "L1-project" / "sdlc-consolidation.md"
OUT_DIR = ROOT / "templates" / "comments"
SOURCE_REL = "knowledge/L1-project/sdlc-consolidation.md"
BEGIN, END = "<!-- BEGIN:comentarios -->", "<!-- END:comentarios -->"
EXPECTED = [f"C-{n:02d}" for n in range(1, 34)]

HEADER_RE = re.compile(r"^\*\*(C-\d{2}(?:\s*/\s*C-\d{2})*)\s*·\s*(.+?)\*\*\s*$")
GROUP_RE = re.compile(r"^###\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```")
TRAILING_PARENS_RE = re.compile(r"^(.*?)\s*\(([^()]*)\)\s*$")
# Paréntesis que solo contiene roles y conectores: "(PO)", "(SM/PO)", "(Dev + aprobación LD)", "(QA o Dev)".
ROLE_RE = re.compile(r"^(?:\s*(?:PO|SM|LD|QA|LQA|RM|DevOps|Dev|SH|aprobación|\+|/|→|o|y)\s*)+$")
STATES_RE = re.compile(r"`[^`]+`(?:.*`[^`]+`)?")

GENERATED_NOTE = (f"> Generado desde {SOURCE_REL} §14. "
                  "No editar a mano: regenerar con build_templates.py.")


def fail(msg):
    sys.stderr.write(f"ERROR build_templates: {msg}\n")
    sys.exit(1)


def read_block():
    if not SOURCE.exists():
        fail(f"no existe la fuente canónica {SOURCE_REL}")
    text = SOURCE.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if BEGIN not in text or END not in text:
        fail(f"no se encontraron los marcadores {BEGIN} / {END} en {SOURCE_REL}")
    block = text.split(BEGIN, 1)[1].split(END, 1)[0]
    return block.split("\n")


def parse(lines):
    """Devuelve (intro, comentarios). Cada comentario: ids, title, group, fences, stray."""
    comments, current, group, intro = [], None, "", []
    in_fence = False
    for line in lines:
        if in_fence:
            current["fences"][-1].append(line)
            if FENCE_RE.match(line.strip()):
                in_fence = False
            continue
        m_header = HEADER_RE.match(line.strip())
        m_group = GROUP_RE.match(line)
        if m_header:
            ids = [i.strip() for i in m_header.group(1).split("/")]
            current = {"ids": ids, "title": m_header.group(2).strip(), "group": group,
                       "fences": [], "stray": []}
            comments.append(current)
        elif m_group:
            group, current = m_group.group(1), None
        elif FENCE_RE.match(line.strip()):
            if current is None:
                fail(f"bloque de código fuera de un comentario: {line!r}")
            current["fences"].append([line])
            in_fence = True
        elif line.strip().startswith(">") and not comments:
            intro.append(line.strip())
        elif line.strip() and current is not None:
            current["stray"].append(line)
    if in_fence:
        fail("bloque de código sin cerrar en §14")
    return intro, comments


def split_title(title):
    """Separa el título en (base, publica, transicion) a partir de la línea en negrita."""
    base, who, when = title, "", ""
    m = TRAILING_PARENS_RE.match(title)
    if m:
        inner = m.group(2).strip()
        if "`" in inner:
            base, when = m.group(1).strip(), inner
        elif ROLE_RE.match(inner):
            base, who = m.group(1).strip(), inner
    if not when:
        s = STATES_RE.search(base)
        if s:
            when = s.group(0)
    return base, who, when


def expand(comment):
    """Un comentario por ID. Las cabeceras combinadas (C-25 / C-26 / C-27) se reparten por estado."""
    base, who, when = split_title(comment["title"])
    if len(comment["ids"]) == 1:
        return [{"id": comment["ids"][0], "title": comment["title"], "group": comment["group"],
                 "who": who, "when": when, "fences": comment["fences"], "suite": None}]
    states = [s.strip() for s in base.split("/")]
    if len(states) != len(comment["ids"]):
        fail(f"cabecera combinada {comment['ids']} con {len(states)} estados; no se puede repartir")
    out = []
    for cid, state in zip(comment["ids"], states):
        title = f"{state} ({who})" if who else state
        out.append({"id": cid, "title": title, "group": comment["group"], "who": who,
                    "when": state, "fences": comment["fences"],
                    "suite": state.strip("`"), "shared": comment["ids"]})
    return out


def render(c):
    lines = [f"# {c['id']} · {c['title']}", "", GENERATED_NOTE, ""]
    lines.append(f"- **Tablero / fase:** {c['group']}")
    if c["when"]:
        lines.append(f"- **Estado / transición:** {c['when']}")
    if c["who"]:
        lines.append(f"- **Quién lo publica:** {c['who']}")
    if c["suite"]:
        shared = " / ".join(c["shared"])
        label = c["suite"].upper()
        lines += ["", f"> **Suite:** {c['suite']}. Plantilla compartida {shared} en la fuente canónica: "
                      f"en el encabezado se usa `{label}`.",
                  "> Las líneas bajo `<!-- Solo en REGRESSION (C-27) -->` "
                  + ("se completan (capa 1 y capa 2)." if label == "REGRESSION"
                     else "no se publican en esta suite.")]
    lines.append("")
    for fence in c["fences"]:
        lines += fence
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def render_index(intro, items):
    rows = ["# Plantillas de comentario C-01 … C-33", "", GENERATED_NOTE, ""]
    rows += intro + [""] if intro else []
    rows += [
        "Las skills del catalyst **preparan** el borrador (en `knowledge/L3-tickets/<id>/comments/` o en la "
        "carpeta del release) y QA/SM lo **publican** en ClickUp. El MCP de ClickUp es de solo lectura.",
        "",
        "| ID | Título | Tablero / fase | Archivo |",
        "|---|---|---|---|",
    ]
    for c in items:
        title = c["title"].replace("|", "\\|")
        rows.append(f"| {c['id']} | {title} | {c['group']} | [`{c['id']}.md`]({c['id']}.md) |")
    rows += ["", "Regenerar: `python -I docs/sdlc-iond/_build/build_templates.py` (desde la raíz del repo)."]
    return "\n".join(rows) + "\n"


def write(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    intro, comments = parse(read_block())
    items = [x for c in comments for x in expand(c)]
    ids = [c["id"] for c in items]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        fail(f"IDs duplicados en §14: {', '.join(dupes)}")
    missing = [i for i in EXPECTED if i not in ids]
    if len(ids) < len(EXPECTED) or missing:
        fail(f"se encontraron {len(ids)} comentarios (mínimo {len(EXPECTED)}); "
             f"faltan: {', '.join(missing) or '—'}")
    for c in items:
        if not c["fences"]:
            fail(f"{c['id']} no tiene bloque de código en §14")
    for c in comments:
        if c["stray"]:
            sys.stderr.write(f"AVISO: texto fuera del bloque de código en {'/'.join(c['ids'])} "
                             f"(no se copia): {c['stray'][0].strip()[:60]}\n")

    items.sort(key=lambda c: int(c["id"][2:]))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = set()
    for c in items:
        name = f"{c['id']}.md"
        write(OUT_DIR / name, render(c))
        generated.add(name)
    for stale in OUT_DIR.glob("C-*.md"):
        if stale.name not in generated:
            stale.unlink()
            print(f"Eliminado (ya no existe en la fuente): {stale.name}")
    write(OUT_DIR / "README.md", render_index(intro, items))
    print(f"OK: {len(items)} plantillas de comentario + README.md en "
          f"{OUT_DIR.relative_to(ROOT).as_posix()}/")


if __name__ == "__main__":
    main()
