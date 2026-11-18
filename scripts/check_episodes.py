"""Check that episode snapshots only diverge where scripts/episodes.toml allows.

Usage: python scripts/check_episodes.py
Exits non-zero and lists violations if any episode drifts.
"""

import filecmp
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALWAYS_ALLOWED = {"README.md"}
IGNORED_PARTS = {"__pycache__", ".venv", "output"}


def files_in(episode: Path) -> set[str]:
    return {
        p.relative_to(episode).as_posix()
        for p in episode.rglob("*")
        if p.is_file() and not IGNORED_PARTS & set(p.parts)
    }


def is_allowed(path: str, allowed: list[str]) -> bool:
    if path in ALWAYS_ALLOWED:
        return True
    return any(path == a or (a.endswith("/") and path.startswith(a)) for a in allowed)


def main() -> int:
    manifest = tomllib.loads((Path(__file__).with_name("episodes.toml")).read_text())
    chain = manifest["chain"]
    allowed_by_episode = manifest.get("allowed", {})
    errors: list[str] = []

    for name in chain:
        if not (ROOT / name).is_dir():
            errors.append(f"{name}: directory listed in chain does not exist")
    if errors:
        print("\n".join(errors))
        return 1

    for prev_name, name in zip(chain, chain[1:]):
        prev, cur = ROOT / prev_name, ROOT / name
        allowed = allowed_by_episode.get(name, [])
        prev_files, cur_files = files_in(prev), files_in(cur)
        for path in sorted(prev_files | cur_files):
            if is_allowed(path, allowed):
                continue
            if path not in cur_files:
                errors.append(f"{name}: removed {path} (not in allowed changes)")
            elif path not in prev_files:
                errors.append(f"{name}: added {path} (not in allowed changes)")
            elif not filecmp.cmp(prev / path, cur / path, shallow=False):
                errors.append(f"{name}: {path} differs from {prev_name} (not in allowed changes)")

    for path in manifest.get("invariant", []):
        holders = [n for n in chain if (ROOT / n / path).is_file()]
        exempt = {n for n in chain if path in allowed_by_episode.get(n, [])}
        baseline = next((n for n in holders if n not in exempt), None)
        for name in holders:
            if name in exempt or name == baseline:
                continue
            if not filecmp.cmp(ROOT / baseline / path, ROOT / name / path, shallow=False):
                errors.append(f"{name}: invariant {path} differs from {baseline}")

    if errors:
        print("Episode drift detected:\n  " + "\n  ".join(errors))
        return 1
    print(f"OK: {len(chain)} episodes consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
