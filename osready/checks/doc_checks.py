"""
checks/doc_checks.py
----------------------
Checks that confirm a repository has the documentation files an
outside contributor expects to see.

Only the README check is implemented in v1. LICENSE and
CONTRIBUTING.md checks are left as good-first-issues — see
ISSUES.md — because they're nearly identical to this one, which
makes them a great first PR.
"""

import os

from osready.models import CheckResult

# We accept a few common spellings/casings for the README file.
README_NAMES = ["README.md", "README.rst", "README.txt", "readme.md"]

LICENSE_NAMES = ["LICENSE", "LICENSE.md", "LICENSE.txt"]


def check_readme_exists(repo_path: str) -> CheckResult:
    """
    Looks in the top level of the repo for any file matching one of
    the names in README_NAMES. Doesn't check the file's *content* —
    just whether it exists — because that's enough to unblock a
    student, and content-quality checking is a good "intermediate"
    follow-up issue.
    """
    for filename in README_NAMES:
        if os.path.isfile(os.path.join(repo_path, filename)):
            return CheckResult(
                name="README present",
                passed=True,
                message=f"Found {filename}.",
                severity="medium",
            )

    return CheckResult(
        name="README present",
        passed=False,
        message=(
            "No README file found. Contributors and maintainers expect a "
            "README.md that explains what the project does and how to run it."
        ),
        severity="medium",
    )


def check_license_exists(repo_path: str) -> CheckResult:
    """
    Looks in the top level of the repo for any file matching one of
    the names in LICENSE_NAMES. Doesn't check the file's content —
    just whether it exists.
    """
    for filename in LICENSE_NAMES:
        if os.path.isfile(os.path.join(repo_path, filename)):
            return CheckResult(
                name="LICENSE present",
                passed=True,
                message=f"Found {filename}.",
                severity="medium",
            )

    return CheckResult(
        name="LICENSE present",
        passed=False,
        message=(
            "No LICENSE file found. A license helps clarify how the "
            "project can be used, modified, and distributed."
        ),
        severity="medium",
    )


def check_contributing_exists(repo_path: str) -> CheckResult:
    """
    Checks whether CONTRIBUTING.md exists in the top level of the repo.
    """
    filename = "CONTRIBUTING.md"

    if os.path.isfile(os.path.join(repo_path, filename)):
        return CheckResult(
            name="CONTRIBUTING.md present",
            passed=True,
            message=f"Found {filename}.",
            severity="low",
        )

    return CheckResult(
        name="CONTRIBUTING.md present",
        passed=False,
        message=(
            "No CONTRIBUTING.md file found. Add one to explain how "
            "contributors can report issues and submit pull requests."
        ),
        severity="low",
    )


CHECKS = [
    check_readme_exists,
    check_license_exists,
    check_contributing_exists,
]
