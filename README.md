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
    └── read_aloud.py           # Generic edge-tts text-to-speech script
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

## License

MIT.
