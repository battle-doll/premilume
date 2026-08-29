#!/usr/bin/env python3
"""Validate the public marketplace repository and skills-only plugin package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse

from release_contract import (
    RELEASE_CREATE_SYSTEM,
    RELEASE_FILES,
    RELEASE_TIMESTAMP,
    RELEASE_UNIX_MODE,
    native_release_path,
    release_tree_differences,
)

try:
    import yaml
except ImportError:  # pragma: no cover - reported as a validation error
    yaml = None


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "premilume"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "premilume-mode"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

REQUIRED_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "README.ko.md",
    REPO_ROOT / "README.ja.md",
    REPO_ROOT / "README.zh-CN.md",
    REPO_ROOT / "README.ru.md",
    REPO_ROOT / "PRIVACY.md",
    REPO_ROOT / "TERMS.md",
    REPO_ROOT / "SUPPORT.md",
    REPO_ROOT / "SECURITY.md",
    REPO_ROOT / "LICENSE",
    REPO_ROOT / "NOTICE.md",
    REPO_ROOT / "evals" / "submission-cases.json",
    REPO_ROOT / "evals" / "regression-cases.json",
    PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
    SKILL_ROOT / "SKILL.md",
    SKILL_ROOT / "agents" / "openai.yaml",
    SKILL_ROOT / "references" / "routing.md",
    SKILL_ROOT / "references" / "knowledge-frontier.md",
    SKILL_ROOT / "references" / "safety-and-values.md",
    PLUGIN_ROOT / "assets" / "icon.svg",
    PLUGIN_ROOT / "assets" / "logo.svg",
    SKILL_ROOT / "assets" / "icon.svg",
    SKILL_ROOT / "assets" / "logo.svg",
    MARKETPLACE_PATH,
]

for language in ("ko", "ja", "zh-CN", "ru"):
    for document in (
        "PRIVACY.md",
        "TERMS.md",
        "SUPPORT.md",
        "SECURITY.md",
        "NOTICE.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
    ):
        REQUIRED_FILES.append(REPO_ROOT / "docs" / language / document)

TEXT_SUFFIXES = {".cfg", ".ini", ".json", ".md", ".py", ".svg", ".toml", ".txt", ".yaml", ".yml"}
EXECUTABLE_SUFFIXES = {".bat", ".cmd", ".com", ".exe", ".js", ".ps1", ".py", ".sh", ".ts"}
STRICT_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)

# SHA-256 digests of retired public role identifiers. Hashes avoid reintroducing
# those identifiers into the distributable source while still enforcing the gate.
FORBIDDEN_WORD_HASHES = {
    "9202af6ce925b26ae6b25adfff0b2705147e195fa38dd58ae6ecc58ed263751f",
    "d1068beeb96a6a79937661d5cc9f290dddaa5730e64b7ab2b238078a1194c614",
    "8db59feb4d217f26c79d6e76eea6ff80398e8b823e376bb783be870a96cab9e7",
}

WINDOWS_RESERVED_NAMES = {
    "aux",
    "clock$",
    "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
    "con",
    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
    "nul",
    "prn",
}


def unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_json_object)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid JSON: {path.relative_to(REPO_ROOT)} ({exc})")
        return None


def load_yaml_text(contents: str, label: str, errors: list[str]) -> object | None:
    if yaml is None:
        errors.append("PyYAML is required for duplicate-safe YAML validation; install tools/requirements-dev.txt")
        return None

    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_unique_mapping(loader: object, node: object, deep: bool = False) -> dict[object, object]:
        mapping: dict[object, object] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_unique_mapping,
    )
    try:
        return yaml.load(contents, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        errors.append(f"invalid or duplicate-key YAML: {label} ({exc})")
        return None


def prospective_public_files() -> list[Path]:
    """Return tracked and unignored files that would be published from this repository."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        relatives = [item for item in result.stdout.decode("utf-8").split("\0") if item]
        return sorted(
            path
            for relative in relatives
            if (path := REPO_ROOT / relative).is_file()
        )
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        excluded = {".git", ".playwright-mcp", "__pycache__", "dist"}
        return sorted(
            path
            for path in REPO_ROOT.rglob("*")
            if path.is_file() and not any(part in excluded for part in path.relative_to(REPO_ROOT).parts)
        )


def public_text_files() -> list[Path]:
    return [
        path
        for path in prospective_public_files()
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}
    ]


def validate_required_files(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(REPO_ROOT)}")


def validate_public_tree(errors: list[str]) -> None:
    compatibility_paths: set[str] = set()
    for path in prospective_public_files():
        relative = path.relative_to(REPO_ROOT)
        relative_name = relative.as_posix()
        compatibility_name = unicodedata.normalize("NFKC", relative_name).casefold()
        if compatibility_name in compatibility_paths:
            errors.append(f"case or Unicode-colliding public path: {relative}")
        compatibility_paths.add(compatibility_name)
        if path.is_symlink():
            errors.append(f"symlink is not allowed in prospective public tree: {relative}")
        if any(part in {".playwright-mcp", "__pycache__", "dist"} for part in relative.parts) or (
            len(relative.parts) >= 2 and relative.parts[:2] == ("evals", "transcripts")
        ):
            errors.append(f"private or generated path is not allowed in prospective public tree: {relative}")
        if re.search(
            r"(?:^|/)(?:\.env(?:\..*)?|id_(?:rsa|dsa|ed25519)|credentials?(?:\.[^/]*)?|"
            r"secrets?(?:\.[^/]*)?|[^/]+\.(?:pem|key|p12|pfx))$",
            relative_name,
            re.IGNORECASE,
        ):
            errors.append(f"secret-like filename in prospective public tree: {relative}")
        try:
            raw = path.read_bytes()
        except OSError as exc:
            errors.append(f"unreadable prospective public file: {relative} ({exc})")
            continue
        if any(
            pattern.search(raw)
            for pattern in (
                re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
                re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
                re.compile(rb"AKIA[0-9A-Z]{16}"),
                re.compile(rb"xox[baprs]-[A-Za-z0-9-]{10,}"),
                re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            )
        ):
            errors.append(f"possible secret in prospective public file: {relative}")


def validate_text(errors: list[str]) -> None:
    placeholder_patterns = (
        "[" + "TODO:",
        "Local " + "developer",
        "plugin " + "scaffold",
        "[" + "PLACEHOLDER]",
    )
    local_path_patterns = (
        re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
        re.compile(r"/(?:Users|home)/[^\s/]+/"),
    )
    secret_patterns = (
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    )
    pii_patterns = (
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        re.compile(r"\b\d{6}-[1-8]\d{6}\b"),
    )

    for path in public_text_files():
        relative = path.relative_to(REPO_ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"unreadable public text file: {relative} ({exc})")
            continue

        for marker in placeholder_patterns:
            if marker in text:
                errors.append(f"unfinished placeholder in {relative}: {marker}")
        for pattern in local_path_patterns:
            if pattern.search(text):
                errors.append(f"local absolute path in public file: {relative}")
        for pattern in secret_patterns:
            if pattern.search(text):
                errors.append(f"possible secret in public file: {relative}")
        for pattern in pii_patterns:
            if pattern.search(text):
                errors.append(f"possible personal identifier in public file: {relative}")

        for word in re.findall(r"[A-Za-z]+", text):
            digest = hashlib.sha256(word.lower().encode("utf-8")).hexdigest()
            if digest in FORBIDDEN_WORD_HASHES:
                errors.append(f"retired public role identifier in {relative}")
                break


def validate_internal_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in public_text_files():
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().strip("<>")
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("#"):
                continue
            relative_target = unquote(target.split("#", 1)[0])
            if not relative_target:
                continue
            resolved = (path.parent / relative_target).resolve()
            if not resolved.is_relative_to(REPO_ROOT) or not resolved.exists():
                errors.append(f"broken or escaping Markdown link in {path.relative_to(REPO_ROOT)}: {target}")


def validate_plugin_manifest(errors: list[str]) -> None:
    payload = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json", errors)
    if not isinstance(payload, dict):
        return

    if payload.get("name") != PLUGIN_ROOT.name:
        errors.append("plugin folder and plugin.json name must match")
    version = payload.get("version")
    if not isinstance(version, str) or STRICT_SEMVER.fullmatch(version) is None:
        errors.append("plugin version must be strict semver")
    for field in ("mcpServers", "apps", "hooks"):
        if field in payload:
            errors.append(f"skills-only manifest must not include {field}")

    interface = payload.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin interface must be an object")
        return
    if "screenshots" in interface:
        errors.append("skills-only plugin without UI must not include screenshots")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append("interface.defaultPrompt must contain one to three prompts")
    elif any(not isinstance(prompt, str) or not prompt.strip() or "\n" in prompt or len(prompt) > 128 for prompt in prompts):
        errors.append("starter prompts must be non-empty, single-line, and at most 128 characters")
    elif len(set(prompts)) != len(prompts):
        errors.append("starter prompts must be unique")

    for field in ("composerIcon", "logo"):
        raw = interface.get(field)
        if not isinstance(raw, str):
            errors.append(f"interface.{field} is required")
            continue
        candidate = PurePosixPath(raw)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"interface.{field} must stay inside the package")
            continue
        if not (PLUGIN_ROOT / candidate.as_posix()).is_file():
            errors.append(f"interface.{field} points to a missing asset")


def validate_skill(errors: list[str]) -> None:
    skill_path = SKILL_ROOT / "SKILL.md"
    try:
        contents = skill_path.read_text(encoding="utf-8")
    except OSError:
        return
    if not contents.startswith("---\n") or "\n---\n" not in contents[4:]:
        errors.append("skill must contain closed YAML frontmatter")
        return

    frontmatter_end = contents.find("\n---\n", 4)
    frontmatter = load_yaml_text(
        contents[4:frontmatter_end],
        str(skill_path.relative_to(REPO_ROOT)),
        errors,
    )
    if not isinstance(frontmatter, dict):
        errors.append("skill frontmatter must be a YAML mapping")
    else:
        if frontmatter.get("name") != "premilume-mode":
            errors.append("skill frontmatter name is missing or incorrect")
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append("skill frontmatter description must contain 1 to 1,024 characters")

    agent_path = SKILL_ROOT / "agents" / "openai.yaml"
    agent_payload = load_yaml_text(
        agent_path.read_text(encoding="utf-8"),
        str(agent_path.relative_to(REPO_ROOT)),
        errors,
    )
    if not isinstance(agent_payload, dict):
        errors.append("agents/openai.yaml must be a YAML mapping")
        return
    policy = agent_payload.get("policy")
    if not isinstance(policy, dict) or policy.get("allow_implicit_invocation") is not True:
        errors.append("invocation policy must match the documented guarded natural-language design")
    if "dependencies" in agent_payload:
        errors.append("skills-only v0.1 must not declare tool dependencies")


def validate_marketplace(errors: list[str]) -> None:
    payload = load_json(MARKETPLACE_PATH, errors)
    if not isinstance(payload, dict):
        return
    if payload.get("name") != "premilume-marketplace":
        errors.append("marketplace name must be premilume-marketplace")
    plugins = payload.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        errors.append("marketplace must contain exactly one plugin entry")
        return
    entry = plugins[0]
    if entry.get("name") != "premilume":
        errors.append("marketplace plugin name mismatch")
    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local" or source.get("path") != "./plugins/premilume":
        errors.append("marketplace source must point to ./plugins/premilume")
    policy = entry.get("policy")
    if not isinstance(policy, dict) or policy.get("installation") != "AVAILABLE" or policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
        errors.append("marketplace policy is missing or invalid")


def validate_package_surface(errors: list[str]) -> None:
    forbidden_names = {".app.json", ".mcp.json", "hooks.json"}
    forbidden_dirs = {"hooks", "scripts"}
    for path in PLUGIN_ROOT.rglob("*"):
        relative = path.relative_to(PLUGIN_ROOT)
        if path.is_symlink():
            errors.append(f"symlink is not allowed in plugin package: {relative}")
        if path.name in forbidden_names:
            errors.append(f"unexpected runtime component: {relative}")
        if path.is_dir() and path.name in forbidden_dirs:
            errors.append(f"unexpected runtime directory: {relative}")
        if path.is_file() and path.suffix.lower() in EXECUTABLE_SUFFIXES:
            errors.append(f"executable file is not allowed in skills-only package: {relative}")
    missing, extra = release_tree_differences(PLUGIN_ROOT)
    if missing:
        errors.append(f"plugin release allowlist files are missing: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"plugin tree has files outside the release allowlist: {', '.join(sorted(extra))}")
    try:
        if (REPO_ROOT / "LICENSE").read_bytes() != (PLUGIN_ROOT / "LICENSE").read_bytes():
            errors.append("repository and distributable MIT license files must match")
    except OSError:
        pass


def validate_svg_contents(contents: str, label: str, errors: list[str]) -> None:
    if len(contents.encode("utf-8")) > 1024 * 1024:
        errors.append(f"SVG exceeds the 1 MiB static-asset limit: {label}")
        return
    lowered_contents = contents.lower()
    if any(marker in lowered_contents for marker in ("<!doctype", "<!entity", "<?", "@import", "url(")):
        errors.append(f"active or externally extensible SVG syntax in {label}")
        return
    try:
        root = ET.fromstring(contents)
    except ET.ParseError as exc:
        errors.append(f"invalid SVG: {label} ({exc})")
        return
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        errors.append(f"SVG root element or namespace is invalid: {label}")
        return
    elements = list(root.iter())
    if len(elements) > 128:
        errors.append(f"SVG has too many elements: {label}")
        return

    allowed_attributes = {
        "svg": {"viewBox", "role", "aria-labelledby"},
        "title": {"id"},
        "desc": {"id"},
        "rect": {"width", "height", "rx", "fill"},
        "path": {"d", "fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin"},
        "circle": {"cx", "cy", "r", "fill"},
    }
    color_pattern = re.compile(r"(?:#[0-9A-Fa-f]{6}|none)")
    number_pattern = re.compile(r"[0-9]+(?:\.[0-9]+)?")
    for element in elements:
        tag = element.tag.rsplit("}", 1)[-1].lower()
        if tag not in allowed_attributes:
            errors.append(f"SVG element is outside the static allowlist in {label}: {tag}")
            continue
        for raw_name, value in element.attrib.items():
            name = raw_name.rsplit("}", 1)[-1].lower()
            lowered = value.strip().lower()
            allowed_for_tag = {attribute.lower() for attribute in allowed_attributes[tag]}
            if name not in allowed_for_tag:
                errors.append(f"SVG attribute is outside the static allowlist in {label}: {tag}.{name}")
            if "\\" in value or any(ord(character) < 32 for character in value):
                errors.append(f"escaped or control content is not allowed in SVG attributes: {label}")
            if any(marker in lowered for marker in ("http:", "https:", "data:", "javascript:", "url(", "@import")):
                errors.append(f"external or active SVG value in {label}")
            if name in {"fill", "stroke"} and color_pattern.fullmatch(value) is None:
                errors.append(f"SVG paint value is outside the static allowlist in {label}: {value}")
            elif name in {"width", "height", "rx", "cx", "cy", "r", "stroke-width"} and number_pattern.fullmatch(value) is None:
                errors.append(f"SVG numeric value is invalid in {label}: {tag}.{name}")
            elif name == "d" and re.fullmatch(r"[0-9A-Za-z .,+-]+", value) is None:
                errors.append(f"SVG path data is outside the static allowlist in {label}")
            elif name in {"stroke-linecap", "stroke-linejoin"} and value not in {"butt", "round", "square", "miter", "bevel"}:
                errors.append(f"SVG stroke value is outside the static allowlist in {label}: {value}")
            elif name == "role" and value != "img":
                errors.append(f"SVG role must be img in {label}")
            elif name in {"id", "aria-labelledby"} and re.fullmatch(r"[A-Za-z][A-Za-z0-9 _.-]*", value) is None:
                errors.append(f"SVG identifier value is invalid in {label}: {value}")
            elif name == "viewbox" and re.fullmatch(r"[0-9]+(?:\.[0-9]+)?(?: [0-9]+(?:\.[0-9]+)?){3}", value) is None:
                errors.append(f"SVG viewBox is invalid in {label}")


def validate_svg(errors: list[str]) -> None:
    for path in list((PLUGIN_ROOT / "assets").glob("*.svg")) + list((SKILL_ROOT / "assets").glob("*.svg")):
        relative = path.relative_to(REPO_ROOT)
        try:
            contents = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"invalid SVG: {relative} ({exc})")
            continue
        validate_svg_contents(contents, str(relative), errors)


def validate_evals(errors: list[str]) -> None:
    submission = load_json(REPO_ROOT / "evals" / "submission-cases.json", errors)
    if isinstance(submission, dict):
        positive = submission.get("positive")
        negative = submission.get("negative")
        if not isinstance(positive, list) or len(positive) != 5:
            errors.append("submission evals must contain exactly five positive cases")
        if not isinstance(negative, list) or len(negative) != 3:
            errors.append("submission evals must contain exactly three negative cases")
        identifiers = [case.get("id") for group in (positive, negative) if isinstance(group, list) for case in group if isinstance(case, dict)]
        if len(identifiers) != len(set(identifiers)):
            errors.append("submission eval IDs must be unique")

    regression = load_json(REPO_ROOT / "evals" / "regression-cases.json", errors)
    if isinstance(regression, dict):
        cases = regression.get("cases")
        if not isinstance(cases, list) or len(cases) < 20:
            errors.append("regression suite must contain at least twenty cases")

    if (REPO_ROOT / "evals" / "transcripts").exists():
        errors.append("real transcript directory must not exist in the public tree")


def validate_gitignore(errors: list[str]) -> None:
    try:
        entries = set((REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines())
    except OSError:
        errors.append("missing .gitignore")
        return
    required = {".playwright-mcp/", "PLUGIN_HANDOFF.md", "PLUGIN_CHAT_PROMPT.md", "*.log", ".env", ".env.*", "evals/transcripts/"}
    missing = sorted(required - entries)
    if missing:
        errors.append(f".gitignore is missing sensitive working patterns: {', '.join(missing)}")


def validate_archive(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"archive does not exist: {path}")
        return
    if path.stat().st_size > 100 * 1024 * 1024:
        errors.append("archive exceeds 100 MiB")
        return
    try:
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if archive.comment:
                errors.append("archive comment is not allowed")
            if len(entries) != len(RELEASE_FILES):
                errors.append(f"archive must contain exactly {len(RELEASE_FILES)} canonical file entries")
            bad_crc = archive.testzip()
            if bad_crc is not None:
                errors.append(f"archive CRC or decompression check failed: {bad_crc}")
            if len(entries) > 5000:
                errors.append("archive exceeds 5,000 entries")
            if sum(entry.file_size for entry in entries) > 512 * 1024 * 1024:
                errors.append("archive exceeds 512 MiB uncompressed")

            names: set[str] = set()
            compatibility_names: set[str] = set()
            actual_files: set[str] = set()
            for entry in entries:
                name = entry.filename
                normalized_name = name.rstrip("/")
                compatibility_name = unicodedata.normalize("NFKC", normalized_name).casefold()
                if normalized_name in names or compatibility_name in compatibility_names:
                    errors.append(f"duplicate archive entry is not allowed: {name}")
                names.add(normalized_name)
                compatibility_names.add(compatibility_name)
                parts = PurePosixPath(name).parts
                if "\x00" in name or "\\" in name or name.startswith(("/", "\\")) or ".." in parts:
                    errors.append(f"unsafe archive path: {name}")
                for component in normalized_name.split("/"):
                    compatibility_component = unicodedata.normalize("NFKC", component)
                    windows_base = compatibility_component.split(".", 1)[0].casefold()
                    if (
                        not component
                        or component in {".", ".."}
                        or component.endswith((" ", "."))
                        or any(character in compatibility_component for character in '<>:"/\\|?*')
                        or any(ord(character) < 32 for character in component)
                        or windows_base in WINDOWS_RESERVED_NAMES
                    ):
                        errors.append(f"Windows-unsafe archive component in {name}: {component!r}")
                if len(parts) > 20:
                    errors.append(f"archive path is deeper than 20 levels: {name}")
                if entry.flag_bits & 0x1:
                    errors.append(f"encrypted archive entry is not allowed: {name}")
                if entry.flag_bits != 0:
                    errors.append(f"archive entry flags are not canonical: {name}")
                if entry.is_dir():
                    errors.append(f"directory archive entry is not allowed: {name}")
                if entry.comment:
                    errors.append(f"archive entry comment is not allowed: {name}")
                if entry.extra:
                    errors.append(f"archive entry extra metadata is not allowed: {name}")
                if entry.date_time != RELEASE_TIMESTAMP:
                    errors.append(f"archive entry timestamp is not canonical: {name}")
                if entry.compress_type != zipfile.ZIP_DEFLATED:
                    errors.append(f"archive entry compression is not canonical: {name}")
                if entry.create_system != RELEASE_CREATE_SYSTEM:
                    errors.append(f"archive entry creator system is not canonical: {name}")
                if entry.create_version != 20 or entry.extract_version != 20:
                    errors.append(f"archive entry ZIP version metadata is not canonical: {name}")
                if entry.internal_attr != 0:
                    errors.append(f"archive entry internal attributes are not canonical: {name}")
                if entry.volume != 0 or entry.reserved != 0:
                    errors.append(f"archive entry volume metadata is not canonical: {name}")
                unix_mode = entry.external_attr >> 16
                file_type = unix_mode & 0o170000
                if file_type == 0o120000:
                    errors.append(f"archive symlink is not allowed: {name}")
                elif file_type not in {0, 0o040000, 0o100000}:
                    errors.append(f"archive special file is not allowed: {name}")

                if entry.is_dir():
                    continue
                if unix_mode != RELEASE_UNIX_MODE or entry.external_attr != RELEASE_UNIX_MODE << 16:
                    errors.append(f"archive entry file mode is not canonical: {name}")
                if unix_mode & 0o111:
                    errors.append(f"executable permission bits are not allowed: {name}")
                actual_files.add(name)
                suffix = PurePosixPath(name).suffix.lower()
                if suffix in EXECUTABLE_SUFFIXES:
                    errors.append(f"executable archive entry is not allowed: {name}")
                if re.search(
                    r"(?:^|/)(?:\.env(?:\..*)?|id_(?:rsa|dsa|ed25519)|credentials?(?:\.[^/]*)?|"
                    r"secrets?(?:\.[^/]*)?|[^/]+\.(?:pem|key|p12|pfx))$",
                    name,
                    re.IGNORECASE,
                ):
                    errors.append(f"secret-like archive filename is not allowed: {name}")
                if (
                    PurePosixPath(name).name in {".app.json", ".mcp.json", "hooks.json"}
                    or any(component in {"hooks", "scripts"} for component in PurePosixPath(name).parts)
                ):
                    errors.append(f"unexpected runtime component in archive: {name}")

            expected_files = set(RELEASE_FILES)
            missing_files = sorted(expected_files - actual_files)
            extra_files = sorted(actual_files - expected_files)
            if missing_files:
                errors.append(f"archive is missing source files: {', '.join(missing_files)}")
            if extra_files:
                errors.append(f"archive has unexpected files: {', '.join(extra_files)}")

            for name in sorted(expected_files & actual_files):
                source_bytes = native_release_path(PLUGIN_ROOT, name).read_bytes()
                archived_bytes = archive.read(name)
                if archived_bytes != source_bytes:
                    errors.append(f"archive content differs from plugin source: {name}")
                if PurePosixPath(name).suffix.lower() in TEXT_SUFFIXES:
                    try:
                        archived_text = archived_bytes.decode("utf-8")
                    except UnicodeDecodeError:
                        errors.append(f"archive text entry is not valid UTF-8: {name}")
                        continue
                    if any(
                        pattern.search(archived_text)
                        for pattern in (
                            re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
                            re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
                            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
                        )
                    ):
                        errors.append(f"possible secret in archive entry: {name}")
                    if any(
                        pattern.search(archived_text)
                        for pattern in (
                            re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
                            re.compile(r"/(?:Users|home)/[^\s/]+/"),
                        )
                    ):
                        errors.append(f"local absolute path in archive entry: {name}")
                    if any(
                        marker in archived_text
                        for marker in (
                            "[" + "TODO:",
                            "Local " + "developer",
                            "plugin " + "scaffold",
                            "[" + "PLACEHOLDER]",
                        )
                    ):
                        errors.append(f"unfinished placeholder in archive entry: {name}")
                    for word in re.findall(r"[A-Za-z]+", archived_text):
                        digest = hashlib.sha256(word.lower().encode("utf-8")).hexdigest()
                        if digest in FORBIDDEN_WORD_HASHES:
                            errors.append(f"retired public role identifier in archive entry: {name}")
                            break
                    if PurePosixPath(name).suffix.lower() == ".svg":
                        validate_svg_contents(archived_text, f"archive:{name}", errors)

            required = {
                ".codex-plugin/plugin.json",
                "skills/premilume-mode/SKILL.md",
            }
            missing = sorted(required - names)
            if missing:
                errors.append(f"archive is missing required entries: {', '.join(missing)}")
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f"invalid archive: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="Optional release ZIP to validate")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    validate_required_files(errors)
    validate_public_tree(errors)
    validate_text(errors)
    validate_internal_links(errors)
    validate_plugin_manifest(errors)
    validate_skill(errors)
    validate_marketplace(errors)
    validate_package_surface(errors)
    validate_svg(errors)
    validate_evals(errors)
    validate_gitignore(errors)
    if args.archive is not None:
        validate_archive(args.archive.resolve(), errors)

    if errors:
        print("Package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Package validation passed: premilume 0.1.1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
