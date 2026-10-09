# Command guide

Run commands from the repository root. Python commands support both forms:

```bash
python scripts/data/prepare_dataset.py --help
python -m scripts.data.prepare_dataset --help
```

Use `--help` before running a pipeline. The former flat command paths have
been replaced by the folders below; filenames and command arguments are unchanged.

| Folder | Purpose |
| --- | --- |
| [data/](data/) | Download, prepare, sample, tokenize, and inspect datasets |
| [tokenizer/](tokenizer/) | Train, inspect, and compare tokenizers |
| [training/](training/) | Train, validate run manifests, run preflight and benchmarks |
| [inference/](inference/) | Generate text, native chat, and the chat bridge |
| [evaluation/](evaluation/) | Evaluate checkpoints, decoding, memory, and training data |
| [export/](export/) | Export native and LM Studio models |
| [monitoring/](monitoring/) | Training viewers, GPU monitoring, and progress summaries |
| [memory/](memory/) | Memory worker and saved conversation-memory summaries |
| [specialist/](specialist/) | Specialist pipeline and embedding-state inspection |

See the [workflow examples](../documentation/commands/WORKFLOWS.md) for complete
commands. Training launchers retain their progress-viewer integration.
This repository is retired; use the active workspace for new training.
