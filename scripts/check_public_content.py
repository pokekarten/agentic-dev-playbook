from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK_PATHS = [ROOT / "README.md", ROOT / "runbooks", ROOT / "patterns"]
DISALLOWED_MARKERS = {
    ".env",
    "api_key",
    "apikey",
    "password",
    "private key",
    "raw chat",
    "raw transcript",
    "customer data",
    "personal data",
}


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in CHECK_PATHS:
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return sorted(files)


def main() -> int:
    errors: list[str] = []
    files = iter_markdown_files()

    if not files:
        errors.append("No public Markdown files found to check.")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        for marker in sorted(DISALLOWED_MARKERS):
            if marker in text:
                rel = path.relative_to(ROOT)
                errors.append(f"{rel}: contains disallowed marker: {marker}")

    if errors:
        print("Public content guardrail failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Public content guardrail passed for {len(files)} Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
