# Draft definition baseline and unresolved references

Each of the six practices in the candidate analytical release has a T0 definition. Start with T0 for the practice scope and listed references, then use FAM for its sub-practices and suitability families. [Browse practice definitions](configuration/recipes) · [Family register](configuration/FAM_family_registry.csv) · [Candidate table counts by practice](https://github.com/RuralScan/evidence/blob/b0fd4ea66d817509c16584a3c1f128194c144478/workflows/recipe_release/counts.md)

## Source versions

All six T0 files match the practice definitions in the [pinned recipe source](https://github.com/CIAT/nbs_ruralscan/tree/157a26c2729c05cccf2b1d9374a63e28c97acac6/schema/recipes). The shared draft definitions retain their [earlier source revision](https://github.com/CIAT/nbs_ruralscan/tree/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema). The table records upstream file hashes. Use the [method snapshot](definition-snapshot.json) for the exact distributed files and the method Git revision that contains them.

The historical terrace replay pins the five-identity snapshot, including the earlier forest scope. The current reference adds the mangrove record and aligns the forest record with that separate coastal practice. [Historical replay snapshot](https://github.com/RuralScan/method/blob/aad360c25efd64d6a2754138e79ca558d2b472c7/data-model/definition-snapshot.json)

| Local file | Pinned source | Upstream SHA-256 |
|---|---|---|
| `LICENSE` | [LICENSE](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/LICENSE) | `2c7cec6f2a5b382f97d69f9e1924779bedd44ccfa53baab6f0e720ac55855c18` |
| `data-model/spec.md` | [schema/spec.md](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/spec.md) | `9535ec70971d550fc827ffe8f8f0c4295e525d9db807cf25e9deaf8691d76dc1` |
| `data-model/structure/columns.json` | [schema/structure/columns.json](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/structure/columns.json) | `a14fde2e23271d448939b7def1195f093d37f513621a92eee2b70190fc6aa9da` |
| `data-model/configuration/T1_data_registry.csv` | [schema/T1_data_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/T1_data_registry.csv) | `1746c118f1c13594e18baf884238718e67d8f528d2c1ac25d2c6d0ca2e55e5b0` |
| `data-model/configuration/T2_climate_risk.csv` | [schema/T2_climate_risk.csv](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/T2_climate_risk.csv) | `be738086bdc53e86cc31878d6311c80ab839ac9bf999a63efbcb572629eff5c1` |
| `data-model/configuration/T5_opportunity_space.csv` | [schema/T5_opportunity_space.csv](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/T5_opportunity_space.csv) | `cdb5ae63b4380fa4ee1400a1f1ab8cc00f7a13fe2114f5f66c64c622ebff4069` |
| `data-model/configuration/T7_geographic_context.csv` | [schema/T7_geographic_context.csv](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/T7_geographic_context.csv) | `bdba18eb0c6350646035eba2d72d22e93d14e9fb354ba1c219c0ed3bbef719a0` |
| `data-model/configuration/FAM_family_registry.csv` | [schema/registers/FAM_family_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/registers/FAM_family_registry.csv) | `3050387be3fd30d2913effcde7dc51fe60de833366be95fb111518959e214136` |
| `data-model/configuration/VONT_variable_ontology.csv` | [schema/registers/VONT_variable_ontology.csv](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/registers/VONT_variable_ontology.csv) | `077931150bc3c8b806080c25a82d2103268a8155e609b7dc51b286984bf9d1be` |
| `data-model/configuration/BIND_dataset_binding.csv` | [schema/registers/BIND_dataset_binding.csv](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/registers/BIND_dataset_binding.csv) | `6aeb5481a121cca768efd69ebe277b95a85e2c7f1ef9941e9cc74536c9bcfa35` |
| `data-model/configuration/recipes/agroforestry/T0_nbs_registry.csv` | [schema/recipes/agroforestry/T0_nbs_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/157a26c2729c05cccf2b1d9374a63e28c97acac6/schema/recipes/agroforestry/T0_nbs_registry.csv) | `77515030198f36185a8ec12fbe12fe3a4f39ae4b665b4780288d5bf1b22bb19b` |
| `data-model/configuration/recipes/forest_restoration/T0_nbs_registry.csv` | [schema/recipes/forest_restoration/T0_nbs_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/157a26c2729c05cccf2b1d9374a63e28c97acac6/schema/recipes/forest_restoration/T0_nbs_registry.csv) | `b9a620d556598c8e021a594698d73de084b77371ba4194945d700bcec3a1da86` |
| `data-model/configuration/recipes/mangrove_restoration/T0_nbs_registry.csv` | [schema/recipes/mangrove_restoration/T0_nbs_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/157a26c2729c05cccf2b1d9374a63e28c97acac6/schema/recipes/mangrove_restoration/T0_nbs_registry.csv) | `a69f3a04d56ddd1e0b0b31a086658667928905a1a1439dafcfbe38d80009d257` |
| `data-model/configuration/recipes/riparian_buffer/T0_nbs_registry.csv` | [schema/recipes/riparian_buffer/T0_nbs_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/157a26c2729c05cccf2b1d9374a63e28c97acac6/schema/recipes/riparian_buffer/T0_nbs_registry.csv) | `3448d1af7042bf13573c1495abc94b4e023726ea7b91ea927b7f201d28600a06` |
| `data-model/configuration/recipes/water_harvesting_conservation/T0_nbs_registry.csv` | [schema/recipes/water_harvesting_conservation/T0_nbs_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/157a26c2729c05cccf2b1d9374a63e28c97acac6/schema/recipes/water_harvesting_conservation/T0_nbs_registry.csv) | `10c18ae2c25d95d1bb37b079edf4050148719d51aff27973798ac81f8d0ca068` |
| `data-model/configuration/recipes/wetland_management/T0_nbs_registry.csv` | [schema/recipes/wetland_management/T0_nbs_registry.csv](https://github.com/CIAT/nbs_ruralscan/blob/157a26c2729c05cccf2b1d9374a63e28c97acac6/schema/recipes/wetland_management/T0_nbs_registry.csv) | `f54f294d9c8129a53f2aa20873c0f2647ef853e5cce41057f54aa2b23f44c45c` |

## Verify the definition files

From a full method checkout, verify the exact Git objects named by the manifest. To inspect a historical file, open it at the manifest’s `source_revision`; the commit containing the manifest can have a different tree.

```sh
python3 - <<'VERIFY'
import hashlib, json, subprocess
from pathlib import Path

manifest = json.loads(Path("data-model/definition-snapshot.json").read_bytes())
for name, expected in manifest["sha256"].items():
    pinned = subprocess.check_output(["git", "show", f"{manifest['source_revision']}:{name}"])
    if hashlib.sha256(pinned).hexdigest() != expected:
        raise SystemExit(f"Definition mismatch: {name}")
print(f"Verified {len(manifest['sha256'])} definition files.")
VERIFY
```

## Status and dependency index

- **Practice coverage.** The 56 FAM sub-practices belong to 28 suitability families across six T0 practices. Planting and ecological mangrove restoration share the tidal-coastal family. Mangrove establishment time, time to benefit and recurrent cost require local evidence. Their missing values must stay unset until the site, intervention and outcome are specified. [Mangrove definition](configuration/recipes/mangrove_restoration/T0_nbs_registry.csv)
- **Variable statuses:** VONT has 68 canonical, 31 pending_review, 18 pending, 45 blank and 2 rejected records. Preserve every status; blank does not mean approved.
- **Dataset availability:** 16 of 46 BIND rows require an upload. T1 is metadata, with per-source restrictions; no underlying dataset is bundled or licensed by this snapshot.
- **Evidence provenance:** resolve claim references against pinned [EV](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/registers/EV_evidence_register.csv) and [SRC](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/registers/SRC_source_register.csv). These registers remain external dependencies of this method snapshot.
- **Other configuration dependencies:** [lookups](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/lookups) and the remaining [registers](https://github.com/CIAT/nbs_ruralscan/blob/dd80226700432e9abd4aa9262262b9ad5ad6dfd5/schema/registers) are external dependencies. Compilation policies, crosswalks, confidence conventions and source-specific adjudications must be resolved before building a complete analytical bundle.
- **Analytical outputs held:** all T4 mappings, function-bound run policies, compiled T3/T6/T6E files and accepted analytical manifests are not included. This is not a complete recipe bundle.
- **Specification status:** source prose contains historical counts and relative links. Use the earlier shared-definition source to resolve them. Historical counts and missing relative targets have not yet been fully reconciled; the versioned source and included structure manifest remain available for comparison.

The [start-here guide](../handbook/start-here.md) explains the conceptual workflow.
