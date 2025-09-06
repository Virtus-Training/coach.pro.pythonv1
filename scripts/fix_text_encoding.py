import sys
from pathlib import Path

try:
    from ftfy import fix_text
except Exception as e:
    print("ftfy is required: pip install ftfy", file=sys.stderr)
    raise


def fix_file(path: Path, dry_run: bool = False) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    fixed = fix_text(original)
    if fixed != original:
        if not dry_run:
            path.write_text(fixed, encoding="utf-8")
        return True
    return False


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/fix_text_encoding.py <file-or-dir> [--dry-run]")
        sys.exit(1)
    target = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv

    paths: list[Path] = []
    if target.is_dir():
        paths = [p for p in target.rglob("*.py") if "__pycache__" not in p.parts]
    else:
        paths = [target]

    changed = 0
    for p in paths:
        if fix_file(p, dry_run=dry_run):
            changed += 1
            print(f"fixed: {p}")
    print(f"Total files changed: {changed}")


if __name__ == "__main__":
    main()

