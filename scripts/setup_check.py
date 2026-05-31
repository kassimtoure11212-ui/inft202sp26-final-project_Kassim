#!/usr/bin/env python3
"""SQLite-based setup check for the INFT202 final project.

This script keeps student setup small: repo + SQLite + Codex. It checks Git,
writes short markdown notes for Codex to use later, and confirms that the
project is configured for a local SQLite database file named "final.db".
"""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_FILE = "final.db"


def run(command: list[str], timeout: int = 20) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        return completed.returncode, completed.stdout.strip(), completed.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"{command[0]} not found"
    except subprocess.TimeoutExpired:
        return 124, "", f"{' '.join(command)} timed out"


def git_info() -> list[str]:
    notes: list[str] = []

    if not (ROOT / ".git").exists():
        return ["- [ ] Git repo found: no. Fork and clone the project repo first."]

    notes.append("- [x] Git repo found")

    code, origin, _ = run(["git", "remote", "get-url", "origin"])
    if code == 0 and origin:
        if "github.com" in origin and "YOUR_USERNAME" not in origin:
            notes.append(f"- [x] GitHub remote configured: `{origin}`")
        else:
            notes.append(f"- [ ] GitHub remote may need attention: `{origin}`")
    else:
        notes.append("- [ ] No GitHub remote named `origin` found. Add your fork as `origin`.")

    code, branch, _ = run(["git", "branch", "--show-current"])
    notes.append(f"- [x] Current Git branch: `{branch}`" if code == 0 and branch else "- [ ] Could not detect current Git branch.")

    code, name, _ = run(["git", "config", "user.name"])
    notes.append("- [x] Git user.name configured" if code == 0 and name else "- [ ] Set Git user.name.")

    code, email, _ = run(["git", "config", "user.email"])
    notes.append("- [x] Git user.email configured" if code == 0 and email else "- [ ] Set Git user.email.")

    return notes


def sqlite_info() -> list[str]:
    notes: list[str] = []
    notes.append("- [x] Docker is not required for the SQLite workflow")
    notes.append(f"- [x] SQLite database file will be `{DB_FILE}`")
    if (ROOT / DB_FILE).exists():
        notes.append(f"- [x] `{DB_FILE}` already exists")
    else:
        notes.append(f"- [ ] `{DB_FILE}` has not been created yet")
        notes.append("  - Create it in Beekeeper Studio with connection type SQLite.")
    return notes


def write_outputs(sections: list[tuple[str, list[str]]]) -> None:
    lines = ["# Setup Check", ""]
    for title, notes in sections:
        lines.append(f"## {title}")
        lines.extend(notes)
        lines.append("")

    lines.extend(
        [
            "## Connection Info",
            f"- Database file: `{DB_FILE}`",
            "- Tool: Beekeeper Studio",
            "- Connection type: SQLite",
            "",
            "## Next Step",
            "Create or open `final.db` in Beekeeper Studio, then continue with dataset selection and exploration.",
            "",
        ]
    )
    (ROOT / "database_setup.md").write_text(
        "\n".join(
            [
                "# Database Setup",
                "",
                "This project is using SQLite instead of PostgreSQL because Docker is not working on this computer.",
                "",
                f"Database file: `{DB_FILE}`",
                "",
                "Recommended tool:",
                "- Beekeeper Studio",
                "- Connection type: SQLite",
                f"- File path: choose or create `{DB_FILE}` in this project folder",
                "",
                "Use this SQLite database file for table creation, imports, queries, and the Flask app.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (ROOT / "setup_check.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


def main() -> int:
    sections: list[tuple[str, list[str]]] = []
    sections.append(("Git And GitHub", git_info()))
    sections.append(("SQLite", sqlite_info()))

    write_outputs(sections)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
