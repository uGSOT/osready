from osready.checks.doc_checks import check_readme_exists


def test_passes_when_readme_exists(tmp_path):
    """Ensure repositories with documentation are accepted by the check."""
    (tmp_path / "README.md").write_text("# Test Repository")

    result = check_readme_exists(str(tmp_path))

    assert result.passed is True


def test_fails_when_readme_is_missing(tmp_path):
    """Ensure undocumented repositories are flagged for contributors."""
    result = check_readme_exists(str(tmp_path))

    assert result.passed is False
    assert "No README file found" in result.message