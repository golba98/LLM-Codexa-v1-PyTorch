# Codexa v1 — retained PyTorch source

This repository is retained for review and recovery. Current development lives
in [37-LLM From Scratch (PyTorch Codexa v1)](../37-LLM%20From%20Scratch%20%28PyTorch%20Codexa%20v1%29).
See the [retirement and recovery notice](documentation/reference/RETIREMENT_PENDING.md).

## Folder guide

| Folder | Contents |
| --- | --- |
| `src/` | Reusable model, data, training, inference, memory, and specialist code |
| `scripts/` | Commands grouped by purpose; see the [command guide](scripts/README.md) |
| `configs/` | Model, run, data, evaluation, testing, and specialist settings |
| `tests/` | Regression tests and small fixtures |
| `schemas/` | Dataset and run-report schemas |
| `requirements/` | Development and specialist dependencies; base dependencies remain in `requirements.txt` |
| `documentation/` | Reference material, planning, command examples, and linked training records |
| `data/`, `checkpoints/`, `logs/`, `exports/` | Local generated artifacts, excluded from Git |

## Documentation

- [Workflow commands and setup](documentation/commands/WORKFLOWS.md)
- [Architecture](documentation/reference/ARCHITECTURE.md) and [model card](documentation/reference/MODEL_CARD.md)
- [Dataset](documentation/reference/DATASET.md) and [tokenizer](documentation/reference/TOKENIZER.md)
- [Training plan](documentation/planning/PHASE_PLAN.md)
- [Native chat and memory](documentation/reference/CONVERSATIONAL_MEMORY.md)
- [Specialist pipeline](documentation/reference/SPECIALIST.md)
- [Training viewer](documentation/commands/TRAINING_VIEWER.md)
- [Session decisions](documentation/training/SESSION_DECISIONS.md) and [progress](documentation/training/100M_PROGRESS_LOG.md)
