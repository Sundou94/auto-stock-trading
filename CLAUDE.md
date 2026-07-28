# CLAUDE.md

This file gives Claude Code (and other AI assistants) the context needed to work in this repository.

## Overview

Auto Stock Trading is an AI-driven stock trading app. Per the README, the project starts from a "recursive daily algorithm improvement" idea: the intent is a system that runs once per day and iteratively improves its own trading algorithm/idea over time.

**Current state: this repository is a bare scaffold.** As of now it contains only `README.md` — no source code, package manifest, build system, tests, or CI has been added yet. There is nothing to "run" or "test" yet.

## Repository Structure

```
├── README.md    Project pitch (Korean): AI-based stock trading app, daily recursive algorithm improvement
└── CLAUDE.md    This file
```

## Development Workflow

None established yet — no language/runtime, package manager, linter, or test framework has been chosen. When code is first added to this repo:

- Establish the language/stack choice explicitly (and record it here) before scaffolding — don't assume Python/Node without confirming with the user, since none is committed to yet.
- Set up a minimal project layout (source dir, dependency manifest, a way to run and a way to test) as the first commit, and update this CLAUDE.md's Repository Structure and Development Workflow sections to match.
- Given the "1일 1회 알고리즘 개선" (once-daily algorithm improvement) concept from the README, expect the eventual design to include: a scheduled/cron-driven job runner, a component that evaluates trading performance, and a component that proposes/applies algorithm changes based on that evaluation — keep these concerns separated as the codebase grows.

## Conventions

- README and project framing are in Korean; match this for user-facing docs unless told otherwise.
- No conventions beyond this exist yet. As soon as real code lands, this file should be updated with actual module boundaries, run/test commands, and coding conventions — don't let it go stale.
