"""Fail closed when newly introduced Git commits expose personal Gmail metadata."""

from __future__ import annotations

import argparse
from pathlib import PurePosixPath
import re
import subprocess
import sys

_SHA_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")
_PERSONAL_EMAIL_RE = re.compile(r"@(gmail|googlemail)\.com$", re.IGNORECASE)


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _require_commit(sha: str, label: str) -> None:
    if not _SHA_RE.fullmatch(sha):
        raise ValueError(f"{label} is not a full Git object id")
    result = _git("cat-file", "-e", f"{sha}^{{commit}}", check=False)
    if result.returncode != 0:
        raise ValueError(f"{label} does not resolve to a commit")


def _validate_repo_path(path: str) -> str:
    candidate = PurePosixPath(path)
    if not path or path.startswith("/") or "\\" in path or ".." in candidate.parts:
        raise ValueError("bootstrap path must be a safe repository-relative POSIX path")
    return str(candidate)


def _new_commits(base: str, head: str) -> list[str]:
    result = _git("rev-list", "--reverse", f"{base}..{head}")
    return [line for line in result.stdout.splitlines() if line]


def _metadata(commit: str) -> tuple[str, str, str]:
    result = _git("show", "-s", "--format=%H%x00%ae%x00%ce", commit)
    parts = result.stdout.rstrip("\n").split("\x00")
    if len(parts) != 3:
        raise ValueError(f"could not parse metadata for commit {commit}")
    return parts[0], parts[1].strip(), parts[2].strip()


def _is_personal_email(email: str) -> bool:
    return bool(_PERSONAL_EMAIL_RE.search(email.strip()))


def _path_exists_at(commit: str, path: str) -> bool:
    result = _git("cat-file", "-e", f"{commit}:{path}", check=False)
    return result.returncode == 0


def _path_added_by(commit: str, path: str) -> bool:
    result = _git(
        "diff-tree",
        "--no-commit-id",
        "--diff-filter=A",
        "--name-only",
        "-r",
        commit,
        "--",
        path,
    )
    return result.stdout.splitlines() == [path]


def _bootstrap_allowed(base: str, commits: list[str], bootstrap_path: str | None) -> bool:
    if bootstrap_path is None:
        return False
    path = _validate_repo_path(bootstrap_path)
    if _path_exists_at(base, path):
        return False
    if len(commits) != 1:
        return False
    return _path_added_by(commits[0], path)


def check_range(base: str, head: str, bootstrap_path: str | None = None) -> int:
    _require_commit(base, "base")
    _require_commit(head, "head")

    commits = _new_commits(base, head)
    bootstrap = _bootstrap_allowed(base, commits, bootstrap_path)
    violations: list[tuple[str, str, str]] = []

    for commit in commits:
        commit_sha, author_email, committer_email = _metadata(commit)
        if _is_personal_email(author_email):
            violations.append((commit_sha, "author", author_email))
        if _is_personal_email(committer_email):
            violations.append((commit_sha, "committer", committer_email))

    if not violations:
        print(f"PASS: checked {len(commits)} new commit(s); no Gmail/Googlemail metadata found")
        return 0

    for commit_sha, field, email in violations:
        print(f"VIOLATION: {commit_sha} {field}.email={email}", file=sys.stderr)

    if bootstrap:
        print(
            "BOOTSTRAP: one commit adds the privacy workflow to a base that did not contain it; "
            "violations are reported but this one-time introduction is not blocked",
            file=sys.stderr,
        )
        return 0

    print(
        "BLOCKED: newly introduced commit metadata contains a Gmail/Googlemail address; "
        "use the repository-approved GitHub noreply address",
        file=sys.stderr,
    )
    return 1


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("base")
    parser.add_argument("head")
    parser.add_argument("--bootstrap-path")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        return check_range(args.base, args.head, args.bootstrap_path)
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"ERROR: commit-email privacy check failed closed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
