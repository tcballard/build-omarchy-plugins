#!/usr/bin/env python3
"""Portable structural validation for bundled agent skills."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME = re.compile(r"^name:\s*([a-z0-9-]+)\s*$", re.MULTILINE)
DESCRIPTION = re.compile(r"^description:\s*(.+?)\s*$", re.MULTILINE)
LOCAL_LINK = re.compile(r"\]\((references/[^)#]+|scripts/[^)#]+|assets/[^)#]+)\)")


def validate(skill: Path) -> list[str]:
    errors: list[str] = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return [f"{skill}: missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"{entry}: missing YAML frontmatter boundaries")
    frontmatter = text.split("\n---\n", 1)[0][4:] if "\n---\n" in text else ""
    name_match = NAME.search(frontmatter)
    description_match = DESCRIPTION.search(frontmatter)
    if not name_match:
        errors.append(f"{entry}: missing valid lowercase name")
    elif name_match.group(1) != skill.name:
        errors.append(f"{entry}: name '{name_match.group(1)}' does not match directory '{skill.name}'")
    if not description_match:
        errors.append(f"{entry}: missing one-line description")
    elif len(description_match.group(1).strip().strip('"')) < 40:
        errors.append(f"{entry}: description is too weak for reliable routing")
    if "[TODO:" in text or "TODO" in frontmatter:
        errors.append(f"{entry}: unfinished scaffold placeholder")
    for target in LOCAL_LINK.findall(text):
        if not (skill / target).is_file():
            errors.append(f"{entry}: linked resource does not exist: {target}")

    agent = skill / "agents" / "openai.yaml"
    if not agent.is_file():
        errors.append(f"{skill}: missing agents/openai.yaml")
    else:
        agent_text = agent.read_text(encoding="utf-8")
        if name_match and f"${name_match.group(1)}" not in agent_text:
            errors.append(f"{agent}: default_prompt must mention ${name_match.group(1)}")
        short = re.search(r'^\s*short_description:\s*"([^"]+)"\s*$', agent_text, re.MULTILINE)
        if not short or not 25 <= len(short.group(1)) <= 64:
            errors.append(f"{agent}: short_description must be 25-64 characters")

    for path in skill.rglob("*"):
        if path.is_symlink():
            errors.append(f"{path}: symlinks are not allowed in submitted skill bundles")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills_dir", type=Path)
    args = parser.parse_args(argv or sys.argv[1:])
    skills = sorted(path for path in args.skills_dir.iterdir() if path.is_dir())
    errors = [error for skill in skills for error in validate(skill)]
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"VALID: {len(skills)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
