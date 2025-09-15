"""
Script CLI pour importer des exercices depuis wger dans la base SQLite locale.

Usage:
    python -m scripts.import_wger_exercises [--max N]
"""

from __future__ import annotations

import argparse

from services.exercise_importer import import_from_wger


def main() -> None:
    parser = argparse.ArgumentParser(description="Import d'exercices wger")
    parser.add_argument("--max", type=int, default=None, help="Nombre max à traiter")
    args = parser.parse_args()

    imported, skipped = import_from_wger(max_items=args.max)
    print(f"OK: {imported} insérés, {skipped} ignorés")


if __name__ == "__main__":
    main()
