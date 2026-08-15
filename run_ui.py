from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


def main() -> int:
    root = Path(__file__).resolve().parent
    reports = root / os.getenv("ARTIFACTS_DIR", "reports")
    reports.mkdir(parents=True, exist_ok=True)
    return pytest.main(
        [
            str(root / "tests" / "ui"),
            "-m",
            "ui",
            f"--html={reports / 'ui-report.html'}",
            "--self-contained-html",
            f"--junitxml={reports / 'ui-junit.xml'}",
            *sys.argv[1:],
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
