"""
checks/git_checks.py
---------------------
All checks related to Git configuration and repository state live here.

HOW TO ADD A NEW CHECK (read this before opening a "good first issue" PR):
1. Write a new function. It must:
     - accept one argument: repo_path (a string, the folder to check)
     - return a single CheckResult (import it from osready.models)
2. Add your function to the CHECKS list at the bottom of this file.
That's it. You do NOT need to touch the CLI, the scorer, or the report
printer — they automatically pick up anything you add to CHECKS.

Right now this file only has ONE check implemented on purpose. See
ISSUES.md in the project root for the other Git checks that are open
for contribution (uncommitted changes, remote origin, not-on-main, etc).
"""

import subprocess

from osready.models import CheckResult


def check_git_identity(repo_path: str) -> CheckResult:
    """
    Confirms that `git config user.name` and `git config user.email`
    are both set. Without these, a student's commits are attributed to
    "unknown" and most projects will reject the PR outright.

    We just shell out to `git config` and read what it prints back.
    If it prints nothing, that value isn't set.
    """
    name = _read_git_config(repo_path, "user.name")
    email = _read_git_config(repo_path, "user.email")

    if name and email:
        return CheckResult(
            name="Git identity configured",
            passed=True,
            message=f"Commits will be attributed to {name} <{email}>.",
            severity="high",
        )

    missing = []
    if not name:
        missing.append("user.name")
    if not email:
        missing.append("user.email")

    return CheckResult(
        name="Git identity configured",
        passed=False,
        message=(
            "Missing Git config: "
            + ", ".join(missing)
            + ". Fix with: git config --global user.name \"Your Name\" "
            "and git config --global user.email you@example.com"
        ),
        severity="high",
    )


def _read_git_config(repo_path: str, key: str) -> str:
    """
    Small helper that runs `git config <key>` inside repo_path and
    returns whatever it printed, with whitespace trimmed off.

    We wrap this in try/except because `git config` exits with a
    non-zero status (and subprocess raises an error) when the key
    simply isn't set — that's a normal, expected outcome here, not a
    real error.
    """
    try:
        result = subprocess.run(
            ["git", "config", key],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def check_remote_origin_exists(repo_path: str) -> CheckResult:
    """
    Checks whether the repository has any configured Git remotes
    by running `git remote -v`.
    """
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.stdout.strip():
            return CheckResult(
                name="Git remote configured",
                passed=True,
                message="Found configured Git remote(s).",
                severity="medium",
            )

    except OSError:
        pass

    return CheckResult(
        name="Git remote configured",
        passed=False,
        message=(
            "No Git remotes found. Add a remote using "
            "git remote add origin <repository-url>."
        ),
        severity="medium",
    )

# Every check function in this file must be listed here.
# The rest of the app loops over this list — it never calls
# check_git_identity() by name directly.
CHECKS = [
    check_git_identity,
    check_remote_origin_exists
]
