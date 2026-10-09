# Retained workflow commands

These instructions describe the retained source repository. For current development,
use the active workspace linked from the [repository overview](../../README.md).


Codexa v1 is a from-scratch decoder-only Transformer base-model project built
with typed Python and PyTorch. The active target is the 921,773,568-parameter
configuration in `configs/models/1b.yaml`, with an 8,192-token vocabulary and a
2,048-token context window on one RTX 4080.

This repository currently covers base pretraining: licensed general and
encyclopedic corpus download, FineWeb-Edu preparation, BPE tokenization,
memory-mapped causal-LM data, mixed-precision training, atomic checkpoints,
text completion, and fixed-prompt evaluation. Existing conversational corpora
are downloaded separately and retain their role structure for later SFT.

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
```

Use every script's `--help` before running it. Generated datasets, token data,
logs, and checkpoints are intentionally ignored by Git.

## Training data

The base corpus combines pinned FineWeb-Edu general/educational text with a
pinned English Wikipedia snapshot. Ten FineWeb-Edu `sample-10BT` shards and
the complete `20231101.en` Wikipedia snapshot are the first downloaded source
set. The currently prepared/tokenized artifact still contains only one
FineWeb-Edu shard and 883,814,184 training tokens; regenerate it after the
multi-source preparation path is complete.

Download additional pinned shards:

```bash
.venv/bin/python -m scripts.data.download_fineweb_edu --help
.venv/bin/python -m scripts.data.download_language_corpora --help
```

Prepare them deterministically:

```bash
.venv/bin/python -m scripts.data.prepare_fineweb_edu --help
```

UltraChat 200k and OASST1 are downloaded as later conversational training
sources. They must not be flattened into the base token stream or treated as
Wikipedia/general knowledge. See `documentation/reference/DATASET.md` for
revisions, roles, licenses, and the retained artifact's checksums.

## Tokenizer and token data

```bash
.venv/bin/python -m scripts.tokenizer.train_tokenizer --help
.venv/bin/python -m scripts.data.tokenize_dataset --help
.venv/bin/python -m scripts.tokenizer.inspect_tokenizer --help
.venv/bin/python -m scripts.data.inspect_token_data --help
```

The tokenizer candidates use byte-level BPE. IDs 0–3 are `<pad>`, `<bos>`,
`<eos>`, and `<unk>`; IDs 4–7 reserve future system, user, assistant, and end
control tokens. The production vocabulary is selected only after the checked-in
8K-versus-16K bake-off.

## Validate before a long run

```bash
.venv/bin/python -m scripts.training.run_tiny_overfit --help
.venv/bin/python -m scripts.training.preflight_full_run --help
.venv/bin/python -m scripts.training.benchmark_production_shape --help
```

The long run must start from random weights in a new output directory. Resume
is allowed only after that run has produced its own trusted checkpoint.

## Production command shape — currently blocked

```bash
.venv/bin/python -m scripts.training.train \
  --config configs/models/1b.yaml \
  --train-token-file data/tokenized/base-v1/train.bin \
  --validation-token-file data/tokenized/base-v1/validation.bin \
  --token-manifest data/tokenized/base-v1/token_data_manifest.json \
  --device cuda \
  --precision bf16 \
  --gradient-checkpointing \
  --optimizer adamw8bit \
  --run-name codexa-1b-base-rebuild
```

Do not execute this shape yet. The tokenizer bake-off, full cross-source
preparation, mixture decision, token budget, full-context smoke, throughput
benchmark, and frozen thresholds are still gates. The retained one-shard stream
is pipeline evidence only.

## Generate and evaluate

```bash
.venv/bin/python -m scripts.inference.generate \
  --checkpoint checkpoints/codexa-1b-base-rebuild/best.pt \
  --tokenizer checkpoints/tokenizer-fineweb-edu/tokenizer.json \
  --prompt "The purpose of education is" \
  --device cuda \
  --greedy

.venv/bin/python -m scripts.evaluation.evaluate_checkpoint \
  --checkpoint checkpoints/codexa-1b-base-rebuild/best.pt \
  --tokenizer checkpoints/tokenizer-fineweb-edu/tokenizer.json \
  --validation-token-file data/tokenized/fineweb-edu-1b-v1/validation.bin \
  --token-manifest data/tokenized/fineweb-edu-1b-v1/token_data_manifest.json \
  --output logs/codexa-1b-base-rebuild/evaluation.json \
  --device cuda
```

The base checkpoint is accepted only when fixed unseen prompts produce
coherent continuations without systemic repetition or collapse. Assistant and
multi-turn training are separate future work after that gate passes.

The active execution checklist is
`documentation/planning/PHASE_PLAN.md`. For a plain-language explanation of
what each dataset teaches and why base training and chat fine-tuning are
separate, read `documentation/planning/TRAINING_DATA_PLAN.md`.


## Optional conversational memory

Stage 2 adds opt-in local EmbeddingGemma semantic memory to native Codexa chat, while preserving the independent programming classifier and generative pipeline. See [commands and limitations](../reference/CONVERSATIONAL_MEMORY.md), [encoder-conditioning research](../reference/ENCODER_CONDITIONING.md), and [measured Stage 2 results](../training/STAGE2_RESULTS.md).
