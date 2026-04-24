from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "geomolecular_template.xlsx"


SHEETS: dict[str, list[str]] = {
    "BiologicalDefinitions": [
        "bio_id",
        "term",
        "category",
        "definition",
        "confirmation_role",
        "safety_notes",
        "source_ids",
    ],
    "GeometrySignatures": [
        "geometry_id",
        "geometry_name",
        "section",
        "shape_class",
        "symmetry",
        "topology",
        "scale",
        "polarity_pattern",
        "dynamics",
        "match_features",
        "exclusion_features",
    ],
    "CandidateMaterials": [
        "candidate_id",
        "name",
        "candidate_type",
        "geometry_ids",
        "bio_ids",
        "notes",
        "safety_status",
        "source_ids",
    ],
    "Observations": [
        "observation_id",
        "candidate_id",
        "geometry_id",
        "bio_id",
        "context",
        "observed_pattern",
        "confidence",
        "contradiction",
        "source_ids",
    ],
    "Sources": [
        "source_id",
        "title",
        "source_type",
        "url_or_path",
        "reliability",
        "notes",
    ],
    "ProductIdeas": [
        "idea_id",
        "title",
        "geometry_ids",
        "candidate_ids",
        "intended_domain",
        "concept_note",
        "required_validation",
        "blocked_claims",
    ],
}


SEED_ROWS: dict[str, list[list[str]]] = {
    "BiologicalDefinitions": [
        [
            "BIO-FLY-ATTRACTION",
            "Fly attraction",
            "behavior",
            "Movement or aggregation of flies toward a stimulus.",
            "Confirms whether a geometry-linked volatile, surface, or temporal pattern has behavioral relevance.",
            "Do not infer product efficacy without controlled observation and safety review.",
            "SRC-PROJECT-NOTE-001",
        ],
        [
            "BIO-GNAT-FLIGHT-REDUCTION",
            "Indoor gnat flight reduction",
            "behavior",
            "Observed reduction in flying gnat presence in a defined indoor context.",
            "Confirms whether a geometry-linked environmental or volatile pattern changes observed movement.",
            "Do not create pesticide directions or harmful application instructions.",
            "SRC-PROJECT-NOTE-001",
        ],
    ],
    "GeometrySignatures": [
        [
            "GEO-VOLATILE-PLUME-GRADIENT",
            "Volatile plume gradient",
            "Volatile Plumes",
            "gradient",
            "asymmetric",
            "branching diffusion field",
            "room to organism",
            "volatile polarity gradient",
            "evaporative diffusion",
            "Odor intensity changes over distance; airflow and source surface alter the pattern.",
            "No measurable volatile gradient or behavior occurs only by visual/contact cues.",
        ],
        [
            "GEO-SURFACE-FILM-INTERFACE",
            "Surface film interface",
            "Surface Films",
            "plane",
            "asymmetric",
            "two-phase interface",
            "surface to organism",
            "amphiphilic boundary",
            "adhesive/static",
            "Thin film, meniscus, residue, or coating changes contact behavior at an interface.",
            "Effect occurs without contact or surface interaction.",
        ],
    ],
    "CandidateMaterials": [
        [
            "CAND-APPLE-CIDER-VINEGAR",
            "Apple cider vinegar",
            "food",
            "GEO-VOLATILE-PLUME-GRADIENT",
            "BIO-FLY-ATTRACTION",
            "Keep as food-derived candidate data, not as a finalized product instruction.",
            "needs review",
            "SRC-PROJECT-NOTE-001",
        ],
        [
            "CAND-SUGAR-FERMENT-AROMA",
            "Sugar fermentation aroma",
            "recipe",
            "GEO-VOLATILE-PLUME-GRADIENT",
            "BIO-FLY-ATTRACTION",
            "Recipe-like records are allowed when stored as observations and geometry signatures.",
            "needs review",
            "SRC-PROJECT-NOTE-001",
        ],
    ],
    "Observations": [
        [
            "OBS-001",
            "CAND-APPLE-CIDER-VINEGAR",
            "GEO-VOLATILE-PLUME-GRADIENT",
            "BIO-FLY-ATTRACTION",
            "Household anecdote placeholder",
            "Attraction appears linked to evaporating food odor geometry.",
            "low",
            "No controlled comparison yet.",
            "SRC-PROJECT-NOTE-001",
        ]
    ],
    "Sources": [
        [
            "SRC-PROJECT-NOTE-001",
            "Initial project framing",
            "project note",
            "local",
            "unverified",
            "Seed source used to demonstrate schema only.",
        ]
    ],
    "ProductIdeas": [
        [
            "IDEA-GEOMETRY-LED-INSECT-BEHAVIOR",
            "Geometry-led insect behavior screen",
            "GEO-VOLATILE-PLUME-GRADIENT,GEO-SURFACE-FILM-INTERFACE",
            "CAND-APPLE-CIDER-VINEGAR,CAND-SUGAR-FERMENT-AROMA",
            "household research",
            "Compare candidate materials by geometry signature before biological category.",
            "Controlled observation, exposure safety review, environmental review, and claim review.",
            "Do not claim attraction, repellency, elimination, medical value, or pesticide efficacy yet.",
        ]
    ],
}


def add_table(ws, sheet_name: str, row_count: int, column_count: int) -> None:
    end_column = ws.cell(row=1, column=column_count).column_letter
    table = Table(displayName=f"{sheet_name}Table", ref=f"A1:{end_column}{row_count}")
    style = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    table.tableStyleInfo = style
    ws.add_table(table)


def build_workbook() -> Workbook:
    wb = Workbook()
    wb.remove(wb.active)

    for sheet_name, headers in SHEETS.items():
        ws = wb.create_sheet(sheet_name)
        ws.append(headers)
        for row in SEED_ROWS.get(sheet_name, []):
            ws.append(row)

        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F4E78")

        for column_cells in ws.columns:
            header = str(column_cells[0].value)
            width = max(14, min(42, len(header) + 6))
            ws.column_dimensions[column_cells[0].column_letter].width = width

        ws.freeze_panes = "A2"
        add_table(ws, sheet_name, ws.max_row, len(headers))

    return wb


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    workbook = build_workbook()
    workbook.save(OUTPUT)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()

