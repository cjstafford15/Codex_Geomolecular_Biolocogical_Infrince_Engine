from __future__ import annotations

import json
from pathlib import Path

from geomolecular_data import (
    average,
    average_source_reliability,
    confidence_score,
    has_meaningful_contradiction,
    read_workbook,
    split_ids,
    validation_score,
)

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "data" / "geomolecular_template.xlsx"
VAULT = ROOT / "obsidian-vault"
REPORT_DIR = VAULT / "Agent Reports"


def load_records(workbook_path: Path) -> dict[str, list[dict[str, str]]]:
    return read_workbook(workbook_path)


def generate_concepts(records: dict[str, list[dict[str, str]]]) -> list[dict]:
    geometries = records["GeometrySignatures"]
    candidates = records["CandidateMaterials"]
    observations = records["Observations"]
    existing_ideas = records["ProductIdeas"]
    sources = records["Sources"]

    geo_by_id = {g["geometry_id"]: g for g in geometries if g.get("geometry_id")}
    cand_by_id = {c["candidate_id"]: c for c in candidates if c.get("candidate_id")}
    sources_by_id = {s["source_id"]: s for s in sources if s.get("source_id")}
    evidence_by_geo = _evidence_by_geometry(observations, sources_by_id)

    concepts: list[dict] = []

    # Strategy 1: Candidates sharing the same geometry
    geo_to_candidates: dict[str, list[str]] = {}
    for c in candidates:
        for gid in split_ids(c.get("geometry_ids", "")):
            geo_to_candidates.setdefault(gid, []).append(c["candidate_id"])

    for gid, cand_ids in geo_to_candidates.items():
        if len(cand_ids) < 2:
            continue
        geo = geo_by_id.get(gid)
        if not geo:
            continue

        names = [cand_by_id[cid].get("name", cid) for cid in cand_ids if cid in cand_by_id]

        concepts.append({
            "concept_id": f"CONCEPT-COMBINE-{gid}",
            "strategy": "combine_same_geometry",
            "geometry_id": gid,
            "geometry_name": geo.get("geometry_name", gid),
            "candidate_names": names,
            "evidence_score": evidence_by_geo.get(gid, 0.0),
            "concept_note": (
                f"Candidates {names} all express geometry signature "
                f"'{geo.get('geometry_name', gid)}'. "
                f"Compare features across these candidates and prioritize validation before claims."
            ),
        })

    # Strategy 2: Geometries with observations but few candidates
    obs_by_geo: dict[str, int] = {}
    for o in observations:
        gid = o.get("geometry_id", "")
        if gid:
            obs_by_geo[gid] = obs_by_geo.get(gid, 0) + 1

    for gid, count in obs_by_geo.items():
        cands = geo_to_candidates.get(gid, [])
        if len(cands) < 2 and count >= 1:
            geo = geo_by_id.get(gid)
            if not geo:
                continue
            concepts.append({
                "concept_id": f"CONCEPT-GAP-{gid}",
                "strategy": "fill_geometry_gap",
                "geometry_id": gid,
                "geometry_name": geo.get("geometry_name", gid),
                "candidate_names": [cand_by_id[c].get("name", c) for c in cands],
                "evidence_score": evidence_by_geo.get(gid, 0.0),
                "concept_note": (
                    f"Geometry '{geo.get('geometry_name', gid)}' has {count} observation(s) "
                    f"but only {len(cands)} candidate(s). Add candidates and measurement controls."
                ),
            })

    # Strategy 3: Extend existing product ideas
    for idea in existing_ideas:
        idea_id = idea.get("idea_id", "")
        title = idea.get("title", "")
        geom_ids = split_ids(idea.get("geometry_ids", ""))
        cand_ids = split_ids(idea.get("candidate_ids", ""))

        geo_names = [geo_by_id[g].get("geometry_name", g) for g in geom_ids if g in geo_by_id]
        cand_names = [cand_by_id[c].get("name", c) for c in cand_ids if c in cand_by_id]

        if geo_names and cand_names:
            concepts.append({
                "concept_id": f"CONCEPT-IDEA-{idea_id}",
                "strategy": "extend_existing_idea",
                "geometry_id": ",".join(geom_ids),
                "geometry_name": ", ".join(geo_names),
                "candidate_names": cand_names,
                "evidence_score": average(evidence_by_geo.get(gid, 0.0) for gid in geom_ids),
                "concept_note": (
                    f"Existing idea '{title}' is driven by geometries: {', '.join(geo_names)}. "
                    f"Extend only after evidence gaps and blocked claims are reviewed."
                ),
            })

    return concepts


def _evidence_by_geometry(
    observations: list[dict[str, str]],
    sources_by_id: dict[str, dict[str, str]],
) -> dict[str, float]:
    scores_by_geo: dict[str, list[float]] = {}
    for observation in observations:
        geometry_id = observation.get("geometry_id", "")
        if not geometry_id:
            continue
        score = validation_score(
            confidence_score(observation.get("confidence", "")),
            average_source_reliability(observation.get("source_ids", ""), sources_by_id),
            has_meaningful_contradiction(observation.get("contradiction", "")),
        )
        scores_by_geo.setdefault(geometry_id, []).append(score)
    return {geometry_id: average(scores) for geometry_id, scores in scores_by_geo.items()}


def render_report(concepts: list[dict]) -> str:
    lines = [
        "# Product Concept Report",
        "",
        "Type: `agent-report`",
        "Agent: `product-concept-agent`",
        "",
        "## Summary",
        "",
        f"- Concepts generated: {len(concepts)}",
        "",
        "## Concepts",
        "",
    ]

    for c in concepts:
        lines.append(f"### {c['concept_id']}")
        lines.append("")
        lines.append(f"- Strategy: `{c['strategy']}`")
        lines.append(f"- Geometry: [[{c['geometry_name']}]] (`{c['geometry_id']}`)")
        lines.append(f"- Evidence score: {c['evidence_score']}")
        lines.append("")
        lines.append("**Candidates:**")
        for name in c["candidate_names"]:
            lines.append(f"- [[{name}]]")
        lines.append("")
        lines.append("**Concept Note:**")
        lines.append(c["concept_note"])
        lines.append("")
        lines.append("---")
        lines.append("")

    if not concepts:
        lines.append("No concepts generated. Add more candidates, geometries, or observations.")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    records = load_records(WORKBOOK)
    concepts = generate_concepts(records)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = REPORT_DIR / "product-concept-report.json"
    json_path.write_text(json.dumps(concepts, indent=2), encoding="utf-8")

    md_path = REPORT_DIR / "product-concept-report.md"
    md_path.write_text(render_report(concepts), encoding="utf-8")

    print(f"Report written to {md_path}")


if __name__ == "__main__":
    main()
