"""
Author: Brendan OConnell
Date:   May 2026

Purpose:
    Execute a single Jupyter notebook end to end with `papermill` to verify
    it runs without errors. Reports status to stdout/stderr and writes a
    timestamped Markdown log under `.artifacts_ci/validation/`.

Local usage:
    Run from any working directory inside the repo. The repo root is
    resolved via `git rev-parse --show-toplevel`.

    Validate one notebook:
        python src/scripts/validation/nb_validate.py path/to/nb.ipynb

    Override the log output directory:
        set NB_VALIDATE_OUTPUT_DIR=C:\\tmp\\nb_logs
        python src/scripts/validation/nb_validate.py path/to/nb.ipynb

    Override the kernel name (defaults to `python3`):
        set NB_VALIDATE_KERNEL=mykernel
        python src/scripts/validation/nb_validate.py path/to/nb.ipynb

Exit code:
    0 if the notebook executes successfully, 1 if it fails.

Prerequisites:
    - `papermill`, `ipykernel` (see requirements.txt).
"""

import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import papermill as pm
from papermill.exceptions import PapermillExecutionError


DEFAULT_OUTPUT_DIR = Path(".artifacts_ci/validation")
OUTPUT_DIR_ENV = "NB_VALIDATE_OUTPUT_DIR"
KERNEL_ENV = "NB_VALIDATE_KERNEL"
DEFAULT_KERNEL = "python3"


def log(msg: str, stream=sys.stdout) -> None:
    """Print a timestamped message to the given stream."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=stream, flush=True)


def repo_root() -> Path:
    """Resolve the repo root via git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(
            "Could not determine repository root. nb_validate.py must be "
            "run inside a git repository with `git` available on PATH."
        ) from e
    return Path(result.stdout.strip())


def resolve_output_dir(root: Path) -> Path:
    """
    Return the log directory. Honors NB_VALIDATE_OUTPUT_DIR when set, but
    falls back to the default (with a warning) if the override cannot be
    created. The default itself is created if missing.
    """
    default_path = root / DEFAULT_OUTPUT_DIR
    override = os.environ.get(OUTPUT_DIR_ENV)
    if override:
        candidate = Path(override).expanduser()
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            log(f"Using override output dir from {OUTPUT_DIR_ENV}: {candidate}")
            return candidate
        except OSError as e:
            log(
                f"WARNING: could not create override output dir '{candidate}' "
                f"({type(e).__name__}: {e}). Falling back to default.",
                stream=sys.stderr,
            )
    default_path.mkdir(parents=True, exist_ok=True)
    log(f"Using default output dir: {default_path}")
    return default_path


def resolve_target(arg: str) -> Path:
    """Resolve the CLI notebook argument to an absolute path."""
    p = Path(arg)
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    if not p.exists():
        raise FileNotFoundError(f"Notebook not found: {arg}")
    return p


def execute_notebook(nb_path: Path, kernel_name: str, root: Path) -> dict:
    """
    Run one notebook with papermill. Returns a result dict with keys:
        path, status ('PASS' or 'FAIL'), duration, error,
        failed_cell (index, may be None), failed_ename (may be '').
    Sets cwd to the notebook's parent directory so relative paths inside
    the notebook resolve the same way they would in JupyterLab.
    Output notebook is written to a temp file and discarded.
    """
    rel = nb_path.relative_to(root) if nb_path.is_absolute() else nb_path
    log(f"start: {rel}")
    start = time.perf_counter()
    result = {
        "path": nb_path,
        "status": "PASS",
        "duration": 0.0,
        "error": "",
        "failed_cell": None,
        "failed_ename": "",
    }
    tmp = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)
    tmp.close()
    try:
        pm.execute_notebook(
            input_path=str(nb_path),
            output_path=tmp.name,
            kernel_name=kernel_name,
            cwd=str(nb_path.parent),
            progress_bar=False,
            log_output=False,
        )
    except PapermillExecutionError as e:
        result["status"] = "FAIL"
        result["failed_cell"] = e.cell_index
        result["failed_ename"] = e.ename
        tb = "".join(e.traceback) if e.traceback else ""
        result["error"] = (
            f"Cell {e.cell_index} raised {e.ename}: {e.evalue}\n{tb}"
        ).rstrip()
        log(
            f"caught PapermillExecutionError in {rel}: cell {e.cell_index}, "
            f"{e.ename}: {e.evalue}",
            stream=sys.stderr,
        )
    except Exception as e:
        result["status"] = "FAIL"
        result["failed_ename"] = type(e).__name__
        result["error"] = f"{type(e).__name__}: {e}"
        log(
            f"caught {type(e).__name__} in {rel}: {e}",
            stream=sys.stderr,
        )
    finally:
        Path(tmp.name).unlink(missing_ok=True)
        result["duration"] = time.perf_counter() - start
    marker = "PASS" if result["status"] == "PASS" else "FAIL"
    log(f"end:   {rel} [{marker}] {result['duration']:.2f}s")
    return result


def format_log(result: dict, root: Path, kernel_name: str, started_utc: str) -> str:
    """Build the Markdown log body for a single notebook result."""
    rel = result["path"].relative_to(root) if result["path"].is_absolute() else result["path"]
    lines = [
        "# Notebook validation report",
        "",
        f"- Notebook: `{rel}`",
        f"- Status: **{result['status']}**",
        f"- Duration: {result['duration']:.2f}s",
        f"- Started (UTC): {started_utc}",
        f"- Repo root: `{root}`",
        f"- Kernel: `{kernel_name}`",
        "- Notebook cwd: parent directory of the notebook",
    ]
    if result["status"] == "FAIL":
        cell = result["failed_cell"] if result["failed_cell"] is not None else "n/a"
        lines.append(f"- Failed cell index: {cell}")
        lines.append(f"- Exception type: `{result['failed_ename']}`")
    if result["error"]:
        lines.append("")
        lines.append("## Error detail")
        lines.append("")
        lines.append("```")
        lines.append(result["error"])
        lines.append("```")
    lines.append("")
    return "\n".join(lines)


def write_log(output_dir: Path, nb_path: Path, started_local: datetime, body: str) -> Path:
    """Write the Markdown log with a timestamp + notebook-name suffix."""
    stamp = started_local.strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"nb_validate_{nb_path.stem}_{stamp}.md"
    path.write_text(body, encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(
            "Usage: nb_validate.py <path/to/notebook.ipynb>",
            file=sys.stderr,
        )
        return 2

    log("nb_validate starting")
    root = repo_root()
    output_dir = resolve_output_dir(root)
    kernel_name = os.environ.get(KERNEL_ENV, DEFAULT_KERNEL)
    nb_path = resolve_target(argv[0])

    log(f"Target: {nb_path}. Kernel: '{kernel_name}'.")
    started_local = datetime.now()
    started_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    result = execute_notebook(nb_path, kernel_name, root)

    body = format_log(result, root, kernel_name, started_utc)
    log_path = write_log(output_dir, nb_path, started_local, body)
    log(f"Log written to {log_path}")

    if result["status"] == "FAIL":
        log("nb_validate finished with failure", stream=sys.stderr)
        return 1
    log("nb_validate finished successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
