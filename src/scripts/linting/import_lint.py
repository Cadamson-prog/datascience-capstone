"""
Author: Brendan OConnell
Year:   2026

Purpose:
    Lint check that every import statement in the repository's `.py` and
    `.ipynb` files appears at the top of the file, before any non-import
    code.

    What counts as "OK to appear before / among the imports":
        - A shebang line (e.g. `#!/usr/bin/env python`) on the first line
        - Comments and blank lines
        - A single module-level docstring (the very first statement)
        - Other import statements (`import x`, `from x import y`)
        - `try:` / `if:` blocks whose entire body is itself only imports
          (this covers the common compatibility shim and
          `if TYPE_CHECKING:` patterns)

    What counts as a violation:
        - Any non-import statement (assignment, function/class def,
          executable code, etc.) that appears before an `import` /
          `from ... import ...` statement at module scope.

    For `.ipynb` files:
        - Markdown cells are ignored entirely. Any number of markdown
          cells at the top, or interleaved between code cells, is fine.
        - Code cells are checked in order as if their bodies were
          concatenated: once a code cell contains non-import code, any
          import in that or a later code cell is a violation.

Local usage:
    From anywhere inside the repo:

        python src/scripts/linting/import_lint.py

    The script exits 0 when no violations are found, 1 otherwise. It
    prints each violation on its own line to stderr (prefixed by the
    repo-relative path and notebook cell index, for `.ipynb`) and ALSO
    writes a Markdown report to `.artifacts_ci/import_lint_report.md`
    grouped by file. The script does not auto-fix anything. The report
    is meant to be used as a punch list. The `.artifacts_ci/` directory
    is gitignored.

    NOTE: This script is intentionally NOT wired into `lint.sh` /
    `lint.bat`. Run it manually when you want to verify import-position
    hygiene. See `docs/linting.md` for the full walkthrough.
"""

import ast
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPORT_PATH = Path(".artifacts_ci") / "import_lint_report.md"


@dataclass(frozen=True)
class Violation:
    """A single late import. `cell` is None for `.py` files."""

    file: str
    cell: int | None
    line: int
    import_text: str
    first_loc: str

    def location(self) -> str:
        if self.cell is None:
            return f"{self.file} line {self.line}"
        return f"{self.file} cell {self.cell} line {self.line}"


@dataclass(frozen=True)
class ParseError:
    """A file or cell that could not be parsed. Reported alongside violations."""

    file: str
    cell: int | None
    line: int | None
    message: str

    def location(self) -> str:
        if self.cell is None:
            base = self.file
        else:
            base = f"{self.file} cell {self.cell}"
        if self.line is not None:
            base = f"{base} line {self.line}"
        return base


def repo_root() -> Path:
    """Return the absolute path to the repo root by asking git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(
            "Could not determine repository root. import_lint.py must be run "
            "inside a git repository with `git` available on PATH."
        ) from e
    return Path(result.stdout.strip())


def find_files(root: Path) -> tuple[list[Path], list[Path]]:
    """Return (py_files, ipynb_files) tracked or new (non-gitignored) under git."""

    def _ls(pattern: str) -> list[str]:
        tracked = subprocess.run(
            ["git", "ls-files", pattern],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", pattern],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return (tracked.stdout + untracked.stdout).splitlines()

    py = sorted({(root / r).resolve() for r in _ls("*.py") if r})
    ipynb = sorted({(root / r).resolve() for r in _ls("*.ipynb") if r})
    return list(py), list(ipynb)


def _is_module_docstring(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _is_import_only(node: ast.AST) -> bool:
    """True if `node` is an import or a wrapper whose body contains only imports.

    Handles compatibility shims and `if TYPE_CHECKING:` blocks:

        try:
            import cPickle as pickle
        except ImportError:
            import pickle

        if TYPE_CHECKING:
            from foo import Bar
    """
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return True
    if isinstance(node, ast.Try):
        return (
            all(_is_import_only(n) for n in node.body)
            and all(all(_is_import_only(n) for n in h.body) for h in node.handlers)
            and all(_is_import_only(n) for n in node.orelse)
            and all(_is_import_only(n) for n in node.finalbody)
        )
    if isinstance(node, ast.If):
        return all(_is_import_only(n) for n in node.body) and all(
            _is_import_only(n) for n in node.orelse
        )
    return False


def _strip_ipython_lines(src: str) -> str:
    """Replace IPython magic / shell-escape lines with a no-op so `ast.parse`
    can succeed without changing the line count (so reported line numbers still
    point at the original cell)."""
    out = []
    for line in src.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith(("%", "!", "?")):
            out.append("_ = None  # ipython magic")
        else:
            out.append(line)
    return "\n".join(out)


def _unparse_import(node: ast.AST) -> str:
    """Return a one-line, source-like rendering of an import node."""
    try:
        return ast.unparse(node).strip().splitlines()[0]
    except Exception:
        return "<import>"


def _check_stmts(
    body: list[ast.stmt],
    file: str,
    cell: int | None,
    seen_non_import: bool,
    first_loc: str | None,
    *,
    allow_docstring: bool,
) -> tuple[list[Violation], bool, str | None]:
    """Walk a module/cell body and report any import that appears after
    non-import code.

    Returns (violations, updated seen_non_import, updated first_loc).
    """
    violations: list[Violation] = []
    for i, node in enumerate(body):
        if i == 0 and allow_docstring and _is_module_docstring(node):
            continue
        if _is_import_only(node):
            if seen_non_import:
                assert first_loc is not None
                violations.append(
                    Violation(
                        file=file,
                        cell=cell,
                        line=node.lineno,
                        import_text=_unparse_import(node),
                        first_loc=first_loc,
                    )
                )
        elif not seen_non_import:
            seen_non_import = True
            label = file if cell is None else f"{file} cell {cell}"
            first_loc = f"{label} line {node.lineno}"
    return violations, seen_non_import, first_loc


def check_python_file(
    path: Path, root: Path
) -> tuple[list[Violation], list[ParseError]]:
    rel = path.relative_to(root).as_posix()
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [], [ParseError(file=rel, cell=None, line=e.lineno, message=e.msg)]
    violations, _, _ = _check_stmts(
        tree.body,
        file=rel,
        cell=None,
        seen_non_import=False,
        first_loc=None,
        allow_docstring=True,
    )
    return violations, []


def check_notebook_file(
    path: Path, root: Path
) -> tuple[list[Violation], list[ParseError]]:
    rel = path.relative_to(root).as_posix()
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [], [ParseError(file=rel, cell=None, line=None, message=str(e))]

    violations: list[Violation] = []
    errors: list[ParseError] = []
    seen_non_import = False
    first_loc: str | None = None
    code_cell_idx = 0

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        clean = _strip_ipython_lines(source)
        try:
            tree = ast.parse(clean)
        except SyntaxError as e:
            errors.append(
                ParseError(file=rel, cell=code_cell_idx, line=e.lineno, message=e.msg)
            )
            code_cell_idx += 1
            continue

        v, seen_non_import, first_loc = _check_stmts(
            tree.body,
            file=rel,
            cell=code_cell_idx,
            seen_non_import=seen_non_import,
            first_loc=first_loc,
            allow_docstring=(code_cell_idx == 0 and not seen_non_import),
        )
        violations.extend(v)
        code_cell_idx += 1

    return violations, errors


def _format_report(
    py_count: int,
    ipynb_count: int,
    violations: list[Violation],
    errors: list[ParseError],
) -> str:
    """Render a Markdown report grouped by file."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = []
    lines.append("# Import-Position Lint Report")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append(f"Files checked: {py_count} .py, {ipynb_count} .ipynb")
    by_file: dict[str, list[Violation]] = {}
    for v in violations:
        by_file.setdefault(v.file, []).append(v)
    lines.append(
        f"Violations: {len(violations)} across {len(by_file)} file(s)"
    )
    if errors:
        lines.append(f"Parse errors: {len(errors)}")
    lines.append("")

    if not violations and not errors:
        lines.append("OK: no import-position violations found.")
        lines.append("")
        return "\n".join(lines)

    if violations:
        for file in sorted(by_file):
            file_vs = by_file[file]
            lines.append(f"## {file}")
            lines.append("")
            lines.append(f"First non-import code at: {file_vs[0].first_loc}")
            lines.append("")
            lines.append(f"Offending imports ({len(file_vs)}):")
            lines.append("")
            for v in file_vs:
                lines.append(f"- {v.location()}: `{v.import_text}`")
            lines.append("")

    if errors:
        lines.append("## Parse errors")
        lines.append("")
        lines.append(
            "These files/cells could not be parsed and were skipped. "
            "They do not count as violations but should be investigated."
        )
        lines.append("")
        for e in errors:
            lines.append(f"- {e.location()}: {e.message}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    root = repo_root()
    py_files, ipynb_files = find_files(root)
    print(
        f"Checking {len(py_files)} .py file(s) and "
        f"{len(ipynb_files)} .ipynb file(s) for import-position violations..."
    )

    violations: list[Violation] = []
    errors: list[ParseError] = []
    for p in py_files:
        v, e = check_python_file(p, root)
        violations.extend(v)
        errors.extend(e)
    for p in ipynb_files:
        v, e = check_notebook_file(p, root)
        violations.extend(v)
        errors.extend(e)

    report = _format_report(len(py_files), len(ipynb_files), violations, errors)
    report_path = root / REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    rel_report = report_path.relative_to(root).as_posix()

    if not violations and not errors:
        print("OK: no import-position violations found.")
        print(f"Report written to {rel_report}")
        return 0

    print(
        f"\nFound {len(violations)} violation(s)"
        + (f" and {len(errors)} parse error(s)" if errors else "")
        + ":",
        file=sys.stderr,
    )
    for v in violations:
        print(f"  {v.location()}: {v.import_text}", file=sys.stderr)
    for e in errors:
        print(f"  {e.location()}: parse error: {e.message}", file=sys.stderr)
    print(f"\nFull report written to {rel_report}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
