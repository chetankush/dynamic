# Dynamo Log Report Task

This repository contains a repaired Terminal-Bench 2 Harbor task for parsing an
Apache-style access log into a JSON summary report.

## Task Files

- `instruction.md` describes the task and success criteria shown to the agent.
- `environment/Dockerfile` builds the pinned task image and includes only the
  runtime input plus verifier dependencies.
- `solution/solve.sh` runs the reference solution in `solution/solve.py`.
- `tests/test.sh` runs the pytest verifier and writes Harbor outputs.
- `tests/test_outputs.py` validates the report contents against `/app/access.log`.
- `task.toml` declares task metadata, environment limits, and the artifact path.

## Verification

The repaired task was calibrated locally with Harbor:

```bash
harbor run -p . --agent oracle
harbor run -p . --agent nop
```

Expected results:

- Oracle agent: reward `1.0`
- No-op agent: reward `0.0`
