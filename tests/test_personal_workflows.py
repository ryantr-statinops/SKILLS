"""Consumer-style routing matrix for personal workflows."""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from discover_skills import discover  # noqa: E402


def args_for(query: str):
    return type(
        "Args",
        (),
        {
            "query": query.split(),
            "category": None,
            "scope": None,
            "status": None,
            "invocation": None,
            "bundle": None,
            "limit": 10,
        },
    )()


class PersonalWorkflowMatrixTests(unittest.TestCase):
    def test_representative_and_boundary_queries_route_as_expected(self) -> None:
        matrix = json.loads(
            (ROOT / "tests/fixtures/personal-workflow-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        for case in matrix:
            representative = discover(args_for(case["representative_query"]))
            boundary = discover(args_for(case["boundary_query"]))
            self.assertTrue(representative, case["name"])
            self.assertTrue(boundary, case["name"])
            self.assertEqual(representative[0]["id"], case["expected_skill"], case["name"])
            self.assertEqual(boundary[0]["id"], case["boundary_skill"], case["name"])

    def test_matrix_skills_have_evaluation_cases(self) -> None:
        matrix = json.loads(
            (ROOT / "tests/fixtures/personal-workflow-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        for case in matrix:
            for identifier in (case["expected_skill"], case["boundary_skill"]):
                self.assertTrue(
                    (ROOT / identifier / "examples/evaluation.md").is_file(), identifier
                )


if __name__ == "__main__":
    unittest.main()
