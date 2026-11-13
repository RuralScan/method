"""Practice pages and one detail page per recipe row."""

from collections import Counter

import data
from chapters import chapter_body
from core import (
    BLOCKED_KEYS,
    CIAT_URL,
    PRACTICE_IDS,
    PRACTICE_TEXT,
    PRODUCTS,
    ROW_TABLES,
    SIDE,
    TABLE_FILES,
    TABLE_NAMES,
    badge,
    code,
    dl,
    esc,
    family_name,
    link,
    page,
    practice_name,
    render_value,
    source_file,
    table,
    text,
    words,
)

RISK_ROLE = {
    "livelihood_mitigation": "Livelihood risk mitigation (Module 2)",
    "asset_threat": "Threat to the investment (Module 2b)",
}
METHOD_CHAPTER = {
    "T4": ("ch-suitability-synthesis.html", "How suitability mappings are compiled"),
    "T3": ("ch-effect-synthesis.html", "How hazard responses are synthesised"),
    "T6": ("ch-effect-synthesis.html", "How scorecard effects are synthesised"),
    "T6E": ("ch-cost-profiles.html", "How indicative economic profiles are compiled"),
}
# Signals the effect synthesis records on a row. Wording follows the synthesis method.
SIGNALS = [
    (
        "landscape_scale_only",
        "Off-site effect locus",
        "The practice or family is registered with an off-site effect locus, so the effect is not an on-plot benefit. Mixed-locus rows are not flagged. Read the recorded account.",
    ),
    (
        "intensity_limited",
        "Hazard-intensity discount flagged",
        "Hazard responses for livelihoods only. Measured or modelled findings for the same hazard, other than failures the author called mild, found no benefit or a reversal. The class rank is multiplied by one minus that share, rounded, and floored at the weakest class of the sign. The flag is set even when rounding leaves the class unchanged.",
    ),
    (
        "size_sparse",
        "Size-sparse cap",
        "Applies when at least three same-direction findings exist, fewer than a third of them state a size, and the class would otherwise exceed moderate. The class is capped at moderate.",
    ),
    (
        "modelled_capped",
        "Modelled-only cap",
        "A modelled finding sets the strength without a measured finding behind it; the class is capped at moderate.",
    ),
    (
        "proxy_capped",
        "Proxy cap",
        "No finding in the cell is direct evidence for the target (all are proxies or components), so the class is capped at moderate. Any direct finding lifts the cap.",
    ),
    (
        "context_dependent",
        "Context dependent",
        "Global agreement is low or medium and at least two emitted scope rows differ in sign or class. Read the scope rows.",
    ),
    (
        "family_spread",
        "Families differ",
        "Family rows differ by two or more classes, so the practice-level class hides that spread. Read the family rows.",
    ),
]
PRODUCT_NOTE = {
    "area_suitability": "Reported as a potential area surface.",
    "applicability_zone": "Reported as a zone in which to inspect locations, not as treated area.",
    "zonal_linear": "Reported as corridor or reach length, never as pixel area.",
    "qualitative_only": "Qualitative guidance only: no map and no generated effect rows.",
}


def cls(value):
    """Display a recorded class exactly, in words."""
    return (
        esc(words(value))
        if value not in (None, "")
        else '<span class="none">Not recorded</span>'
    )


def row_title(r):
    raw = r["raw"]
    if r["table"] == "T4":
        label = data.VONT.get(raw["variable"], {}).get("label") or words(
            raw["variable"]
        )
        return f"{label} · {family_name(r['family'])}"
    if r["table"] == "T3":
        where = words(raw.get("farming_system") or "all")
        role = (
            "threat to the investment"
            if raw.get("risk_role") == "asset_threat"
            else where
        )
        return f"{words(raw['hazard_type'])} · {role}"
    if r["table"] == "T6":
        t5 = data.T5.get(raw["variable_id"])
        return t5["ttl_priority_label"] if t5 else words(raw["variable_id"])
    return words(raw.get("economic_indicator_type") or raw["variable_id"])


def scope_label(raw):
    if raw.get("scope_type"):
        return f"{words(raw['scope_type'])}: {words(raw.get('scope_id'))}"
    return "Global row"


def confidence_cell(raw, key):
    axes = ""
    if raw.get("evidence_level") or raw.get("agreement_level"):
        axes = (
            f"<br><small>{cls(raw.get('evidence_level'))} evidence · "
            f"{cls(raw.get('agreement_level'))} agreement</small>"
        )
    return f"{cls(raw.get(key))}{axes}"


def transfer_cell(raw):
    app = raw.get("applicability") or {}
    value = app.get("transfer_class")
    if not value:
        return '<span class="none">Not recorded</span>'
    mark = ' class="warn"' if value == "out_of_context" else ""
    out = f"<span{mark}>{esc(words(value))}</span>"
    income = (app.get("target") or {}).get("income_group")
    if income and income != "lic_lmic":
        # A scope row is judged against its own scope, not against low and lower-middle income settings.
        out += f'<br><small class="warn">for the {esc(words(income))} income scope only</small>'
    return out


def signal_marks(raw):
    just = (
        raw.get("justification") if isinstance(raw.get("justification"), dict) else {}
    )
    marks = []
    if raw.get("landscape_scale_only"):
        marks.append("landscape-scale")
    if just.get("intensity_limited"):
        marks.append("intensity discount")
    harm = just.get("maladaptation") or {}
    if harm.get("n_units"):
        marks.append(f"harm recorded ({harm['n_units']})")
    if just.get("size_sparse"):
        marks.append("size-sparse cap")
    if just.get("modelled_capped"):
        marks.append("modelled cap")
    return "; ".join(marks) or "None recorded"


def evidence_table(ids):
    rows = []
    for i in ids:
        unit = data.EV_BY_ID.get(i)
        if not unit:
            rows.append(
                [
                    code(i),
                    "Not found in the evidence register at this edition",
                    "",
                    "",
                    "",
                    "",
                ]
            )
            continue
        src = data.SRC_BY_ID.get(unit.get("source_id"), {})
        cite = esc(src.get("citation") or unit.get("source_id") or "")
        where = unit.get("locator") or (
            f"p. {unit['page']}" if unit.get("page") else "Not recorded"
        )
        rows.append(
            [
                link(f"{source_file(unit.get('source_id'))}#{esc(i)}", code(i)),
                cite,
                text(str(where)),
                f"{esc(words(unit.get('variable')))}"
                + (
                    f"<br><small>source term: {text(unit['raw_name'])}</small>"
                    if unit.get("raw_name")
                    else ""
                ),
                render_value(unit.get("relationship")),
                f"{esc(words(unit.get('claim_basis')))} · {esc(words(unit.get('claim_scope')))}"
                + (
                    f"<br><small>{esc(src.get('benchmark_tier', '')).lower()} tier</small>"
                    if src.get("benchmark_tier")
                    else ""
                ),
            ]
        )
    return table(
        [
            "Finding",
            "Source",
            "Locator",
            "Variable",
            "Encoded relationship",
            "Basis and scope",
        ],
        rows,
        caption=f"Evidence behind this row ({len(ids)} findings). The verbatim quote for each finding is held in the evidence register.",
        cls="evidence",
    )


def applicability_block(raw):
    app = raw.get("applicability")
    if not app:
        return ""

    def counts(key):
        value = app.get(key) or {}
        return (
            ", ".join(
                f"{esc(words(k))} {v}"
                for k, v in sorted(value.items(), key=lambda kv: -kv[1])
            )
            or "Not recorded"
        )

    share = app.get("weight_share_in_context")
    pairs = [
        ("Transfer class", transfer_cell(raw)),
        ("Target context", render_value(app.get("target"))),
        (
            "Share of evidence weight inside the target context",
            esc(share) if share is not None else None,
        ),
        (
            "Sources in scope",
            esc(app.get("n_sources_in_scope"))
            if app.get("n_sources_in_scope") is not None
            else None,
        ),
        (
            "Income groups of the evidence (independent sources)",
            counts("income_groups"),
        ),
        ("Agro-ecological zones (independent sources)", counts("aezs")),
        ("Farming systems (independent sources)", counts("farming_systems")),
        ("Countries", esc(", ".join(app.get("countries") or [])) or None),
    ]
    note = (
        "<p>The transfer class compares the evidence with this row's target, by share of evidence weight "
        "before any transfer discount: <em>in context</em> when more than half sits in the target context, "
        "<em>out of context</em> when more than half sits two steps away, <em>adjacent</em> when more than "
        "half is within one step, otherwise <em>mixed</em>. Global rows target low and lower-middle income "
        "settings. A scope row targets its own scope, so “in context” on a high-income or upper-middle-income "
        "scope row says nothing about low and lower-middle income settings. "
        'See <a href="ch-effect-synthesis.html">effect synthesis</a>.</p>'
    )
    return '<h2 id="applicability">Applicability and transfer</h2>' + note + dl(pairs)


def signals_block(raw):
    just = (
        raw.get("justification") if isinstance(raw.get("justification"), dict) else {}
    )
    rows = []
    for key, label, meaning in SIGNALS:
        value = raw.get(key) if key in raw else just.get(key)
        if value is None:
            continue
        extra = ""
        if (
            key == "intensity_limited"
            and value
            and just.get("intensity_limit_share") is not None
        ):
            was = just.get("intensity_discounted_from")
            extra = f" (share {esc(just['intensity_limit_share'])}; " + (
                f"class lowered from {esc(words(was))})"
                if was
                else "class unchanged after rounding)"
            )
        if key == "size_sparse" and value and just.get("size_sparse_counts"):
            c = just["size_sparse_counts"]
            extra = f" ({esc(c.get('stating_a_size'))} of {esc(c.get('same_direction'))} state a size)"
        rows.append([esc(label), ("Yes" if value else "No") + extra, esc(meaning)])
    harm = just.get("maladaptation") or {}
    if harm:
        ids = harm.get("ids") or []
        links = ", ".join(
            link(f"{source_file(data.EV_BY_ID[i]['source_id'])}#{esc(i)}", code(i))
            if i in data.EV_BY_ID
            else code(i)
            for i in ids
        )
        rows.append(
            [
                "Measured harm (maladaptation)",
                f"{esc(harm.get('n_units', 0))} findings from {esc(harm.get('n_sources', 0))} sources"
                + (f": {links}" if links else ""),
                "Findings that measured harm are listed even when they are a minority.",
            ]
        )
    if just.get("severity_coverage"):
        rows.append(
            [
                "Hazard severity coverage",
                render_value(just["severity_coverage"]),
                "The severity each source author gave the event, for gains and for failures.",
            ]
        )
    if just.get("strength_basis"):
        rows.append(
            [
                "Strength basis",
                cls(just["strength_basis"]),
                "How the strength class was derived.",
            ]
        )
    if not rows:
        return ""
    return '<h2 id="signals">Signals recorded by the synthesis</h2>' + table(
        ["Signal", "Recorded", "Meaning"], rows, caption="Synthesis signals on this row"
    )


def is_cross(family):
    """Cross-family tags hold evidence pooled across families. They are not parked families."""
    return family.endswith("__cross_family")


ROLE_NOTE = {
    "Suitability score": (
        "<strong>Suitability score, no calibration status recorded.</strong> No calibration status is "
        "recorded on this row. That is not an approval and does not show whether a review took place. "
        "The profiles below are compiled from the cited findings."
    ),
    "Eligibility gate": (
        "<strong>Eligibility gate.</strong> Admits or removes locations before scoring. No numerical "
        "calibration status is recorded on this row."
    ),
    "Hard exclusion": (
        "<strong>Hard exclusion.</strong> Defines the mask interface. No mask is applied until an "
        "assessed mask for the jurisdiction is supplied."
    ),
    "Operational scenario": (
        "<strong>Operational scenario.</strong> An implementation factor that investment can change. "
        "It is screened through project risk (Module 2b) and is not part of structural suitability."
    ),
}


def t4_detail(r):
    raw = r["raw"]
    ready = data.readiness(r) or {}
    var = data.VONT.get(raw["variable"], {})
    params = raw.get("relationship_params") or {}
    cal = (params.get("reviewed_adaptation") or {}).get("numerical_calibration") or {}
    status = ready.get("calibration", "Not recorded")
    role = ready.get("role", "Not recorded")
    held = status == "Held"
    notes = []
    if held:
        notes.append(
            '<p class="callout hold"><strong>Calibration held: no score assigned.</strong> '
            "The values reported by sources are kept below. No breakpoints have been approved, "
            "so this mapping is not part of an executable recipe.</p>"
        )
    else:
        note = ROLE_NOTE.get(role, "<strong>No calibration status recorded.</strong>")
        if role == "Operational scenario" and not raw.get("n_sources"):
            note += " No evidence is attached (0 sources); the parameters are placeholder scenario endpoints."
        notes.append(f'<p class="callout">{note}</p>')
    default = data.default_binding(raw["variable"])
    dataset = raw.get("dataset_id")
    binding = code(dataset) if dataset else '<span class="none">Not recorded</span>'
    if default:
        binding += f" · global default binding {code(default)}"
    binding += "<br><small>These identify data sources only. Neither supplies a calibration.</small>"
    cross = is_cross(r["family"])
    products = (
        "Cross-family context (not a spatial product)"
        if cross
        else (
            ", ".join(PRODUCTS[p][0] for p in data.family_product(r["family"]))
            or "Not registered"
        )
    )
    inactive = (
        " <small>(inactive while the calibration is held)</small>" if held else ""
    )
    facts = dl(
        [
            (
                "Practice",
                link(
                    f"practice-{r['practice']}.html", esc(practice_name(r["practice"]))
                ),
            ),
            (
                "Suitability family",
                link(
                    f"practice-{r['practice']}.html#fam-{esc(r['family'])}",
                    esc(family_name(r["family"])),
                ),
            ),
            ("Spatial product of the family", esc(products)),
            (
                "Variable",
                link(
                    f"variables.html#var-{esc(raw['variable'])}",
                    esc(var.get("label") or words(raw["variable"])),
                )
                + (
                    f" ({esc(var.get('canonical_unit'))})"
                    if var.get("canonical_unit")
                    else ""
                ),
            ),
            ("Function role", esc(role)),
            ("Suitability dimension", cls(raw.get("suitability_dimension"))),
            ("Relationship type", cls(raw.get("relationship_type")) + inactive),
            ("Numerical calibration", esc(status)),
            ("Function options recorded", esc(ready.get("options", "Not recorded"))),
            (
                "Function selected",
                esc(ready.get("selected", "Not recorded"))
                + "<br><small>A selection is a choice recorded for a named target or a gate's default design, not a global approval.</small>",
            ),
            (
                "Execution-ready",
                esc(ready.get("validated", "Not recorded"))
                + "<br><small>The producer's execution-readiness flag, published as “spatially validated”.</small>",
            ),
            ("Scenario candidate", "Yes" if raw.get("is_scenario_candidate") else "No"),
            (
                "Future projection available",
                "Yes" if raw.get("has_future_projection") else "No",
            ),
            (
                "Default weight",
                f"{esc(raw.get('weight_default'))} ({'adjustable' if raw.get('weight_adjustable') else 'fixed'})"
                + inactive,
            ),
            ("Input dataset", binding),
            (
                "Independent sources",
                esc(raw.get("n_sources")) if raw.get("n_sources") is not None else None,
            ),
        ]
    )
    out = "".join(notes) + '<h2 id="result">Recorded mapping</h2>' + facts
    if cal.get("reason"):
        out += f'<h2 id="hold">Why the calibration is held</h2><p>{text(cal["reason"])}</p>'
    if raw.get("justification"):
        out += f'<h2 id="rationale">Recorded rationale</h2><p>{text(raw["justification"])}</p>'
    if held:
        kept = cal.get("retained_source_profiles")
        if kept:
            out += (
                '<h2 id="params">Source values retained</h2>'
                "<p>What each source reported, in its own unit and statistic. These are source values, "
                "not an approved score, range or cutoff.</p>" + render_value(kept)
            )
        record = {
            k: v
            for k, v in cal.items()
            if k
            not in {
                "retained_source_profiles",
                "held_relationship",
                "superseded_mapping",
                "reason",
                "status",
            }
        }
        if record:
            out += "<h3>Review record</h3>" + render_value(record)
        withdrawn = {
            k: cal[k] for k in ("held_relationship", "superseded_mapping") if cal.get(k)
        }
        withdrawn.update(
            {k: v for k, v in params.items() if k != "reviewed_adaptation"}
        )
        if withdrawn:
            out += (
                "<h3>Withdrawn relationship</h3><details><summary>Earlier relationship, not approved, kept for audit</summary>"
                "<p>This relationship was compiled before the review and was withdrawn. It is shown only so the "
                "decision can be audited. It must not be used as a score.</p>"
                + render_value(withdrawn)
                + "</details>"
            )
    else:
        heading = {
            "Operational scenario": "Scenario endpoints as recorded",
            "Hard exclusion": "Mask interface as recorded",
            "Eligibility gate": "Gate definition as recorded",
        }.get(role, "Compiled profiles as recorded")
        out += (
            f'<h2 id="params">{heading}</h2>'
            "<p>Recorded configuration for this mapping. No calibration status is recorded, so nothing here "
            "is an approved score.</p>" + render_value(params)
        )
    if raw.get("context_overrides"):
        out += '<h2 id="overrides">Context overrides</h2>' + render_value(
            raw["context_overrides"]
        )
    return out


def effect_detail(r):
    raw = r["raw"]
    just = (
        raw.get("justification") if isinstance(raw.get("justification"), dict) else {}
    )
    t = r["table"]
    pairs = [
        (
            "Practice",
            link(f"practice-{r['practice']}.html", esc(practice_name(r["practice"]))),
        ),
        (
            "Level",
            link(
                f"practice-{r['practice']}.html#fam-{esc(r['family'])}",
                esc(family_name(r["family"])),
            )
            if r["family"]
            else "Practice-level roll-up: pooled over all the practice's findings, not a mean of family rows",
        ),
        ("Scope", esc(scope_label(raw))),
    ]
    if t == "T3":
        asset = raw.get("risk_role") == "asset_threat"
        pairs += [
            (
                "Risk lens",
                esc(RISK_ROLE.get(raw.get("risk_role"), words(raw.get("risk_role")))),
            ),
            ("Hazard", cls(raw.get("hazard_type"))),
            ("Farming system", cls(raw.get("farming_system"))),
            (
                "Sensitivity of the investment to this hazard",
                cls(raw.get("asset_sensitivity")),
            )
            if asset
            else ("Mitigation potential", cls(raw.get("mitigation_potential"))),
            ("Confidence", confidence_cell(raw, "confidence")),
        ]
    else:
        t5 = data.T5.get(raw.get("variable_id"))
        target = (
            esc(t5["ttl_priority_label"])
            + f" ({esc(words(t5['theme']))}, {esc(t5['mcda_role'])})"
            if t5
            else cls(raw.get("variable_id"))
        )
        pairs.append(("Indicator" if t == "T6E" else "Priority or outcome", target))
        if t == "T6":
            pairs.append(("Effect direction", cls(raw.get("effect_direction"))))
        pairs.append(("Confidence", confidence_cell(raw, "effect_confidence")))
    pairs.append(("Timescale of effect", cls(raw.get("timescale_of_effect"))))
    out = '<h2 id="result">Recorded result</h2>' + dl(pairs)
    out += (
        "<p>Confidence is derived from two axes, evidence level and agreement level, using the "
        '<a href="rules.html#ipcc_confidence_matrix">pinned confidence matrix</a>. A direction of '
        "“conflicting evidence” is reported as such and is not averaged away.</p>"
    )
    if t == "T6E" and raw.get("economic_value_range"):
        out += (
            '<h2 id="range">Indicative range</h2><p>Reported values are not normalised across '
            "currency or price year. They indicate order of size in context. This is not "
            "cost-benefit analysis.</p>" + render_value(raw["economic_value_range"])
        )
    if raw.get("magnitude_summary"):
        out += '<h2 id="magnitude">Magnitude summary</h2>' + render_value(
            raw["magnitude_summary"]
        )
    out += applicability_block(raw) + signals_block(raw)
    for key, title in [
        ("mitigation_mechanism", "Mechanism"),
        ("effect_mechanism", "Mechanism"),
        ("conditionality", "Conditions"),
        ("caveats", "Limits"),
    ]:
        if isinstance(raw.get(key), str) and raw[key]:
            out += f"<h2>{title}</h2><p>{text(raw[key])}</p>"
    if just.get("statement"):
        out += (
            f'<h2 id="rationale">Recorded account</h2><p>{text(just["statement"])}</p>'
        )
    return out


def row_page(r):
    raw = r["raw"]
    t = r["table"]
    body = t4_detail(r) if t == "T4" else effect_detail(r)
    ids = raw.get("evidence_ids") or []
    body += '<h2 id="evidence">Evidence</h2>' + (
        evidence_table(ids)
        if ids
        else "<p>No evidence identifiers are recorded on this row.</p>"
    )
    everything = {k: v for k, v in raw.items() if not BLOCKED_KEYS.search(k)}
    href, label = METHOD_CHAPTER[t]
    body += (
        '<h2 id="record">Full record</h2><details><summary>All fields recorded for this row</summary>'
        + render_value(everything)
        + "</details>"
        + '<ul class="links">'
        + f"<li>{link(href, esc(label))}</li>"
        + f"<li>{link(f'table-{t}.html', 'Table definition: ' + esc(TABLE_NAMES[t]))}</li>"
        + f"<li>{link(CIAT_URL + f'schema/recipes/{r['practice']}/{TABLE_FILES[t]}', 'Source file at the pinned revision')}</li>"
        + "</ul>"
    )
    crumbs = [
        ("practices.html", "Practices"),
        (f"practice-{r['practice']}.html", practice_name(r["practice"])),
    ]
    if r["family"]:
        crumbs.append(
            (
                f"practice-{r['practice']}.html#fam-{r['family']}",
                family_name(r["family"]),
            )
        )
    crumbs.append((f"practice-{r['practice']}.html#{t}", TABLE_NAMES[t]))
    page(
        r["file"],
        "practices.html",
        row_title(r),
        body,
        crumbs=crumbs,
        lead=f"{badge(t)} {esc(TABLE_NAMES[t])} · {code(r['id'])}",
    )


# ---------------------------------------------------------------- practice page


def t4_rows_table(rows, caption):
    body = []
    for r in rows:
        raw, ready = r["raw"], data.readiness(r) or {}
        var = data.VONT.get(raw["variable"], {})
        body.append(
            [
                link(r["file"], esc(var.get("label") or words(raw["variable"]))),
                esc(ready.get("role", "Not recorded")),
                cls(raw.get("suitability_dimension")),
                cls(raw.get("relationship_type")),
                esc(ready.get("calibration", "Not recorded")),
                esc(ready.get("options", "")),
                esc(ready.get("selected", "")),
                esc(ready.get("validated", "")),
                esc(raw.get("n_sources", "")),
            ]
        )
    return table(
        [
            "Variable",
            "Function role",
            "Dimension",
            "Relationship",
            "Numerical calibration",
            "Function options",
            "Function selected",
            "Execution-ready",
            "Sources",
        ],
        body,
        caption=caption,
        numeric=(5, 8),
    )


def t4_family_block(practice, family):
    rows = [
        r
        for r in data.ROWS
        if r["practice"] == practice and r["table"] == "T4" and r["family"] == family
    ]
    kinds = data.family_product(family)
    cross = is_cross(family)
    if not rows:
        if cross:
            return '<p class="empty">Cross-family context: evidence pooled across families. No compiled suitability mapping in this edition.</p>'
        if "qualitative_only" in kinds:
            return '<p class="empty">Parked: qualitative guidance only (no map, no generated effect rows).</p>'
        return '<p class="empty">No compiled suitability mapping in this edition.</p>'
    role = lambda r: (data.readiness(r) or {}).get("role", "")
    structural = sorted(
        (r for r in rows if role(r) != "Operational scenario"), key=role, reverse=True
    )
    operational = [r for r in rows if role(r) == "Operational scenario"]
    note = ""
    if cross:
        note = '<p class="empty">Cross-family context: evidence pooled across the practice\'s families, not a parked family and not a spatial product.</p>'
    elif set(kinds) & {"zonal_linear", "applicability_zone", "qualitative_only"}:
        note = (
            '<p class="empty">'
            + " ".join(PRODUCT_NOTE[k] for k in kinds if k != "area_suitability")
            + "</p>"
        )
    out = note
    if structural:
        out += t4_rows_table(
            structural,
            f"{esc(family_name(family))} · {TABLE_NAMES['T4']} · scores, gates and exclusions",
        )
    if operational:
        out += (
            "<p><strong>Operational scenarios.</strong> Implementation factors that investment can change. "
            "They are screened through project risk (Module 2b) and are kept apart from structural suitability.</p>"
            + t4_rows_table(
                operational,
                f"{esc(family_name(family))} · operational scenarios (project risk, not suitability)",
            )
        )
    return out


def effect_tables(practice, t, family=None, heading=""):
    rows = [
        r
        for r in data.ROWS
        if r["practice"] == practice
        and r["table"] == t
        and r["family"] == (family or "")
    ]
    if not rows:
        return ""
    name = family_name(family) if family else "Practice-level roll-up"
    out = ""
    if t == "T3":
        live = [r for r in rows if r["raw"].get("risk_role") != "asset_threat"]
        asset = [r for r in rows if r["raw"].get("risk_role") == "asset_threat"]
        if live:
            body = [
                [
                    link(r["file"], cls(r["raw"].get("hazard_type"))),
                    cls(r["raw"].get("farming_system")),
                    esc(scope_label(r["raw"])),
                    cls(r["raw"].get("mitigation_potential")),
                    confidence_cell(r["raw"], "confidence"),
                    transfer_cell(r["raw"]),
                    esc(signal_marks(r["raw"])),
                ]
                for r in sorted(
                    live,
                    key=lambda r: (
                        r["raw"].get("hazard_type") or "",
                        r["raw"].get("farming_system") or "",
                        r["raw"].get("scope_id") or "",
                    ),
                )
            ]
            out += table(
                [
                    "Hazard",
                    "Farming system",
                    "Scope",
                    "Mitigation potential",
                    "Confidence",
                    "Transfer",
                    "Signals",
                ],
                body,
                caption=f"{esc(name)} · Hazard responses · risk to livelihoods (Module 2)",
            )
        if asset:
            body = [
                [
                    link(r["file"], cls(r["raw"].get("hazard_type"))),
                    cls(r["raw"].get("asset_sensitivity")),
                    confidence_cell(r["raw"], "confidence"),
                    transfer_cell(r["raw"]),
                ]
                for r in sorted(asset, key=lambda r: r["raw"].get("hazard_type") or "")
            ]
            out += table(
                ["Hazard", "Sensitivity of the investment", "Confidence", "Transfer"],
                body,
                caption=f"{esc(name)} · Hazard responses · threat to the investment (Module 2b)",
            )
    elif t == "T6":

        def theme(r):
            t5 = data.T5.get(r["raw"].get("variable_id"))
            return t5["theme"] if t5 else "other outcome"

        body = [
            [
                link(r["file"], esc(row_title(r))),
                esc(words(theme(r))),
                esc(scope_label(r["raw"])),
                cls(r["raw"].get("effect_direction")),
                confidence_cell(r["raw"], "effect_confidence"),
                transfer_cell(r["raw"]),
                esc(signal_marks(r["raw"])),
            ]
            for r in sorted(
                rows,
                key=lambda r: (theme(r), row_title(r), r["raw"].get("scope_id") or ""),
            )
        ]
        out += table(
            [
                "Priority or outcome",
                "Theme",
                "Scope",
                "Effect direction",
                "Confidence",
                "Transfer",
                "Signals",
            ],
            body,
            caption=f"{esc(name)} · {TABLE_NAMES['T6']}",
        )
    else:
        body = []
        for r in sorted(
            rows, key=lambda r: (row_title(r), r["raw"].get("scope_id") or "")
        ):
            rng = r["raw"].get("economic_value_range") or {}
            shown = (
                f"{esc(rng.get('low'))} to {esc(rng.get('high'))} {esc(words(rng.get('unit')))}"
                if rng.get("low") is not None
                else "Ordinal only: no range published"
            )
            body.append(
                [
                    link(r["file"], esc(row_title(r))),
                    esc(scope_label(r["raw"])),
                    shown,
                    confidence_cell(r["raw"], "effect_confidence"),
                    transfer_cell(r["raw"]),
                ]
            )
        out += table(
            [
                "Indicator",
                "Scope",
                "Indicative range (not normalised)",
                "Confidence",
                "Transfer",
            ],
            body,
            caption=f"{esc(name)} · {TABLE_NAMES['T6E']}",
        )
    return (f"<h4>{esc(heading)}</h4>" if heading else "") + out


def practice_page(practice):
    name = practice_name(practice)
    t0 = data.pinned_json(f"schema/recipes/{practice}/T0_nbs_registry.json")[0]
    counts = {t: data.ROW_COUNTS[(practice, t)] for t in ROW_TABLES}
    fams = data.FAMILIES[practice]
    lead = esc(PRACTICE_TEXT[practice][0])
    body = (
        '<div class="stats">'
        + "".join(
            f"<div><b>{counts[t]}</b><span>{badge(t)} {esc(TABLE_NAMES[t])}</span></div>"
            for t in ROW_TABLES
        )
        + f"<div><b>{len([f for f in fams if f in data.FAMILY_ROWS])}</b><span>registered suitability families</span></div></div>"
        + '<p class="basis">Rows in the draft recipe edition. Counts are rows, not evidence strength.</p>'
    )
    intro, toc = chapter_body(f"practice-{practice}")
    body += '<section class="chapter">' + intro + "</section>"

    body += '<h2 id="registry">Practice registry record</h2>' + render_value(
        {k: v for k, v in t0.items() if k not in {"nbs_id", "is_active"}}
    )

    fam_rows = []
    for f in fams:
        subs = data.FAMILY_ROWS.get(f, [])
        per = Counter(r["table"] for r in data.ROWS if r["family"] == f)
        fam_rows.append(
            [
                link(f"#fam-{esc(f)}", esc(family_name(f)))
                + f"<br><small>{code(f)}</small>",
                ", ".join(esc(s["name"]) for s in subs)
                or "Shared context across families",
                text(subs[0]["dominant_limiting_factor"]) if subs else "",
                "Cross-family context (not a product)"
                if is_cross(f)
                else (
                    ", ".join(esc(PRODUCTS[k][0]) for k in data.family_product(f))
                    or "Not registered"
                ),
            ]
            + [str(per.get(t, 0)) for t in ROW_TABLES]
        )
    body += '<h2 id="families">Suitability families in this edition</h2>' + table(
        ["Family", "Sub-practices", "Shared limiting factor", "Spatial product"]
        + [t for t in ROW_TABLES],
        fam_rows,
        caption=f"{esc(name)} · families, products and family-scoped rows",
        numeric=(4, 5, 6, 7),
    )

    body += f'<h2 id="T4">{badge("T4")} {TABLE_NAMES["T4"]}</h2>'
    body += (
        "<p>Each mapping carries a function role. A <em>suitability score</em> is intended to contribute a "
        "membership value once a function is selected and calibrated. An <em>eligibility gate</em> admits or "
        "removes locations before scoring. A <em>hard exclusion</em> defines a mask interface. An "
        "<em>operational scenario</em> is an implementation factor handled by project risk, shown in its own table. "
        "“Held” means a calibration was reviewed and no score is assigned. “Not recorded” means no calibration "
        "status is on the row; it is not an approval. “Function selected” records a choice for a named target or a "
        "gate's default design, not a global approval. “Execution-ready” is the producer's flag, published as "
        "“spatially validated”.</p>"
    )
    if counts["T4"] == 0:
        body += '<p class="empty">No compiled suitability mapping for any family of this practice in this edition. The family scheme and evidence are described above; effect rows below do not depend on it.</p>'
    for f in fams:
        subs = data.FAMILY_ROWS.get(f, [])
        body += f'<h3 id="fam-{esc(f)}">{esc(family_name(f))}</h3>'
        if f in FAMILY_CAPTION:
            body += f"<p>{esc(FAMILY_CAPTION[f])}</p>"
        if subs:
            body += f"<p><strong>Grouping rationale.</strong> {text(subs[0]['grouping_rationale'])}</p>"
        body += t4_family_block(practice, f)

    for t, intro_text in [
        (
            "T3",
            "Two lenses, kept apart: what the practice does for livelihoods under each hazard, and how each hazard threatens the investment itself.",
        ),
        (
            "T6",
            "Effects on the priorities a task team weighs. The practice-level roll-up is pooled over all the practice's findings and appears once; family rows follow.",
        ),
        (
            "T6E",
            "Indicative, ordinal economic information, including costs and reported cost reductions. Not normalised and not cost-benefit analysis.",
        ),
    ]:
        body += f'<h2 id="{t}">{badge(t)} {TABLE_NAMES[t]}</h2><p>{intro_text}</p>'
        if counts[t] == 0:
            body += '<p class="empty">No compiled row in this edition.</p>'
            continue
        body += "<h3>Practice-level roll-up</h3>" + (
            effect_tables(practice, t)
            or '<p class="empty">No practice-level row in this edition.</p>'
        )
        for f in fams:
            block = effect_tables(practice, t, f)
            if block:
                body += f"<h3>{esc(family_name(f))}</h3>" + block
            elif "qualitative_only" in data.family_product(f) and not is_cross(f):
                body += f'<h3>{esc(family_name(f))}</h3><p class="empty">Parked: qualitative guidance only (no map, no generated effect rows).</p>'

    toc = toc + [
        ("registry", "Practice registry record"),
        ("families", "Suitability families"),
        ("T4", TABLE_NAMES["T4"]),
        ("T3", TABLE_NAMES["T3"]),
        ("T6", TABLE_NAMES["T6"]),
        ("T6E", TABLE_NAMES["T6E"]),
    ]
    page(
        f"practice-{practice}.html",
        "practices.html",
        name,
        body,
        crumbs=[("practices.html", "Practices"), ("", name)],
        lead=lead,
        toc=toc,
    )


FAMILY_CAPTION = {}


def build():
    from core import FAMILY_TEXT

    FAMILY_CAPTION.update({k: v[1] for k, v in FAMILY_TEXT.items()})
    SIDE["practices.html"] = [
        (f"practice-{p}.html", practice_name(p)) for p in PRACTICE_IDS
    ]
    cards = []
    for p in PRACTICE_IDS:
        c = {t: data.ROW_COUNTS[(p, t)] for t in ROW_TABLES}
        fams = [f for f in data.FAMILIES[p] if f in data.FAMILY_ROWS]
        held = sum(
            1
            for r in data.ROWS
            if r["practice"] == p
            and r["table"] == "T4"
            and (data.readiness(r) or {}).get("calibration") == "Held"
        )
        cards.append(
            [
                link(f"practice-{p}.html", esc(practice_name(p)))
                + f"<br><small>{esc(PRACTICE_TEXT[p][0])}</small>",
                str(len(fams)),
                str(c["T4"])
                + (
                    f"<br><small>{held} held</small>"
                    if c["T4"]
                    else "<br><small>none compiled</small>"
                ),
                str(c["T3"]),
                str(c["T6"]),
                str(c["T6E"]),
            ]
        )
    total = {t: data.TABLE_TOTALS[t] for t in ROW_TABLES}
    cards.append(
        [
            "<strong>All six practices</strong>",
            str(
                sum(
                    len([f for f in data.FAMILIES[p] if f in data.FAMILY_ROWS])
                    for p in PRACTICE_IDS
                )
            ),
            f"<strong>{total['T4']}</strong>",
            f"<strong>{total['T3']}</strong>",
            f"<strong>{total['T6']}</strong>",
            f"<strong>{total['T6E']}</strong>",
        ]
    )
    body = (
        "<p>Each practice page gives the scientific basis of its family scheme, then every compiled row "
        "of the draft recipe edition with its status, uncertainty and evidence. Suitability is reasoned "
        "per family, because sub-practices with different limiting factors cannot share one map.</p>"
        + table(
            [
                "Practice",
                "Families",
                TABLE_NAMES["T4"],
                TABLE_NAMES["T3"],
                TABLE_NAMES["T6"],
                TABLE_NAMES["T6E"],
            ],
            cards,
            caption="Six practices in this draft edition · rows by table",
            numeric=(1, 2, 3, 4, 5),
        )
        + f'<p class="basis">{sum(total.values())} recipe rows in total: {sum(1 for r in data.ROWS if r["family"])} scoped to a family '
        f"(including named cross-family context) and {sum(1 for r in data.ROWS if not r['family'])} at practice level. "
        "Counts are rows in this edition and say nothing about evidence strength.</p>"
        "<h2>How to read a practice page</h2><ol>"
        "<li><strong>Family scheme.</strong> Which sub-practices are grouped, the limiting factor they share, and what kind of spatial product the family supports.</li>"
        "<li><strong>Suitability mappings.</strong> One row per variable and family, with its function role and calibration status. Operational scenarios are tabled separately.</li>"
        "<li><strong>Hazard responses.</strong> Risk to livelihoods and threat to the investment, shown separately.</li>"
        "<li><strong>Scorecard effects and indicative economic profiles.</strong> Direction, two-axis confidence, transfer class and any recorded harm.</li>"
        "<li><strong>Row detail.</strong> Every row opens to its full record and the findings and sources behind it.</li></ol>"
    )
    page(
        "practices.html",
        "practices.html",
        "Practices",
        body,
        lead="Six nature-based practices, their suitability families and every compiled row.",
    )
    for p in PRACTICE_IDS:
        practice_page(p)
    for r in data.ROWS:
        row_page(r)
