#!/usr/bin/env python3
"""Validate the portable topology skill, its repository layer, or an installed copy.

Repository layout (the repository layer is never installed by hosts):

    topology-skill/                repository root
    ├── README.md, LICENSE, .gitignore, .github/, scripts/, tests/
    └── skills/topology/           the portable skill: the only thing hosts install

Usage:
    python scripts/validate_skill.py                      # validate skills/topology
    python scripts/validate_skill.py path/to/topology     # validate an installed copy
    python scripts/validate_skill.py --repository         # also check the repository layer
    python scripts/validate_skill.py --repository --npx-smoke

The script needs only the Python standard library. Exit code 0 means no errors.
"""

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


SKILL_NAME = "topology"
SKILL_RELATIVE = Path("skills") / SKILL_NAME
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SKILLS_CLI_VERSION = "1.5.21"
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_DESCRIPTION_CHARS = 1024
MAX_COMPATIBILITY_CHARS = 500
MAX_BODY_LINES = 500
SPEC_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
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
SECRET_PATTERN = re.compile(
    r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN (?:RSA |EC )?PRIVATE KEY)"
)


class ValidationError(Exception):
    """Raised when a subprocess-based validation step fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "root",
        nargs="?",
        help=(
            "skill directory to validate, or the repository root with --repository "
            "(defaults are derived from this script's own location)"
        ),
    )
    parser.add_argument(
        "--repository",
        action="store_true",
        help="treat ROOT as the repository root and also check repository-layer files",
    )
    parser.add_argument(
        "--npx-smoke",
        action="store_true",
        help="run pinned Skills CLI discovery, prompt, and copy-install checks (implies --repository)",
    )
    return parser.parse_args()


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"cannot read UTF-8 text {path}: {exc}")
        return ""


def parse_frontmatter(skill_text: str, errors: list[str]) -> tuple[dict[str, str], str]:
    """Return (frontmatter, body). Only flat ``key: value`` lines are supported."""
    lines = skill_text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md must begin with YAML frontmatter")
        return {}, skill_text
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        errors.append("SKILL.md frontmatter has no closing delimiter")
        return {}, skill_text

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
    return metadata, "\n".join(lines[closing + 1 :])


def markdown_targets(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)]


def validate_links(root: Path, markdown_files: list[Path], errors: list[str]) -> None:
    lexical_root = Path(os.path.abspath(root))
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
            # Keep this check lexical. On Windows the Skills CLI can install through
            # a directory junction, and Path.resolve() would make valid in-skill
            # links appear to escape into the original source directory.
            destination = Path(os.path.abspath(source.parent / relative))
            try:
                destination.relative_to(lexical_root)
            except ValueError:
                errors.append(f"relative link escapes root: {source.relative_to(root)} -> {target}")
                continue
            if not destination.exists():
                errors.append(f"broken relative link: {source.relative_to(root)} -> {target}")


def iter_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and not any(part in {".git", "node_modules"} for part in path.parts)
    ]


def validate_common_hygiene(root: Path, files: list[Path], errors: list[str]) -> None:
    unfinished_tokens = ("TO" + "DO", "T" + "BD", "FIX" + "ME", "PLACE" + "HOLDER")
    unfinished_pattern = re.compile(r"\b(?:" + "|".join(unfinished_tokens) + r")\b", re.IGNORECASE)
    for path in files:
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_DIRECTORIES for part in relative.parts):
            errors.append(f"forbidden dependency/build directory committed: {relative}")
        if path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            errors.append(f"unexpected binary artifact: {relative}")
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            errors.append(f"environment file must not be committed: {relative}")
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                errors.append(f"file exceeds {MAX_FILE_BYTES} bytes: {relative}")
        except OSError as exc:
            errors.append(f"cannot stat {relative}: {exc}")
            continue
        if path.suffix.lower() in {".md", ".py", ".yaml", ".yml", ".txt", ".json"}:
            text = read_text(path, errors)
            if path.suffix.lower() == ".md" and unfinished_pattern.search(text):
                errors.append(f"unfinished marker found in {relative}")
            if SECRET_PATTERN.search(text):
                errors.append(f"possible secret found in {relative}")


def validate_skill(skill_root: Path) -> list[str]:
    """Validate the portable skill directory against the Agent Skills spec."""
    errors: list[str] = []
    skill_path = skill_root / "SKILL.md"
    if not skill_path.is_file():
        return [f"missing SKILL.md in {skill_root}"]

    skill_text = read_text(skill_path, errors)
    metadata, body = parse_frontmatter(skill_text, errors)

    name = metadata.get("name", "")
    if name != SKILL_NAME:
        errors.append(f"frontmatter name must be {SKILL_NAME!r}, found {name!r}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("frontmatter name must be 1-64 chars of lowercase letters, digits, and single hyphens")
    if name != skill_root.name:
        errors.append(f"frontmatter name {name!r} must equal directory name {skill_root.name!r}")

    description = metadata.get("description", "")
    if not description:
        errors.append("frontmatter description must be non-empty")
    if len(description) > MAX_DESCRIPTION_CHARS:
        errors.append(f"frontmatter description exceeds {MAX_DESCRIPTION_CHARS} chars")
    if "<" in description or ">" in description:
        errors.append("frontmatter description must not contain angle brackets")
    if len(metadata.get("compatibility", "")) > MAX_COMPATIBILITY_CHARS:
        errors.append(f"frontmatter compatibility exceeds {MAX_COMPATIBILITY_CHARS} chars")
    for key in metadata:
        if key not in SPEC_FRONTMATTER_KEYS:
            errors.append(f"non-spec frontmatter key {key!r}; claude.ai and the Skills API reject it")

    body_lines = body.count("\n") + 1
    if body_lines > MAX_BODY_LINES:
        errors.append(f"SKILL.md body has {body_lines} lines; keep it under {MAX_BODY_LINES}")

    for phrase in REQUIRED_CONTRACT_PHRASES:
        if phrase not in skill_text:
            errors.append(f"SKILL.md is missing required contract phrase: {phrase!r}")
    for reference in REQUIRED_REFERENCES:
        if f"]({reference})" not in skill_text:
            errors.append(f"SKILL.md does not link required reference: {reference}")

    files = iter_files(skill_root)
    markdown_files = [path for path in files if path.suffix.lower() == ".md"]

    # Every bundled reference must be discoverable from SKILL.md.
    for path in markdown_files:
        relative = path.relative_to(skill_root).as_posix()
        if relative.startswith("references/") and f"]({relative})" not in skill_text:
            errors.append(f"reference is not linked from SKILL.md: {relative}")

    # Portability: no absolute paths, no parent traversal, no repository-layer dependencies.
    portability_pattern = re.compile(r"(?<![\w/])\.\./|(?<![\w:])(?:[A-Za-z]:[\\/]|/(?:home|Users)/)")
    for path in markdown_files:
        text = read_text(path, errors)
        relative = path.relative_to(skill_root)
        if portability_pattern.search(text):
            errors.append(f"absolute or parent-relative path in {relative}")
        if re.search(r"\bREADME\.md\b|\.env\.example|\bskills-lock\.json\b", text):
            errors.append(f"skill content must not depend on repository-layer files: {relative}")

    validate_links(skill_root, markdown_files, errors)
    validate_common_hygiene(skill_root, files, errors)

    for forbidden in FORBIDDEN_PATHS:
        if (skill_root / forbidden).exists():
            errors.append(f"forbidden runtime or metadata path committed: {forbidden}")

    agent_metadata_path = skill_root / "agents" / "openai.yaml"
    if agent_metadata_path.is_file():
        agent_metadata = read_text(agent_metadata_path, errors)
        if 'display_name: "Topology Architecture"' not in agent_metadata:
            errors.append("agents/openai.yaml must use the Topology Architecture display name")
        if f"${SKILL_NAME}" not in agent_metadata:
            errors.append(f"agents/openai.yaml default prompt must reference ${SKILL_NAME}")
        if "allow_implicit_invocation: true" not in agent_metadata:
            errors.append("agents/openai.yaml must allow implicit invocation")

    return errors


def validate_repository(repo_root: Path) -> list[str]:
    """Validate the repository layer that wraps the skill."""
    errors: list[str] = []
    skill_root = repo_root / SKILL_RELATIVE
    if not skill_root.is_dir():
        return [f"missing skill directory: {SKILL_RELATIVE.as_posix()}"]
    if (repo_root / "SKILL.md").exists():
        errors.append("SKILL.md must not be at the repository root; keep it in skills/topology/")

    errors.extend(validate_skill(skill_root))

    required_repository_files = {
        ".github/workflows/validate.yml",
        ".gitignore",
        "LICENSE",
        "README.md",
        "tests/behavior-cases.md",
    }
    for relative in required_repository_files:
        if not (repo_root / relative).is_file():
            errors.append(f"missing repository file: {relative}")

    gitignore = read_text(repo_root / ".gitignore", errors) if (repo_root / ".gitignore").is_file() else ""
    if not re.search(r"^\.env$", gitignore, re.MULTILINE) or not re.search(r"^\.env\.\*$", gitignore, re.MULTILINE):
        errors.append(".gitignore must ignore .env and .env.*")

    license_text = read_text(repo_root / "LICENSE", errors) if (repo_root / "LICENSE").is_file() else ""
    if "MIT License" not in license_text or "Copyright (c) 2026 Sisyphe42" not in license_text:
        errors.append("LICENSE must be MIT with Copyright (c) 2026 Sisyphe42")

    readme_path = repo_root / "README.md"
    readme_text = read_text(readme_path, errors) if readme_path.is_file() else ""
    if f"--skill {SKILL_NAME}" not in readme_text:
        errors.append(f"README.md install commands must select --skill {SKILL_NAME}")

    cases_path = repo_root / "tests/behavior-cases.md"
    cases_text = read_text(cases_path, errors) if cases_path.is_file() else ""
    for case_id in BEHAVIOR_CASE_IDS:
        if cases_text.count(case_id) != 1:
            errors.append(f"behavior case must appear exactly once: {case_id}")

    repo_files = [path for path in iter_files(repo_root) if skill_root not in path.parents]
    repo_markdown = [path for path in repo_files if path.suffix.lower() == ".md"]
    validate_links(repo_root, repo_markdown, errors)
    validate_common_hygiene(repo_root, repo_files, errors)
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


def validate_npx(repo_root: Path) -> list[str]:
    errors: list[str] = []
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx:
        return ["npx is required for --npx-smoke"]

    env = os.environ.copy()
    env["DISABLE_TELEMETRY"] = "1"
    env["DO_NOT_TRACK"] = "1"
    base = [npx, "--yes", f"skills@{SKILLS_CLI_VERSION}"]
    root_arg = str(repo_root)
    try:
        listed = run_command(base + ["add", root_arg, "--list"], repo_root, env)
        plain_listed = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", listed)
        if SKILL_NAME not in plain_listed:
            errors.append(f"Skills CLI discovery did not list {SKILL_NAME}")
        found_count = re.search(r"Found\s+(\d+)\s+skills?\b", plain_listed)
        if not found_count or found_count.group(1) != "1":
            errors.append("Skills CLI discovery did not report exactly one skill")

        prompt = run_command(base + ["use", root_arg, "--skill", SKILL_NAME], repo_root, env)
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
                expected_installed = {"SKILL.md", "agents/openai.yaml", *REQUIRED_REFERENCES}
                for relative in expected_installed:
                    if not (installed / relative).is_file():
                        errors.append(f"installed copy is missing: {relative}")
                errors.extend(f"installed copy: {error}" for error in validate_skill(installed))
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    args = parse_args()
    repository = args.repository or args.npx_smoke

    if repository:
        root = Path(args.root).resolve() if args.root else REPOSITORY_ROOT
    else:
        root = Path(args.root).resolve() if args.root else REPOSITORY_ROOT / SKILL_RELATIVE
    if not root.is_dir():
        print(f"ERROR: root does not exist: {root}", file=sys.stderr)
        return 1

    errors = validate_repository(root) if repository else validate_skill(root)
    if args.npx_smoke:
        errors.extend(validate_npx(root))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    modes = ["skill"]
    if repository:
        modes.append("repository")
    if args.npx_smoke:
        modes.append(f"skills@{SKILLS_CLI_VERSION}")
    print(f"PASS: {SKILL_NAME} ({', '.join(modes)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
