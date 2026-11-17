# Coding standard and GitHub workflow

Group-owned MicroPython code lives in `project/`. Put screen classes in `project/pages/` and API and data logic alongside `main.py`. Use snake_case for modules, functions and variables, PascalCase for classes, UPPER_CASE for constants and four spaces per indent. Keep hardware-independent calculations separate from screen code. Explain board-specific constraints near the relevant code. Keep host tests in `tests/` and project documentation in `docs/` so neither is flashed.

Preserve the supplied firmware, drivers, boot files, board definitions and PlatformIO packaging/configuration. In review, inspect the changed paths with `git diff --name-only origin/main...HEAD`. For final NF4 acceptance compare the supplied paths against the course original. Keep credentials only in ignored `project/secrets.py`.

## Format and test a change

Use Ruff 0.11.13 with its default Python formatting rules on team-owned Python files touched by the PR. Install it in a development environment on the computer with `python3 -m pip install ruff==0.11.13`. From the repository root, pass the changed Python paths explicitly, for example:

```sh
ruff format --check project/pages/departure_screen.py tests/test_departures.py
python3 -m unittest discover -s tests -v
pio run -e t4s3-micropython
```

If formatting fails, run the same Ruff command without `--check`, inspect the diff and rerun the check. PlatformIO Build packages the application; verify touch, the live service and persistence separately on a board.

## From issue to merge

1. Identify the GitHub issue, owner and acceptance criteria. Start a topic branch from current main (GitHub Desktop: Fetch origin, update main, then New Branch).
2. Commit the related app changes, tests and docs together. Publish the branch and open a PR to the group's main. Contributors with read access can use a fork.
3. Link the issue, explain the user-visible change, and record formatter and test results with the build identifier. Use the [peer-review checklist](acceptance.md#peer-review-checklist).
4. Have one teammate review. Address findings and repeat affected checks. Record physical tests as pending until a tester runs them.
5. Merge after review and passing applicable checks. Link remaining device work and update the issue and project board to reflect actual progress.

These are review rules proposed in this PR. Branch protection and CI enforcement require separate repository configuration.
