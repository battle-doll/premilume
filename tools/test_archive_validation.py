#!/usr/bin/env python3
"""Regression tests for release archive contamination controls."""

from __future__ import annotations

import tempfile
import unittest
import warnings
import zipfile
import shutil
from pathlib import Path

from build_release_zip import build_archive
from release_contract import (
    RELEASE_CREATE_SYSTEM,
    RELEASE_FILES,
    RELEASE_TIMESTAMP,
    RELEASE_UNIX_MODE,
    native_release_path,
)
from validate_package import PLUGIN_ROOT, validate_archive


class ArchiveValidationTests(unittest.TestCase):
    def assert_archive_error(self, archive: Path, fragment: str) -> None:
        errors: list[str] = []
        validate_archive(archive, errors)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def source_files(self) -> list[Path]:
        return [native_release_path(PLUGIN_ROOT, relative) for relative in RELEASE_FILES]

    def write_source_archive(
        self,
        output: Path,
        *,
        mutate: str | None = None,
        executable: str | None = None,
        extra_metadata: str | None = None,
    ) -> None:
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for source in self.source_files():
                name = source.relative_to(PLUGIN_ROOT).as_posix()
                payload = source.read_bytes()
                if name == mutate:
                    payload += b"\n"
                info = zipfile.ZipInfo(name, RELEASE_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = RELEASE_CREATE_SYSTEM
                info.external_attr = (0o100755 if name == executable else RELEASE_UNIX_MODE) << 16
                if name == extra_metadata:
                    info.extra = b"\xff\xff\x00\x00"
                archive.writestr(info, payload)

    def test_clean_archive_matches_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "clean.zip")
            errors: list[str] = []
            validate_archive(archive, errors)
            self.assertEqual(errors, [])

    def test_extra_secret_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "extra.zip")
            with zipfile.ZipFile(archive, "a") as handle:
                handle.writestr(".env", "TOKEN=synthetic")
            self.assert_archive_error(archive, "secret-like archive filename")
            self.assert_archive_error(archive, "unexpected files")

    def test_modified_source_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "modified.zip"
            self.write_source_archive(archive, mutate="skills/premilume-mode/SKILL.md")
            self.assert_archive_error(archive, "content differs from plugin source")

    def test_duplicate_and_unicode_collision_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "collision.zip")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(archive, "a") as handle:
                    handle.writestr("README", "synthetic")
                    handle.writestr("ＲＥＡＤＭＥ", "synthetic")
            self.assert_archive_error(archive, "duplicate archive entry")

    def test_windows_unsafe_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "windows-path.zip")
            with zipfile.ZipFile(archive, "a") as handle:
                handle.writestr("assets/CON.txt", "synthetic")
            self.assert_archive_error(archive, "Windows-unsafe archive component")

    def test_nfkc_windows_reserved_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "nfkc-windows-path.zip")
            with zipfile.ZipFile(archive, "a") as handle:
                handle.writestr("assets/COM¹.txt", "synthetic")
            self.assert_archive_error(archive, "Windows-unsafe archive component")

    def test_windows_forbidden_character_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "forbidden-character.zip")
            with zipfile.ZipFile(archive, "a") as handle:
                handle.writestr("assets/bad?.txt", "synthetic")
            self.assert_archive_error(archive, "Windows-unsafe archive component")

    def test_executable_permission_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "executable.zip"
            self.write_source_archive(archive, executable="skills/premilume-mode/SKILL.md")
            self.assert_archive_error(archive, "executable permission bits")

    def test_builder_rejects_local_extra_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plugin_copy = Path(directory) / "plugin"
            shutil.copytree(PLUGIN_ROOT, plugin_copy)
            (plugin_copy / ".DS_Store").write_bytes(b"synthetic local metadata")
            with self.assertRaisesRegex(ValueError, "release allowlist"):
                build_archive(Path(directory) / "contaminated.zip", plugin_root=plugin_copy)

    def test_directory_entry_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "directory.zip")
            with zipfile.ZipFile(archive, "a") as handle:
                handle.writestr("hidden/", b"")
            self.assert_archive_error(archive, "directory archive entry")
            self.assert_archive_error(archive, "exactly 12 canonical file entries")

    def test_archive_comment_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(Path(directory) / "comment.zip")
            with zipfile.ZipFile(archive, "a") as handle:
                handle.comment = b"synthetic comment"
            self.assert_archive_error(archive, "archive comment is not allowed")

    def test_entry_extra_metadata_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "entry-extra.zip"
            self.write_source_archive(
                archive,
                extra_metadata="skills/premilume-mode/SKILL.md",
            )
            self.assert_archive_error(archive, "archive entry extra metadata")


if __name__ == "__main__":
    unittest.main()
