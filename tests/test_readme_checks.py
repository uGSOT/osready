#Atanu's code for testing the README check function
import pytest

from osready.checks.doc_checks import README_NAMES, check_readme_exists


@pytest.mark.parametrize("filename", README_NAMES)
def test_check_readme_exists_passes_with_readme(tmp_path, filename):
    (tmp_path / filename).write_text("# Test project\n")

    result = check_readme_exists(str(tmp_path))

    assert result.passed is True
    assert result.name == "README present"
    assert result.message.lower() == f"found {filename}.".lower()
    assert result.severity == "medium"


def test_check_readme_exists_fails_without_readme(tmp_path):
    result = check_readme_exists(str(tmp_path))

    assert result.passed is False
    assert result.name == "README present"
    assert "No README file found" in result.message
    assert result.severity == "medium"