#!/usr/bin/env python3
"""Build a deterministic ZIP from the public skills-only plugin root."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from release_contract import (
    RELEASE_CREATE_SYSTEM,
    RELEASE_FILES,
    RELEASE_TIMESTAMP,
    RELEASE_UNIX_MODE,
    native_release_path,
    release_tree_differences,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "premilume"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "dist" / "premilume-0.1.0.zip",
        help="Destination ZIP path",
    )
    return parser.parse_args()


def build_archive(output: Path, plugin_root: Path = PLUGIN_ROOT) -> Path:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    missing, extra = release_tree_differences(plugin_root)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing: {', '.join(sorted(missing))}")
        if extra:
            details.append(f"unexpected: {', '.join(sorted(extra))}")
        raise ValueError("plugin tree does not match the release allowlist (" + "; ".join(details) + ")")

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in RELEASE_FILES:
            source = native_release_path(plugin_root, relative)
            if source.is_symlink() or not source.is_file():
                raise ValueError(f"release entry must be a regular non-symlink file: {relative}")
            info = zipfile.ZipInfo(relative, RELEASE_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = RELEASE_CREATE_SYSTEM
            info.external_attr = RELEASE_UNIX_MODE << 16
            info.internal_attr = 0
            info.extra = b""
            info.comment = b""
            archive.writestr(info, source.read_bytes())

    return output


def main() -> int:
    args = parse_args()
    output = build_archive(args.output)

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
