---
title: "M2b: Project disaster risk screen"
slug: m2b-project-risk
summary: Read hazard threats and operational barriers as a separate investment-risk screen.
sources:
  - methodology/modules/M2b_project_risk.md
  - method:priority/README.md
  - method:data-model/agent-effects-contract.json
  - method:decisions/current.csv
  - evidence:workflows/synthesis/README.md
  - methodology/T3_T6_generation_method.md
  - AGENTS.md
  - schema/recipes/agroforestry/T4_suitability_mappings.csv
  - schema/lookups/m2b_variable_policy.csv
  - methodology/RULESET_VERSIONS.md
  - methodology/modules/M6_handoff.md
  - method:handbook/implement-a-scan.md
---

## Question this module answers

Module 2b (M2b) asks what could damage the proposed intervention or prevent it from working as intended. It provides an early investment-risk screen, with two parts: **Stream A** examines hazards to the intervention; **Stream B** examines operational barriers such as access, tenure and finance. [src: methodology/modules/M2b_project_risk.md §3] [src: methodology/modules/M2b_project_risk.md §12]

### Two risk lenses

[[ch:m2-climate-risk|M2]] describes climate-related need among people and production systems. M2b describes threats to the investment. A flood-prone landscape may need protection while also posing risks to proposed restoration. Keep both questions visible; never add M2b to suitability or the priority score. [src: methodology/modules/M2b_project_risk.md §2] [src: method:priority/README.md]

### What M2b is not

This screen does not predict engineering failure, establish safety or complete project-level disaster-risk assessment. It identifies questions for feasibility and design. A low flag means that no screened threat stands out under the stated rules, not that the site is safe. [src: methodology/modules/M2b_project_risk.md §3] [src: methodology/modules/M2b_project_risk.md §10]

## Inputs

Table: Inputs to the two investment-risk screens.

| Input | Purpose |
|---|---|
| Practice, family and candidate footprint | Identify what could be affected and where. |
| Baseline and future hazard data | Describe exposure under named scenarios. |
| T3 asset-threat evidence | Explain the intervention's sensitivity, confidence and applicability. |
| Establishment period and vulnerability window | Identify when damage could matter most. |
| Operational evidence and data | Describe barriers to delivery and maintenance. |

[src: methodology/modules/M2b_project_risk.md §4] [src: methodology/modules/M2b_project_risk.md §12]

## Method, Stream A: asset hazard exposure

### Step A1. Scope the asset-threat hazards

Use [[table:T3]] rows that address threats to the asset. Evidence that a practice protects livelihoods does not establish that the practice itself withstands the same hazard. If no asset hazards have been screened, report that gap explicitly. [src: method:data-model/agent-effects-contract.json] [src: methodology/modules/M2b_project_risk.md §6]

### Step A2. Accepted asset-threat judgments

An AI proposal explains sensitivity, confidence and applicability from reviewed evidence; a human reviewer accepts the exact judgments. [[ch:effect-synthesis]] describes that process. Historical T3 rows remain historical until explicitly replaced. [src: method:decisions/current.csv §t3t6_agent_synthesis]

### Step A3. Asset-threat-only hazards

Where a threat has no compatible spatial layer, retain it as a descriptive warning. A textual judgment about sedimentation, extreme rainfall or landslides does not create a mapped hazard surface. [src: evidence:workflows/synthesis/README.md]

### Step A4. Use accepted weights without filling gaps

If a weighted assessment is proposed, its accepted set must cover drought, flood, heat stress, fire, wind/cyclone and waterlogging, with weights summing to one. Missing or held weights mean no accepted weighted assessment. Code does not derive weights from sensitivity ranks or substitute equal weights. These requirements do not by themselves define the spatial risk calculation. [src: evidence:workflows/synthesis/README.md] [src: method:data-model/agent-effects-contract.json]

### Step A5. Read the vulnerability window with the establishment period

Read the period of greatest vulnerability beside the establishment period in [[table:T0]]. Newly planted vegetation may face different threats from an established system. State the horizon being screened; establishment duration alone supplies no numerical multiplier for future hazards. Practice records retain their reported periods and gaps. [src: methodology/T3_T6_generation_method.md §7.5] [src: methodology/modules/M2b_project_risk.md §12]

### Step A6. Compose the asset-hazard rating

Show hazard exposure alongside accepted sensitivity judgments. Any combined rating needs a separately specified calculation, footprint measure, missing-data treatment and class boundaries. Do not infer these from historical weights or draft equations. Where no approved formulation applies, report the individual threats and uncertainty instead. [src: methodology/modules/M2b_project_risk.md §11] [src: method:decisions/current.csv §t3t6_agent_synthesis]

Compare future and baseline conditions using compatible hazard measures and declared exposure assumptions. A change in map scaling must not be presented as a physical change in risk. [src: methodology/modules/M2b_project_risk.md §6] [[ch:m2-climate-risk]]

## Method, Stream B: operational and enabling environment

### Why these variables live here

Road access, finance, tenure, extension and labour can affect delivery without defining whether a practice is biophysically suitable. Treat these as operational questions and possible investment scenarios. Applicable hard legal or physical exclusions remain suitability masks; a favourable score elsewhere cannot offset them. [src: AGENTS.md §What is locked]

Operational findings use the evidence role `operational_risk`. Some historical records sit in T4, but that storage location does not make them structural suitability criteria. [src: AGENTS.md §What is locked] [src: schema/recipes/agroforestry/T4_suitability_mappings.csv]

### The eight levers

Table: Operational questions to investigate.

| Factor | Question |
|---|---|
| Accessibility | Can people, materials and maintenance reach the site? |
| Electrification | Does implementation depend on unavailable power? |
| Tenure | Are access, use and management rights secure and understood? |
| Conflict and fragility | Could insecurity disrupt delivery or maintenance? |
| Governance and extension | Is suitable institutional and technical support available? |
| Finance and credit | Can establishment and recurrent costs be financed? |
| Market and value chain | Are relevant services and markets accessible? |
| Labour | Is the required labour available at the necessary times? |

[src: methodology/modules/M2b_project_risk.md §12] Dataset definitions and context-specific choices are linked through [[table:VONT]] and [[table:BIND]], rather than repeated as a second catalogue here.

### Variable policy: what Stream B must not hold

Adoption is an outcome of the operating environment, not itself an operational-risk cause. It can inform effect conditions and implementation guidance. Details such as planting material or restorable patch size belong to feasibility. The extraction policy records these distinctions; a policy mention or site description alone does not demonstrate cause and effect. [src: schema/lookups/m2b_variable_policy.csv] [src: methodology/RULESET_VERSIONS.md §v1.9.0]

### The safeguard flag

Mapped overlap with Indigenous Peoples' and local community land raises the recorded `FPIC_REQUIRED` flag and a prompt for free, prior and informed consent and World Bank Environmental and Social Standard 7 assessment. It does not establish consent or discharge safeguards. Missing mapped overlap does not establish absence of people or rights. [[ch:m6-handoff]] explains the follow-up. [src: methodology/modules/M2b_project_risk.md §12] [src: methodology/modules/M6_handoff.md §10]

### How Stream B is applied

Report each operational factor with its source, context, uncertainty and follow-up question. State any screening threshold explicitly. Do not invent a combined operational index or turn an investment-addressable barrier into a structural exclusion. Scenarios can show what would change if a barrier were addressed. [src: methodology/modules/M2b_project_risk.md §11] [src: methodology/modules/M2b_project_risk.md §12]

## Applying the screen to the opportunity space

Show the screen alongside candidate areas and priority results. If a documented screening rule removes areas from a shortlist, preserve the original result and state the reason and affected footprint. Otherwise retain the areas with flags. M2b never contributes a weighted term to the priority sum. [src: methodology/modules/M2b_project_risk.md §8] [src: method:priority/README.md]

## Outputs

Provide hazard-specific maps where supported, sensitivity evidence, operational flags and questions for local assessment. State scenarios, footprint units, data gaps and any approved combined calculation. Keep baseline and future outputs distinguishable. [src: methodology/modules/M2b_project_risk.md §5] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Worked illustration

Consider a restoration area with flood exposure and uncertain access for maintenance. The flood layer describes exposure; the asset-threat evidence describes possible damage; the access flag identifies an implementation question. Together they guide further assessment. None supplies a loss probability, and none is added to the area's poverty or biodiversity priority score. This is a hypothetical reading example, not a calculated risk result. [src: methodology/modules/M2b_project_risk.md §2] [src: methodology/modules/M2b_project_risk.md §12]

## Assumptions and limits

Sparse asset evidence, coarse hazard layers and national operational proxies can miss local risks. Historical or incomplete weights do not fill gaps in an accepted assessment. Feasibility must assess hazards and design at site scale, verify tenure and access, and carry out the relevant consultation and safeguard processes. [src: evidence:workflows/synthesis/README.md] [src: methodology/modules/M2b_project_risk.md §10] [src: methodology/modules/M2b_project_risk.md §12]

## Where this is configured

[[table:T3]] holds asset-threat judgments and [[table:T2]] identifies climate variables. [[table:T0]] records establishment periods. [[table:EV]] retains asset-vulnerability and operational findings. [[table:VONT]], [[table:T1]] and [[table:BIND]] define variables and datasets. [[table:T4]] keeps structural exclusions separate. The application record must state any approved risk formulation and screening choices.
