The `src` directory contains reusable code to support notebook exploration & project reproducibility.

The `utils` directory replicates many of the custom functions originally used in our notebooks. The authors are credited, and docstrings are included with usage details.

> As of 5/8/2026, we haven't incorporated the `src` code into our notebooks, but the plumbing is there and fully functional. 
To use code from `src`, complete steps 1 & 2 in [QuickStart](https://github.com/bkoconnell/datascience-capstone/blob/main/docs/QuickStart.md), *or* complete the [Developer Setup](https://github.com/bkoconnell/datascience-capstone/blob/main/docs/DEVELOPER_SETUP.md) walkthrough, which includes usage example to **import** `src` code into notebooks. After developer setup, you can also run the unit tests which confirm that our custom functions work.

__Scripts__

- `julia/`  - scripts for unpacking raw NIST source data
- `linting` - scripts for static code analysis (ruff formatting, import statement checks, etc.)
- NIST source data concatenation script
- NFI source data concatenation script (For reference only. Not to be reused.)

__EDA__

Functions to reproduce critical EDA data steps.

__Exceptions__

Custom exceptions.

__Utils__

Reusable functions to support reproducibility across the project, organized by usage.
