# cursor-tools

Cursor agent skills and utility scripts — clone once, get everything.

```bash
git clone https://github.com/snps-harutk/cursor-tools.git
```

## Structure

```
cursor-tools/
├── skills/
│   └── reading-spec-or-book/   # Cursor skill: read a spec/book section, explain it clearly, generate audio
│       ├── SKILL.md
│       ├── EXPLANATION_TEMPLATE.md
│       └── examples.md
└── scripts/
    ├── read_aloud.py           # Generic edge-tts text-to-speech script
    └── count_tokens.py         # Report tiktoken token counts and context-window usage
```

## Skills

### reading-spec-or-book

Reads a section of a spec, book, or PDF and produces an extra-clear written explanation with everyday analogies, plus an auto-playing MP3. See [skills/reading-spec-or-book/README.md](skills/reading-spec-or-book/README.md) for details.

To install as a Cursor personal skill, symlink or copy the folder:

```bash
# Windows
mklink /D "%USERPROFILE%\.cursor\skills\reading-spec-or-book" "%cd%\skills\reading-spec-or-book"

# macOS / Linux
ln -s "$(pwd)/skills/reading-spec-or-book" ~/.cursor/skills/reading-spec-or-book
```

## Scripts

### read_aloud.py

Generic text-to-speech script using [edge-tts](https://pypi.org/project/edge-tts/). Converts a text file to MP3 with configurable voice and speech rate.

```bash
pip install edge-tts
python scripts/read_aloud.py --file input.txt -o output.mp3
```

### count_tokens.py

Reports [tiktoken](https://pypi.org/project/tiktoken/) token counts for one or
more text files, plus the percentage of a context window each file consumes.
Handy for estimating how much of an LLM prompt budget a chat transcript,
source file, or spec will eat.

```bash
pip install tiktoken
python scripts/count_tokens.py transcript.jsonl
python scripts/count_tokens.py --all-encodings transcript.jsonl
python scripts/count_tokens.py *.sv                 # multi-file, with TOTAL
cat file.txt | python scripts/count_tokens.py -     # read from stdin
```

By default uses `cl100k_base` (GPT-4 tokenizer), which is a reasonable proxy
for Claude (typically within ~5%). Use `--encoding o200k_base` for GPT-4o, or
`--all-encodings` to compare. The assumed context window is 200k tokens;
override with `--window 1000000` for a 1M-token model.

## License

MIT.
