#!/usr/bin/env python3
"""Install Phantom API into native Agent Skills discovery locations."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SKILL_NAME = "implement-ui-case-simulator"

PLATFORM_PATHS = {
    "codex": (Path(".agents/skills"), Path(".agents/skills")),
    "claude": (Path(".claude/skills"), Path(".claude/skills")),
    "copilot": (Path(".copilot/skills"), Path(".github/skills")),
    "cursor": (Path(".cursor/skills"), Path(".cursor/skills")),
    "gemini": (Path(".gemini/skills"), Path(".gemini/skills")),
    "windsurf": (
        Path(".codeium/windsurf/skills"),
        Path(".windsurf/skills"),
    ),
    "cline": (Path(".cline/skills"), Path(".cline/skills")),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install Phantom API for one or more AI coding agents using each "
            "agent's native skill directory."
        )
    )
    parser.add_argument(
        "--platform",
        nargs="+",
        choices=["all", *PLATFORM_PATHS],
        default=["all"],
        help="Agent host(s) to install for (default: all).",
    )
    parser.add_argument(
        "--scope",
        choices=["user", "project"],
        default="user",
        help="Install globally for the current user or into a project.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Project root. Required with --scope project unless cwd is the target.",
    )
    parser.add_argument(
        "--mode",
        choices=["symlink", "copy"],
        default="symlink",
        help="Link to this clone or copy the skill files (default: symlink).",
    )
    parser.add_argument(
        "--custom-path",
        type=Path,
        action="append",
        default=[],
        help=(
            "Additional skills directory for another agent. Relative paths use "
            "the selected user or project root. Repeat as needed."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print destinations without changing the filesystem.",
    )
    return parser.parse_args()


def selected_platforms(values: list[str]) -> list[str]:
    if "all" in values:
        return list(PLATFORM_PATHS)
    return list(dict.fromkeys(values))


def destination_for(
    platform: str, scope: str, project_root: Path | None
) -> Path:
    user_path, project_path = PLATFORM_PATHS[platform]
    base = Path.home() if scope == "user" else project_root
    if base is None:
        raise ValueError("A project root is required for project scope.")
    selected_path = user_path if scope == "user" else project_path
    return base.expanduser().resolve() / selected_path / SKILL_NAME


def custom_destination(
    custom_path: Path, scope: str, project_root: Path | None
) -> Path:
    base = Path.home() if scope == "user" else project_root
    if base is None:
        raise ValueError("A project root is required for project scope.")
    skills_directory = (
        custom_path.expanduser()
        if custom_path.is_absolute()
        else base / custom_path.expanduser()
    )
    return skills_directory.resolve() / SKILL_NAME


def is_same_location(source: Path, destination: Path) -> bool:
    try:
        return source.samefile(destination)
    except (FileNotFoundError, OSError):
        return False


def install(source: Path, destination: Path, mode: str, dry_run: bool) -> str:
    if is_same_location(source, destination):
        return f"ready   {destination} (source location)"

    if destination.exists() or destination.is_symlink():
        return f"skip    {destination} (already exists)"

    if destination.is_relative_to(source):
        raise ValueError(
            f"Refusing recursive install inside the source repository: {destination}"
        )

    if dry_run:
        return f"would {mode:7} {destination}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        destination.symlink_to(source, target_is_directory=True)
    else:
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(".git", ".DS_Store", "__pycache__"),
        )
    return f"{mode:7} {destination}"


def main() -> int:
    args = parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    source = repository_root / "skills" / SKILL_NAME
    if not (source / "SKILL.md").is_file():
        print(f"error: SKILL.md not found in {source}", file=sys.stderr)
        return 1

    project_root = (
        (args.target or Path.cwd()).expanduser().resolve()
        if args.scope == "project"
        else None
    )

    try:
        for platform in selected_platforms(args.platform):
            destination = destination_for(platform, args.scope, project_root)
            result = install(source, destination, args.mode, args.dry_run)
            print(f"{platform:9} {result}")
        for custom_path in args.custom_path:
            destination = custom_destination(custom_path, args.scope, project_root)
            result = install(source, destination, args.mode, args.dry_run)
            print(f"{'custom':9} {result}")
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
