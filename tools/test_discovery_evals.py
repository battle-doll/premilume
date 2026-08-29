from __future__ import annotations

import copy
import json
import unittest

from validate_package import REPO_ROOT, validate_discovery_evals


class DiscoveryEvalTests(unittest.TestCase):
    def load_payload(self) -> dict[str, object]:
        path = REPO_ROOT / "evals" / "discovery-cases.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_checked_in_discovery_set_matches_contract(self) -> None:
        errors: list[str] = []
        validate_discovery_evals(self.load_payload(), errors)
        self.assertEqual(errors, [])

    def test_wrong_count_and_selection_are_rejected(self) -> None:
        payload = copy.deepcopy(self.load_payload())
        payload["direct"].pop()
        payload["negative"][0]["expected_selection"] = "select"
        errors: list[str] = []
        validate_discovery_evals(payload, errors)
        self.assertTrue(any("exactly 10 direct" in error for error in errors))
        self.assertTrue(any("wrong expected_selection" in error for error in errors))

    def test_non_object_payload_is_rejected(self) -> None:
        errors: list[str] = []
        validate_discovery_evals([], errors)
        self.assertIn("discovery eval payload must be an object", errors)


if __name__ == "__main__":
    unittest.main()
