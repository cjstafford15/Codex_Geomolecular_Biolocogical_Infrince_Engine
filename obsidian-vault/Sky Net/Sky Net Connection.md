---
id: skynet-connection
type: system-bridge
organ: project-codex-geomolecular-biolocogical-infrince-engine
---

# Sky Net Connection

This vault is directly connected to the **Codex Sky Net** overwatch layer.

## Organ Registration

- **Organ ID:** `project-codex-geomolecular-biolocogical-infrince-engine`
- **Body Role:** `project-organ`
- **State:** `discovered`
- **Path:** `C:\Users\cjsta\OneDrive\Documents\Codex_Geomolecular_Biolocogical_Infrince_Engine`

## Sky Net Links

- [[Skynet Index]] (Sky Net master index)
- [[project-codex-geomolecular-biolocogical-infrince-engine]] (Sky Net organ record)
- [[project-codex-geomolecular-biolocogical-infrince-engine-intake]] (Workflow slot)

## Direct Communication Channels

### GitHub
- Repository: `https://github.com/cjstafford15/Codex_Geomolecular_Biolocogical_Infrince_Engine`
- Remote: `origin/master`

### n8n Webhooks
- `POST /webhook/geomolecular-pattern-scan` — Triggers geometry pattern agent
- `POST /webhook/geomolecular-product-concept` — Triggers product concept agent

### Local Scripts
- `scripts/geometry_pattern_agent.py` — Scans for repeated geometric patterns
- `scripts/product_concept_agent.py` — Proposes non-actionable product concepts
- `scripts/excel_to_obsidian.py` — Exports Excel workbook to this vault

## Agent Handoff Protocol

When Sky Net assigns work to this organ:

1. Check [[project-codex-geomolecular-biolocogical-infrince-engine-intake]] for active assignments.
2. Run geometry-first analysis before biological confirmation.
3. Export results to Obsidian via `excel_to_obsidian.py`.
4. Write handoff notes to `handoffs/` if transferring to another agent.
5. Update workflow slot status in Sky Net registry when complete.

## Physiology Weights (Operational)

| Metric | Weight |
| --- | --- |
| criticality | 0.5 |
| dependency_load | 0.3 |
| signal_frequency | 0.25 |
| latency_sensitivity | 0.25 |
| metabolic_cost | 0.25 |
| failure_impact | 0.4 |
| redundancy | 0.5 |
| recovery_priority | 0.45 |
| health | 1 |

