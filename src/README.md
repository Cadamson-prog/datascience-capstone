The `src` directory contains reusable code to support notebook exploration & project reproducibility.

To use code from `src`, follow the steps in `docs/DEVELOPER_SETUP.md`

__Scripts__

- `julia/` - scripts for unpacking raw NIST source data
- NIST source data concatenation script
- NFI source data concatenation script (For reference only. Not to be reused.)

__EDA__

Functions to reproduce critical EDA data steps.

__Exceptions__

Custom exceptions.

__Utils__

Common reusable helpers across the project, organized by topic.

- `utils/fileops.py` - file operations (e.g. locating and loading project data files)
