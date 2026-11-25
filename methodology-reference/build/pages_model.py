"""Data-model pages: relationship diagram, table dictionary, variables, datasets, rule tables."""

import re
import json

import data
import markdown
import current_t2
from chapters import TITLES, chapter_file
from core import (
    BLOCKED_KEYS,
    CIAT_URL,
    METHOD,
    METHOD_URL,
    PRACTICE_IDS,
    SIDE,
    TABLE_NAMES,
    badge,
    code,
    dl,
    esc,
    link,
    page,
    pinned_csv,
    pinned_exists,
    pinned_json,
    pinned_list,
    scrub,
    table,
    text,
    words,
)

MANIFEST = pinned_json("schema/structure/columns.json")
# The immutable source manifest still describes retired tables. Current reference
# pages expose only supported interfaces; do not rewrite the source schema.
TABLES = {key: value for key, value in MANIFEST["tables"].items()
          if key != "T4_NUMERIC_POLICY"}
# Effects now have an AI authoring contract; old data counts remain historical.
CURRENT_EFFECTS = json.loads((METHOD / "data-model/structure/columns.json").read_bytes())
for effect_table in ("T3", "T6"):
    TABLES[effect_table] = CURRENT_EFFECTS["tables"][effect_table]
EXPLAINED_IN = {
    "T0": ["m0-setup", "m2b-project-risk", "m6-handoff"],
    "T1": ["m0-setup", "farming-systems-and-data"],
    "T2": ["m2-climate-risk", "m2b-project-risk"],
    "T3": ["m2-climate-risk", "m2b-project-risk", "m5-scorecard", "effect-synthesis"],
    "T4": ["m1-suitability", "suitability-synthesis"],
    "T5": ["m3-characterisation", "m4-hotspots"],
    "T6": ["m5-scorecard", "effect-synthesis"],
    "T6E": ["m5-scorecard", "cost-profiles"],
    "T7": ["m0-setup", "farming-systems-and-data"],
    "SRC": ["evidence-principles", "acquisition"],
    "EV": ["evidence-principles", "extraction", "review-and-quality"],
    "VONT": ["m1-suitability", "farming-systems-and-data"],
    "FAM": ["m1-suitability"],
    "BIND": ["farming-systems-and-data"],
    "SRCH": ["discovery"],
    "XW": ["effect-synthesis"],
    "BANDS": ["effect-synthesis"],
    "TOOL": ["extraction"],
    "T4_RUN": ["suitability-synthesis"],
}
SPEC_HEADING = {
    "T0": "## T0",
    "T1": "## T1",
    "T2": "## T2",
    "T3": "## T3",
    "T4": "## T4",
    "T5": "## T5",
    "T6": "## T6",
    "T6E": "## T6",
    "T7": "## T7",
    "SRC": "### SRC",
    "EV": "### EV",
    "VONT": "### VONT",
    "FAM": "### FAM",
    "BIND": "### BIND",
    "XW": "### XW",
    "BANDS": "### BANDS",
    "TOOL": "### TOOL",
    "T4_RUN": "## T4_RUN",
    "SRCH": "### SRCH",
}
GROUPS = [
    ("Configuration", ["T0", "T7", "T1", "T5", "T2"]),
    ("Recipe tables", ["T4", "T4_RUN", "T3", "T6", "T6E"]),
    (
        "Evidence and configuration registers",
        ["FAM", "VONT", "BIND", "EV", "SRC", "TOOL", "SRCH", "XW", "BANDS"],
    ),
]

# Explain the purpose on hover and to assistive technology, not just the table ID.
TABLE_HELP = {
    "T0": "Defines each practice and its implementation profile.",
    "T1": "Lists datasets, how to access them and their limitations.",
    "T2": "Registers climate-risk variables and explicit problem-classification rules; no composite climate-risk index.",
    "T3": "Records effects on livelihood hazards and threats to the investment as separate assessments.",
    "T4": "Links environmental or land-use conditions to suitability for a practice family.",
    "T4_RUN": "Records inputs and execution settings for a suitability run.",
    "T5": "Lists variables that describe opportunity areas and priorities used to rank hotspots.",
    "T6": "Records assessed effects of a practice on scorecard priorities, with their evidence and context.",
    "T6E": "Records indicative economic values, units and evidence. Existing profiles are historical; new synthesis is frozen.",
    "T7": "Defines geographic and farming-system contexts used by the other tables.",
    "FAM": "Groups subpractices into suitability families with shared limiting conditions.",
    "VONT": "Gives each analytical variable a consistent name, definition and unit.",
    "BIND": "Connects a variable to the dataset appropriate for its geographic context.",
    "EV": "Stores individual findings with their source, quoted passage, location and review state.",
    "SRC": "Catalogues source documents, their identity and where reviewers can find them.",
    "TOOL": "Catalogues documented tools and methods used as sources.",
    "SRCH": "Records search terms, scope, screening criteria and counts so searches can be traced.",
    "XW": "Links reported outcomes to analytical targets. Relevance still requires scientific judgment.",
    "BANDS": "Records historical magnitude bands. These do not automatically score new AI synthesis outputs.",
}


def references(table_id):
    out = []
    for field, target in (TABLES[table_id].get("fk") or {}).items():
        targets = [target] if isinstance(target, str) else target.get("targets", [])
        literals = [] if isinstance(target, str) else target.get("literals", [])
        for t in targets:
            out.append((field, t.split(".")[0], t.split(".")[1], literals))
    return out


def edition_rows(table_id):
    """Rows of a table in this edition, as (count, list-of-dicts or None)."""
    if table_id in data.TABLE_TOTALS:
        return data.TABLE_TOTALS[table_id], None
    if table_id == "T0":
        rows = [
            pinned_csv(f"schema/recipes/{p}/T0_nbs_registry.csv")[0]
            for p in PRACTICE_IDS
        ]
        return len(rows), rows
    if table_id == "T4_RUN":
        rows = []
        for p in PRACTICE_IDS:
            path = f"schema/recipes/{p}/T4_run_policy.csv"
            if pinned_exists(path):
                rows += pinned_csv(path)
        return len(rows), rows
    fixed = {
        "T1": "schema/T1_data_registry.csv",
        "T2": "schema/T2_climate_risk.csv",
        "T5": "schema/T5_opportunity_space.csv",
        "T7": "schema/T7_geographic_context.csv",
        "BIND": "schema/registers/BIND_dataset_binding.csv",
        "FAM": "schema/registers/FAM_family_registry.csv",
        "XW": "schema/registers/XW_target_crosswalk.csv",
        "BANDS": "schema/registers/BANDS_magnitude_bands.csv",
        "TOOL": "schema/registers/TOOL_tool_registry.csv",
    }
    if table_id in fixed:
        rows = pinned_csv(fixed[table_id])
        return len(rows), rows
    counts = {
        "SRC": len(data.SRC),
        "EV": len(data.EV),
        "VONT": len(data.VONT),
        "SRCH": len(data.SRCH),
    }
    return counts[table_id], None


def csv_table(rows, caption, limit=None):
    if not rows:
        return '<p class="empty">No rows in this edition.</p>'
    columns = [
        c
        for c in rows[0]
        if not BLOCKED_KEYS.search(c) and c not in {"ruled_by", "date", "note"}
    ]
    shown = rows[:limit] if limit else rows
    body = [[text(r.get(c, "")) for c in columns] for r in shown]
    return table([esc(words(c)) for c in columns], body, caption=caption, cls="rule")


def spec_section(table_id):
    lines = (METHOD / "data-model/spec.md").read_text().splitlines()
    head = SPEC_HEADING[table_id]
    level = head.split(" ")[0]
    start = next((i for i, l in enumerate(lines) if l.startswith(head)), None)
    if start is None:
        return ""
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## ") or (
            level == "###" and lines[i].startswith("### ")
        ):
            end = i
            break
    body = "\n".join(lines[start + 1 : end])
    body = re.sub(
        r"\[([^\]]+)\]\([^)]+\)", r"\1", body
    )  # relative links do not resolve here
    body = re.sub(r"[;,]?\s*(?:issue|PR)\s*#\d+|\(#\d+\)", "", body)
    body = re.sub(
        r"^(#+) ", lambda m: "#" * (len(m.group(1)) + 1) + " ", body, flags=re.MULTILINE
    )
    html = markdown.markdown(
        scrub(body), extensions=["tables", "fenced_code", "sane_lists"]
    )
    return html.replace(
        "<table>", '<div class="tablewrap" tabindex="0"><table>'
    ).replace("</table>", "</table></div>")


def diagram():
    width, height, bw, bh = 1100, 500, 104, 44
    pos = {}
    for band, (label, ids) in enumerate(GROUPS):
        gap = (width - 40 - bw) / max(len(ids) - 1, 1)
        for i, t in enumerate(ids):
            pos[t] = (20 + i * gap, 50 + band * 170)
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="group" aria-label="Table relationships" aria-describedby="erd-desc" class="erd">',
        '<desc id="erd-desc">Each line joins a table to a table it references. The same relationships are listed in the table below the figure.</desc>',
    ]
    for band, (label, ids) in enumerate(GROUPS):
        y = 30 + band * 170
        parts.append(f'<text x="20" y="{y}" class="band">{esc(label)}</text>')
    for t in TABLES:
        for field, target, column, _ in references(t):
            if target == t or target not in pos:
                continue
            (x1, y1), (x2, y2) = pos[t], pos[target]
            sx, tx = x1 + bw / 2, x2 + bw / 2
            if y1 == y2:
                sy = ty = y1
                bend = 26 + abs(x2 - x1) / 14
                d = f"M{sx:.0f},{sy:.0f} C{sx:.0f},{sy - bend:.0f} {tx:.0f},{ty - bend:.0f} {tx:.0f},{ty:.0f}"
            else:
                sy = y1 if y2 < y1 else y1 + bh
                ty = y2 + bh if y2 < y1 else y2
                mid = (sy + ty) / 2
                d = f"M{sx:.0f},{sy:.0f} C{sx:.0f},{mid:.0f} {tx:.0f},{mid:.0f} {tx:.0f},{ty:.0f}"
            parts.append(
                f'<path d="{d}" class="edge"><title>{esc(TABLE_NAMES[t])} ({esc(t)}) links to '
                f'{esc(TABLE_NAMES[target])} ({esc(target)}).\n'
                f'Join: {esc(t)}.{esc(field)} → {esc(target)}.{esc(column)}</title></path>'
            )
    for t, (x, y) in pos.items():
        key = (
            t
            if t in {"T0", "T1", "T2", "T3", "T4", "T5", "T6", "T6E", "T7"}
            else "register"
        )
        name = TABLE_NAMES[t]
        short = name if len(name) <= 19 else name[:18] + "…"
        hint = f"{t} — {name}\n{TABLE_HELP[t]}\nOpen the definition, fields and recorded contents."
        parts.append(
            f'<a href="table-{t}.html" aria-label="{esc(hint)}"><g class="node" data-t="{key}">'
            f'<title>{esc(hint)}</title><rect x="{x:.0f}" y="{y:.0f}" width="{bw}" height="{bh}" rx="5"/>'
            f'<text x="{x + bw / 2:.0f}" y="{y + 18:.0f}" class="id">{esc(t)}</text>'
            f'<text x="{x + bw / 2:.0f}" y="{y + 34:.0f}" class="nm">{esc(short)}</text></g></a>'
        )
    parts.append("</svg>")
    return "".join(parts)


def table_overview():
    """Reader-facing story; definitions stay in the linked table dictionary."""
    def item(table_id, label=None):
        return link(f"table-{table_id}.html", esc(label or table_id))

    return (
        '<h2 id="overview">How the tables work together</h2>'
        '<p>The tables connect a scoping question to its evidence, spatial data and recorded decisions. '
        'They make those decisions traceable and usable by software; they do not all perform the same job.</p>'
        f'<p><strong>Define what is being assessed.</strong> {item("T0")} describes each nature-based practice. '
        f'{item("FAM")} groups subpractices into suitability families with shared limiting conditions. '
        f'{item("T7")} identifies the geographic and farming-system contexts in which a rule or finding applies.</p>'
        f'<p><strong>Preserve the evidence behind decisions.</strong> {item("SRCH")} records searches and screening; '
        f'{item("SRC")} catalogues the sources found. {item("EV")} holds individual findings, with their '
        f'quotations, locators and review state. {item("TOOL")} records tools and methods used as sources. '
        'Finding review establishes what an extracted claim can support; it does not approve a resulting recipe.</p>'
        f'<p><strong>Connect findings to variables and maps.</strong> {item("VONT")} defines variable names, '
        f'meanings and units. {item("T1")} catalogues datasets, while {item("BIND")} connects each variable '
        f'to a suitable dataset for its context. {item("XW")} links reported outcomes to analytical targets; '
        'the synthesis still has to justify their scientific relevance.</p>'
        f'<p><strong>Answer the scoping questions.</strong> {item("T4")} records where a practice '
        f'family could fit; {item("T4_RUN")} records suitability execution settings, separately from how '
        f'the mapping was derived. {item("T2")} records climate-risk variables. {item("T3")} records hazard '
        f'responses, keeping protection of livelihoods separate from threats to the investment. '
        f'{item("T5")} defines variables that describe opportunity areas and priorities for locating hotspots. '
        f'{item("T6")} records effects on scorecard priorities, and {item("T6E")} holds indicative economic profiles.</p>'
        '<p>M2b is the '
        + link(chapter_file("m2b-project-risk"), 'investment-risk screening module')
        + ', not a separate table in this edition. Its hazard screen uses T2 and the investment-risk part of T3; '
        'operational findings remain in EV with their own role. Investment-risk screening stays separate from '
        'the priority score.</p>'
        '<p><strong>Turn evidence into accepted outputs.</strong> AI authors new scientific synthesis proposals '
        'from the evidence and configuration. Code validates '
        'the proposal; a human reviewer accepts the exact scientific judgments; code then packages the accepted '
        'values for runtime use without re-rating them.</p>'
        '<p>The '
        + link(chapter_file("effect-synthesis"), 'T3/T6 proposal and acceptance route')
        + ' is implemented. The '
        + link(chapter_file("suitability-synthesis"), 'agent-led T4 workflow')
        + ' is adopted, but its production proposal and packaging route remains outstanding. '
        'Existing T3, T4 and T6 outputs remain historical until explicitly replaced by accepted outputs; new T6E '
        f'synthesis is frozen. {item("BANDS")} preserves historical magnitude classifications and does not '
        'automatically score new AI effect proposals.</p>'
    )


def table_page(table_id):
    spec = TABLES[table_id]
    count, rows = edition_rows(table_id)
    refs = references(table_id)
    by_field = {}
    for field, target, column, literals in refs:
        cell = link(f"table-{target}.html", f"{esc(target)}.{esc(column)}")
        if literals:
            cell += " or one of " + ", ".join(code(x) for x in literals)
        by_field.setdefault(field, []).append(cell)
    enums = spec.get("enum_values") or {}
    field_rows = []
    for rule in ("required", "optional", "conditional", "derived"):
        for field in spec.get(rule) or []:
            allowed = enums.get(field)
            field_rows.append(
                [
                    code(field)
                    + (
                        " <small>(key)</small>"
                        if field == spec.get("primary_key")
                        else ""
                    ),
                    esc(rule),
                    "; ".join(by_field.get(field, [])),
                    ", ".join(code(v) for v in allowed)
                    if isinstance(allowed, list)
                    else (text(str(allowed)) if allowed else ""),
                ]
            )
    used_by = [
        (t, f)
        for t in TABLES
        for f, target, _, _ in references(t)
        if target == table_id and t != table_id
    ]
    facts = dl(
        [
            ("Manifest name", esc(spec["name"])),
            ("One row is identified by", code(spec.get("primary_key"))),
            (
                "Kept",
                "Once per practice"
                if spec.get("per_nbs")
                else "Once for all practices",
            ),
            ("File location", code(spec["location"])),
            ("Rows in this edition", f"{count:,}"),
            (
                "Referenced by",
                ", ".join(
                    link(f"table-{t}.html", f"{esc(t)}.{esc(f)}") for t, f in used_by
                )
                or "No other table",
            ),
            (
                "Explained in",
                ", ".join(
                    link(chapter_file(c), esc(TITLES.get(c, c)))
                    for c in EXPLAINED_IN[table_id]
                ),
            ),
        ]
    )
    body = facts
    if spec.get("note"):
        body += f"<p>{text(spec['note'])}</p>"
    body += '<h2 id="fields">Fields</h2>' + table(
        ["Field", "Rule", "References", "Allowed values"],
        field_rows,
        caption=(f"{esc(table_id)} · current AI scientific output fields" if table_id in {"T3", "T6"}
                 else f"{esc(table_id)} · fields in the frozen column manifest {esc(MANIFEST['manifest_version'])}"),
    )
    body += (
        '<p class="basis">Rules: <em>required</em> present and non-empty on every row; <em>optional</em> may be blank; '
        "<em>conditional</em> required when its trigger holds; <em>derived</em> computed, never authored by hand.</p>"
    )
    section = spec_section(table_id)
    spec_block = ""
    if section:
        spec_block = (
            '<h2 id="spec">Specification text</h2>'
            f'<p class="basis">From the method data-model specification ({link(METHOD_URL + "data-model/spec.md", "spec.md")}'
            + (", section shared with Scorecard effects" if table_id == "T6E" else "")
            + ").</p>"
            + f'<div class="spec">{section}</div>'
        )
        if table_id != "T2":
            body += spec_block
    body += '<h2 id="contents">Contents in this edition</h2>'
    if rows is not None:
        body += csv_table(
            rows, f"{esc(table_id)} · all {count} rows at the pinned revision"
        )
    elif table_id in data.TABLE_TOTALS:
        per = "".join(
            f"<li>{link(f'practice-{p}.html#{table_id}', esc(data.pinned_json(f'schema/recipes/{p}/T0_nbs_registry.json')[0]['nbs_name']))}: "
            f"{data.ROW_COUNTS[(p, table_id)]} rows</li>"
            for p in PRACTICE_IDS
        )
        body += f"<p>{count} rows, shown on the practice pages:</p><ul>{per}</ul>"
        if table_id == "T4":
            example = next(
                r
                for r in data.ROWS
                if r["id"] == "water_harvesting__terracing__annual_precipitation"
            )
            body += f"<p>Worked example row: {link(example['file'], 'annual precipitation for terracing')} (calibration held).</p>"
    else:
        where = {
            "SRC": ("sources.html", "Sources"),
            "EV": ("evidence-base.html", "Evidence base"),
            "VONT": ("variables.html", "Variable ontology"),
            "SRCH": ("searches.html", "Search records"),
        }[table_id]
        body += f"<p>{count:,} rows, shown in {link(where[0], where[1])}.</p>"
    current_toc = []
    if table_id in {"T2", "T5"}:
        policy = json.loads((METHOD / "data-model/priority-contract.json").read_text())
        current = policy["table_fields"][table_id]
        intro = '<h2 id="current-priority">Current classification interface</h2>'
        intro += '<p>' + esc(current["purpose"]) + '</p>'
        if table_id == 'T2':
            intro += '<p>The current T2 registry above implements these definition fields. Classification references remain empty; it supplies no accepted analytical defaults.</p>'
        else:
            intro += '<p>These fields define the new priority configuration. The archived CSV rows below have not been migrated or calibrated. They are not runnable defaults.</p>'
        if table_id != "T2":
            intro += table(["Field", "Meaning"], [[code(k), esc(v)] for k, v in current["fields"].items()],
                           caption=table_id + " · current variable definition")
        intro += table(["Rule field", "Meaning"], [[code(k), esc(v)] for k, v in policy["rule_fields"].items()],
                       caption="Shared problem-classification rule")
        intro += '<p>See ' + link('ch-m3-characterisation.html', 'classification workflow') + ' and ' + link('ch-m4-hotspots.html', 'explicit user weighting') + '. Machine-readable contract: ' + link(METHOD_URL + 'data-model/priority-contract.json', 'priority-contract.json') + '.</p>'
        if table_id == 'T2':
            intro = current_t2.render() + intro + spec_block
        body = intro + '<details><summary>Historical edition fields and records</summary>' + body + '</details>'
        current_toc = ([("current-t2", "Current entries"), ("t2-blockers", "Before use"), ("t2-fields", "Current fields")] if table_id == "T2" else []) + [("current-priority", "Classification interface")]
    page(
        f"table-{table_id}.html",
        "data-model.html",
        f"{TABLE_NAMES[table_id]} ({table_id})",
        body,
        crumbs=[("data-model.html", "Data model"), ("", table_id)],
        lead=f"{badge(table_id)} {esc(TABLE_NAMES[table_id] if table_id == 'T2' else spec['name'])}",
        toc=current_toc + [("fields", "Historical fields" if current_toc else "Fields")]
        + ([("spec", "Specification text")] if section else [])
        + [("contents", "Contents in this edition")],
    )


def build():
    SIDE["data-model.html"] = [
        ("data-model.html", "Tables and relationships"),
        ("variables.html", "Variable ontology"),
        ("datasets.html", "Datasets and bindings"),
        ("rules.html", "Rule tables"),
    ]
    index = []
    for label, ids in GROUPS:
        for t in ids:
            count, _ = edition_rows(t)
            index.append(
                [
                    badge(t),
                    link(f"table-{t}.html", esc(TABLE_NAMES[t])),
                    esc(label),
                    code(TABLES[t].get("primary_key")),
                    f"{count:,}",
                    ", ".join(
                        sorted(
                            {
                                link(f"table-{x[1]}.html", esc(x[1]))
                                for x in references(t)
                                if x[1] != t
                            }
                        )
                    )
                    or "None",
                ]
            )
    rel = []
    for t in TABLES:
        for field, target, column, literals in references(t):
            rel.append(
                [
                    link(f"table-{t}.html", esc(t)),
                    code(field),
                    link(f"table-{target}.html", esc(target)),
                    code(column),
                    ", ".join(code(x) for x in literals),
                ]
            )
    body = (
        table_overview()
        + "<p>The diagram below shows table references, not the order of AI work or review. "
        "Definitions are generated from the pinned structural manifest, with the current T3/T6 scientific "
        "output contract. Row counts describe the historical data edition; they do not count accepted AI proposals.</p>"
        f'<p class="basis">Column manifest {esc(MANIFEST["manifest_version"])} at the pinned revision. '
        f"{len(TABLES)} tables, {sum(len(references(t)) for t in TABLES)} references between them.</p>"
        '<h2 id="diagram">Relationship diagram</h2>'
        f"<figure>{diagram()}<figcaption>Hover over a table for its full name and purpose; select it to open its definition. "
        "Lines show references between tables, not the order of synthesis. "
        "The same relationships are listed below.</figcaption></figure>"
        f'<h2 id="tables">The {len(TABLES)} tables</h2>'
        + table(
            ["", "Table", "Layer", "Key", "Rows in this edition", "References"],
            index,
            caption="Tables, keys and row counts in this edition",
            numeric=(4,),
        )
        + '<h2 id="relationships">Relationships</h2>'
        + table(
            ["Table", "Field", "References table", "Field", "Also allowed literals"],
            rel,
            caption="Every reference declared in the manifest (text equivalent of the diagram)",
        )
    )
    page(
        "data-model.html",
        "data-model.html",
        "Data model",
        body,
        lead=f"{len(TABLES)} tables that hold the method, their fields and how they join.",
        toc=[
            ("overview", "How the tables work together"),
            ("diagram", "Relationship diagram"),
            ("tables", f"The {len(TABLES)} tables"),
            ("relationships", "Relationships"),
        ],
    )
    for t in TABLES:
        table_page(t)

    # Variable ontology
    used = {}
    for r in data.ROWS:
        if r["table"] == "T4":
            used.setdefault(r["raw"]["variable"], []).append(r)
    rows = []
    for vid, v in sorted(data.VONT.items()):
        uses = used.get(vid, [])
        rows.append(
            [
                f'<span id="var-{esc(vid)}"></span>{code(vid)}<br>{text(v.get("label", ""))}',
                esc(v.get("canonical_unit") or ""),
                esc(words(v.get("group_id"))) if v.get("group_id") else "",
                esc(v.get("min_meaningful_resolution_m") or ""),
                "Yes" if v.get("derive_then_aggregate") else "No",
                esc(v.get("context_sensitivity") or ""),
                ", ".join(code(d) for d in v.get("candidate_dataset_ids") or []),
                ", ".join(
                    link(
                        r["file"], esc(r["family"].split("__", 1)[-1].replace("_", " "))
                    )
                    for r in uses
                ),
                text(", ".join(v.get("aliases") or [])),
            ]
        )
    body = (
        "<p>The variable ontology gives each analytical variable one canonical identifier, unit and "
        "definition, so that findings reported under different names and units are harmonised before "
        "synthesis. It also carries the resolution rule for each variable: the coarsest grid at which the "
        "variable still means something, and whether it must be derived at native resolution before "
        "aggregation. Context sensitivity marks nationally derived variables for which a scoping output "
        "should recommend a country-endorsed source.</p>"
        '<p><label for="vf">Filter variables</label> <input id="vf" type="search" data-filter="vont" placeholder="for example slope, rainfall, tenure"></p>'
        + table(
            [
                "Variable",
                "Unit",
                "Group",
                "Minimum meaningful resolution (m)",
                "Derive then aggregate",
                "Context sensitivity",
                "Candidate datasets",
                "Site-suitability mappings using it",
                "Aliases harmonised to it",
            ],
            rows,
            caption=f"Variable ontology · {len(rows)} variables at the pinned revision",
            ident="vont",
            numeric=(3,),
        )
    )
    page(
        "variables.html",
        "data-model.html",
        "Variable ontology",
        body,
        crumbs=[("data-model.html", "Data model"), ("", "Variable ontology")],
        lead="Canonical variables, units, resolution rules and context sensitivity.",
    )

    # Datasets and bindings
    t1 = [
        [
            f'<span id="ds-{esc(d["dataset_id"])}"></span>{code(d["dataset_id"])}<br>{text(d.get("dataset_name", ""))}',
            esc(words(d.get("analytical_module")))
            if d.get("analytical_module")
            else "",
            esc(d.get("time_period", "")),
            esc(d.get("spatial_resolution_m", "")),
            esc(words(d.get("access_type"))) if d.get("access_type") else "",
            esc(d.get("license", "")),
            text(d.get("limitations", "")),
            esc(d.get("citation", "")),
        ]
        for d in data.T1.values()
    ]
    bind = [
        [
            link(f"variables.html#var-{esc(b['variable'])}", code(b["variable"])),
            esc(words(b["scope_type"]))
            + (f": {esc(b['scope_id'])}" if b.get("scope_id") else ""),
            link(f"#ds-{esc(b['dataset_id'])}", code(b["dataset_id"]))
            if b["dataset_id"] in data.T1
            else code(b["dataset_id"]),
            esc(b.get("preference_rank", "")),
            esc(words(b.get("status"))),
            text(b.get("fitness_note", "")),
        ]
        for b in data.BIND
    ]
    body = (
        "<p>Datasets are chosen for fitness first and platform second. Where an equally fit dataset is "
        "hosted server-side, that version is preferred so that cropping and resampling happen before "
        "transfer. A global recipe binds each variable to a default dataset; country, zone or region "
        "bindings refine it, and the most specific context wins. A binding marked as requiring upload "
        "tells the user that a better local dataset should be supplied. See "
        f"{link('ch-farming-systems-and-data.html', 'Farming systems, contexts and data')}.</p>"
        '<h2 id="registry">Data registry</h2>'
        + table(
            [
                "Dataset",
                "Module",
                "Period",
                "Resolution (m)",
                "Access",
                "Licence",
                "Limitations",
                "Citation",
            ],
            t1,
            caption=f"Data registry (T1) · {len(t1)} datasets",
            numeric=(3,),
        )
        + '<h2 id="bindings">Dataset bindings</h2>'
        + table(
            [
                "Variable",
                "Scope",
                "Dataset",
                "Preference rank",
                "Status",
                "Fitness note",
            ],
            bind,
            caption=f"Dataset bindings (BIND) · {len(bind)} bindings",
            numeric=(3,),
        )
    )
    page(
        "datasets.html",
        "data-model.html",
        "Datasets and bindings",
        body,
        crumbs=[("data-model.html", "Data model"), ("", "Datasets and bindings")],
        lead="Every registered dataset, with its limits, and the binding of variables to datasets by context.",
        toc=[("registry", "Data registry"), ("bindings", "Dataset bindings")],
    )

    # Rule tables (lookups)
    parts, toc = [], []
    for path in pinned_list("schema/lookups"):
        if not path.endswith(".csv"):
            continue
        name = path.split("/")[-1][:-4]
        rows = pinned_csv(path)
        toc.append((name, words(name)))
        block = csv_table(
            rows,
            f'<a href="{CIAT_URL}{esc(path)}"><code>{esc(path)}</code></a> · {len(rows)} rows',
        )
        if len(rows) > 40:
            block = f"<details><summary>Show all {len(rows)} rows</summary>{block}</details>"
        parts.append(f'<h2 id="{esc(name)}">{esc(words(name))}</h2>{block}')
    body = (
        "<p>Small deterministic tables read by the synthesis and display code. They hold the weights, "
        "matrices, policies and vocabularies that would otherwise be buried in code. Each is shown in "
        "full from the pinned revision. The chapters explain how each is used: "
        f"{link('ch-effect-synthesis.html', 'effect synthesis')}, {link('ch-suitability-synthesis.html', 'suitability synthesis')}, "
        f"{link('ch-extraction.html', 'extraction')} and {link('ch-m5-scorecard.html', 'the scorecard')}. "
        f"The magnitude bands and the outcome crosswalk are registers with their own pages: "
        f"{link('table-BANDS.html', 'BANDS')}, {link('table-XW.html', 'XW')}.</p>"
        + "".join(parts)
    )
    page(
        "rules.html",
        "data-model.html",
        "Rule tables",
        body,
        crumbs=[("data-model.html", "Data model"), ("", "Rule tables")],
        lead="Weights, matrices, policies and vocabularies, shown in full.",
        toc=toc,
    )
