"""Render the current T2 registry without activating historical defaults."""
import importlib.util
from core import METHOD, METHOD_REV, METHOD_URL, FILES, code, esc, link, table

spec = importlib.util.spec_from_file_location("t2_registry", METHOD / "priority/t2/registry.py")
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)


def publish(checks):
    manifest = registry.check(METHOD)
    paths = [item["path"] for item in manifest["files"]] + ["priority/t2/manifest.json"]
    for path in paths:
        # Keep the repository-relative paths so manifest hashes resolve after download.
        FILES["data/current-t2/" + path] = (METHOD / path).read_text()
    checks.append(("Current T2 downloads match their declared hashes",
                   all(registry.digest(FILES["data/current-t2/" + item["path"]].encode()) == item["sha256"] for item in manifest["files"]),
                   str(len(manifest["files"])) + " hashed downloads"))
    checks.append(("Current T2 preserves all IDs and has no runnable classifications",
                   manifest["rows"] == 11 and manifest["runnable_variables"] == 0,
                   "11 preserved IDs; explicit unverified bindings and blocked readiness"))
    return {"revision": METHOD_REV, "status": manifest["status"],
            "rows": manifest["rows"], "runnableVariables": 0,
            "browse": "table-T2.html#current-t2", "manifest": "data/current-t2/priority/t2/manifest.json",
            "files": [{**item, "url": "data/current-t2/" + item["path"]} for item in manifest["files"]]}


def render():
    rows, schema, migration = registry.read(METHOD)
    body = '<h2 id="current-t2">Current climate-variable registry</h2>'
    body += '<p>T2 lists individual variables. It does not calculate a Climate Risk Index. All eleven existing IDs are retained. No entry is ready for analysis: dataset bindings and classification rules still need verification and acceptance.</p>'
    body += '<p>Roles below are proposed routing for review of this migration. A priority label does not approve a layer for scoring. Context descriptors and the operational investment-risk screen stay outside the climate-need sum. Unknown values are not zero.</p>'
    body += '<p>Download ' + ' · '.join(link('data/current-t2/priority/t2/' + name, label) for name, label in [('variables.csv','current T2 CSV'),('schema.json','field schema'),('migration.json','migration trace'),('manifest.json','manifest')]) + '. Read ' + link(METHOD_URL + 'priority/t2/README.md','registry guide') + '.</p>'
    body += table(['Variable', 'Scenario', 'Proposed role', 'Candidate dataset', 'Readiness'],
                  [[link('#t2-' + r['variable_id'], esc(r['label'])) + '<br>' + code(r['variable_id']),
                    esc(r['scenario_type'].replace('_',' ')), esc(r['mcda_role'].replace('_',' ')),
                    code(r['candidate_dataset_id']), 'Not ready — see blockers'] for r in rows],
                  caption='T2 · current entries awaiting binding and classification')
    body += '<h3 id="t2-blockers">What each entry still needs</h3>'
    for row in rows:
        body += '<details id="t2-' + esc(row['variable_id']) + '"><summary>' + esc(row['label']) + '</summary>'
        body += '<p><strong>Intended quantity:</strong> ' + esc(row['quantity']) + '. <strong>Unit:</strong> ' + esc(row['unit'] or 'not established') + '. <strong>Time statistic:</strong> ' + esc(row['temporal_statistic']) + '.</p>'
        body += '<p><strong>Possible shared concern:</strong> ' + code(row['concern_id']) + '. This identifies overlap for review, not equivalence.</p>'
        body += '<p><strong>Before use:</strong> ' + esc(row['blockers']) + '</p></details>'
    body += '<h3 id="t2-fields">Current field definitions</h3>'
    body += table(['Field','Meaning'], [[code(k),esc(v['description'])] for k,v in schema['fields'].items()],caption='T2 · current registry fields')
    body += '<p>Earlier mode flags, normalization recipes, weights and justifications are preserved in the migration trace and historical records below. No evidence IDs or review decisions were changed.</p>'
    return body
