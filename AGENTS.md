# Project Operating Instructions

This project treats biology as confirmation metadata and geometry as the primary matching language.

## Core Principle

- Define matches by geometry first: shape class, symmetry, topology, surface polarity pattern, binding-pocket fit, diffusion path, temporal pattern, and environmental geometry.
- Use biological labels second: taxonomy, tissue, receptor, behavior, pathway, phenotype, attractant/repellent observation, pharmacology, toxicology, and safety evidence.
- Preserve recipes, foods, household observations, botanical materials, and product ideas as data sources.

## Data Flow

1. Excel stores structured definitions, geometry signatures, source evidence, observations, and candidate materials.
2. A converter exports the workbook to an Obsidian vault.
3. Obsidian arranges notes by geometry section so agents can search for geometric patterns instead of biological names.
4. Biology validates candidate fits after the geometric match has been found.

## Agent Roles

- **Geometry Pattern Agent** (`scripts/geometry_pattern_agent.py`): Scans the workbook for repeated geometry signatures across food, household, ecological, medical, and product records. Outputs `obsidian-vault/Agent Reports/geometry-pattern-report.md`.
- **Biological Confirmation Agent**: Checks whether biological observations support or contradict the proposed geometry match.
- **Product Concept Agent** (`scripts/product_concept_agent.py`): Proposes product concepts, test questions, and review needs from confirmed geometry matches. Outputs `obsidian-vault/Agent Reports/product-concept-report.md`.
- **Evidence Agent**: Tracks source quality, uncertainty, and missing measurements.

## Sky Net Integration

This organ is registered in the Codex Sky Net overwatch layer:
- **Organ ID:** `project-codex-geomolecular-biolocogical-infrince-engine`
- **Intake Slot:** `project-codex-geomolecular-biolocogical-infrince-engine-intake`
- **GitHub:** `https://github.com/cjstafford15/Codex_Geomolecular_Biolocogical_Infrince_Engine`

### n8n Workflows

- `n8n/workflows/geomolecular-pattern-trigger.json` — Webhook-triggered geometry pattern scan
- `n8n/workflows/geomolecular-product-concept.json` — Webhook-triggered product concept generation

Import these into n8n and connect the Execute Command nodes to this project's working directory.
