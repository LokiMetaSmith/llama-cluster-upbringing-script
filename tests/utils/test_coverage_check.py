import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from pipecatapp.utils.coverage_check import check_docs_index, CheckResult

def test_check_docs_index_paths_found_all_exist():
    # Setup mock behavior
    repo_root = Path("/fake/repo")
    skill_path = Path("/fake/repo/skill.md")
    paths = ["docs/page1.md", "docs/page2.md"]

    with patch("pipecatapp.utils.coverage_check.extract_docs_index_paths") as mock_extract:
        mock_extract.return_value = paths

        with patch.object(Path, "exists") as mock_exists:
            # We want exists() to return True for both missing files
            mock_exists.return_value = True

            result = check_docs_index(repo_root, skill_path)

            assert result.passed is True
            assert result.name == "Docs index file paths"
            assert result.details[0] == "Index entries: 2, missing files: 0"
            mock_extract.assert_called_once_with(skill_path)

def test_check_docs_index_paths_found_some_missing():
    # Setup mock behavior
    repo_root = Path("/fake/repo")
    skill_path = Path("/fake/repo/skill.md")
    paths = ["docs/page1.md", "docs/page2.md"]

    with patch("pipecatapp.utils.coverage_check.extract_docs_index_paths") as mock_extract:
        mock_extract.return_value = paths

        with patch.object(Path, "exists") as mock_exists:
            # Since it's called twice for the files in the list
            mock_exists.side_effect = [True, False]

            result = check_docs_index(repo_root, skill_path)

            assert result.passed is False
            assert result.name == "Docs index file paths"
            assert result.details[0] == "Index entries: 2, missing files: 1"
            assert "  MISSING FILE: docs/page2.md" in result.details
            mock_extract.assert_called_once_with(skill_path)

def test_check_docs_index_no_paths_mkdocs_exists():
    repo_root = Path("/fake/repo")
    skill_path = Path("/fake/repo/skill.md")

    with patch("pipecatapp.utils.coverage_check.extract_docs_index_paths") as mock_extract:
        mock_extract.return_value = []

        with patch.object(Path, "exists") as mock_exists:
            # For the mkdocs check
            mock_exists.return_value = True

            result = check_docs_index(repo_root, skill_path)

            assert result.passed is False
            assert result.name == "Docs index"
            assert result.details == ["mkdocs.yml found but no docs index in skill"]
            # verify it checked mkdocs
            mock_exists.assert_called()

def test_check_docs_index_no_paths_no_mkdocs():
    repo_root = Path("/fake/repo")
    skill_path = Path("/fake/repo/skill.md")

    with patch("pipecatapp.utils.coverage_check.extract_docs_index_paths") as mock_extract:
        mock_extract.return_value = []

        with patch.object(Path, "exists") as mock_exists:
            # For the mkdocs check
            mock_exists.return_value = False

            result = check_docs_index(repo_root, skill_path)

            assert result.passed is True
            assert result.name == "Docs index"
            assert result.details == ["No mkdocs.yml, docs index skipped"]
            # verify it checked mkdocs
            mock_exists.assert_called()
