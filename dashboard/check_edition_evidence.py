"""Verify the public evidence downloads and review queue against their pinned workbook and review join."""

import csv
import io
import json
import re
from collections import Counter
from hashlib import sha256
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen


def check(directory):
    root = str(directory).rstrip("/") + "/"
    local = not root.startswith("https://")

    def read(name):
        if local:
            return (Path(directory) / name).read_bytes()
        with urlopen(urljoin(root, name), timeout=60) as response:
            return response.read()

    catalogue = json.loads(read("catalog.json"))
    (item,) = [
        d
        for d in catalogue["dataset"]
        if d["identifier"] == "ruralscan-edition-evidence"
    ]
    hashes = {a["contentUrl"]: a["sha256"] for a in item["distribution"]}
    doc = read("evidence-tables/datapackage.json")
    assert sha256(doc).hexdigest() == hashes[item["@id"]]
    package = json.loads(doc)
    status = json.loads(read("review-status.json"))
    workbook = json.loads(
        re.search(
            rb'id="publication">(.+?)</script>', read("workbook.html"), re.DOTALL
        )[1]
    )
    assert (
        package["producerRevision"]
        == status["producer_revision"]
        == workbook["source_revision"]
    )
    assert package["cookbookRelease"] == status["release_id"] == workbook["release_id"]
    assert package["version"] == catalogue["version"] == item["version"]
    raw = {}
    for r in package["resources"]:
        data = read("evidence-tables/" + r["path"])
        digest = sha256(data).hexdigest()
        assert (
            digest == hashes[urljoin(item["@id"], r["path"])]
            and r["hash"] == "sha256:" + digest
            and len(data) == r["bytes"]
        )
        reader = csv.DictReader(io.StringIO(data.decode(r["encoding"])))
        fields = r["schema"]["fields"]
        assert reader.fieldnames == [f["name"] for f in fields]
        rows = list(reader)
        key = r["schema"]["primaryKey"]
        key = key if isinstance(key, list) else [key]
        assert len({tuple(row[k] for k in key) for row in rows}) == len(rows)
        for f in fields:
            values = [row[f["name"]] for row in rows]
            if f["constraints"]["required"]:
                assert all(values), (r["name"], f["name"])
            if "enum" in f["constraints"]:
                assert set(values) <= set(f["constraints"]["enum"])
            if f["type"] == "object":
                assert all(isinstance(json.loads(v), dict) for v in values if v)
        raw[r["name"]] = rows
    for r in package["resources"]:
        for link in r["schema"].get("foreignKeys", []):
            ref = link["reference"]
            ids = {x[ref["fields"]] for x in raw[ref["resource"]]}
            assert all(
                not row[link["fields"]] or row[link["fields"]] in ids
                for row in raw[r["name"]]
            )
    findings = {r["evidence_id"]: r for r in raw["findings"]}
    assert findings.keys() == status["findings"].keys()
    assert all(
        f["status"] == status["findings"][eid]["status"]
        and f["source_id"] == status["findings"][eid]["source_id"]
        for eid, f in findings.items()
    )
    links = {
        (r["record_id"], r["evidence_id"], r["kind"]) for r in raw["record-findings"]
    }
    rows = {r["id"]: r for r in workbook["rows"] if r["table"] in ("T3", "T4", "T6")}
    assert {r["record_id"] for r in raw["records"]} == rows.keys()
    expected_links = {
        (rid, eid, kind)
        for rid, row in rows.items()
        for kind, ids in (
            ("direct", row["evidence_ids"]),
            ("context", row["context_ids"]),
            ("setter", status["rows"].get(rid, {}).get("setter_ids", [])),
        )
        for eid in ids
    }
    assert links == expected_links
    for lane in ("T3", "T4", "T6"):
        assert {r["record_id"] for r in raw[lane.lower()]} == {
            rid for rid, row in rows.items() if row["table"] == lane
        }
    for r in raw["t3"] + raw["t6"]:
        state = status["rows"][r["record_id"]]
        assert (r["rating"], r["confidence"], r["setter_coverage"]) == (
            state["rating"] or "",
            state["confidence"],
            state["coverage"],
        )
        assert r["provisional"] == (
            "" if state["provisional"] is None else str(state["provisional"])
        )
    unresolved = {
        eid
        for state in status["rows"].values()
        for eid in state["unresolved_setter_ids"]
    }
    held = {
        rid
        for rid, row in rows.items()
        if row["table"] == "T4"
        and row["fields"]["Reviewed numerical calibration"] == "Held"
    }
    queued = {(r["task"], r["target_id"]) for r in raw["queue"]}
    assert queued == {("unresolved_setter", eid) for eid in unresolved} | {
        ("held_calibration", rid) for rid in held
    }
    for r in raw["queue"]:
        if r["task"] == "held_calibration":
            assert (
                r["record_id"] == r["target_id"]
                and not r["evidence_id"]
                and not r["live_review_url"]
            )
        else:
            eid = r["evidence_id"]
            assert (
                eid == r["target_id"]
                and r["status"] in ("held", "unreviewed")
                and not r["record_id"]
            )
            assert r["live_review_url"] == findings[eid]["live_review_url"]
    counts = Counter(f["status"] for f in status["findings"].values())
    expected = {
        ("EV", "All registered findings"): counts,
        ("T4", "Numerical calibration"): Counter(
            r["fields"]["Reviewed numerical calibration"]
            for r in rows.values()
            if r["table"] == "T4"
        ),
    }
    for lane in ("T3", "T6"):
        lane_status = [r for r in status["rows"].values() if r["table"] == lane]
        expected[lane, "Setter assessment"] = Counter(
            r["coverage"] for r in lane_status
        )
        labels = {True: "provisional", False: "assessed_clear", None: "undetermined"}
        expected[lane, "Rating status"] = Counter(
            labels[r["provisional"]] for r in lane_status
        )
    seen = set()
    for r in raw["coverage"]:
        group = (r["group"], r["population"])
        assert int(r["count"]) == expected[group][r["status"]] and int(
            r["denominator"]
        ) == sum(expected[group].values())
        seen.add((*group, r["status"]))
    assert all((*group, label) in seen for group, c in expected.items() for label in c)
    roose = "ev_flood_hazard_roose17_2"
    assert (
        sum(eid == roose and kind == "direct" for _, eid, kind in links) == 7
        and roose not in unresolved
    )
    assert findings["ev_drought_hazard_ieg20_4"]["status"] == "rejected"
    assert not any(
        eid == "ev_drought_hazard_ieg20_4" and kind == "direct"
        for _, eid, kind in links
    )
    print(
        f"{len(rows)} analytical rows, {len(links)} evidence links, {len(unresolved)} unresolved setters and {len(held)} held mappings verified."
    )


if __name__ == "__main__":
    import sys

    check(sys.argv[1])
