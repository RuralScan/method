"""Render the pinned field dictionary, its declared joins and the module walkthrough."""

import hashlib
import json
import re
import subprocess
from html import escape

METHOD = "247d5cf98d3dd6daf010aa5bfe51fad21ea35849"
PRODUCER = "e5c8da02e72810956cfd179cb32cd137fc4ba398"
BASE = f"https://github.com/RuralScan/method/blob/{METHOD}/data-model"
SOURCE = f"https://github.com/CIAT/nbs_ruralscan/blob/{PRODUCER}/schema"
MODULES = [
    (
        "M0",
        "Setup and scope",
        "Which investment question and landscape will the scan address?",
        "T0 FAM T7 T1 BIND",
        "Choose the practice, family, area, dates, spatial product and input bindings.",
        "An analysis boundary and an explicit decision question.",
        "Record unresolved local inputs before interpreting coverage.",
    ),
    (
        "M1",
        "Opportunity space",
        "Where could this family be considered?",
        "T4 FAM VONT T1 T7",
        "Combine supported biophysical and host-system requirements with hard exclusions.",
        "Candidate locations, exclusions and unknowns.",
        "A held calibration leaves its score unassigned. Linear practices require corridor reporting.",
    ),
    (
        "M2",
        "Rural livelihood risk",
        "Where are rural livelihoods exposed to climate hazards?",
        "T1 T2",
        "Combine baseline or future hazard with livelihood exposure for the chosen period.",
        "A layer of climate-related need.",
        "Adding vulnerability indicators again in the priority index would double count them.",
    ),
    (
        "M2b",
        "Project risk screen",
        "What could threaten this investment?",
        "T2 T3",
        "Screen asset exposure and sensitivity, then consider operational barriers such as access and tenure.",
        "Project-risk flags and implementation questions.",
        "Keep these filters separate from the livelihood-priority score.",
    ),
    (
        "M3",
        "Characterise opportunities",
        "Which people and production systems overlap candidate areas?",
        "T1 T5",
        "Summarise priority and descriptor variables inside the opportunity space.",
        "Counts and distributions with units and denominators.",
        "Report missing coverage and spatial support.",
    ),
    (
        "M4",
        "Priority hotspots",
        "Which areas rank highly for the chosen priorities?",
        "T5",
        "Select eligible priorities, group correlated variables and vary weights.",
        "Ranked areas with sensitivity to assumptions.",
        "Country-level indicators can flag context but cannot distinguish sites within a country.",
    ),
    (
        "M5",
        "Compare practice responses",
        "What benefits, costs and trade-offs does the evidence support?",
        "T3 T6 T6E",
        "Read effect direction, strength, confidence and scope alongside economic units.",
        "A comparison of practice responses and evidence gaps.",
        "Indicative costs require local assumptions for a feasibility assessment.",
    ),
    (
        "M6",
        "Implementation handoff",
        "What should the project team check locally?",
        "T0 T6 T6E",
        "Pass the shortlist, evidence holds and local checks to the country team.",
        "Questions for site, tenure, safeguard and engineering assessment.",
        "Country maps and reproducible runs belong to the separate runtime pilot.",
    ),
]
GRAINS = {
    "T0": "One practice and its implementation profile.",
    "T1": "One catalogued dataset, access route and limitations.",
    "T2": "One shared climate-risk variable or formulation.",
    "T3": "One hazard-response assessment at its recorded practice, family, farming system and scope.",
    "T4": "One mapping from an input variable to a family’s suitability relationship.",
    "T5": "One opportunity-space priority or descriptor.",
    "T6": "One assessed effect on a scorecard priority in its recorded scope.",
    "T6E": "One scoped economic indicator with its value, unit and evidence.",
    "T7": "One geographic or farming-system context.",
    "SRC": "One catalogued source.",
    "EV": "One located finding from a source.",
    "VONT": "One canonical analytical variable.",
    "BIND": "One dataset assignment for a variable and context.",
    "FAM": "One registered subpractice or cross-family entry. Several entries can share a family ID.",
    "TOOL": "One documented tool or method.",
    "SRCH": "One logged search protocol within a run and scope.",
    "XW": "One route from an evidence outcome to an analytical target.",
    "BANDS": "One set of magnitude bands for an effect metric.",
    "T4_NUMERIC_POLICY": "One evidence-specific decision governing numeric compilation.",
    "T4_RUN": "One approved input or setting for a suitability run.",
}


def link(url, label):
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def badge(key):
    colour = key if key in {f"T{i}" for i in range(8)} | {"T6E"} else "register"
    return f'<a class="badge" data-ruralscan-table="{colour}" href="table-{key}.html">{key}</a>'


def definitions(spec):
    fields = {}
    table = None
    for line in spec.splitlines():
        header = re.match(
            r"^#{2,3} (T[0-7]|SRC|EV|VONT|FAM|BIND|TOOL|XW|BANDS|T4_RUN) [—–]", line
        )
        if header:
            table = header[1]
        parts = re.split(r"(?<!\\)\|", line.strip("|"))
        field = re.fullmatch(r"\s*`(\w+)`\s*", parts[0])
        if table and field and len(parts) >= 4:
            fields[table, field[1]] = re.sub(
                r"[`*]", "", parts[3].replace(r"\|", " | ").strip()
            )
    return fields


def generate(method, ciat, write):
    model = method / "data-model"
    for relative, digest in json.loads(
        (model / "definition-snapshot.json").read_text()
    )["sha256"].items():
        if hashlib.sha256((method / relative).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Definition mismatch: {relative}")
    manifest = json.loads((model / "structure/columns.json").read_text())["tables"]
    fields = definitions((model / "spec.md").read_text())
    cards = []
    for key, title, question, inputs, operation, output, limit in MODULES:
        example = {
            "M2b": "synthesis-t3.html",
            "M5": "synthesis-t6.html",
            "M6": "recipe-water_harvesting_conservation.html",
        }.get(key, "terrace.html")
        handoff = (
            link(
                "https://nbviewer.org/github/RuralScan/runtime/blob/e690d4e413d925c28c273945a5268ddbfb2d67cc/notebooks/01_agroforestry.ipynb",
                "Country pilot handoff · Haiti first-pass notebook",
            )
            if key == "M6"
            else ""
        )
        cards.append(
            f'<article id="{key}"><h2>{key} · {title}</h2><p class="lead">{question}</p><p>{" ".join(badge(k) for k in inputs.split())}</p><dl><dt>Operation</dt><dd>{operation}</dd><dt>Output</dt><dd>{output}</dd><dt>Limit</dt><dd>{limit}</dd></dl>{link(example, "Follow a practice example")} {handoff}</article>'
        )
    write(
        "methods.html",
        "Methods",
        "Scan method",
        '<p class="lead">Follow one investment question from scope to implementation handoff.</p><nav class="choices">'
        + "".join(link("#" + m[0], m[0] + " · " + m[1]) for m in MODULES)
        + "</nav>"
        + "".join(cards),
    )
    entries, relations = [], []
    for key, t in manifest.items():
        name = t["name"]
        joins = []
        for field, target in t.get("fk", {}).items():
            targets = [target] if isinstance(target, str) else target.get("targets", [])
            for target_field in targets:
                dest = target_field.split(".")[0]
                if dest not in manifest:
                    raise ValueError(target_field)
                joins.append(
                    "<li><code>"
                    + escape(field)
                    + "</code> → "
                    + link("table-" + dest + ".html", target_field)
                    + "</li>"
                )
        if joins:
            relations.append(
                f"<details><summary>{key} · {escape(name)}</summary><ul>{''.join(joins)}</ul></details>"
            )
        rows = []
        for status in ["required", "optional", "conditional", "derived"]:
            for field in t.get(status, []):
                desc = fields.get((key, field), "")
                if key == "T6E" and not desc:
                    desc = fields.get(("T6", field), "")
                enums = t.get("enum_values", {}).get(field, [])
                if enums:
                    desc += " Allowed values: " + ", ".join(map(str, enums)) + "."
                rows.append(
                    f'<tr><th scope="row">{escape(field)}</th><td>{status}</td><td>{escape(desc) or "See pinned field specification."}</td></tr>'
                )
        location = (
            t["location"]
            .replace("<nbs_id>", "water_harvesting_conservation")
            .replace("{csv,json}", "csv")
        )
        module_refs = " · ".join(
            link("methods.html#" + m[0], m[0]) for m in MODULES if key in m[3].split()
        )
        examples = {
            "T4": "terrace.html",
            "T3": "synthesis-t3.html",
            "T6": "synthesis-t6.html",
            "T6E": "synthesis-t6e.html",
            "EV": "evidence.html",
            "SRCH": "searches.html",
            "FAM": "recipes.html",
        }
        source = link(f"{SOURCE}/{location}", "Producer CSV")
        # Some policies are populated for only selected practices.
        if key == "T4_RUN":
            source = link(
                f"{SOURCE}/recipes/agroforestry/T4_run_policy.csv",
                "Agroforestry policy CSV",
            )
        grain = GRAINS[key]
        entries.append(
            f"<li data-filter-item>{badge(key)} {link('table-' + key + '.html', name)}<p>{grain}</p></li>"
        )
        write(
            f"table-{key}.html",
            "Methods",
            name,
            f'<p>{badge(key)}</p><p class="lead">{grain}</p><dl><dt>Primary key</dt><dd><code>{escape(str(t["primary_key"]))}</code></dd><dt>Storage</dt><dd>{escape(t["location"])}</dd><dt>Use in the method</dt><dd>{module_refs or "Upstream evidence, configuration or compilation."}</dd></dl><p>{link(examples[key], "Inspect the example") + " · " if key in examples else ""}{source} · {link(BASE + "/spec.md", "Pinned field specification")}</p><h2>Declared relationships</h2><ul>{"".join(joins) or "<li>No foreign key declared in this manifest.</li>"}</ul><h2>Fields</h2><div class="scroll"><table><thead><tr><th>Field</th><th>Requirement</th><th>Meaning and units where specified</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>',
        )
    lookups = subprocess.check_output(
        [
            "git",
            "-C",
            str(ciat),
            "ls-tree",
            "--name-only",
            PRODUCER + ":schema/lookups",
        ],
        text=True,
    ).splitlines()
    policies = "".join(
        "<li>"
        + link(f"{SOURCE}/lookups/{p}", p.removesuffix(".csv").replace("_", " "))
        + "</li>"
        for p in lookups
        if p.endswith(".csv")
    )
    write(
        "dictionary.html",
        "Methods",
        "Table dictionary",
        '<p class="lead">Find what one record represents, its fields and where it joins other records.</p><p>The historical interface calls shared climate-risk formulation T2a. Its physical table is T2. The candidate manifest declares no T2b table.</p><label>Find a table <input type="search" data-filter placeholder="Name, code or purpose"></label><ul class="catalog">'
        + "".join(entries)
        + "</ul><h2>Producer lookups and policy files</h2><ul>"
        + policies
        + "</ul>",
    )
    chain = " → ".join(badge(k) for k in ["T4", "EV", "SRC"])
    write(
        "model.html",
        "Methods",
        "Data model",
        f'<p class="lead">A recipe records the compiled decision. Its evidence IDs lead to findings, each with a source and locator.</p><figure><p class="chain">{chain}</p><figcaption>A mapping may cite several evidence units. Each finding identifies its source. Multiple subpractices can share the same suitability family.</figcaption></figure><p>{link("terrace.html", "Trace the bench-terrace mapping")}</p><h2>Declared field joins</h2><p>Arrows lead from the referencing field to its target in the pinned manifest. Enumerated literals also occur in context and economic keys. The manifest does not assert a unique family record for every family ID.</p>'
        + "".join(relations)
        + f"<p>{link(BASE + '/structure/columns.json', 'Definition manifest')} · {link('https://github.com/CIAT/nbs_ruralscan/blob/bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06/docs/erd.html', 'Historical ERD source')}</p>",
    )
