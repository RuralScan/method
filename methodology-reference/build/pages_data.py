"""Data access: downloads, field guide, tested query recipes and machine-readable entry points.

The published data package is the single copy of the edition tables. This module links to it,
renders its own field definitions, and runs every query shown on the page against it. Nothing
about the tables is retyped here except short reading notes, which are marked as such.
"""

import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import data
from core import (
    CATALOG_URL,
    CIAT_RAW,
    CIAT_URL,
    EDITION_CATALOG_URL,
    EVIDENCE,
    EVIDENCE_RAW,
    EVIDENCE_REV,
    EVIDENCE_URL,
    FILES,
    PACKAGE_BASE,
    PACKAGE_DIR,
    PACKAGE_EDITION,
    PACKAGE_SHA256,
    PACKAGE_URL,
    PRACTICE_IDS,
    PRODUCER,
    RELEASE,
    TABLE_NAMES,
    code,
    esc,
    link,
    page,
    pinned,
    pinned_csv,
    pinned_exists,
    pinned_list,
    practice_name,
    source_file,
    table,
    words,
)

CHECKS = []  # (name, passed, detail), read by the build
TERRACE = "water_harvesting__terracing__annual_precipitation"
ROW_TABLE_FILES = {
    "T0": "T0_nbs_registry",
    "T3": "T3_nbs_hazard_farming",
    "T4": "T4_suitability_mappings",
    "T6": "T6_nbs_scorecard",
    "T6E": "T6E_economic_profile",
}
REGISTERS = {
    "SRC": "SRC_source_register",
    "EV": "EV_evidence_register",
    "SRCH": "SRCH_search_register",
    "VONT": "VONT_variable_ontology",
    "FAM": "FAM_family_registry",
    "BIND": "BIND_dataset_binding",
    "XW": "XW_target_crosswalk",
    "BANDS": "BANDS_magnitude_bands",
    "TOOL": "TOOL_tool_registry",
}
CONFIG = {
    "T1": "T1_data_registry",
    "T2": "T2_climate_risk",
    "T5": "T5_opportunity_space",
    "T7": "T7_geographic_context",
}
# Reading note for each table of the package: what one row is. The field definitions
# themselves are rendered from the package descriptor.
ONE_ROW = {
    "sources": "One registered source.",
    "findings": "One extracted finding, with its review status at this edition.",
    "records": "One hazard, suitability or scorecard row. The index that the three row tables join to.",
    "t3": "One hazard rating.",
    "t4": "One suitability mapping.",
    "t6": "One scorecard rating.",
    "record-findings": "One link from a row to a finding, with the kind of link.",
    "context-sources": "One link from a row to a source cited for context.",
    "queue": "One unresolved review task: a finding that can change a rating, or a held calibration.",
    "coverage": "One count of review status, with its denominator.",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def view(name):
    return name.replace("-", "_")


def size(n):
    return (
        f"{n / 1_000_000:.1f} MB" if n >= 1_000_000 else f"{max(n / 1000, 0.1):.0f} kB"
    )


def load_package():
    descriptor_file = PACKAGE_DIR / "datapackage.json"
    if not descriptor_file.is_file():
        raise SystemExit(
            f"The published data package is not in {PACKAGE_DIR}.\n"
            "Run: python3 build/fetch_package.py"
        )
    raw = descriptor_file.read_bytes()
    descriptor = json.loads(raw)
    changed = [] if sha(raw) == PACKAGE_SHA256 else ["datapackage.json"]
    tables = {}
    for resource in descriptor["resources"]:
        body = (PACKAGE_DIR / resource["path"]).read_bytes()
        if "sha256:" + sha(body) != resource["hash"]:
            changed.append(resource["path"])
        tables[resource["name"]] = list(
            csv.DictReader(io.StringIO(body.decode("utf-8"), newline=""))
        )
    catalog = json.loads((PACKAGE_DIR / "catalog.json").read_text())
    return descriptor, tables, catalog, changed


# ---------------------------------------------------------------- query recipes


def setup_sql(resources):
    lines = [
        "-- DuckDB. Each view reads one table of this edition from its published address."
    ]
    for r in resources:
        lines.append(
            f"CREATE VIEW {view(r['name'])} AS FROM read_csv('{PACKAGE_BASE}{r['path']}');"
        )
    return "\n".join(lines)


SQL = [
    {
        "id": "trace",
        "title": "Follow one row back to its findings and sources",
        "why": "The basic join. A row links to findings, and each finding names its source and where in the source it sits.",
        "sql": f"""SELECT rf.kind, f.evidence_id, f.status, f.page, s.source_id, s.citation
FROM records r
JOIN record_findings rf USING (record_id)
JOIN findings f USING (evidence_id)
JOIN sources s USING (source_id)
WHERE r.record_id = '{TERRACE}'
ORDER BY rf.kind, f.evidence_id;""",
        "reading": "One finding is cited directly and two give context. None has an applied human decision at this edition.",
    },
    {
        "id": "status",
        "title": "Tell an unreviewed finding from a signed-off one",
        "why": "Most findings behind the rows have no applied human decision yet. Count them by table before relying on a rating.",
        "sql": """SELECT r."table", f.status, count(DISTINCT f.evidence_id) AS findings
FROM records r
JOIN record_findings rf USING (record_id)
JOIN findings f USING (evidence_id)
WHERE rf.kind = 'direct'
GROUP BY ALL
ORDER BY 1, 2;""",
        "reading": "A finding cited by rows in two tables is counted under both.",
    },
    {
        "id": "provisional",
        "title": "Tell a provisional rating from an excluded finding",
        "why": "A rating is provisional when a finding that can change it is still unreviewed or held. An excluded finding is different: it has been dropped and no row cites it.",
        "sql": """SELECT t.record_id, t.rating, t.confidence,
       count(*) FILTER (f.status IN ('unreviewed', 'held')) AS unresolved_setters
FROM t3 t
JOIN record_findings rf USING (record_id)
JOIN findings f USING (evidence_id)
WHERE t.provisional AND rf.kind = 'setter'
GROUP BY ALL
ORDER BY unresolved_setters DESC, t.record_id
LIMIT 5;""",
        "reading": "The five hazard ratings with the most unresolved rating-setting findings.",
    },
    {
        "id": "excluded",
        "title": "Confirm that no row rests on an excluded finding",
        "why": "Excluded findings stay in the table for their history. This shows that none is linked to a row.",
        "sql": """SELECT f.status, f.excluded, count(*) AS findings,
       count(rf.evidence_id) AS links_to_rows
FROM findings f
LEFT JOIN record_findings rf USING (evidence_id)
GROUP BY ALL
ORDER BY 1;""",
        "reading": "A finding linked to several rows adds several links, so links can exceed findings.",
    },
    {
        "id": "calibration",
        "title": "Tell a held calibration from evidence of observed use",
        "why": "A source can record where a practice is used without supporting a score. The mapping then keeps the observed range and holds the numerical calibration.",
        "sql": f"""SELECT t.calibration, t.function_selected, f.evidence_id, f.status,
       json_extract_string(f.reported, '$.abs_min') AS used_from,
       json_extract_string(f.reported, '$.abs_max') AS used_to,
       json_extract_string(f.reported, '$.unit') AS unit
FROM t4 t
JOIN record_findings rf USING (record_id)
JOIN findings f USING (evidence_id)
WHERE t.record_id = '{TERRACE}' AND rf.kind = 'direct';""",
        "reading": "The use range is recorded evidence. The calibration is held and no function is selected, so there is no score.",
    },
    {
        "id": "reconcile",
        "title": "Check that the published totals match the tables",
        "why": "The coverage table states totals with denominators. Recount them from the findings table.",
        "sql": """SELECT c.status, c."count" AS published, n.counted, c.denominator
FROM coverage c
JOIN (SELECT status, count(*) AS counted FROM findings GROUP BY status) n USING (status)
WHERE c."group" = 'EV'
ORDER BY 1;""",
        "reading": "Published and recounted totals agree.",
    },
    {
        "id": "context",
        "title": "See how much study context is recorded",
        "why": "Geography on a finding describes where the study was done, not where the practice might apply. Check how often it is recorded before filtering on it.",
        "sql": """SELECT count(*) AS findings,
       count(study_context) AS with_study_context,
       count(json_extract_string(study_context, '$.study_country')) AS with_study_country
FROM findings;""",
        "reading": "Study country is recorded on few findings in this edition. A filter on it would discard most of the evidence.",
    },
]

PYTHON = f'''import hashlib
import io
import json
import urllib.request

import pandas as pd

base = "{PACKAGE_BASE}"


def fetch(name):
    with urllib.request.urlopen(base + name) as response:
        return response.read()


package = json.loads(fetch("datapackage.json"))
tables = {{}}
for resource in package["resources"]:
    raw = fetch(resource["path"])
    # Stop if a file is not the one the package describes.
    assert "sha256:" + hashlib.sha256(raw).hexdigest() == resource["hash"], resource["path"]
    tables[resource["name"]] = pd.read_csv(io.BytesIO(raw)).convert_dtypes()

row = "{TERRACE}"
trace = (
    tables["record-findings"]
    .query("record_id == @row")
    .merge(tables["findings"], on="evidence_id")
    # The sources table has its own `kind` column (document type), so take only what is needed.
    .merge(tables["sources"][["source_id", "citation"]], on="source_id")
    .sort_values(["kind", "evidence_id"])
)
print(trace[["kind", "evidence_id", "status", "page", "source_id"]].to_string(index=False))
mapping = tables["t4"].set_index("record_id").loc[row]
print("calibration:", mapping["calibration"], "| function selected:", mapping["function_selected"])
'''

R = f'''base <- "{PACKAGE_BASE}"
read <- function(name) read.csv(paste0(base, name), na.strings = "", stringsAsFactors = FALSE)

links <- read("record-findings.csv")
findings <- read("findings.csv")
sources <- read("sources.csv")
t4 <- read("t4.csv")

row <- "{TERRACE}"
# The sources table has its own `kind` column (document type), so take only what is needed.
trace <- merge(links[links$record_id == row, ], findings, by = "evidence_id")
trace <- merge(trace, sources[, c("source_id", "citation")], by = "source_id")
trace <- trace[order(trace$kind, trace$evidence_id), ]
print(trace[, c("kind", "evidence_id", "status", "page", "source_id")], row.names = FALSE)
print(t4[t4$record_id == row, c("calibration", "function_selected")], row.names = FALSE)
'''


def run_sql(resources):
    try:
        import duckdb
    except ImportError:
        raise SystemExit(
            "The query recipes are run at build time and need DuckDB and pandas.\n"
            "Run: uv run --with markdown --with duckdb --with pandas python3 -B build/build.py --out site"
        ) from None
    con = duckdb.connect()
    con.execute(setup_sql(resources).replace(PACKAGE_BASE, str(PACKAGE_DIR) + "/"))
    out = {}
    for recipe in SQL:
        result = con.execute(recipe["sql"])
        out[recipe["id"]] = ([d[0] for d in result.description], result.fetchall())
    con.close()
    return out, duckdb.__version__


def run_script(command, script, base, suffix):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"recipe{suffix}"
        path.write_text(script.replace(PACKAGE_BASE, base))
        done = subprocess.run(
            [*command, str(path)],
            capture_output=True,
            text=True,
            check=False,
            timeout=600,
        )
    if done.returncode:
        return False, done.stderr.strip()[-600:]
    return True, done.stdout.rstrip()


def cell(value):
    if value is None:
        return '<span class="none">blank</span>'
    if isinstance(value, bool):
        return "true" if value else "false"
    return esc(value)


def result_table(columns, rows, caption):
    numeric = tuple(
        i
        for i in range(len(columns))
        if rows
        and all(
            isinstance(r[i], (int, float)) and not isinstance(r[i], bool) for r in rows
        )
    )
    return table(
        [code(c) for c in columns],
        [[cell(v) for v in r] for r in rows],
        caption=caption,
        numeric=numeric,
        cls="result",
    )


# ---------------------------------------------------------------- native files


def asset(ident, title, path, dictionary=None, practice=None):
    raw = pinned(path)
    entry = {
        "id": ident,
        "title": title,
        "path": path,
        "url": CIAT_RAW + path,
        "mediaType": "text/csv" if path.endswith(".csv") else "application/json",
        "bytes": len(raw),
        "sha256": sha(raw),
    }
    if path.endswith(".csv"):
        entry["rows"] = len(pinned_csv(path))
    if dictionary:
        entry["dictionary"] = dictionary
    if practice:
        entry["practice"] = practice
    return entry


def native_assets():
    recipe, registers, config, rules = [], [], [], []
    for t, stem in ROW_TABLE_FILES.items():
        for p in PRACTICE_IDS:
            path = f"schema/recipes/{p}/{stem}.csv"
            if pinned_exists(path):
                recipe.append(
                    asset(
                        f"{t}:{p}",
                        f"{TABLE_NAMES[t]}, {practice_name(p)}",
                        path,
                        f"table-{t}.html",
                        p,
                    )
                )
    for t, stem in REGISTERS.items():
        registers.append(
            asset(t, TABLE_NAMES[t], f"schema/registers/{stem}.csv", f"table-{t}.html")
        )
    for t, stem in CONFIG.items():
        config.append(asset(t, TABLE_NAMES[t], f"schema/{stem}.csv", f"table-{t}.html"))
    for path in pinned_list("schema/lookups"):
        if path.endswith(".csv"):
            name = path.rsplit("/", 1)[-1][:-4]
            rules.append(asset(f"rule:{name}", words(name), path))
    return recipe, registers, config, rules


def later_registers():
    manifest = json.loads((EVIDENCE / "registers/manifest.json").read_text())
    rows = []
    for path, meta in manifest["files"].items():
        if path.startswith("schema/registers/"):
            stem = path.rsplit("/", 1)[-1].split("_", 1)[0]
            rows.append(
                {
                    "id": stem,
                    "path": "registers/" + path,
                    "url": EVIDENCE_RAW + "registers/" + path,
                    "rows": meta.get("rows"),
                    "bytes": meta["bytes"],
                    "sha256": meta["sha256"],
                }
            )
    return manifest, rows


# ---------------------------------------------------------------- pages


def downloads_table(resources, tables):
    rows = []
    for r in resources:
        digest = r["hash"].split(":", 1)[1]
        rows.append(
            [
                f"<strong>{esc(r['title'])}</strong><br><small>{esc(ONE_ROW[r['name']])}</small>",
                f"{len(tables[r['name']]):,}",
                size(r["bytes"]),
                link(PACKAGE_BASE + r["path"], code(r["path"])),
                f'<code title="SHA-256 {digest}">{digest[:12]}…</code>',
                link(f"data-guide.html#t-{r['name']}", "Fields"),
            ]
        )
    return table(
        ["Table", "Rows", "Size", "Download", "SHA-256", "What the fields mean"],
        rows,
        caption=f"Edition {esc(PACKAGE_EDITION)} · ten CSV files, UTF-8, comma-separated, one header row",
        numeric=(1, 2),
        ident="downloads",
    )


def field_table(resource, tables):
    rows = []
    data_rows = tables[resource["name"]]
    for f in resource["schema"]["fields"]:
        allowed = ""
        enum = f.get("constraints", {}).get("enum")
        if enum:
            counts = Counter(r[f["name"]] for r in data_rows)
            allowed = "<br>".join(f"{code(v)} · {counts.get(v, 0):,}" for v in enum)
        elif f["type"] == "boolean":
            counts = Counter(r[f["name"]] for r in data_rows)
            allowed = "<br>".join(
                f"{label} · {counts.get(raw, 0):,}"
                for raw, label in (("True", "true"), ("False", "false"), ("", "blank"))
                if counts.get(raw)
            )
        rows.append(
            [
                code(f["name"]),
                esc(f["type"]),
                "Yes" if f.get("constraints", {}).get("required") else "No",
                esc(f.get("description", "")),
                allowed,
            ]
        )
    return table(
        [
            "Field",
            "Type",
            "Always filled",
            "Definition in the package",
            "Values and counts",
        ],
        rows,
        cls="fields",
    )


def keys(schema):
    primary = schema.get("primaryKey")
    primary = primary if isinstance(primary, list) else [primary]
    return " + ".join(code(k) for k in primary if k)


def build():
    descriptor, tables, catalog, changed = load_package()
    resources = descriptor["resources"]
    by_name = {r["name"]: r for r in resources}
    CHECKS.append(
        (
            "The published data package matches its catalogued digest, and each table matches the digest in the package",
            not changed,
            ", ".join(changed) or f"{len(resources)} tables and the descriptor",
        )
    )
    CHECKS.append(
        (
            "The data package is built from the producer revision this reference uses",
            descriptor["producerRevision"] == PRODUCER,
            descriptor["producerRevision"][:12],
        )
    )

    # Reconcile the package with the registers and rows this reference reads directly.
    mine = {
        t: {r["id"] for r in data.ROWS if r["table"] == t} for t in ("T3", "T4", "T6")
    }
    theirs = {
        t: {r["record_id"] for r in tables["records"] if r["table"] == t}
        for t in ("T3", "T4", "T6")
    }
    excluded = {f["evidence_id"] for f in tables["findings"] if f["excluded"] == "True"}
    dropped = {u["evidence_id"] for u in data.EV if not data.retained(u)}
    differences = []
    if {f["evidence_id"] for f in tables["findings"]} != set(data.EV_BY_ID):
        differences.append("finding identifiers")
    if {s["source_id"] for s in tables["sources"]} != set(data.SRC_BY_ID):
        differences.append("source identifiers")
    differences += [f"{t} row identifiers" for t in mine if mine[t] != theirs[t]]
    if excluded != dropped:
        differences.append(
            f"excluded findings ({len(excluded)} in the package, {len(dropped)} dropped in the register)"
        )
    CHECKS.append(
        (
            "Package findings, sources, rows and exclusions equal the registers and tables at the pinned revision",
            not differences,
            "; ".join(differences)
            or f"{len(tables['findings']):,} findings, {len(tables['sources']):,} sources, "
            f"{len(tables['records']):,} rows, {len(excluded):,} excluded",
        )
    )

    results, duck = run_sql(resources)
    py_ok, py_out = run_script(
        [sys.executable], PYTHON, PACKAGE_DIR.as_uri() + "/", ".py"
    )
    rscript = shutil.which("Rscript")
    r_ok, r_out = (
        run_script([rscript, "--vanilla"], R, str(PACKAGE_DIR) + "/", ".R")
        if rscript
        else (None, "")
    )
    CHECKS.append(
        (
            "Every query recipe runs against the pinned tables",
            py_ok and r_ok is not False and all(rows for _, rows in results.values()),
            (py_out if not py_ok else r_out if r_ok is False else "")
            or f"{len(SQL)} SQL recipes, Python"
            + (", R" if r_ok else " (R not installed here, R recipe not run)"),
        )
    )

    recipe, registers, config, rules = native_assets()
    manifest, later = later_registers()
    total_bytes = sum(r["bytes"] for r in resources)

    # ------------------------------------------------------------ landing page
    stats = (
        '<div class="stats">'
        f"<div><b>{len(tables['sources']):,}</b><span>sources</span></div>"
        f"<div><b>{len(tables['findings']):,}</b><span>findings</span></div>"
        f"<div><b>{len(tables['records']):,}</b><span>hazard, suitability and scorecard rows</span></div>"
        f"<div><b>{len(tables['record-findings']):,}</b><span>row-to-finding links</span></div>"
        f"<div><b>{size(total_bytes)}</b><span>in ten CSV files</span></div></div>"
    )
    matrix = []
    for t in ROW_TABLE_FILES:
        cells = [f"{esc(TABLE_NAMES[t])} ({esc(t)})"]
        for p in PRACTICE_IDS:
            hit = next((a for a in recipe if a["id"] == f"{t}:{p}"), None)
            cells.append(link(hit["url"], f"CSV · {hit['rows']:,}") if hit else "")
        cells.append(link(f"table-{t}.html", "Fields"))
        matrix.append(cells)

    def native_rows(assets):
        return [
            [
                f"{esc(a['title'])} ({esc(a['id'])})",
                f"{a['rows']:,}",
                size(a["bytes"]),
                link(a["url"], "CSV"),
                f'<code title="SHA-256 {a["sha256"]}">{a["sha256"][:12]}…</code>',
                link(a["dictionary"], "Fields"),
            ]
            for a in assets
        ]

    in_package = {"T3", "T4", "T6", "SRC", "EV"}
    study_country = sum(
        1 for f in tables["findings"] if '"study_country"' in f["study_context"]
    )
    body = (
        "<p>This section is for getting the evidence out and using it. Every rating in the method rests on "
        "findings extracted from sources. The tables below hold those findings, the sources, the rows they "
        "support and the review status of each, for one fixed edition. They are plain CSV files with a "
        "machine-readable description, so they open in a spreadsheet, load in R or Python, and can be queried "
        "where they sit.</p>" + stats + '<div class="grid3">'
        f'<div class="card"><h3>1. Download</h3><p>Ten tables, one edition, each with a checksum. '
        f"{link('#download', 'Go to the downloads')}.</p></div>"
        f'<div class="card"><h3>2. Understand</h3><p>What each table and field means, how the tables join, and one '
        f"row followed end to end. {link('data-guide.html', 'Field guide and joins')}.</p></div>"
        f'<div class="card"><h3>3. Query</h3><p>Worked questions in SQL, Python and R, each run against this edition. '
        f"{link('data-queries.html', 'Query the data')}.</p></div></div>"
        '<h2 id="download">Download the edition tables</h2>'
        "<p>The tables are published once, with the live dashboard, and this reference links to that copy. "
        "Each address includes the edition, so it keeps returning the same file after later editions appear.</p>"
        + downloads_table(resources, tables)
        + "<ul>"
        f"<li>{link(PACKAGE_URL, 'Package description')} (<code>datapackage.json</code>): every table, field, type, key, "
        "join and checksum, in the Frictionless Tabular Data Package format. Its own SHA-256 is "
        f"<code>{PACKAGE_SHA256}</code>.</li>"
        f"<li>{link(EDITION_CATALOG_URL, 'Catalogue entry for this edition')} and the "
        f"{link(CATALOG_URL, 'site catalogue')}, in schema.org JSON-LD, which is where a program starts.</li>"
        "<li>This build downloaded the ten tables and checked each against the checksum in the package. "
        f"{link('reproduce.html#checks', 'Build checks')}.</li></ul>"
        '<p class="basis">Blank means not reported or not applicable in every table. '
        "Two fields hold JSON objects: <code>reported</code> and <code>study_context</code> on findings, and <code>parameters</code> on suitability mappings.</p>"
        '<h2 id="native">Tables the package does not carry</h2>'
        "<p>The package covers hazard, suitability and scorecard rows with their findings and sources. The tables below "
        "are not in it. They are in the producer repository at the same revision, so they describe the same edition. "
        "Each link is the file itself at that revision.</p>"
        + table(
            ["Table"]
            + [esc(practice_name(p)) for p in PRACTICE_IDS]
            + ["What the fields mean"],
            matrix,
            caption="Recipe tables by practice, in their native form, with row counts",
            cls="matrix",
        )
        + '<p class="basis">The native hazard, suitability and scorecard tables carry more fields than the package tables, '
        "including the compiled justification. Indicative economic profiles are only available here.</p>"
        + table(
            ["Register", "Rows", "Size", "Download", "SHA-256", "What the fields mean"],
            native_rows([a for a in registers if a["id"] not in in_package]),
            caption="Registers that are not in the package",
            numeric=(1, 2),
        )
        + table(
            ["Register", "Rows", "Size", "Download", "SHA-256", "What the fields mean"],
            native_rows([a for a in registers if a["id"] in in_package]),
            caption="Native source and evidence registers. The package tables are the public view of these; "
            "the native files add the verbatim quote, the source credibility fields and the review fields.",
            numeric=(1, 2),
        )
        + table(
            [
                "Configuration table",
                "Rows",
                "Size",
                "Download",
                "SHA-256",
                "What the fields mean",
            ],
            native_rows(config),
            caption="Method configuration tables",
            numeric=(1, 2),
        )
        + f"<p>{len(rules)} rule tables (weights, policies and crosswalks used by synthesis) are in "
        f"{link(CIAT_URL + 'schema/lookups', 'the rule-table folder')}. The column list of every table is in "
        f"{link(CIAT_RAW + 'schema/structure/columns.json', 'the column manifest')}. "
        f"Every file above is listed with its address and checksum in {link('data/assets.json', 'the asset list')}.</p>"
        '<h2 id="later">Registers after this edition</h2>'
        "<p>The registers continue to change after an edition is fixed. The evidence repository holds a later copy of "
        "the registers and review logs, with a manifest of row counts and checksums. Use it to see current work. "
        "Do not combine its counts with this edition.</p>"
        + table(
            [
                "Register",
                "Rows at the later revision",
                "Rows at this edition",
                "Download",
            ],
            [
                [
                    esc(TABLE_NAMES.get(r["id"], r["id"])) + f" ({esc(r['id'])})",
                    f"{r['rows']:,}",
                    f"{next((a['rows'] for a in registers if a['id'] == r['id']), 0):,}",
                    link(r["url"], "CSV"),
                ]
                for r in later
            ],
            caption=f"Registers in the evidence repository at revision {esc(EVIDENCE_REV[:12])}",
            numeric=(1, 2),
        )
        + f"<p>{link(EVIDENCE_URL + 'registers/manifest.json', 'Register manifest')} · "
        f"{link(EVIDENCE_URL + 'workflows/evidence_snapshot/README.md', 'how to inspect and verify the registers')}.</p>"
        '<h2 id="machine">For scripts and software agents</h2>'
        "<p>A program should not need to read these pages. Four files give it everything above.</p>"
        + table(
            ["File", "What it is", "Use it to"],
            [
                [
                    link("llms.txt", code("llms.txt")),
                    "A short plain-text guide written for language-model agents.",
                    "Learn what the data is, where the files are, how they join and what not to conclude.",
                ],
                [
                    link("data/assets.json", code("data/assets.json")),
                    "Every downloadable file named on this page, with address, revision, size, row count and checksum.",
                    "Fetch and verify files without parsing HTML.",
                ],
                [
                    link(PACKAGE_URL, code("datapackage.json")),
                    "The package description published with the edition.",
                    "Read field names, types, allowed values, keys and joins.",
                ],
                [
                    link(EDITION_CATALOG_URL, code("catalog.json")),
                    "The edition catalogue, in schema.org JSON-LD.",
                    "Discover the package from the site address and get its checksum.",
                ],
            ],
            caption="Machine-readable entry points",
        )
        + '<h2 id="cite">Cite and reuse</h2>'
        f"<p><strong>Citation.</strong> {esc(descriptor['citation'])}</p>"
        f"<p><strong>Access and reuse.</strong> {esc(descriptor['accessRights'])}</p>"
        "<p>No reuse licence is stated for the extracted data in this edition. Until one is, treat the tables as "
        "readable and citable, and ask before redistributing them. Questions and corrections go to "
        f"{link(descriptor['contact'], 'the evidence repository')}.</p>"
        '<h2 id="gaps">What is not yet available as data</h2><ul>'
        "<li><strong>Verbatim quotes.</strong> The package gives the page and locator of each finding, not the quoted passage. "
        "The quote is in the native evidence register.</li>"
        "<li><strong>Source credibility and setting.</strong> The package sources table has the citation, kind and link. "
        "Credibility tier, venue, study design and income group are in the native source register.</li>"
        f"<li><strong>Study location.</strong> A study country is recorded on {study_country:,} of "
        f"{len(tables['findings']):,} findings in the package.</li>"
        "<li><strong>Economic profiles, searches, variables, datasets and rule tables.</strong> Available as native files above, "
        "not yet described in a package with field definitions.</li>"
        "<li><strong>A persistent identifier.</strong> The package is addressed by its edition address. It has no DOI.</li>"
        "<li><strong>A query service.</strong> There is no database endpoint. The files are small enough to query directly; "
        f"see {link('data-queries.html', 'Query the data')}.</li></ul>"
        '<h2 id="browse">Browse instead</h2><ul>'
        f"<li>{link('sources.html', 'Sources')}: every registered source, with its findings and the rows that cite them.</li>"
        f"<li>{link('searches.html', 'Search records')}: every recorded search with its terms and criteria.</li>"
        f"<li>{link('practices.html', 'Practices')}: every row, by practice and table.</li>"
        f"<li>{link('evidence-counts.html', 'Counts and definitions')}: what the registers hold, with a definition for every count.</li>"
        f"<li>{link('review.html', 'Review queues and records')}: where human review happens and how its records are kept apart.</li></ul>"
    )
    dataset = next(d for d in catalog["dataset"] if d["@id"] == PACKAGE_URL)
    body += (
        '<script type="application/ld+json">'
        + json.dumps({"@context": "https://schema.org", **dataset}).replace(
            "</", "<\\/"
        )
        + "</script>"
    )
    page(
        "evidence-base.html",
        "evidence-base.html",
        "Evidence base: get and use the data",
        body,
        lead="Download the evidence behind every rating, read what each field means, and query it. Everything here is fixed to one edition.",
        toc=[
            ("download", "Download the edition tables"),
            ("native", "Tables the package does not carry"),
            ("later", "Registers after this edition"),
            ("machine", "For scripts and software agents"),
            ("cite", "Cite and reuse"),
            ("gaps", "What is not yet available as data"),
            ("browse", "Browse instead"),
        ],
    )

    # ------------------------------------------------------------ field guide
    joins = []
    for r in resources:
        for fk in r["schema"].get("foreignKeys", []):
            fields = fk["fields"] if isinstance(fk["fields"], list) else [fk["fields"]]
            ref = fk["reference"]
            joins.append(
                [
                    link(f"#t-{r['name']}", code(view(r["name"]))),
                    ", ".join(code(f) for f in fields),
                    link(f"#t-{ref['resource']}", code(view(ref["resource"]))),
                    esc(ONE_ROW[r["name"]]),
                ]
            )
    terrace_row = next(r for r in data.ROWS if r["id"] == TERRACE)
    record = next(r for r in tables["records"] if r["record_id"] == TERRACE)
    mapping = next(r for r in tables["t4"] if r["record_id"] == TERRACE)
    links = sorted(
        (r for r in tables["record-findings"] if r["record_id"] == TERRACE),
        key=lambda r: (r["kind"] != "direct", r["evidence_id"]),
    )
    finding_by_id = {f["evidence_id"]: f for f in tables["findings"]}
    source_by_id = {s["source_id"]: s for s in tables["sources"]}
    steps = []
    for item in links:
        f = finding_by_id[item["evidence_id"]]
        s = source_by_id[f["source_id"]]
        steps.append(
            [
                esc(item["kind"]),
                link(
                    f"{source_file(f['source_id'])}#{f['evidence_id']}",
                    code(f["evidence_id"]),
                ),
                esc(f["status"]),
                esc(f["page"]) if f["page"] else '<span class="none">blank</span>',
                code(f["reported"])
                if f["reported"]
                else '<span class="none">blank</span>',
                link(source_file(s["source_id"]), esc(s["citation"][:90] + "…")),
            ]
        )
    task = next((q for q in tables["queue"] if q["record_id"] == TERRACE), None)
    counts = Counter(f["status"] for f in tables["findings"])
    prov = {t: Counter(r["provisional"] for r in tables[t]) for t in ("t3", "t6")}
    kinds = Counter(r["kind"] for r in tables["record-findings"])
    calib = Counter(r["calibration"] for r in tables["t4"])
    body = (
        "<p>The edition tables are ten CSV files that join on three identifiers: a row identifier, a finding identifier "
        "and a source identifier. This page says what each table and field means, using the definitions published in the "
        "package itself, and follows one row through every join.</p>"
        '<h2 id="shape">How the tables fit together</h2>'
        "<p>Start from a row. A row links to findings. A finding names one source.</p>"
        '<pre class="shape"><code>t3, t4, t6        ──record_id────▶  records\n'
        "record_findings   ──record_id────▶  records\n"
        "record_findings   ──evidence_id──▶  findings  ──source_id──▶  sources\n"
        "context_sources   ──record_id────▶  records\n"
        "context_sources   ──source_id────▶  sources\n"
        "queue             ──evidence_id──▶  findings   (a finding that can change a rating)\n"
        "queue             ──record_id────▶  records    (a held calibration)</code></pre>"
        + table(
            ["Table", "Field", "Joins to", "One row of the table is"],
            joins,
            caption="Every join declared in the package. Table names are written as the query recipes name them.",
        )
        + '<p class="basis">Identifiers are the ones used in the registers and on the pages of this reference. '
        "A <code>record_id</code> opens a row page, an <code>evidence_id</code> is an anchor on its source page, and a "
        "<code>source_id</code> opens a source page.</p>"
        '<h2 id="read">Fields to read with care</h2>'
        "<p>Four fields carry most of the meaning. The definitions are quoted from the package; the notes under them are this reference’s reading.</p>"
        + table(
            [
                "Field",
                "Values at this edition",
                "Definition in the package",
                "Reading note",
            ],
            [
                [
                    "<code>findings.status</code>",
                    "<br>".join(
                        f"{code(k)} · {v:,}" for k, v in sorted(counts.items())
                    ),
                    esc(_definition(by_name, "findings", "status")),
                    (
                        "The status is the human decision applied at this edition. Unreviewed means none is applied; it does not mean the finding is wrong. "
                        "Signed off confirms the extraction against its source. It does not approve a score or a rating."
                    ),
                ],
                [
                    "<code>findings.excluded</code>",
                    f"true · {sum(1 for f in tables['findings'] if f['excluded'] == 'True'):,}",
                    esc(_definition(by_name, "findings", "excluded")),
                    "Excluded findings stay in the table for their history. No row links to one.",
                ],
                [
                    "<code>t3.provisional</code>, <code>t6.provisional</code>",
                    "<br>".join(
                        f"{t.upper()}: true · {prov[t]['True']:,}, false · {prov[t]['False']:,}, blank · {prov[t]['']:,}"
                        for t in ("t3", "t6")
                    ),
                    esc(_definition(by_name, "t3", "provisional")),
                    (
                        "Blank is the commonest value. It means the findings that can change the rating have not been fully assessed, "
                        "so the rating is neither confirmed provisional nor cleared."
                    ),
                ],
                [
                    "<code>record_findings.kind</code>",
                    "<br>".join(f"{code(k)} · {v:,}" for k, v in sorted(kinds.items())),
                    esc(_definition(by_name, "record-findings", "kind")),
                    (
                        "Count direct links when asking what a row cites. A setter link marks a finding that can change the rating; "
                        "the same finding can also be a direct link."
                    ),
                ],
                [
                    "<code>t4.calibration</code>",
                    "<br>".join(f"{code(k)} · {v:,}" for k, v in sorted(calib.items())),
                    esc(_definition(by_name, "t4", "calibration")),
                    (
                        "Held means the evidence was reviewed and does not support a numerical function. Not recorded means no calibration decision is recorded. "
                        "Neither is a score, and neither means reviewed and accepted."
                    ),
                ],
            ],
            caption="Status fields and what they do and do not say",
        )
        + '<h2 id="worked">One row, followed through every join</h2>'
        f"<p>The row is {link(terrace_row['file'], code(TERRACE))}: annual precipitation for the terracing family.</p><ol>"
        f"<li><strong>records.</strong> Table {code(record['table'])}, practice {code(record['practice'])}, family {code(record['family'])}, "
        f"subject “{esc(record['subject'])}”. {link(record['record_url'], 'The native row at the pinned revision')}.</li>"
        f"<li><strong>t4.</strong> Function role “{esc(mapping['function_role'])}”, calibration {code(mapping['calibration'])}, "
        f"function selected {code(mapping['function_selected'].lower())}, spatially validated {code(mapping['spatially_validated'].lower())}.</li>"
        f"<li><strong>record_findings → findings → sources.</strong> {len(links)} links:</li></ol>"
        + table(
            ["Kind", "Finding", "Status", "Page", "Reported values", "Source"],
            steps,
            caption="The findings linked to this row, each with its source",
        )
        + (
            f"<p><strong>queue.</strong> The row has one open task: {code(task['task'])}, status {code(task['status'])}.</p>"
            if task
            else ""
        )
        + "<p>Read together: one source records that this terrace type is used within a rainfall range. That is evidence of "
        "observed use. It does not give a score inside the range, so the calibration is held and no function is selected. "
        f"The same trace as a query is on {link('data-queries.html#q-trace', 'Query the data')}.</p>"
        '<h2 id="tables">Every table and field</h2>'
    )
    for r in resources:
        schema = r["schema"]
        body += (
            f'<h3 id="t-{esc(r["name"])}">{esc(r["title"])} <small>{code(r["path"])}</small></h3>'
            f"<p>{esc(ONE_ROW[r['name']])} {len(tables[r['name']]):,} rows. Key: {keys(schema)}. "
            f"{link(PACKAGE_BASE + r['path'], 'Download')}.</p>"
            + field_table(r, tables)
        )
    body += (
        '<h2 id="native-fields">Fields of the native tables</h2>'
        f"<p>The native recipe tables and registers have more fields than the package. Their field dictionary is the "
        f"{link('data-model.html', 'data model')}, with one page per table and the keys between them.</p>"
    )
    page(
        "data-guide.html",
        "evidence-base.html",
        "Field guide and joins",
        body,
        crumbs=[("evidence-base.html", "Evidence base"), ("", "Field guide and joins")],
        lead="What each table and field means, how the tables join, and one row followed end to end.",
        toc=[
            ("shape", "How the tables fit together"),
            ("read", "Fields to read with care"),
            ("worked", "One row, followed through every join"),
            ("tables", "Every table and field"),
            ("native-fields", "Fields of the native tables"),
        ],
    )

    # ------------------------------------------------------------ queries
    body = (
        "<p>The tables are small enough to query where they are published, with no database to set up. "
        "Each question below is answered with a query, and each query was run against this edition when this page was built. "
        "The results shown are that run’s output.</p>"
        '<h2 id="setup">Set up once</h2>'
        f"<p>These recipes use {link('https://duckdb.org/', 'DuckDB')}, a free query tool that reads CSV files straight from a web address. "
        f"Run the block below once in a DuckDB session (the build used version {esc(duck)}). To work offline, download the ten files and replace the address with the folder you saved them in.</p>"
        f"<pre><code>{esc(setup_sql(resources))}</code></pre>"
        '<p class="basis">DuckDB reads blank cells as missing and reads <code>true</code> and <code>false</code> as logical values. '
        "<code>table</code>, <code>group</code> and <code>count</code> are column names that need double quotes.</p>"
        '<h2 id="questions">Questions and queries</h2>'
    )
    for n, recipe_ in enumerate(SQL, 1):
        columns, rows = results[recipe_["id"]]
        body += (
            f'<h3 id="q-{recipe_["id"]}">{n}. {esc(recipe_["title"])}</h3>'
            f"<p>{esc(recipe_['why'])}</p>"
            f"<pre><code>{esc(recipe_['sql'])}</code></pre>"
            + result_table(columns, rows, "Result at this edition")
            + f'<p class="basis">{esc(recipe_["reading"])}</p>'
        )
    body += (
        '<h2 id="python">The same trace in Python</h2>'
        "<p>This script reads the package description, checks every file against its checksum, loads the tables with pandas and follows the row in question 1.</p>"
        f"<pre><code>{esc(PYTHON)}</code></pre>"
        f'<p class="basis">Output at this edition:</p><pre class="out"><code>{esc(py_out)}</code></pre>'
        '<h2 id="r">The same trace in R</h2>'
        "<p>Base R only, no packages.</p>"
        f"<pre><code>{esc(R)}</code></pre>"
        + (
            f'<p class="basis">Output at this edition:</p><pre class="out"><code>{esc(r_out)}</code></pre>'
            if r_ok
            else '<p class="basis">This recipe was not run on this build because R was not installed where the build ran.</p>'
        )
        + '<h2 id="verify">Check a file you downloaded</h2>'
        "<p>Each file’s SHA-256 is in the package description and in the downloads table. Compare it with the file on disk.</p>"
        "<pre><code>shasum -a 256 findings.csv        # macOS and Linux\n"
        "Get-FileHash findings.csv -Algorithm SHA256   # Windows PowerShell</code></pre>"
        f"<p>The expected value for <code>findings.csv</code> is <code>{esc(by_name['findings']['hash'].split(':', 1)[1])}</code>.</p>"
        '<h2 id="limits">What a query cannot tell you</h2><ul>'
        "<li>A count of findings is not strength of evidence. Confidence is stated on each row and is compiled from the level of evidence and its agreement.</li>"
        "<li>A study location is where the evidence was produced. It is not where a practice is suitable.</li>"
        "<li>A held calibration has no score. Do not fill it from the reported range.</li>"
        "<li>Counts from this edition and from the later registers describe different revisions. Do not add or compare them.</li>"
        f"<li>The reported values are as extracted. Units are source-specific and are in the <code>unit</code> key when recorded. {link('ch-extraction.html', 'Extraction')}.</li></ul>"
    )
    page(
        "data-queries.html",
        "evidence-base.html",
        "Query the data",
        body,
        crumbs=[("evidence-base.html", "Evidence base"), ("", "Query the data")],
        lead="Worked questions in SQL, Python and R. Every query on this page was run against this edition by the build.",
        toc=[
            ("setup", "Set up once"),
            ("questions", "Questions and queries"),
            ("python", "The same trace in Python"),
            ("r", "The same trace in R"),
            ("verify", "Check a file you downloaded"),
            ("limits", "What a query cannot tell you"),
        ],
    )

    # ------------------------------------------------------------ machine-readable files
    assets = {
        "name": "Rural NbS Scan methodology reference: downloadable data",
        "release": RELEASE,
        "producerRevision": PRODUCER,
        "accessRights": descriptor["accessRights"],
        "citation": descriptor["citation"],
        "package": {
            "edition": PACKAGE_EDITION,
            "descriptor": PACKAGE_URL,
            "sha256": PACKAGE_SHA256,
            "catalogue": EDITION_CATALOG_URL,
            "fieldGuide": "data-guide.html",
            "resources": [
                {
                    "name": r["name"],
                    "title": r["title"],
                    "url": PACKAGE_BASE + r["path"],
                    "mediaType": r["mediatype"],
                    "bytes": r["bytes"],
                    "sha256": r["hash"].split(":", 1)[1],
                    "rows": len(tables[r["name"]]),
                    "primaryKey": r["schema"].get("primaryKey"),
                    "foreignKeys": r["schema"].get("foreignKeys", []),
                }
                for r in resources
            ],
        },
        "native": {
            "note": "Files in the producer repository at the same revision as the package. "
            "Field definitions are in the data model pages named in `dictionary`.",
            "revision": PRODUCER,
            "columnManifest": CIAT_RAW + "schema/structure/columns.json",
            "files": recipe + registers + config + rules,
        },
        "later": {
            "note": "Registers in the evidence repository at a later revision than the package. "
            "Do not combine counts with the edition.",
            "revision": EVIDENCE_REV,
            "sourceRevision": manifest["source_revision"],
            "manifest": EVIDENCE_RAW + "registers/manifest.json",
            "files": later,
        },
    }
    FILES["data/assets.json"] = json.dumps(assets, indent=1) + "\n"
    FILES["llms.txt"] = llms(descriptor, resources, tables, counts)
    listed = [a["url"] for a in assets["native"]["files"]] + [
        r["url"] for r in assets["package"]["resources"]
    ]
    CHECKS.append(
        (
            "The asset list and the agent guide name every download at a pinned address with a checksum",
            all(u.startswith((CIAT_RAW, PACKAGE_BASE)) for u in listed)
            and all(len(a["sha256"]) == 64 for a in assets["native"]["files"])
            and all((PACKAGE_BASE + r["path"]) in FILES["llms.txt"] for r in resources)
            and PACKAGE_URL in FILES["llms.txt"],
            f"{len(listed)} files",
        )
    )


def _definition(by_name, resource, field):
    return next(
        f["description"]
        for f in by_name[resource]["schema"]["fields"]
        if f["name"] == field
    )


def llms(descriptor, resources, tables, counts):
    """Plain-text guide for language-model agents, in the llms.txt convention."""
    lines = [
        "# Rural NbS Scan methodology reference",
        "",
        (
            "> A scoping method for locating where nature-based solutions could be invested in across rural landscapes, "
            "with the evidence base behind its ratings. This file tells a software agent where the data is, how it joins "
            "and what not to conclude from it. Paths without a scheme are relative to this file."
        ),
        "",
        "## Edition",
        "",
        f"- Recipe release: {RELEASE} (candidate, not released)",
        f"- Producer revision of every table and register: {PRODUCER}",
        f"- Data package edition: {PACKAGE_EDITION}",
        "- Counts from different revisions must never be added or compared.",
        "",
        "## Data package (start here)",
        "",
        f"- [Package description, Frictionless Tabular Data Package]({PACKAGE_URL}): fields, types, allowed values, keys, joins, checksums. SHA-256 {PACKAGE_SHA256}",
        f"- [Edition catalogue, schema.org JSON-LD]({EDITION_CATALOG_URL})",
    ]
    for r in resources:
        lines.append(
            f"- [{r['title']}]({PACKAGE_BASE}{r['path']}): {ONE_ROW[r['name']]} "
            f"{len(tables[r['name']]):,} rows. SHA-256 {r['hash'].split(':', 1)[1]}"
        )
    lines += [
        "",
        "## Joins",
        "",
        "- t3, t4, t6 -> records on record_id",
        "- record-findings -> records on record_id; record-findings -> findings on evidence_id",
        "- findings -> sources on source_id",
        "- context-sources -> records on record_id; context-sources -> sources on source_id",
        "- queue -> findings on evidence_id (unresolved_setter) or records on record_id (held_calibration)",
        "- Blank means not reported or not applicable. `reported`, `study_context` and `parameters` hold JSON objects.",
        "",
        "## How to read status",
        "",
        "- findings.status: "
        + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
        + ". Unreviewed means no human decision is applied; it does not mean wrong. Signed off confirms the extraction, not a score or a rating.",
        "- findings.excluded true: dropped from synthesis, kept for history, linked to no row.",
        "- t3.provisional, t6.provisional: true = a finding that can change the rating is unresolved; false = fully assessed and clear; blank = not determined.",
        "- record-findings.kind: direct = cited by the row; context = contextual; setter = can change the rating.",
        "- t4.calibration Held or Not recorded: there is no score. Never derive one from a reported range.",
        "",
        "## Do not conclude",
        "",
        "- This is a scoping method. It flags where to look. Local feasibility assessment validates.",
        "- A count of findings or sources is not strength of evidence. Use the confidence on each row.",
        "- Study geography describes where evidence was produced, not where a practice is suitable.",
        "- Line, zone and qualitative practices are not areas of pixels.",
        "- Economic values are indicative and ordinal. They are not cost-benefit analysis.",
        f"- Access: {descriptor['accessRights']}",
        "",
        "## More files",
        "",
        "- [All downloadable files with addresses and checksums](data/assets.json)",
        f"- [Column manifest of every native table]({CIAT_RAW}schema/structure/columns.json)",
        "",
        "## Pages",
        "",
        "- [Get and use the data](evidence-base.html)",
        "- [Field guide and joins](data-guide.html)",
        "- [Query recipes in SQL, Python and R](data-queries.html)",
        "- [Data model: every table and field](data-model.html)",
        "- [Method](method.html)",
        "- [Evidence methods](evidence-methods.html)",
        "- [Continue the evidence base with an AI system](ch-continue-with-ai.html)",
        "- [Practices and every compiled row](practices.html)",
        "- [Review queues and records](review.html)",
        "- [Editions and build checks](editions.html)",
        "- [Glossary](glossary.html)",
        "",
    ]
    return "\n".join(lines)
