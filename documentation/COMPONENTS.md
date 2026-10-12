# Codexa component catalog

Codexa is developed as eight independently versioned repositories. This
showcase pins each one as a Git submodule under `components/`. The pinned
commits below are the `main` branch heads verified on 2026-10-12; they change
only when a showcase pull request deliberately moves them (see
[working with submodules](SUBMODULES.md)).

Each component's own README is the authoritative technical documentation for
its package; this catalog summarizes and links to it rather than copying it.

| Component | Submodule path | Pinned commit | Depends on |
| --- | --- | --- | --- |
| [LLM-From-Scratch](#llm-from-scratch) | `components/LLM-From-Scratch` | [`b980ea7`][fs-pin] | Architecture, Tokenizer, Data, Training, Inference, Memory; Specialist optional |
| [LLM-Architecture](#llm-architecture) | `components/LLM-Architecture` | [`57a0b46`][arch-pin] | — |
| [LLM-Tokenizer](#llm-tokenizer) | `components/LLM-Tokenizer` | [`2828b94`][tok-pin] | — |
| [LLM-Data](#llm-data) | `components/LLM-Data` | [`dd7cd64`][data-pin] | Tokenizer |
| [LLM-Training](#llm-training) | `components/LLM-Training` | [`c107367`][train-pin] | Architecture, Tokenizer, Data |
| [LLM-Inference](#llm-inference) | `components/LLM-Inference` | [`75e58e8`][inf-pin] | Architecture, Tokenizer; Memory optional |
| [LLM-Memory](#llm-memory) | `components/LLM-Memory` | [`be14176`][mem-pin] | — (talks to a Specialist worker out of process) |
| [LLM-Specialist](#llm-specialist) | `components/LLM-Specialist` | [`af076f0`][spec-pin] | — |

Dependencies are taken from each package's `pyproject.toml`. All component
packages are version 0.1.0, require Python 3.11 or newer, are MIT licensed and
are not published to PyPI.

## LLM-From-Scratch

- **Repository:** https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1
- **Purpose:** the integration repository (`codexa-workspace`). It owns
  orchestration and operator workflows, evaluation and research tooling, recipes,
  configs and schemas, central tests, the model card and the training records.
  `run.py` launches tests and commands across the sibling repositories.
- **Relationships:** depends on every generative component and optionally on
  Specialist. Its `compatibility.json` records the exact component commits it
  was tested with. No component imports it.
- **Documentation:** [README][fs-readme], [model card][fs-model-card],
  [validation][fs-validation], [sibling layout][fs-sibling],
  [environments][fs-environments], [training records][fs-training].
- **Note:** newer integration work (conversational SFT preparation, training
  supervision and diagnostics) is under review in that repository and is not
  part of this pin.

## LLM-Architecture

- **Repository:** https://github.com/golba98/LLM-Architecture-PyTorch-Codexa-v1
- **Purpose:** the decoder-only Transformer — embeddings, learned or RoPE
  positions, causal scaled-dot-product attention, RMSNorm, SwiGLU, KV caches —
  plus native checkpoint readers. Labels arrive already shifted from Data.
- **Relationships:** a leaf package (depends only on PyTorch). Used by Training,
  Inference and the integration repository.
- **Entry points:** imported as a library.
- **Documentation:** [README][arch-readme], [provenance][arch-provenance].

## LLM-Tokenizer

- **Repository:** https://github.com/golba98/LLM-Tokenizer-PyTorch-Codexa-v1
- **Purpose:** byte-level BPE training and inspection, and the shared
  role/END conversation serialization. Reserved token IDs 0–7 are fixed.
- **Relationships:** a leaf package (depends only on Hugging Face
  `tokenizers`). Used by Data, Training, Inference and the integration
  repository. It does not clean corpora.
- **Entry points:** `python -m llm_tokenizer.cli.train_tokenizer`,
  `python -m llm_tokenizer.cli.inspect_tokenizer`.
- **Documentation:** [README][tok-readme], [provenance][tok-provenance].

## LLM-Data

- **Repository:** https://github.com/golba98/LLM-Data-PyTorch-Codexa-v1
- **Purpose:** reproducible corpus preparation — cleaning, provenance, exact
  duplicate removal, stable splits, source mixtures — and binary token packing
  with memory-mapped datasets. Includes FineWeb-Edu download/preparation and
  conversational SFT preparation commands.
- **Relationships:** depends on Tokenizer; PyTorch, Parquet and Hugging Face Hub
  support are optional extras. Used by Training and the integration repository.
- **Entry points:** `python -m llm_data.cli.prepare_dataset`,
  `python -m llm_data.cli.tokenize_dataset`,
  `python -m llm_data.cli.inspect_token_data` and more (see README).
- **Documentation:** [README][data-readme], [provenance][data-provenance].

## LLM-Training

- **Repository:** https://github.com/golba98/LLM-Training-PyTorch-Codexa-v1
- **Purpose:** base and conversational training — optimizers, precision-aware
  loops, logging, combined YAML configuration, recoverable checkpoint writing
  and resume, and GPU monitoring.
- **Relationships:** depends on Architecture, Tokenizer and Data (with its
  PyTorch extra); 8-bit optimizers come from the optional `cuda` extra. Used by
  the integration repository, which keeps cross-component orchestration.
- **Entry points:** `python -m llm_training.cli.train`,
  `python -m llm_training.cli.train_conversational_sft`,
  `python -m llm_training.cli.monitor_gpu` and more (see README).
- **Documentation:** [README][train-readme], [provenance][train-provenance].

## LLM-Inference

- **Repository:** https://github.com/golba98/LLM-Inference-PyTorch-Codexa-v1
- **Purpose:** native generation and stopping, chat history, the native chat
  bridge protocol, retrieval-to-prompt composition and exports. GPT-2/Llama
  export adapters are experimental; native export preserves fidelity.
- **Relationships:** depends on Architecture and Tokenizer; Memory is an
  optional extra and plain inference needs neither Memory nor Specialist. Used
  by the integration repository.
- **Entry points:** `python -m llm_inference.cli.generate`,
  `python -m llm_inference.cli.chat_native` and more (see README).
- **Documentation:** [README][inf-readme], [provenance][inf-provenance].

## LLM-Memory

- **Repository:** https://github.com/golba98/LLM-Memory-PyTorch-Codexa-v1
- **Purpose:** scoped SQLite conversation storage — immutable turns,
  user/conversation scopes, normalized 768-dimensional vectors, exact cosine
  ranking, deletion, caching and worker fallback. Exact search targets small
  local stores.
- **Relationships:** depends only on NumPy. Obtains embeddings from a
  separately launched Specialist worker over JSON lines (no Python import). Used
  optionally by Inference and by the integration repository.
- **Entry points:** imported as a library.
- **Documentation:** [README][mem-readme], [provenance][mem-provenance].

## LLM-Specialist

- **Repository:** https://github.com/golba98/LLM-Specialist-PyTorch-Codexa-v1
- **Purpose:** the pretrained EmbeddingGemma adapter (frozen; not trained from
  scratch), a frozen embedding cache, linear/MLP classifiers, and the memory
  worker process.
- **Relationships:** independent of the other components. It must live in its
  own environment because its Transformers/tokenizers pins differ from the
  generative stack. Serves Memory through its worker command; optional for the
  integration repository.
- **Entry points:** `python -m llm_specialist.cli.specialist`,
  `python -m llm_specialist.cli.memory_worker`,
  `python -m llm_specialist.cli.probe_embedding_states`.
- **Documentation:** [README][spec-readme], [provenance][spec-provenance].

[fs-pin]: https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1/tree/b980ea7b477ae3f7f3c76a0a755dac80e1af3652
[fs-readme]: https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1/blob/b980ea7b477ae3f7f3c76a0a755dac80e1af3652/README.md
[fs-model-card]: https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1/blob/b980ea7b477ae3f7f3c76a0a755dac80e1af3652/MODEL_CARD.md
[fs-validation]: https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1/blob/b980ea7b477ae3f7f3c76a0a755dac80e1af3652/VALIDATION.md
[fs-sibling]: https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1/blob/b980ea7b477ae3f7f3c76a0a755dac80e1af3652/documentation/migration/SIBLING_LAYOUT.md
[fs-environments]: https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1/blob/b980ea7b477ae3f7f3c76a0a755dac80e1af3652/documentation/migration/ENVIRONMENTS.md
[fs-training]: https://github.com/golba98/LLM-From-Scratch-PyTorch-Codexa-v1/tree/b980ea7b477ae3f7f3c76a0a755dac80e1af3652/documentation/training
[arch-pin]: https://github.com/golba98/LLM-Architecture-PyTorch-Codexa-v1/tree/57a0b4665674420db3d2458ee62c67c2db53c366
[arch-readme]: https://github.com/golba98/LLM-Architecture-PyTorch-Codexa-v1/blob/57a0b4665674420db3d2458ee62c67c2db53c366/README.md
[arch-provenance]: https://github.com/golba98/LLM-Architecture-PyTorch-Codexa-v1/blob/57a0b4665674420db3d2458ee62c67c2db53c366/PROVENANCE.md
[tok-pin]: https://github.com/golba98/LLM-Tokenizer-PyTorch-Codexa-v1/tree/2828b94dea7c74310b30e17b2e191ee764c60132
[tok-readme]: https://github.com/golba98/LLM-Tokenizer-PyTorch-Codexa-v1/blob/2828b94dea7c74310b30e17b2e191ee764c60132/README.md
[tok-provenance]: https://github.com/golba98/LLM-Tokenizer-PyTorch-Codexa-v1/blob/2828b94dea7c74310b30e17b2e191ee764c60132/PROVENANCE.md
[data-pin]: https://github.com/golba98/LLM-Data-PyTorch-Codexa-v1/tree/dd7cd64c8fca75ed44f12f8ad701bf75b8d0584a
[data-readme]: https://github.com/golba98/LLM-Data-PyTorch-Codexa-v1/blob/dd7cd64c8fca75ed44f12f8ad701bf75b8d0584a/README.md
[data-provenance]: https://github.com/golba98/LLM-Data-PyTorch-Codexa-v1/blob/dd7cd64c8fca75ed44f12f8ad701bf75b8d0584a/PROVENANCE.md
[train-pin]: https://github.com/golba98/LLM-Training-PyTorch-Codexa-v1/tree/c10736752ea8a6c2d64d28fa0ad600b06c4a7d09
[train-readme]: https://github.com/golba98/LLM-Training-PyTorch-Codexa-v1/blob/c10736752ea8a6c2d64d28fa0ad600b06c4a7d09/README.md
[train-provenance]: https://github.com/golba98/LLM-Training-PyTorch-Codexa-v1/blob/c10736752ea8a6c2d64d28fa0ad600b06c4a7d09/PROVENANCE.md
[inf-pin]: https://github.com/golba98/LLM-Inference-PyTorch-Codexa-v1/tree/75e58e815167910887f72afced0e5e4d1f9cf6d4
[inf-readme]: https://github.com/golba98/LLM-Inference-PyTorch-Codexa-v1/blob/75e58e815167910887f72afced0e5e4d1f9cf6d4/README.md
[inf-provenance]: https://github.com/golba98/LLM-Inference-PyTorch-Codexa-v1/blob/75e58e815167910887f72afced0e5e4d1f9cf6d4/PROVENANCE.md
[mem-pin]: https://github.com/golba98/LLM-Memory-PyTorch-Codexa-v1/tree/be14176b6107b51d5478d862f2e085a6674dda91
[mem-readme]: https://github.com/golba98/LLM-Memory-PyTorch-Codexa-v1/blob/be14176b6107b51d5478d862f2e085a6674dda91/README.md
[mem-provenance]: https://github.com/golba98/LLM-Memory-PyTorch-Codexa-v1/blob/be14176b6107b51d5478d862f2e085a6674dda91/PROVENANCE.md
[spec-pin]: https://github.com/golba98/LLM-Specialist-PyTorch-Codexa-v1/tree/af076f0321754bfd41bf017d07282bb6761bcc35
[spec-readme]: https://github.com/golba98/LLM-Specialist-PyTorch-Codexa-v1/blob/af076f0321754bfd41bf017d07282bb6761bcc35/README.md
[spec-provenance]: https://github.com/golba98/LLM-Specialist-PyTorch-Codexa-v1/blob/af076f0321754bfd41bf017d07282bb6761bcc35/PROVENANCE.md
