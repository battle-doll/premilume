#!/usr/bin/env python3
"""Regression tests for the strict static-SVG policy."""

from __future__ import annotations

import unittest

from validate_package import validate_svg_contents


class SvgValidationTests(unittest.TestCase):
    def validate(self, contents: str) -> list[str]:
        errors: list[str] = []
        validate_svg_contents(contents, "synthetic.svg", errors)
        return errors

    def test_minimal_static_svg_is_allowed(self) -> None:
        contents = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" role="img" '
            'aria-labelledby="title"><title id="title">Synthetic</title>'
            '<circle cx="5" cy="5" r="4" fill="#000000"/></svg>'
        )
        self.assertEqual(self.validate(contents), [])

    def test_style_import_is_rejected(self) -> None:
        contents = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            '<style>@import url(https://example.invalid/a.css);</style></svg>'
        )
        self.assertTrue(self.validate(contents))

    def test_style_attribute_url_is_rejected(self) -> None:
        contents = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            '<circle cx="5" cy="5" r="4" style="fill:url(https://example.invalid/a.svg)"/></svg>'
        )
        self.assertTrue(self.validate(contents))

    def test_css_escaped_url_in_paint_is_rejected(self) -> None:
        contents = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            r'<rect width="10" height="10" rx="1" fill="u\72l(https\3a//example.invalid/a.svg)"/>'
            '</svg>'
        )
        self.assertTrue(self.validate(contents))

    def test_smil_animation_is_rejected(self) -> None:
        contents = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            '<circle cx="5" cy="5" r="4" fill="#000000">'
            '<animate attributeName="r" values="1;4"/></circle></svg>'
        )
        self.assertTrue(self.validate(contents))

    def test_doctype_and_entity_are_rejected(self) -> None:
        contents = (
            '<!DOCTYPE svg [<!ENTITY payload "synthetic">]>'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            '<title>&payload;</title></svg>'
        )
        self.assertTrue(self.validate(contents))


if __name__ == "__main__":
    unittest.main()
