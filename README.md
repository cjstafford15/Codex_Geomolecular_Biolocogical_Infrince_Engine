# Geomolecular Biological Inference Engine

Geometry is the primary matching layer. Biology is the confirmation layer.

This workspace gives you a practical pipeline:

1. Build or edit `data/geomolecular_template.xlsx` in Excel.
2. Add biological definitions, geometry signatures, sources, observations, candidate materials, and product ideas.
3. Export the workbook to an Obsidian vault grouped by geometry.
4. Let agents search for repeated geometric patterns first, then use biological evidence to confirm or reject the fit.

## Quick Start

Install the one Python dependency:

```powershell
pip install -r requirements.txt
```

Create the Excel workbook template:

```powershell
python scripts/create_excel_template.py
```

Export the workbook to Obsidian markdown:

```powershell
python scripts/excel_to_obsidian.py --workbook data/geomolecular_template.xlsx --vault obsidian-vault
```

Open `obsidian-vault` as an Obsidian vault.

## Geometry-First Method

Each record should answer:

- What is the geometry?
- What biological observation confirms or contradicts it?
- What material, food, molecule, structure, habitat, or behavior expresses that geometry?
- What evidence supports the match?
- What risk or uncertainty blocks product or medical interpretation?

The system is designed so a fly attractant, indoor gnat deterrent, food aroma, plant compound, receptor pocket, delivery surface, or medical hypothesis can share a geometric signature without being forced into the same biological category too early.

## Workbook Sheets

- `BiologicalDefinitions`: controlled biological vocabulary.
- `GeometrySignatures`: geometry-first descriptors and scoring dimensions.
- `CandidateMaterials`: foods, recipes, botanicals, materials, molecules, surfaces, and product ingredients as candidates.
- `Observations`: observed effects, context, organism, geometry link, and confidence.
- `Sources`: citations, URLs, lab notes, or internal evidence.
- `ProductIdeas`: concepts and review needs.

## Agent Automation

Run agents locally:

```powershell
# Scan for repeated geometry signatures
python scripts/geometry_pattern_agent.py

# Score evidence quality, contradictions, and missing measurements
python scripts/evidence_agent.py

# Generate product concepts from matches
python scripts/product_concept_agent.py

# Check private GitHub posture, n8n readiness, and agent connectivity
python scripts/captain_connectivity_.py

# Full pipeline: export Excel -> Obsidian -> run agents
python scripts/run_pipeline.py
```

## n8n Integration

Import the workflow JSON files from `n8n/workflows/` into your n8n instance:

- `geomolecular-pattern-trigger.json` — webhook to trigger pattern scan
- `geomolecular-product-concept.json` — webhook to trigger product concept generation

Both workflows run `python scripts/run_pipeline.py`, which now refreshes the captain connectivity report. Configure the Execute Command nodes to point to this project's directory, keep webhook URLs private, and review any new external egress node before import.

## Sky Net Connection

This project is registered as an organ in the **Codex Sky Net** overwatch layer:

- **Organ ID:** `project-codex-geomolecular-biolocogical-infrince-engine`
- **GitHub:** `https://github.com/cjstafford15/Codex_Geomolecular_Biolocogical_Infrince_Engine`
- **Sky Net Path:** `C:\Users\cjsta\OneDrive\Documents\Codex_Sky_Net_`

To sync with Sky Net:

```powershell
cd ..\Codex_Sky_Net_
.\scripts\scan-projects.ps1 -Register
.\scripts\export-obsidian.ps1
