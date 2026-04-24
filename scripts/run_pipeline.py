from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=False)
    if result.returncode != 0:
        print(f"Warning: command exited with code {result.returncode}")


def main() -> None:
    print("=== Geomolecular Pipeline ===")
    print("Step 1: Export Excel to Obsidian")
    run([
        sys.executable,
        str(ROOT / "scripts" / "excel_to_obsidian.py"),
        "--workbook", str(ROOT / "data" / "geomolecular_template.xlsx"),
        "--vault", str(ROOT / "obsidian-vault"),
    ])

    print("\nStep 2: Run Geometry Pattern Agent")
    run([sys.executable, str(ROOT / "scripts" / "geometry_pattern_agent.py")])

    print("\nStep 3: Run Product Concept Agent")
    run([sys.executable, str(ROOT / "scripts" / "product_concept_agent.py")])

    print("\n=== Pipeline Complete ===")
    print(f"Vault: {ROOT / 'obsidian-vault'}")
    print(f"Reports: {ROOT / 'obsidian-vault' / 'Agent Reports'}")


if __name__ == "__main__":
    main()

