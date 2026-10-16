"""
tests/test_git_checks.py
---------------------------
An example test, kept deliberately small. Copy this pattern when you
add a test for your own check: create a tiny temp repo with tmp_path
(a built-in pytest fixture), run your check against it, and assert on
the CheckResult it returns.
"""

import subprocess

from osready.checks.git_checks import check_git_identity


def _init_repo(path, set_identity=True):
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    if set_identity:
        subprocess.run(
            ["git", "config", "user.name", "Test Student"], cwd=path, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "student@example.com"], cwd=path, check=True
        )


def test_passes_when_identity_is_set(tmp_path):
    _init_repo(tmp_path, set_identity=True)

    result = check_git_identity(str(tmp_path))

    assert result.passed is True


def test_fails_when_identity_is_missing(tmp_path):
    _init_repo(tmp_path, set_identity=False)

    result = check_git_identity(str(tmp_path))

    assert result.passed is False
    assert "user.name" in result.message or "user.email" in result.message



#idjvahvjfjajaljfajdf