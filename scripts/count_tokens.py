#!/usr/bin/env python3
"""
count_tokens.py - Report token counts for one or more text files.

Useful for estimating how much of an LLM context window a file (e.g. a chat
transcript, source code, or spec) will consume when attached to a prompt.

Uses OpenAI's `tiktoken` library. `cl100k_base` (GPT-4) is used by default and
is a reasonable proxy for Anthropic Claude's tokenizer (typically within ~5%).

Install
-------
    pip install tiktoken

Usage
-----
    count_tokens.py FILE [FILE ...]
    count_tokens.py --all-encodings FILE
    count_tokens.py --encoding o200k_base FILE
    cat file.txt | count_tokens.py -

Examples
--------
    count_tokens.py transcript.jsonl
    count_tokens.py *.sv
    count_tokens.py --all-encodings transcript.jsonl
    count_tokens.py --window 1000000 huge.txt    # report % of a 1M window
"""

import argparse
import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    sys.exit(
        "ERROR: tiktoken is not installed for this interpreter.\n"
        f"       Interpreter: {sys.executable}\n"
        "       Install with: pip install tiktoken"
    )


KNOWN_ENCODINGS = ["cl100k_base", "o200k_base", "p50k_base", "r50k_base"]
DEFAULT_CONTEXT_WINDOW = 200_000
EXTRA_WINDOWS = [1_000_000]  # additional window sizes always shown alongside the default


def count(text: str, encoding_name: str) -> int:
    """Return the number of tokens in `text` for the given encoding."""
    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))


def read_input(path: str) -> str:
    """Read a file (or stdin if path is '-')."""
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(errors="replace")


def report(path: str, text: str, encodings: list, window: int) -> None:
    """Print a one-or-more-line report for a single input."""
    n_chars = len(text)
    n_lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)

    label = path if path != "-" else "<stdin>"
    print(f"\n{label}")
    print(f"  chars: {n_chars:,}    lines: {n_lines:,}")

    all_windows = [window] + [w for w in EXTRA_WINDOWS if w != window]
    for enc_name in encodings:
        try:
            n_tokens = count(text, enc_name)
        except Exception as exc:
            print(f"  {enc_name:14s}  ERROR: {exc}")
            continue
        ratio = n_chars / n_tokens if n_tokens else 0.0
        pct_parts = "   ".join(
            f"{100.0 * n_tokens / w:5.2f}% of {w // 1000}k" for w in all_windows
        )
        print(
            f"  {enc_name:14s}  tokens = {n_tokens:>9,}   "
            f"chars/tok = {ratio:5.2f}   "
            f"[ {pct_parts} ]"
        )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Count tokens in text files using tiktoken.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Encodings:\n"
            "  cl100k_base  - GPT-4 / GPT-3.5-turbo (good Claude proxy, default)\n"
            "  o200k_base   - GPT-4o\n"
            "  p50k_base    - GPT-3 (Codex, davinci)\n"
            "  r50k_base    - GPT-3 (older)\n"
        ),
    )
    p.add_argument("paths", nargs="+", help="File(s) to analyze (use '-' for stdin).")
    p.add_argument(
        "-e", "--encoding",
        default="cl100k_base",
        help="Tokenizer encoding (default: cl100k_base).",
    )
    p.add_argument(
        "--all-encodings", action="store_true",
        help="Report token counts for all known encodings.",
    )
    p.add_argument(
        "-w", "--window", type=int, default=DEFAULT_CONTEXT_WINDOW,
        help=f"Context window size to compute %% against (default: {DEFAULT_CONTEXT_WINDOW}).",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    encodings = KNOWN_ENCODINGS if args.all_encodings else [args.encoding]

    total_tokens = {e: 0 for e in encodings}
    total_chars = 0
    n_files_ok = 0

    for path in args.paths:
        try:
            text = read_input(path)
        except OSError as exc:
            print(f"\n{path}\n  ERROR: {exc}", file=sys.stderr)
            continue
        total_chars += len(text)
        n_files_ok += 1
        for enc_name in encodings:
            try:
                total_tokens[enc_name] += count(text, enc_name)
            except Exception:
                pass
        report(path, text, encodings, args.window)

    if n_files_ok > 1:
        all_windows = [args.window] + [w for w in EXTRA_WINDOWS if w != args.window]
        print("\nTOTAL")
        print(f"  chars: {total_chars:,}")
        for enc_name in encodings:
            n = total_tokens[enc_name]
            pct_parts = "   ".join(
                f"{100.0 * n / w:5.2f}% of {w // 1000}k" for w in all_windows
            )
            print(
                f"  {enc_name:14s}  tokens = {n:>9,}   "
                f"[ {pct_parts} ]"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
