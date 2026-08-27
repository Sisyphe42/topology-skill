#!/usr/bin/env python3
"""Validate the portable topology-skill repository or an installed copy."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit


SKILL_NAME = "topology-skill"
SKILLS_CLI_VERSION = "1.5.21"
MAX_FILE_BYTES = 2 * 1024 * 1024
FORBIDDEN_DIRECTORIES = {
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
FORBIDDEN_PATHS = {"package.json", ".well-known"}
FORBIDDEN_BINARY_SUFFIXES = {
    ".bin",
    ".dll",
    ".dylib",
    ".exe",
    ".gz",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".so",
    ".tar",
    ".zip",
}
REQUIRED_REFERENCES = {
    "references/artifact-contract.md",
    "references/decision-standard.md",
    "references/format-routing.md",
    "references/rendering.md",
}
REQUIRED_CONTRACT_PHRASES = {
    "Assume a blank environment",
    "one concentrated gate",
    "explicit authorization",
}
BEHAVIOR_CASE_IDS = {
    "CASE-01-BLANK-INLINE",
    "CASE-02-COMPLEX-SPLIT",
    "CASE-03-INCREMENTAL-SOURCE",
    "CASE-04-FIGMA-FALLBACK",
    "CASE-05-SENSITIVE-OFFLINE",
    "CASE-06-EXPLICIT-FILE",
}


class ValidationError(Exception):
    """Raised when a subprocess-based validation step fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="skill root to validate")
    parser.add_argument(
        "--repository",
        action="store_true",
        help="also require repository-only release and test files",
    )
    parser.add_argument(
        "--npx-smoke",
        action="store_true",
        help="run pinned Skills CLI discovery, prompt, and copy-install checks",
    )
    return parser.parse_args()


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"cannot read UTF-8 text {path}: {exc}")
        return ""


def parse_frontmatter(skill_text: str, errors: list[str]) -> dict[str, str]:
    lines = skill_text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md must begin with YAML frontmatter")
        return {}
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        errors.append("SKILL.md frontmatter has no closing delimiter")
        return {}

    metadata: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.+)", line)
        if not match:
            errors.append(f"unsupported frontmatter line: {line!r}")
            continue
        key, value = match.groups()
        metadata[key] = value.strip().strip("'\"")
    return metadata


def markdown_targets(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)]


def validate_links(root: Path, markdown_files: list[Path], errors: list[str]) -> None:
    for source in markdown_files:
        text = read_text(source, errors)
        for raw_target in markdown_targets(text):
            target = raw_target.split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#") or target.startswith("//"):
                continue
            relative = unquote(parsed.path).replace("/", os.sep)
            if not relative:
                continue
            destination = (source.parent / relative).resolve()
            try:
                destination.relative_to(root)
            except ValueError:
                errors.append(f"relative link escapes skill root: {source.relative_to(root)} -> {target}")
                continue
            if not destination.exists():
                errors.append(f"broken relative link: {source.relative_to(root)} -> {target}")


def validate_tree(root: Path, repository: bool = False) -> list[str]:
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return ["missing SKILL.md"]

    skill_text = read_text(skill_path, errors)
    metadata = parse_frontmatter(skill_text, errors)
    if metadata.get("name") != SKILL_NAME:
        errors.append(f"frontmatter name must be {SKILL_NAME!r}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata.get("name", "")):
        errors.append("frontmatter name must use lowercase letters, digits, and hyphens")
    if not metadata.get("description"):
        errors.append("frontmatter description must be non-empty")

    for phrase in REQUIRED_CONTRACT_PHRASES:
        if phrase not in skill_text:
            errors.append(f"SKILL.md is missing required contract phrase: {phrase!r}")
    for reference in REQUIRED_REFERENCES:
        if f"]({reference})" not in skill_text:
            errors.append(f"SKILL.md does not link required reference: {reference}")

    agent_metadata_path = root / "agents" / "openai.yaml"
    if agent_metadata_path.is_file():
        agent_metadata = read_text(agent_metadata_path, errors)
        if 'display_name: "Topology Architecture"' not in agent_metadata:
            errors.append("agents/openai.yaml must use the Topology Architecture display name")
        if "$topology-skill" not in agent_metadata:
            errors.append("agents/openai.yaml default prompt must reference $topology-skill")
        if "allow_implicit_invocation: true" not in agent_metadata:
            errors.append("agents/openai.yaml must allow implicit invocation")

    files = [path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts]
    markdown_files = [path for path in files if path.suffix.lower() == ".md"]
    validate_links(root, markdown_files, errors)

    unfinished_tokens = ("TO" + "DO", "T" + "BD", "FIX" + "ME", "PLACE" + "HOLDER")
    unfinished_pattern = re.compile(r"\b(?:" + "|".join(unfinished_tokens) + r")\b", re.IGNORECASE)
    for path in markdown_files:
        text = read_text(path, errors)
        if unfinished_pattern.search(text):
            errors.append(f"unfinished marker found in {path.relative_to(root)}")

    for forbidden in FORBIDDEN_PATHS:
        if (root / forbidden).exists():
            errors.append(f"forbidden runtime or metadata path committed: {forbidden}")
    for path in files:
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_DIRECTORIES for part in relative.parts):
            errors.append(f"forbidden dependency/build directory committed: {relative}")
        if path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            errors.append(f"unexpected binary artifact: {relative}")
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                errors.append(f"file exceeds {MAX_FILE_BYTES} bytes: {relative}")
        except OSError as exc:
            errors.append(f"cannot stat {relative}: {exc}")

    if repository:
        required_repository_files = {
            ".github/workflows/validate.yml",
            "LICENSE",
            "README.md",
            "tests/behavior-cases.md",
        }
        for relative in required_repository_files:
            if not (root / relative).is_file():
                errors.append(f"missing repository file: {relative}")

        license_text = read_text(root / "LICENSE", errors) if (root / "LICENSE").is_file() else ""
        if "MIT License" not in license_text or "Copyright (c) 2026 Sisyphe42" not in license_text:
            errors.append("LICENSE must be MIT with Copyright (c) 2026 Sisyphe42")

        cases_path = root / "tests/behavior-cases.md"
        cases_text = read_text(cases_path, errors) if cases_path.is_file() else ""
        for case_id in BEHAVIOR_CASE_IDS:
            if cases_text.count(case_id) != 1:
                errors.append(f"behavior case must appear exactly once: {case_id}")

    return errors


def run_command(args: list[str], cwd: Path, env: dict[str, str]) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode:
        raise ValidationError(
            f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stdout.strip()}"
        )
    return completed.stdout


def validate_npx(root: Path) -> list[str]:
    errors: list[str] = []
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx:
        return ["npx is required for --npx-smoke"]

    env = os.environ.copy()
    env["DISABLE_TELEMETRY"] = "1"
    env["DO_NOT_TRACK"] = "1"
    base = [npx, "--yes", f"skills@{SKILLS_CLI_VERSION}"]
    root_arg = str(root)
    try:
        listed = run_command(base + ["add", root_arg, "--list"], root, env)
        if SKILL_NAME not in listed:
            errors.append("Skills CLI discovery did not list topology-skill")
        if not re.search(r"Found\s+1\s+skill\b", listed):
            errors.append("Skills CLI discovery did not report exactly one skill")

        prompt = run_command(base + ["use", root_arg, "--skill", SKILL_NAME], root, env)
        if not prompt.strip():
            errors.append("Skills CLI generated an empty use prompt")
        if SKILL_NAME not in prompt and "Topology Architecture" not in prompt:
            errors.append("Skills CLI use prompt does not identify the skill entry point")

        with tempfile.TemporaryDirectory(prefix="topology-skill-smoke-") as temporary:
            temp_root = Path(temporary)
            run_command(
                base
                + [
                    "add",
                    root_arg,
                    "--skill",
                    SKILL_NAME,
                    "--agent",
                    "codex",
                    "--copy",
                    "--yes",
                ],
                temp_root,
                env,
            )
            installed = temp_root / ".agents" / "skills" / SKILL_NAME
            if not installed.is_dir():
                errors.append(f"Skills CLI did not create expected copy: {installed}")
            else:
                expected_installed = {
                    "SKILL.md",
                    "README.md",
                    "agents/openai.yaml",
                    *REQUIRED_REFERENCES,
                }
                for relative in expected_installed:
                    if not (installed / relative).is_file():
                        errors.append(f"installed copy is missing: {relative}")
                errors.extend(f"installed copy: {error}" for error in validate_tree(installed))
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR: skill root does not exist: {root}", file=sys.stderr)
        return 1

    errors = validate_tree(root, repository=args.repository)
    if args.npx_smoke:
        errors.extend(validate_npx(root))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    modes = ["core"]
    if args.repository:
        modes.append("repository")
    if args.npx_smoke:
        modes.append(f"skills@{SKILLS_CLI_VERSION}")
    print(f"PASS: {SKILL_NAME} ({', '.join(modes)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
