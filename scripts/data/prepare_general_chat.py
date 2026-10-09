"""Prepare Stage 2 conversational data from existing local source derivatives."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.data.general_chat import prepare_general_chat
from src.tokenizer import load_tokenizer


def main() -> None:
    """Run the explicit command-line operation with validated inputs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, action='append')
    parser.add_argument('--output', type=Path, default=Path('data/processed/general-chat-sft-v2'))
    parser.add_argument('--tokenizer', type=Path, default=Path('checkpoints/tokenizer-base-v1/tokenizer.json'))
    args = parser.parse_args()
    paths = args.input or sorted(Path('data/processed/chat-sft-v1').glob('*/train.jsonl')) + sorted(Path('data/processed/chat-sft-v1').glob('*/validation.jsonl'))
    print(json.dumps(prepare_general_chat(paths, args.output, load_tokenizer(args.tokenizer))))


if __name__ == '__main__':
    main()
