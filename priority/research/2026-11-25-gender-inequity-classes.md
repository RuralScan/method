# Gender inequity: approved approach and limitations

25 November 2026. Pete approved the classification approach and limitations. No data edition or numeric cutoffs calibrated.

Approval (chat): “ok approved, capture the gender inequity approach and limitations, noting national context only and no none/very little cutoff, then proceed to the next variable”

T5 links to `priority/classifications/rules.csv#gender_inequity_national_context`. `requires_reference_calibration` records the approach with blank cutoffs and no sample; scalar previews remain unknown. Global scope identifies the pooled reference approach, not local spatial coverage. The release-workflow state remains `proposed`; approach approval does not activate a dataset or runtime release.

The existing profile uses UNDP's national Gender Inequality Index (GII). It combines reproductive health, empowerment and labour-market dimensions. Values range from 0 to 1, with higher values indicating greater measured inequality. Its coverage is limited to countries with sufficient data. It is not an agriculture-specific measure of women's access to land, credit or decision-making. [UNDP: About GII](https://hdr.undp.org/data-center/thematic-composite-indices/gender-inequality-index).

The reviewed UNDP guidance does not provide a transferable None / Low / Medium / High classification for GII. Do not borrow HDI's four development bands or GDI's five parity groups: they classify different indices. The reader's guide distinguishes these explicitly under Human development classification and Tables 4–5. [UNDP reader's guide](https://hdr.undp.org/human-development-report-2020-readers-guide).

## Approved approach

Retain national GII as qualified country context. If class labels are useful, use Low / Medium / High terciles across a single global reference set of low-, lower-middle- and upper-middle-income economies with observed GII values for a common year in one UNDP release. Give each economy equal weight and retain raw GII values. This is a RuralScan relative convention, not UNDP severity thresholds. A common reference preserves the same interpretation across the eligible countries; regional or income-tier recalibration would need its own rationale.

No None / Very little cutoff is established. Even a low GII is not evidence that all forms of gender inequity are absent. Missing data remain unknown. Pin the release, year, income-group vintage and eligible countries before computing boundaries; do not mix latest-available years. No numerical thresholds are claimed in this note.

National classes cannot distinguish within-country hotspots and must not be rasterized into artificial local variation. Local prioritisation needs an appropriate subnational gender measure and separate interpretation. Do not transfer national GII cutoffs to a different local indicator, or construct local GII without its required components and a justified method. Until then, retain national context and leave local gender classification unavailable.

## Search record

Bounded primary-source search on 25 November 2026 used:

- `site.hdr.undp.org gender inequality index classification low medium high thresholds GII`
- `site.hdr.undp.org GII gender inequality index dimensions reproductive health empowerment labour market national`
- `site.hdr.undp.org "GII" "thresholds"`
- `site.hdr.undp.org "Gender Inequality Index" "quintiles"`

Read UNDP's current GII explanatory page and its published reader's guide sections distinguishing GII, GDI and HDI. No universal four-band standard was found in this bounded review; this is not a claim that no study has ever grouped GII. No dataset acquired, formal source registered or release decision recorded.

UNDP definition archived as a web-text excerpt in the team-library mirror under `0_Methodology_&_Frameworks/priority_classification/gender_inequity_2026_11_25/classification_sources.zip`. Direct HTML returned 403. Member readback matched saved bytes; remote team access not checked. Excerpt SHA-256: `a3417587f8f34d00ae6902f6310fc70ed757a88f53ad562e8a2ac6239317ab17`. Archive SHA-256: `27ff137a402a53c7b9701562ab2e21e1016d09d03f255b959802729b17f1be9d`.
