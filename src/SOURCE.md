The `src` directory contains reusable code to support notebook exploration & project reproducibility.

The `utils` directory replicates many of the custom functions originally used in our notebooks. The authors are credited, and docstrings are included with usage details.

> NOTE: As of 5/8/2026, we haven't incorporated the `src` code into our notebooks, but the plumbing is there and fully functional. To use code from `src`, follow the steps in `docs/DEVELOPER_SETUP.md` which includes example import usage into notebooks. After developer setup, you can also run the unit tests which confirm our custom functions work.

__Scripts__

- `julia/`  - scripts for unpacking raw NIST source data
- `linting` - scripts for static code analysis (formatting, import statements, etc.)
- NIST source data concatenation script
- NFI source data concatenation script (For reference only. Not to be reused.)

__EDA__

Functions to reproduce critical EDA data steps.

__Exceptions__

Custom exceptions.

__Utils__

Reusable functions to support reproducibility across the project, organized by usage.
