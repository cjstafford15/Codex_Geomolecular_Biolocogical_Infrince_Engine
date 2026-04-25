from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from geomolecular_data import (
    average,
    average_source_reliability,
    confidence_score,
    has_meaningful_contradiction,
    index_by,
    read_workbook,
    split_ids,
    validate_records,
    validation_score,
)


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "data" / "geomolecular_template.xlsx"
VAULT = ROOT / "obsidian-vault"
REPORT_DIR = VAULT / "Agent Reports"


def analyze_evidence(records: dict[str, list[dict[str, str]]]) -> dict:
    geometries = records["GeometrySignatures"]
    candidates = records["CandidateMaterials"]
    observations = records["Observations"]
    bios = records["BiologicalDefinitions"]
    sources = records["Sources"]
    product_ideas = records["ProductIdeas"]

    geo_by_id = index_by(geometries, "geometry_id")
    cand_by_id = index_by(candidates, "candidate_id")
    bio_by_id = index_by(bios, "bio_id")
    sources_by_id = index_by(sources, "source_id")

    validation_issues = validate_records(records)
    observation_evidence = [
        _score_observation(observation, cand_by_id, geo_by_id, bio_by_id, sources_by_id)
        for observation in observations
    ]

    evidence_by_geometry = _aggregate_by_geometry(observation_evidence, geo_by_id)
    evidence_by_candidate = _aggregate_by_candidate(observation_evidence, cand_by_id, candidates)
    source_inventory = _source_inventory(sources)
    measurement_gaps = _measurement_gaps(
        observation_evidence,
        evidence_by_geometry,
        candidates,
        product_ideas,
        geo_by_id,
        cand_by_id,
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "geometry_count": len(geometries),
            "candidate_count": len(candidates),
            "observation_count": len(observations),
            "source_count": len(sources),
            "product_idea_count": len(product_ideas),
            "validation_issue_count": len(validation_issues),
            "average_observation_evidence_score": average(item["evidence_score"] for item in observation_evidence),
        },
        "validation_issues": [issue.__dict__ for issue in validation_issues],
        "source_inventory": source_inventory,
        "observation_evidence": sorted(observation_evidence, key=lambda item: item["evidence_score"]),
        "evidence_by_geometry": sorted(evidence_by_geometry, key=lambda item: item["evidence_score"]),
        "evidence_by_candidate": sorted(evidence_by_candidate, key=lambda item: item["evidence_score"]),
        "measurement_gaps": measurement_gaps,
    }


def _score_observation(
    observation: dict[str, str],
    cand_by_id: dict[str, dict[str, str]],
    geo_by_id: dict[str, dict[str, str]],
    bio_by_id: dict[str, dict[str, str]],
    sources_by_id: dict[str, dict[str, str]],
) -> dict:
    confidence = confidence_score(observation.get("confidence", ""))
    source_reliability = average_source_reliability(observation.get("source_ids", ""), sources_by_id)
    contradiction = has_meaningful_contradiction(observation.get("contradiction", ""))
    score = validation_score(confidence, source_reliability, contradiction)
    candidate = cand_by_id.get(observation.get("candidate_id", ""), {})
    geometry = geo_by_id.get(observation.get("geometry_id", ""), {})
    bio = bio_by_id.get(observation.get("bio_id", ""), {})

    reasons = []
    if confidence < 0.5:
        reasons.append("low confidence")
    if source_reliability < 0.5:
        reasons.append("weak source reliability")
    if contradiction:
        reasons.append("contradiction or confounder recorded")
    if not split_ids(observation.get("source_ids", "")):
        reasons.append("missing source")

    return {
        "observation_id": observation.get("observation_id", ""),
        "candidate_id": observation.get("candidate_id", ""),
        "candidate_name": candidate.get("name", observation.get("candidate_id", "")),
        "geometry_id": observation.get("geometry_id", ""),
        "geometry_name": geometry.get("geometry_name", observation.get("geometry_id", "")),
        "bio_id": observation.get("bio_id", ""),
        "bio_term": bio.get("term", observation.get("bio_id", "")),
        "confidence": confidence,
        "source_reliability": source_reliability,
        "has_contradiction": contradiction,
        "evidence_score": score,
        "source_ids": split_ids(observation.get("source_ids", "")),
        "reasons": reasons,
    }


def _aggregate_by_geometry(
    observation_evidence: list[dict],
    geo_by_id: dict[str, dict[str, str]],
) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in observation_evidence:
        grouped[item["geometry_id"]].append(item)

    rows = []
    for geometry_id, geometry in geo_by_id.items():
        items = grouped.get(geometry_id, [])
        rows.append({
            "geometry_id": geometry_id,
            "geometry_name": geometry.get("geometry_name", geometry_id),
            "observation_count": len(items),
            "evidence_score": average(item["evidence_score"] for item in items),
            "lowest_observation_score": min((item["evidence_score"] for item in items), default=0.0),
            "contradiction_count": sum(1 for item in items if item["has_contradiction"]),
        })
    return rows


def _aggregate_by_candidate(
    observation_evidence: list[dict],
    cand_by_id: dict[str, dict[str, str]],
    candidates: list[dict[str, str]],
) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in observation_evidence:
        grouped[item["candidate_id"]].append(item)

    rows = []
    for candidate in candidates:
        candidate_id = candidate.get("candidate_id", "")
        items = grouped.get(candidate_id, [])
        rows.append({
            "candidate_id": candidate_id,
            "candidate_name": cand_by_id.get(candidate_id, {}).get("name", candidate_id),
            "safety_status": candidate.get("safety_status", ""),
            "observation_count": len(items),
            "evidence_score": average(item["evidence_score"] for item in items),
            "needs_safety_review": candidate.get("safety_status", "").lower() in {"needs review", "restricted", "unknown"},
        })
    return rows


def _source_inventory(sources: list[dict[str, str]]) -> dict:
    reliability_counts = Counter(source.get("reliability", "unknown") or "unknown" for source in sources)
    type_counts = Counter(source.get("source_type", "unknown") or "unknown" for source in sources)
    return {
        "reliability_counts": dict(sorted(reliability_counts.items())),
        "type_counts": dict(sorted(type_counts.items())),
    }


def _measurement_gaps(
    observation_evidence: list[dict],
    evidence_by_geometry: list[dict],
    candidates: list[dict[str, str]],
    product_ideas: list[dict[str, str]],
    geo_by_id: dict[str, dict[str, str]],
    cand_by_id: dict[str, dict[str, str]],
) -> list[dict]:
    gaps: list[dict] = []

    for item in observation_evidence:
        if item["evidence_score"] < 0.5:
            gaps.append({
                "gap_type": "observation_validation",
                "target": item["observation_id"],
                "reason": ", ".join(item["reasons"]) or "evidence score below validation threshold",
                "recommended_next_measurement": _recommended_measurement(item["geometry_id"]),
            })

    for item in evidence_by_geometry:
        if item["observation_count"] == 0:
            gaps.append({
                "gap_type": "geometry_without_observation",
                "target": item["geometry_name"],
                "reason": "geometry has no observation record",
                "recommended_next_measurement": _recommended_measurement(item["geometry_id"]),
            })

    for candidate in candidates:
        if candidate.get("safety_status", "").lower() in {"needs review", "unknown", "restricted"}:
            gaps.append({
                "gap_type": "safety_review",
                "target": candidate.get("name", candidate.get("candidate_id", "")),
                "reason": f"safety status is {candidate.get('safety_status', 'unknown')}",
                "recommended_next_measurement": "Record safe handling limits and blocked claims before product interpretation.",
            })

    for idea in product_ideas:
        for geometry_id in split_ids(idea.get("geometry_ids", "")):
            geometry = geo_by_id.get(geometry_id, {})
            if not geometry:
                continue
            gaps.append({
                "gap_type": "product_validation",
                "target": idea.get("title", idea.get("idea_id", "")),
                "reason": idea.get("required_validation", "required validation not recorded"),
                "recommended_next_measurement": _recommended_measurement(geometry_id),
            })

        for candidate_id in split_ids(idea.get("candidate_ids", "")):
            candidate = cand_by_id.get(candidate_id, {})
            if candidate.get("safety_status", "").lower() == "needs review":
                gaps.append({
                    "gap_type": "blocked_claim_review",
                    "target": idea.get("title", idea.get("idea_id", "")),
                    "reason": f"{candidate.get('name', candidate_id)} still needs review.",
                    "recommended_next_measurement": idea.get("blocked_claims", "Record blocked claims."),
                })

    return gaps


def _recommended_measurement(geometry_id: str) -> str:
    if "PLUME" in geometry_id:
        return "Measure volatile concentration over distance and time with a matched control."
    if "PULSE" in geometry_id:
        return "Record frequency, duty cycle, and matched steady-output controls."
    if "SURFACE" in geometry_id:
        return "Measure contact angle, surface roughness, and treated versus untreated adhesion."
    if "BINDING" in geometry_id:
        return "Record structural model source, pocket fit metric, and experimental binding status."
    if "SKIN" in geometry_id:
        return "Use a permeation assay or literature measurement with irritation and safety review."
    return "Add a controlled observation with a clear counterfactual and source record."


def render_report(analysis: dict) -> str:
    summary = analysis["summary"]
    lines = [
        "# Evidence Report",
        "",
        "Type: `agent-report`",
        "Agent: `evidence-agent`",
        "",
        "## Summary",
        "",
        f"- Geometries: {summary['geometry_count']}",
        f"- Candidates: {summary['candidate_count']}",
        f"- Observations: {summary['observation_count']}",
        f"- Sources: {summary['source_count']}",
        f"- Product ideas: {summary['product_idea_count']}",
        f"- Validation issues: {summary['validation_issue_count']}",
        f"- Average observation evidence score: {summary['average_observation_evidence_score']}",
        "",
    ]

    lines.extend(_render_validation_issues(analysis["validation_issues"]))
    lines.extend(_render_geometry_scores(analysis["evidence_by_geometry"]))
    lines.extend(_render_weak_observations(analysis["observation_evidence"]))
    lines.extend(_render_measurement_gaps(analysis["measurement_gaps"]))

    lines.extend([
        "## Method",
        "",
        "Evidence score combines observation confidence, source reliability, and a penalty for contradictions or confounders. It is a readiness score, not a truth claim.",
        "",
    ])
    return "\n".join(lines)


def _render_validation_issues(issues: list[dict]) -> list[str]:
    lines = ["## Data Integrity", ""]
    if not issues:
        lines.append("No referential integrity issues found.")
        lines.append("")
        return lines

    for issue in issues:
        lines.append(f"- `{issue['severity']}` {issue['sheet']} `{issue['record_id']}`: {issue['message']}")
    lines.append("")
    return lines


def _render_geometry_scores(rows: list[dict]) -> list[str]:
    lines = ["## Geometry Evidence Scores", ""]
    for row in rows:
        lines.append(f"### {row['geometry_name']} (`{row['geometry_id']}`)")
        lines.append("")
        lines.append(f"- Observation count: {row['observation_count']}")
        lines.append(f"- Evidence score: {row['evidence_score']}")
        lines.append(f"- Lowest observation score: {row['lowest_observation_score']}")
        lines.append(f"- Contradictions/confounders: {row['contradiction_count']}")
        lines.append("")
    return lines


def _render_weak_observations(rows: list[dict]) -> list[str]:
    lines = ["## Weakest Observations", ""]
    weak_rows = [row for row in rows if row["evidence_score"] < 0.5]
    if not weak_rows:
        lines.append("No observations are below the current evidence threshold.")
        lines.append("")
        return lines

    for row in weak_rows:
        reasons = ", ".join(row["reasons"]) or "below evidence threshold"
        lines.append(f"- `{row['observation_id']}` {row['candidate_name']} -> {row['geometry_name']}: score {row['evidence_score']} ({reasons})")
    lines.append("")
    return lines


def _render_measurement_gaps(gaps: list[dict]) -> list[str]:
    lines = ["## Measurement And Review Gaps", ""]
    for gap in gaps[:30]:
        lines.append(f"- `{gap['gap_type']}` {gap['target']}: {gap['recommended_next_measurement']}")
    if len(gaps) > 30:
        lines.append(f"- ... {len(gaps) - 30} additional gaps in JSON report")
    lines.append("")
    return lines


def main() -> None:
    records = read_workbook(WORKBOOK)
    analysis = analyze_evidence(records)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = REPORT_DIR / "evidence-report.json"
    json_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")

    md_path = REPORT_DIR / "evidence-report.md"
    md_path.write_text(render_report(analysis), encoding="utf-8")

    print(f"Report written to {md_path}")


if __name__ == "__main__":
    main()
