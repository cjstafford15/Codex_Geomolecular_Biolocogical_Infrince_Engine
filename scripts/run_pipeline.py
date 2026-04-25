from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print(f"\n>>> {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    print("=== Geomolecular Pipeline ===", flush=True)
    print("Step 1: Export Excel to Obsidian", flush=True)
    run([
        sys.executable,
        str(ROOT / "scripts" / "excel_to_obsidian.py"),
        "--workbook", str(ROOT / "data" / "geomolecular_template.xlsx"),
        "--vault", str(ROOT / "obsidian-vault"),
    ])

    print("\nStep 2: Run Geometry Pattern Agent", flush=True)
    run([sys.executable, str(ROOT / "scripts" / "geometry_pattern_agent.py")])

    print("\nStep 3: Run Evidence Agent", flush=True)
    run([sys.executable, str(ROOT / "scripts" / "evidence_agent.py")])

    print("\nStep 4: Run Product Concept Agent", flush=True)
    run([sys.executable, str(ROOT / "scripts" / "product_concept_agent.py")])

    print("\nStep 5: Run Captain Connectivity Agent", flush=True)
    run([sys.executable, str(ROOT / "scripts" / "captain_connectivity_.py")])

    print("\n=== Pipeline Complete ===", flush=True)
    print(f"Vault: {ROOT / 'obsidian-vault'}", flush=True)
    print(f"Reports: {ROOT / 'obsidian-vault' / 'Agent Reports'}", flush=True)


if __name__ == "__main__":
    main()

