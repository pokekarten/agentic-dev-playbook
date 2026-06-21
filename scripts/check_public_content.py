from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Keep this guardrail intentionally narrow.
# It catches high-signal secret-like markers, not every privacy-related word.
# Policy documents must be allowed to say phrases such as "personal data"
# when they explain what must not be published.
DISALLOWED_MARKERS = {
    "api_key=",
    "apikey=",
    "password=",
    "secret=",
    "token=",
    "private_key=",
    "begin private key",
    "begin rsa private key",
    "begin openssh private key",
}


def iter_markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and path.is_file()
    )


def main() -> int:
    errors: list[str] = []
    files = iter_markdown_files()

    if not files:
        errors.append("No public Markdown files found to check.")

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        for marker in sorted(DISALLOWED_MARKERS):
            if marker.lower() in text:
                rel = path.relative_to(ROOT)
                errors.append(f"{rel}: contains high-signal secret-like marker: {marker}")

    if errors:
        print("Public content guardrail failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Public content guardrail passed for {len(files)} Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
