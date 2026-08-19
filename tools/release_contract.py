#!/usr/bin/env python3
"""Single source of truth for the skills-only release file set."""

from __future__ import annotations

from pathlib import Path, PurePosixPath


RELEASE_FILES = (
    ".codex-plugin/plugin.json",
    "assets/icon.svg",
    "assets/logo.svg",
    "LICENSE",
    "NOTICE.md",
    "skills/premilume-mode/agents/openai.yaml",
    "skills/premilume-mode/assets/icon.svg",
    "skills/premilume-mode/assets/logo.svg",
    "skills/premilume-mode/references/knowledge-frontier.md",
    "skills/premilume-mode/references/routing.md",
    "skills/premilume-mode/references/safety-and-values.md",
    "skills/premilume-mode/SKILL.md",
)
RELEASE_TIMESTAMP = (2020, 1, 1, 0, 0, 0)
RELEASE_CREATE_SYSTEM = 3
RELEASE_UNIX_MODE = 0o100644


def native_release_path(plugin_root: Path, relative: str) -> Path:
    return plugin_root.joinpath(*PurePosixPath(relative).parts)


def release_tree_differences(plugin_root: Path) -> tuple[set[str], set[str]]:
    expected = set(RELEASE_FILES)
    actual = {
        path.relative_to(plugin_root).as_posix()
        for path in plugin_root.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    return expected - actual, actual - expected
