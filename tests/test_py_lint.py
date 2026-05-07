"""Unit tests for src/scripts/linting/py_lint.py"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import src.scripts.linting.py_lint as py_lint


def _completed(stdout: str = "", returncode: int = 0) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=""
    )


class TestRepoRoot:
    """`repo_root()` shells out to `git rev-parse --show-toplevel`."""

    def test_returns_path_from_git(self):
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.return_value = _completed(stdout="/tmp/fake/repo\n")
            root = py_lint.repo_root()
        assert root == Path("/tmp/fake/repo")
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )

    def test_called_outside_git_repo_raises(self):
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=128, cmd="git"
            )
            with pytest.raises(RuntimeError):
                py_lint.repo_root()

    def test_git_not_installed_raises(self):
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.side_effect = FileNotFoundError("git")
            with pytest.raises(RuntimeError):
                py_lint.repo_root()


class TestFindPythonFiles:
    """`find_python_files()` returns absolute, deduplicated, sorted paths."""

    def test_combines_tracked_and_untracked(self, tmp_path):
        tracked_out = "src/foo.py\ntests/test_foo.py\n"
        untracked_out = "src/new_module.py\n"

        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.side_effect = [
                _completed(stdout=tracked_out),
                _completed(stdout=untracked_out),
            ]
            files = py_lint.find_python_files(tmp_path)

        assert files == sorted(
            [
                (tmp_path / "src" / "foo.py").resolve(),
                (tmp_path / "src" / "new_module.py").resolve(),
                (tmp_path / "tests" / "test_foo.py").resolve(),
            ]
        )

    def test_deduplicates_overlap(self, tmp_path):
        # If a file shows up in both lists (unlikely but possible), it
        # should appear once in the result.
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.side_effect = [
                _completed(stdout="src/foo.py\n"),
                _completed(stdout="src/foo.py\n"),
            ]
            files = py_lint.find_python_files(tmp_path)

        assert len(files) == 1
        assert files[0] == (tmp_path / "src" / "foo.py").resolve()

    def test_empty_repo_returns_empty_list(self, tmp_path):
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.side_effect = [_completed(stdout=""), _completed(stdout="")]
            files = py_lint.find_python_files(tmp_path)
        assert files == []

    def test_invokes_git_with_correct_filters(self, tmp_path):
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.side_effect = [_completed(stdout=""), _completed(stdout="")]
            py_lint.find_python_files(tmp_path)

        first_call = mock_run.call_args_list[0]
        second_call = mock_run.call_args_list[1]
        assert first_call.args[0] == ["git", "ls-files", "*.py"]
        assert second_call.args[0] == [
            "git",
            "ls-files",
            "--others",
            "--exclude-standard",
            "*.py",
        ]
        assert first_call.kwargs["cwd"] == tmp_path
        assert second_call.kwargs["cwd"] == tmp_path


class TestRunBlack:
    """`run_black()` shells out to the `black` CLI."""

    def test_no_files_skips_subprocess(self, capsys):
        with patch.object(py_lint.subprocess, "run") as mock_run:
            rc = py_lint.run_black([])
        assert rc == 0
        mock_run.assert_not_called()
        assert "No Python files" in capsys.readouterr().out

    def test_invokes_black_with_files(self):
        files = [Path("/repo/a.py"), Path("/repo/b.py")]
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            rc = py_lint.run_black(files)

        assert rc == 0
        # Compare against str(Path(...)) so the test passes on both POSIX
        # and Windows (which use different path separators).
        mock_run.assert_called_once_with(["black", str(files[0]), str(files[1])])

    def test_returns_black_exit_code(self):
        files = [Path("/repo/a.py")]
        with patch.object(py_lint.subprocess, "run") as mock_run:
            mock_run.return_value = MagicMock(returncode=123)
            rc = py_lint.run_black(files)
        assert rc == 123


class TestMain:
    """`main()` wires the helpers together."""

    def test_happy_path(self, tmp_path):
        files = [tmp_path / "x.py"]
        with (
            patch.object(py_lint, "repo_root", return_value=tmp_path) as mock_root,
            patch.object(py_lint, "find_python_files", return_value=files) as mock_find,
            patch.object(py_lint, "run_black", return_value=0) as mock_black,
        ):
            rc = py_lint.main()

        assert rc == 0
        mock_root.assert_called_once_with()
        mock_find.assert_called_once_with(tmp_path)
        mock_black.assert_called_once_with(files)

    def test_propagates_black_failure(self, tmp_path):
        with (
            patch.object(py_lint, "repo_root", return_value=tmp_path),
            patch.object(py_lint, "find_python_files", return_value=[]),
            patch.object(py_lint, "run_black", return_value=2),
        ):
            assert py_lint.main() == 2
