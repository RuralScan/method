"""Publish native, edition-scoped recipe, synthesis and evidence routes."""

import csv
import io
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cookbook.pages import FAMILIES, PRACTICES, PRODUCTS

EVIDENCE = "e47349055f1c34a5dd755b37ab9c4e7012882823"
EVIDENCE_BASE = f"https://github.com/RuralScan/evidence/blob/{EVIDENCE}/"
TABLES = {
    "T4": "Site suitability",
    "T3": "Hazard effects",
    "T6": "Scorecard effects",
    "T6E": "Costs",
}
TERRACE = "water_harvesting__terracing__annual_precipitation"
WOCAT = "ev_wh_precip_wocatgl13_benchterraces"


def snapshot(repo, revision, path):
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{revision}:{path}"]
    )


def esc(value):
    return escape(str(value), quote=True)


def link(href, label):
    return f'<a href="{esc(href)}">{esc(label)}</a>'


def words(value):
    return str(value or "").replace("__", " · ").replace("_", " ")


def row_file(row):
    if row["id"] == TERRACE:
        return "terrace.html"
    return f"row-{row['table'].lower()}-{row['id']}.html"


def recipe_file(practice):
    return f"recipe-{practice}.html"


def claim_file(claim):
    return "claim-" + claim["id"] + ".html"


def source_file(source):
    return "source-" + source["id"] + ".html"


def practice_name(practice):
    return (
        "Water harvesting and conservation"
        if practice == "water_harvesting_conservation"
        else words(practice).capitalize()
    )


def family_name(family):
    return FAMILIES[family][0] if family else "Practice-wide"


def record_name(row):
    scope = row["fields"].get("Scope") or row["fields"].get("Family")
    extra = [row["fields"].get(k) for k in ("Risk role", "Farming system")]
    return " · ".join(n for n in [row["subject"], scope, *extra] if n)


def claim_name(claim):
    return words(claim["variable"] or claim["role"] or claim["id"]).capitalize()


def locator(claim):
    parts = []
    if claim["page"] is not None:
        parts.append(f"PDF p. {claim['page']}")
    if claim["locator"]:
        parts.append(f"{words(claim['locator_type'])} {claim['locator']}")
    return " · ".join(parts) or "Locator unreported"


def entries(values):
    return (
        "<dl>"
        + "".join(
            f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>"
            for k, v in values
            if v is not None and v != ""
        )
        + "</dl>"
    )


def listing(links):
    return "<ul>" + "".join("<li>" + item + "</li>" for item in links) + "</ul>"


def row_table(rows):
    if not rows:
        return "<p>No compiled row in this edition.</p>"
    fields = list(rows[0]["fields"])
    headings = "".join(f'<th scope="col">{esc(k)}</th>' for k in fields)
    tr = []
    for row in rows:
        values = row["fields"]
        first = link(row_file(row), values[fields[0]])
        rest = "".join(f"<td>{esc(values[k])}</td>" for k in fields[1:])
        tr.append(f'<tr id="{esc(row["id"])}"><th scope="row">{first}</th>{rest}</tr>')
    return (
        '<div class="table-wrap" tabindex="0" aria-label="Compiled relationships"><table><thead><tr>'
        + headings
        + "</tr></thead><tbody>"
        + "".join(tr)
        + "</tbody></table></div>"
    )


def terrace_note():
    return (
        "<section><h2>Can a site receiving 350 mm/year be scored?</h2>"
        "<p><strong>Numerical calibration held. Leave the rainfall suitability score unassigned.</strong> "
        "WOCAT describes forward-sloping bench terraces used in areas receiving 200–600 mm/year "
        "(PDF p. 129, printed p. 116). The observation supports this design’s documented use. "
        "It supplies no response curve or failure threshold. Of three profiles considered, "
        "only WOCAT directly supports annual rainfall for these benches.</p>"
        "<p>The Ronquillo model uses October–April rainfall in one watershed. The FAO manual "
        "describes contour stone lines. Both are contextual records. The historical mapping "
        "records WorldClim precipitation; CHELSA BIO12 illustrates the catalogue’s global annual default.</p>"
        "<h3>Replay the decision</h3><p>From the pinned evidence checkout, with Git and uv installed:</p>"
        "<p>Historical compiler <code>2023cb82</code> · 43 T4 rows. The terrace hold is recorded in this edition.</p>"
        "<pre><code>uv run --python 3.12 --locked --script examples/terrace-rainfall/replay.py</code></pre><p>"
        + link(
            EVIDENCE_BASE + "examples/terrace-rainfall/README.md",
            "Historical replay, inputs and expected digest",
        )
        + "</p><p>Candidate compiler <code>e5c8da02</code> · 806 analytical rows. This edition also records a hold.</p>"
        "<pre><code>uv run --python 3.12 --locked --script workflows/recipe_release/check.py --check-method --json</code></pre><p>"
        + link(
            EVIDENCE_BASE + "workflows/recipe_release/README.md",
            "Rebuild the candidate and verify its method definitions",
        )
        + "</p></section>"
    )


def structured_fields(record, fields):
    values = []
    for key in fields:
        value = record.get(key)
        if value is None or value == "" or value == [] or value == {}:
            continue
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        values.append((words(key).capitalize(), value))
    return entries(values) if values else ""


def suitability_relationship(raw):
    params = raw.get("relationship_params") or {}
    result = "<h3>Compiled relationship</h3>" + structured_fields(
        raw, ["relationship_type", "suitability_dimension", "dataset_id"]
    )
    calibration = params.get("reviewed_adaptation", {}).get("numerical_calibration", {})
    result += structured_fields(calibration, ["status", "reason"])
    result += structured_fields(
        params,
        [
            "abs_min",
            "opt_low",
            "opt_high",
            "abs_max",
            "threshold",
            "above_is_suitable",
            "unit",
            "class_labels",
            "class_map",
            "class_requirements",
            "unmapped_policy",
            "interpretation",
            "host_crop",
            "footprint_rule",
            "score_interpretation",
            "outside_domain",
            "profile_selection",
            "legal_mask_contract",
        ],
    )
    for profile in params.get("profiles", []):
        intervals = profile.get("intervals") or []
        result += (
            "<details><summary>"
            + esc("Source profile · " + profile["profile_id"])
            + "</summary>"
        )
        result += structured_fields(
            profile, ["applicability_note", "unit", "score_policy"]
        )
        if intervals:
            result += '<div class="table-wrap"><table><caption>Recorded profile intervals</caption><thead><tr><th>Interval</th><th>Class</th><th>Score</th><th>Score basis</th></tr></thead><tbody>'
            for band in intervals:
                lower = band.get("lower")
                upper = band.get("upper")
                span = (
                    ("[" if band.get("lower_inclusive") else "(")
                    + str(lower if lower is not None else "−∞")
                    + ", "
                    + str(upper if upper is not None else "∞")
                    + ("]" if band.get("upper_inclusive") else ")")
                )
                result += (
                    "<tr>"
                    + "".join(
                        "<td>" + esc(x if x is not None else "Unreported") + "</td>"
                        for x in [
                            span,
                            band.get("label"),
                            band.get("score"),
                            words(band.get("score_basis")),
                        ]
                    )
                    + "</tr>"
                )
            result += "</tbody></table></div>"
        result += "</details>"
    return result


def decision(raw, table):
    rationale = raw.get("justification")
    if isinstance(rationale, dict):
        rationale = rationale.get("statement")
    parts = [suitability_relationship(raw)] if table == "T4" else []
    if table == "T6E" and raw.get("economic_value_range"):
        interval = raw["economic_value_range"]
        parts.append(
            entries(
                [
                    ("Low", interval.get("low")),
                    ("High", interval.get("high")),
                    ("Unit", words(interval.get("unit"))),
                    ("Source conditions", interval.get("source_note")),
                ]
            )
        )
    for title, key in [
        ("Mechanism", "mitigation_mechanism"),
        ("Mechanism", "effect_mechanism"),
        ("Conditions", "conditionality"),
        ("Limits", "caveats"),
    ]:
        if isinstance(raw.get(key), str) and raw[key]:
            parts.append(f"<h3>{title}</h3><p>{esc(raw[key])}</p>")
    if isinstance(rationale, str) and rationale:
        parts.append(f"<h3>Recorded rationale</h3><p>{esc(rationale)}</p>")
    else:
        parts.append("<p>No rationale recorded in this edition.</p>")
    return "".join(parts)


def generate(out, evidence, ciat, write):
    """write(relative_filename, section, title, html_body) supplies the shared shell."""
    out = Path(out)
    workbook = snapshot(evidence, EVIDENCE, "publication/workbook/index.html")
    match = re.search(
        rb'<script type="application/json" id="publication">(.+?)</script>',
        workbook,
        re.DOTALL,
    )
    if not match:
        raise ValueError("Missing pinned workbook data")
    pub = json.loads(match[1])
    pin = json.loads(snapshot(evidence, EVIDENCE, "workflows/recipe_release/pin.json"))
    if any(pub[key] != pin[key] for key in ("source_revision", "release_id")):
        raise ValueError("Workbook differs from candidate pin")
    revision = pin["source_revision"]
    rows = pub["rows"]
    if Counter(r["table"] for r in rows) != Counter(pub["totals"]):
        raise ValueError("Candidate counts differ from published edition")
    (out / "workbook.html").write_bytes(workbook)
    claims = {c["id"]: c for c in pub["claims"]}
    sources = {s["id"]: s for s in pub["sources"]}
    indexed = defaultdict(list)
    by_family = defaultdict(list)
    evidence_values = {
        r["evidence_id"]: r
        for r in json.loads(
            snapshot(ciat, revision, "schema/registers/EV_evidence_register.json")
        )
        if r["evidence_id"] in claims
    }
    raw_rows = {}
    direct, contextual, source_rows, source_claims = (
        defaultdict(list) for _ in range(4)
    )
    for c in claims.values():
        source_claims[c["source_id"]].append(c)
    for row in rows:
        indexed[row["practice"], row["table"]].append(row)
        by_family[row["practice"], row["family"], row["table"]].append(row)
        for key in row["evidence_ids"]:
            direct[key].append(row)
        for key in row["context_ids"]:
            contextual[key].append(row)
        for key in row["context_source_ids"]:
            source_rows[key].append(row)
    for (practice, table), subset in indexed.items():
        filename = subset[0]["url"].split("/")[-1].split("#")[0]
        records = json.loads(
            snapshot(ciat, revision, f"schema/recipes/{practice}/{filename}")
        )
        key = "mapping_id" if table == "T4" else "record_id"
        if {r[key] for r in records} != {r["id"] for r in subset}:
            raise ValueError(f"Workbook IDs differ for {practice}/{table}")
        raw_rows.update((r[key], r) for r in records)
    if len(raw_rows) != len(rows):
        raise ValueError("Ambiguous row IDs")
    fam_rows = csv.DictReader(
        io.StringIO(
            snapshot(
                ciat, revision, "schema/registers/FAM_family_registry.csv"
            ).decode()
        )
    )
    families = defaultdict(dict)
    for f in fam_rows:
        families[f["nbs_id"]].setdefault(f["suitability_family_id"], []).append(f)
    practices = pin["practices"]
    write(
        "recipes.html",
        "recipes",
        "Practice recipes",
        "<p>Choose a practice, then a family to see its siting question, spatial product and compiled evidence.</p>"
        + listing(
            link(recipe_file(p), practice_name(p)) + " — " + esc(PRACTICES[p][0])
            for p in practices
        ),
    )
    for practice in practices:
        body = f"<p>{esc(PRACTICES[practice][1])}</p><h2>Choose a family</h2>"
        groups = families[practice]
        body += listing(
            link("#" + f, family_name(f))
            + " · "
            + esc(PRODUCTS[variants[0]["spatial_product_type"]][0])
            for f, variants in groups.items()
        )
        body += "<p>" + link("#practice-wide", "Practice-wide relationships") + "</p>"
        for family in [*groups, None]:
            body += f'<section id="{family or "practice-wide"}"><h2>{esc(family_name(family))}</h2>'
            if family:
                variants = groups[family]
                product, description = PRODUCTS[variants[0]["spatial_product_type"]]
                body += f"<p>{esc(FAMILIES[family][1])}</p><p><strong>{esc(product)}.</strong> {esc(description)}</p>"
                body += (
                    "<p>Practices in this family include "
                    + esc(", ".join(v["name"] for v in variants))
                    + ".</p>"
                )
            else:
                body += "<p>These rows apply across this practice, subject to each row’s geographic and farming-system conditions.</p>"
            for table, name in TABLES.items():
                group = by_family[practice, family, table]
                body += (
                    f"<h3>{link('table-' + table + '.html', name + ' (' + table + ')')} · {len(group)} rows</h3>"
                    + row_table(group)
                )
            body += "</section>"
        write(recipe_file(practice), "recipes", practice_name(practice), body)
    synthesis_links = [
        link("terrace.html", "4.1 Worked example · Bench-terrace rainfall")
    ]
    for i, (table, name) in enumerate(TABLES.items(), 2):
        synth_file = "synthesis-" + table.lower() + ".html"
        synthesis_links.append(link(synth_file, f"4.{i} {name} ({table})"))
        content = (
            "<p>"
            + link("table-" + table + ".html", f"Read the {table} table definition")
            + "</p>"
        )
        content += (
            "<p>"
            + " · ".join(link("#" + p, practice_name(p)) for p in practices)
            + "</p>"
        )
        if table == "T4":
            content += (
                "<p>"
                + link(
                    "../../legacy.html#evidence-explorer",
                    "Compare source plots in the original Evidence explorer (progress snapshot bec50bc0)",
                )
                + "</p>"
            )
        for practice in practices:
            content += (
                f'<h2 id="{practice}">{esc(practice_name(practice))}</h2>'
                + row_table(indexed[practice, table])
            )
        write(synth_file, "synthesis", f"{name} ({table})", content)
    write(
        "synthesis.html",
        "synthesis",
        "Evidence synthesis",
        "<p>Inspect one compiled decision, then follow its supporting and contextual findings.</p>"
        + listing(synthesis_links),
    )
    for row in rows:
        key, table, practice = row["id"], row["table"], row["practice"]
        back = link(
            recipe_file(practice) + "#" + key,
            practice_name(practice) + " · " + family_name(row["family"]),
        )
        body = (
            "<p>"
            + back
            + " · "
            + link("table-" + table + ".html", f"{table} definition")
            + "</p>"
        )
        if key == TERRACE:
            body += terrace_note()
        body += entries(row["fields"].items())
        body += decision(raw_rows[key], table)
        protocol = (
            "T4_generation_method.md" if table == "T4" else "T3_T6_generation_method.md"
        )
        body += (
            "<p>"
            + link(
                f"https://github.com/CIAT/nbs_ruralscan/blob/{revision}/methodology/{protocol}",
                f"Read the pinned {table} synthesis protocol",
            )
            + "</p>"
        )
        for title, ids in [
            ("Direct supporting findings", row["evidence_ids"]),
            ("Additional contextual findings", row["context_ids"]),
        ]:
            if ids or title.startswith("Direct"):
                body += f"<h2>{title}</h2>"
                body += (
                    listing(
                        link(
                            claim_file(claims[i]),
                            claim_name(claims[i])
                            + " · "
                            + locator(claims[i])
                            + " · "
                            + i,
                        )
                        for i in ids
                    )
                    if ids
                    else "<p>No direct findings recorded.</p>"
                )
        if row["context_source_ids"]:
            body += "<h2>Sources named in the record</h2>" + listing(
                link(source_file(sources[i]), sources[i]["citation"])
                for i in row["context_source_ids"]
            )
        body += (
            "<p>"
            + link(row["url"], "Open pinned analytical record")
            + " · <code>"
            + esc(key)
            + "</code></p>"
        )
        write(
            row_file(row),
            "synthesis",
            ("Bench-terrace rainfall" if key == TERRACE else row["subject"]),
            body,
        )
    for claim in claims.values():
        key = claim["id"]
        source = sources[claim["source_id"]]
        body = (
            "<p>"
            + link(source_file(source), source["citation"] or source["id"])
            + "</p>"
        )
        record = evidence_values[key]
        rel = record.get("relationship") or {}
        if isinstance(rel, dict):
            finding = structured_fields(
                rel,
                [
                    "outcome_raw",
                    "metric",
                    "direction",
                    "magnitude",
                    "magnitude_low",
                    "magnitude_high",
                    "value_with",
                    "value_without",
                    "unit",
                    "threshold",
                    "abs_min",
                    "opt_low",
                    "opt_high",
                    "abs_max",
                    "observed_min",
                    "observed_max",
                    "observed_classes",
                    "condition",
                    "significance",
                    "design",
                ],
            )
            if finding:
                body += "<h2>Reported finding</h2>" + finding
        context = record.get("context")
        if isinstance(context, dict):
            body += structured_fields(
                context, ["study_country", "study_area", "farming_system", "aez"]
            )
        if key == WOCAT:
            body += "<p>WOCAT records use of forward-sloping bench terraces in areas receiving 200–600 mm/year. PDF p. 129, printed p. 116, paragraph on contour forward-sloping bench terraces.</p>"
        body += entries(
            [
                ("Source locator", locator(claim)),
                (
                    "Practice",
                    practice_name(claim["practice"])
                    if claim["practice"]
                    else "Unreported",
                ),
                ("Family", words(claim["family"])),
                ("Claim scope", words(claim["scope"])),
                ("Role", words(claim["role"])),
                ("Evidence basis", words(claim["basis"])),
                ("Extraction confidence", words(claim["confidence"])),
            ]
        )
        for title, matches in [
            ("Synthesis rows citing this finding", direct[key]),
            ("Rows using this finding as context", contextual[key]),
        ]:
            if matches:
                body += f"<h2>{title}</h2>" + listing(
                    link(row_file(r), r["table"] + " · " + record_name(r))
                    for r in matches
                )
        if not direct[key] and not contextual[key]:
            body += "<p>No compiled row cites this finding in this edition.</p>"
        body += (
            "<p>"
            + link(claim["url"], "Open pinned finding")
            + " · <code>"
            + esc(key)
            + "</code></p>"
        )
        write(claim_file(claim), "evidence", claim_name(claim), body)
    for source in sources.values():
        key = source["id"]
        body = entries(
            [
                ("Source type", words(source["kind"])),
                ("Discovery category", words(source["category"])),
            ]
        )
        publication = source["publication_url"] or source["publisher_url"]
        if publication:
            body += "<p>" + link(publication, "Open publication") + "</p>"
        if key == "wocat_wh_guidelines_2013" and source["publisher_url"]:
            body += (
                "<p>"
                + link(
                    source["publisher_url"] + "#page=129",
                    "Read WOCAT PDF p. 129 (printed p. 116)",
                )
                + "</p>"
            )
        body += "<h2>Findings from this source</h2>"
        body += (
            listing(
                link(
                    claim_file(c), claim_name(c) + " · " + locator(c) + " · " + c["id"]
                )
                for c in source_claims[key]
            )
            if source_claims[key]
            else "<p>No linked findings in this edition.</p>"
        )
        if source_rows[key]:
            body += "<h2>Synthesis rows naming this source</h2>" + listing(
                link(row_file(r), r["table"] + " · " + record_name(r))
                for r in source_rows[key]
            )
        body += (
            "<p>"
            + link(source["url"], "Open pinned source record")
            + " · <code>"
            + esc(key)
            + "</code></p>"
        )
        write(source_file(source), "evidence", source["citation"] or key, body)
    catalogue = []
    for source in sources.values():
        label = source["citation"] or source["id"]
        catalogue.append(
            {
                "label": label,
                "path": source_file(source),
                "search": (label + " " + source["id"]).lower(),
            }
        )
    for c in claims.values():
        label = f"{claim_name(c)} · {locator(c)} · {c['id']}"
        catalogue.append(
            {
                "label": label,
                "path": claim_file(c),
                "search": (label + " " + c["practice"] + " " + c["source_id"]).lower(),
            }
        )
    (out / "recipe-catalogue.json").write_text(
        json.dumps(catalogue, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    (out / "recipe-search.js").write_bytes(
        Path(__file__).with_name("recipe-search.js").read_bytes()
    )
    search = (
        '<form id="evidence-search" action="evidence.html"><label for="evidence-query">Search findings and sources</label> '
        '<input id="evidence-query" name="q" type="search" required> <button type="submit">Search</button></form>'
        '<p id="evidence-status" role="status" aria-live="polite"></p>'
        '<button id="evidence-retry" type="button" hidden>Retry search</button><ul id="evidence-results"></ul>'
        '<script defer src="recipe-search.js"></script>'
    )
    write(
        "evidence.html",
        "evidence",
        "Evidence",
        search
        + "<p>Browse the pinned candidate workbook by finding or source. Search progress uses its own dated snapshot.</p>"
        + listing(
            [
                link(
                    "workbook.html#claims",
                    f"{len(claims):,} extracted findings in the candidate workbook",
                ),
                link(
                    "workbook.html#bibliography",
                    f"{len(sources):,} bibliographic sources in the candidate workbook",
                ),
                link("searches.html", "Recorded searches in the progress snapshot"),
                link("terrace.html", "Follow the bench-terrace finding to its source"),
            ]
        )
        + '<p><a href="workbook.html" download>Download this edition’s evidence workbook</a></p>',
    )
    return pub
