from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
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


def analyze_patterns(records: dict[str, list[dict[str, str]]]) -> dict:
    geometries = records["GeometrySignatures"]
    candidates = records["CandidateMaterials"]
    observations = records["Observations"]
    bios = records["BiologicalDefinitions"]
    sources = records["Sources"]

    bio_by_id = {b["bio_id"]: b for b in bios if b.get("bio_id")}
    geo_by_id = {g["geometry_id"]: g for g in geometries if g.get("geometry_id")}
    sources_by_id = {s["source_id"]: s for s in sources if s.get("source_id")}

    # Group candidates by geometry
    candidates_by_geo: dict[str, list[dict]] = defaultdict(list)
    for c in candidates:
        for gid in split_ids(c.get("geometry_ids", "")):
            candidates_by_geo[gid].append(c)

    # Group observations by geometry
    observations_by_geo: dict[str, list[dict]] = defaultdict(list)
    for o in observations:
        gid = o.get("geometry_id", "")
        if gid:
            observations_by_geo[gid].append(o)

    # Find cross-biology geometry matches (same geometry, different biology)
    cross_bio_matches = []
    for gid, geo in geo_by_id.items():
        cand_list = candidates_by_geo.get(gid, [])
        obs_list = observations_by_geo.get(gid, [])

        bio_ids = set()
        for c in cand_list:
            bio_ids.update(split_ids(c.get("bio_ids", "")))
        for o in obs_list:
            if o.get("bio_id"):
                bio_ids.add(o["bio_id"])

        bio_terms = [bio_by_id[bid].get("term", bid) for bid in bio_ids if bid in bio_by_id]

        if len(bio_terms) >= 2 or len(cand_list) >= 2:
            cross_bio_matches.append({
                "geometry_id": gid,
                "geometry_name": geo.get("geometry_name", gid),
                "section": geo.get("section", ""),
                "candidate_count": len(cand_list),
                "observation_count": len(obs_list),
                "bio_terms": bio_terms,
                "candidates": [c.get("name", c.get("candidate_id", "")) for c in cand_list],
                "match_features": geo.get("match_features", ""),
                "confidence": _avg_confidence(obs_list),
                "source_reliability": _avg_source_reliability(obs_list, sources_by_id),
                "evidence_score": _avg_evidence_score(obs_list, sources_by_id),
            })

    # Rank by breadth first, then evidence quality.
    cross_bio_matches.sort(
        key=lambda x: (
            x["candidate_count"] + x["observation_count"],
            x["evidence_score"],
            x["confidence"],
        ),
        reverse=True,
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "geometry_count": len(geometries),
        "candidate_count": len(candidates),
        "observation_count": len(observations),
        "high_frequency_geometries": cross_bio_matches,
    }


def _avg_confidence(observations: list[dict]) -> float:
    return average(confidence_score(o.get("confidence", "")) for o in observations)


def _avg_source_reliability(
    observations: list[dict],
    sources_by_id: dict[str, dict[str, str]],
) -> float:
    return average(average_source_reliability(o.get("source_ids", ""), sources_by_id) for o in observations)


def _avg_evidence_score(
    observations: list[dict],
    sources_by_id: dict[str, dict[str, str]],
) -> float:
    return average(
        validation_score(
            confidence_score(o.get("confidence", "")),
            average_source_reliability(o.get("source_ids", ""), sources_by_id),
            has_meaningful_contradiction(o.get("contradiction", "")),
        )
        for o in observations
    )


def render_report(analysis: dict) -> str:
    lines = [
        "# Geometry Pattern Report",
        "",
        "Type: `agent-report`",
        "Agent: `geometry-pattern-agent`",
        "",
        "## Summary",
        "",
        f"- Total geometries: {analysis['geometry_count']}",
        f"- Total candidates: {analysis['candidate_count']}",
        f"- Total observations: {analysis['observation_count']}",
        "",
        "## High-Frequency Geometry Matches",
        "",
        "These geometries appear across multiple candidates or biological contexts. They are the primary pattern matches to investigate.",
        "",
    ]

    for match in analysis["high_frequency_geometries"]:
        lines.append(f"### {match['geometry_name']} (`{match['geometry_id']}`)")
        lines.append("")
        lines.append(f"- Section: {match['section']}")
        lines.append(f"- Candidates: {match['candidate_count']}")
        lines.append(f"- Observations: {match['observation_count']}")
        lines.append(f"- Average confidence: {match['confidence']}")
        lines.append(f"- Source reliability: {match['source_reliability']}")
        lines.append(f"- Evidence score: {match['evidence_score']}")
        lines.append(f"- Match features: {match['match_features']}")
        lines.append("")
        lines.append("**Candidates:**")
        for c in match["candidates"]:
            lines.append(f"- [[{c}]]")
        lines.append("")
        if match["bio_terms"]:
            lines.append("**Biological contexts:**")
            for b in match["bio_terms"]:
                lines.append(f"- [[{b}]]")
            lines.append("")
        lines.append("---")
        lines.append("")

    if not analysis["high_frequency_geometries"]:
        lines.append("No multi-candidate or multi-biology geometry matches found yet.")
        lines.append("")

    lines.append("## Method")
    lines.append("")
    lines.append("This report ignores biological categories until after geometric matches are identified. Biology is used only as confirmation metadata.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    records = load_records(WORKBOOK)
    analysis = analyze_patterns(records)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Write JSON for machine consumption
    json_path = REPORT_DIR / "geometry-pattern-report.json"
    json_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")

    # Write markdown for Obsidian
    md_path = REPORT_DIR / "geometry-pattern-report.md"
    md_path.write_text(render_report(analysis), encoding="utf-8")

    print(f"Report written to {md_path}")


if __name__ == "__main__":
    main()
