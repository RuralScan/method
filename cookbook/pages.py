"""Render the recipe selection guide from checked method and evidence inventories."""

TABLES = ("T3", "T4", "T6", "T6E")
EVIDENCE = "https://github.com/RuralScan/evidence/blob"
METHOD = "https://github.com/RuralScan/method/blob"

# Reader-facing descriptions explain what to inspect; numerical rules remain in the release.
PRACTICES = {
    "agroforestry": (
        "Integrate trees with crops or livestock, or retain woody regrowth on farms.",
        "Start with how trees become established. A planted system, regrowth from existing rootstock, a field boundary and a shade crop each need different site information.",
        "For shaded perennial crops, check where the host crop is grown. For regeneration, check local evidence of viable woody regrowth. Record tenure, finance and access separately when assessing implementation.",
    ),
    "forest_restoration": (
        "Choose a recovery pathway for degraded land or protect existing forest.",
        "Distinguish recovery toward an ecological baseline from production forestry. Check whether seed sources and residual trees can support recovery, whether planting is needed, or whether existing forest needs protection.",
        "Confirm prior land cover and the intended ecological baseline before proposing tree planting. On non-forest ecosystems, assess the risk of harm from afforestation.",
    ),
    "mangrove_restoration": (
        "Restore coastal mangrove habitat through planting or recovery of tidal exchange.",
        "Both variants belong to one family. Check tidal exchange, intertidal elevation and sediment conditions, then establish whether propagules can reach the site.",
        "Verify local tidal connectivity before choosing planting or hydrological restoration. Establishment time, time to benefit and recurrent cost need site-specific evidence.",
    ),
    "riparian_buffer": (
        "Establish or restore vegetation along watercourses.",
        "Identify the watercourse and the condition of its banks. Choose between restoring existing riparian vegetation and establishing a planted strip.",
        "Check how accurately the stream network, adjacent land use and buffer width can be resolved. Confirm the width on the ground before estimating a planted footprint.",
    ),
    "water_harvesting_conservation": (
        "Retain rainfall in fields, reshape slopes or collect runoff for storage or use.",
        "Identify where water originates and where it will be used. A field receiving rainfall, a short slope feeding a basin and a channel supplying storage belong to different families.",
        "For bench terraces, check the slope and soil information for the proposed design. The documented annual rainfall range in the worked example supports a siting observation. Its numerical calibration remains on hold.",
    ),
    "wetland_management": (
        "Restore wetland hydrology, rewet peat or assess wetland creation.",
        "Check present and former wetland extent, soil and water source. Creation, restoration of a former wetland, peatland rewetting and engineered treatment answer different siting questions.",
        "For reconnection, verify former wetland extent and hydraulic connectivity. For peatland work, establish peat presence, drainage history and water-table conditions.",
    ),
}

PRODUCTS = {
    "area_suitability": (
        "Area suitability",
        "A potential area surface at a resolution supported by the inputs.",
    ),
    "applicability_zone": (
        "Applicability zone",
        "A zone in which to inspect individual locations. Field layouts and structure footprints need local delineation.",
    ),
    "zonal_linear": (
        "Linear corridor",
        "A reach or corridor along a network. Report its length or reach-level coverage and document any width assumption.",
    ),
    "qualitative_only": (
        "Qualitative guidance",
        "A qualitative assessment or contextual evidence. No pixel-area footprint is assigned.",
    ),
}

# The family register supplies membership. These captions translate its limiting
# factors into field questions, keeping implementation and scoring distinct.
CROSS_FAMILY = (
    "Cross-family context",
    "Read shared observations here. Choose a specific intervention family when defining a map.",
)
FAMILIES = {
    "agroforestry__cross_family": CROSS_FAMILY,
    "agroforestry__homegardens_proximity": (
        "Homegardens",
        "Check household access to water and proximity to settlements at the local site.",
    ),
    "agroforestry__linear_boundary": (
        "Linear plantings and boundaries",
        "Locate the field boundary, prevailing wind or contour line that sets the planting position.",
    ),
    "agroforestry__planted_silvoarable": (
        "Trees planted on cropland",
        "Check whether planting can fit cultivable land and field operations.",
    ),
    "agroforestry__regeneration_farmland": (
        "Regeneration on farmland",
        "Look for remnant trees, rootstock or seed supply that can support regrowth.",
    ),
    "agroforestry__shaded_perennial": (
        "Shaded perennial crops",
        "Locate the host crop and consider the conditions under which shade would help it.",
    ),
    "agroforestry__silvopastoral": (
        "Trees with livestock",
        "Check the grazing system and forage conditions alongside tree establishment.",
    ),
    "forest_restoration__active_planting": (
        "Active planting",
        "Check land history, existing canopy and whether the intended trees can establish.",
    ),
    "forest_restoration__assisted_regeneration": (
        "Assisted regeneration",
        "Identify surviving regeneration potential and the intervention needed for recovery.",
    ),
    "forest_restoration__cross_family": CROSS_FAMILY,
    "forest_restoration__passive_regeneration": (
        "Passive regeneration",
        "Look for seed sources and residual cover, and assess whether the pressure preventing recovery can be removed.",
    ),
    "forest_restoration__plantation": (
        "Plantation forestry",
        "Confirm that production forestry is the objective and assess establishment of the target species.",
    ),
    "forest_restoration__protection_cbfm": (
        "Protection and community forest management",
        "Locate existing forest and the pressures that threaten it.",
    ),
    "mangrove_restoration__tidal_coastal": (
        "Tidal mangrove systems",
        "Check the coastal water and sediment regime. For natural recovery, also check propagule supply.",
    ),
    "riparian_buffer__natural_restored": (
        "Natural or restored riparian vegetation",
        "Identify bank degradation, existing vegetation, regeneration potential and connection to the watercourse.",
    ),
    "riparian_buffer__planted": (
        "Planted riparian buffers",
        "Inspect slope and available width beside the watercourse and the runoff entering from adjoining fields.",
    ),
    "water_harvesting__cross_family": CROSS_FAMILY,
    "water_harvesting__in_situ": (
        "In-field water conservation",
        "Examine how rainfall infiltrates and is retained in the cultivated soil.",
    ),
    "water_harvesting__micro_catchment": (
        "Microcatchments",
        "Locate the short runoff-producing slope and the adjacent basin or planting strip it supplies.",
    ),
    "water_harvesting__rooftop": (
        "Rooftop harvesting",
        "Inspect the roof and domestic storage arrangement at building scale.",
    ),
    "water_harvesting__runoff_catchment": (
        "Runoff capture and storage",
        "Trace the contributing drainage area, then check storage terrain and the chosen structure’s siting requirements.",
    ),
    "water_harvesting__spate": (
        "Spate or floodwater harvesting",
        "Locate an ephemeral channel and examine the floodwater and sediment it carries.",
    ),
    "water_harvesting__terracing": (
        "Terracing",
        "Inspect slope and the soil depth needed to reshape it. For stone structures, check material availability.",
    ),
    "wetland_management__coastal": (
        "Coastal wetlands",
        "Check tidal inundation, salinity and elevation.",
    ),
    "wetland_management__constructed": (
        "Constructed treatment wetlands",
        "Identify the inflow or drainage source and assess the engineered site.",
    ),
    "wetland_management__creation": (
        "Wetland creation or reconstruction",
        "Check water supply, terrain and soils where a wetland could be established.",
    ),
    "wetland_management__peatland": (
        "Peatland rewetting and paludiculture",
        "Confirm peat soils, drainage state and water table. Paludiculture also requires a suitable wet crop.",
    ),
    "wetland_management__restoration_rewetting": (
        "Restoration and rewetting",
        "Check former wetland extent, altered drainage and hydraulic connectivity.",
    ),
}


def numbers(counts):
    return " | ".join(f"{counts[key]:,}" for key in TABLES)


def cell(value):
    return " ".join(value.split()).replace("|", r"\|")


def recipe_page(practice, profile, definition_revision, evidence_revision):
    families = sorted(
        profile["families"].items(),
        key=lambda pair: (FAMILIES[pair[0]] == CROSS_FAMILY, FAMILIES[pair[0]][0]),
    )
    _, decision, field_check = PRACTICES[practice]
    evidence_page = f"{EVIDENCE}/{evidence_revision}/publication/recipes/{practice}.md"
    data = f"{METHOD}/{definition_revision}/data-model/configuration"
    lines = [
        f"# {profile['name']}",
        "",
        "[Choose another practice](README.md)",
        "",
        decision,
        "",
        "## Choose a family",
        "",
        "| Family | What determines the choice? | Registered variants | Intended spatial product |",
        "|---|---|---|---|",
    ]
    for fid, family in families:
        title, question = FAMILIES[fid]
        names = ", ".join(cell(v["name"]) for v in family["variants"])
        product, _ = PRODUCTS[family["product_type"]]
        lines.append(f"| {title} | {question} | {names} | {product} |")
    lines += [
        "",
        f"[Practice definition (T0)]({data}/recipes/{practice}/T0_nbs_registry.csv) · [Variant definitions and grouping rationale (FAM)]({data}/FAM_family_registry.csv)",
        "",
        "## Interpret the spatial output",
        "",
    ]
    for kind in sorted({f["product_type"] for _, f in families}):
        product, meaning = PRODUCTS[kind]
        lines.append(f"- **{product}.** {meaning}")
    lines += ["", field_check, ""]
    if practice == "water_harvesting_conservation":
        lines += [
            "[Trace the bench-terrace rainfall decision](../handbook/read-a-suitability-recipe.md)",
            "",
        ]
    lines += [
        "## Inspect compiled evidence",
        "",
        "Each count is an analytical row in the pinned candidate. The family named on the row determines where it is counted. Rows with no family ID appear once under **Practice-wide**, including rows limited to a particular geography or farming system.",
        "",
        "| Scope | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles |",
        "|---|---:|---:|---:|---:|",
    ]
    for fid, family in families:
        lines.append(f"| {FAMILIES[fid][0]} | {numbers(family['counts'])} |")
    lines.extend(
        [
            f"| **Practice-wide** | {numbers(profile['practice_counts'])} |",
            f"| **All scopes** | {numbers(profile['totals'])} |",
            "",
            f"[Inspect individual rows, context and evidence references]({evidence_page})",
            "",
            "## Check suitability before mapping",
            "",
        ]
    )
    mappings = [(fid, f) for fid, f in families if f["counts"]["T4"]]
    if mappings:
        lines += [
            "Read each mapping’s evidence and limitations. A row can offer several functions. Selection identifies the effective function. The spatial validation count uses the producer’s execution-readiness flag.",
            "",
            "| Family | Variables in T4 | Mappings with options | With selected function | Spatially validated |",
            "|---|---|---:|---:|---:|",
        ]
        for fid, family in mappings:
            variables = ", ".join(f"`{v}`" for v in family["mapping_variables"])
            lines.append(
                f"| {FAMILIES[fid][0]} | {variables} | {family['with_options']} | {family['selected']} | {family['spatially_validated']} |"
            )
        if practice == "agroforestry":
            lines += [
                "",
                "Access, finance and tenure can appear in compiled records. Evaluate these implementation factors through the investment-risk screen and local follow-up. The core suitability assessment uses its structural constraints and hard exclusions.",
            ]
    else:
        lines += [
            "This candidate contains zero compiled T4 mappings for this practice. The family definitions describe the intended product. A local suitability score would require supported mappings and spatial validation."
        ]
    lines += [
        "",
        f"[Open the candidate’s T4 section]({evidence_page}#t4-suitability-mappings) · [Prepare a scoping brief](../handbook/implement-a-scan.md)",
    ]
    lines += [
        "",
        "<details>",
        "<summary>Family IDs for configuration and evidence lookup</summary>",
        "",
        f"Use `{practice}` for the practice ID.",
        "",
    ]
    for fid, _ in families:
        lines.append(f"- {FAMILIES[fid][0]} · `{fid}`")
    lines += ["", "</details>"]
    return "\n".join(lines) + "\n"


def pages(profiles, pin, evidence_revision, definition_revision):
    """Return selector and practice pages. All counts come from the verified release."""
    result = {}
    lines = [
        "# Choose a recipe",
        "",
        "Start with the intervention you are considering. Open its recipe to choose a family of sub-practices with similar siting constraints, see what spatial product it supports and inspect its compiled evidence.",
        "",
        "| Practice | Decision to scope | Registered families | T4 mappings |",
        "|---|---|---:|---:|",
    ]
    for practice, profile in sorted(profiles.items()):
        filename = f"{practice}.md"
        lines.append(
            f"| [{profile['name']}]({filename}) | {PRACTICES[practice][0]} | {len(profile['families'])} | {profile['totals']['T4']} |"
        )
        result[filename] = recipe_page(
            practice, profile, definition_revision, evidence_revision
        )

    totals = {t: sum(p["totals"][t] for p in profiles.values()) for t in TABLES}
    families = [f for p in profiles.values() for f in p["families"].values()]
    family_counts = {t: sum(f["counts"][t] for f in families) for t in TABLES}
    whole_counts = {
        t: sum(p["practice_counts"][t] for p in profiles.values()) for t in TABLES
    }
    cross_entries = sum(
        len(group["variants"])
        for profile in profiles.values()
        for fid, group in profile["families"].items()
        if FAMILIES[fid] == CROSS_FAMILY
    )
    lines += [
        "",
        "## What the counts mean",
        "",
        f"The family register contains {sum(len(f['variants']) for f in families)} entries grouped into {len(families)} families. Of those entries, {cross_entries} record cross-family context. The candidate contains {sum(totals.values())} analytical rows. A source can contribute to several rows.",
        "",
        "| Scope of the row | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles | Total |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Assigned to a family | {numbers(family_counts)} | {sum(family_counts.values())} |",
        f"| Practice-wide | {numbers(whole_counts)} | {sum(whole_counts.values())} |",
        f"| **All rows** | {numbers(totals)} | **{sum(totals.values())}** |",
        "",
        "Practice-wide rows appear once per practice. Check the record for any geographic or farming-system conditions before applying it.",
        "",
        "T3 distinguishes how a practice may mitigate livelihood risk from hazards to the investment itself. T6 records scorecard effects. T6E supplies indicative economic profiles. For T4, a zero count means the release has no compiled suitability mapping in that scope. Local suitability remains undetermined.",
        "",
        f"Of {totals['T4']} T4 mappings, {sum(f['with_options'] for f in families)} offer function options, {sum(f['selected'] for f in families)} have a selected function and {sum(f['spatially_validated'] for f in families)} are spatially validated. These counts overlap. Use an accepted analytical release and compatible runtime for spatial execution.",
        "",
        f"Candidate release `{pin['release_id']}`. [Browse the pinned analytical rows]({EVIDENCE}/{evidence_revision}/publication/recipes/README.md) · [Pinned method definitions]({METHOD}/{pin['method']['revision']}/{pin['method']['manifest']})",
        "",
        "[Follow the seven modules](../handbook/start-here.md) · [Implement a scan](../handbook/implement-a-scan.md) · [Trace a worked suitability mapping](../handbook/read-a-suitability-recipe.md) · [Reproduce these guides](../handbook/reproduce-recipe-guides.md)",
    ]
    lines += ["", "[Download the print edition](rural-scan-cookbook.html)"]
    result["README.md"] = "\n".join(lines) + "\n"
    return result
