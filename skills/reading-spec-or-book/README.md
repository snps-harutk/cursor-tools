# reading-spec-or-book

A [Cursor Agent Skill](https://docs.cursor.com/agent/skills) that turns a request like *"do section 3.4"* or *"explain chapter 5"* into two artifacts:

1. An **extra-clear written explanation** as `section_<X>_<Y>_text.txt`, written in conversational prose with everyday analogies (city roads, conveyor belts, restaurant tokens, three houses on a field, ...).
2. An **auto-playing MP3** generated from that text via a TTS script.

The skill was extracted from a real workflow walking through chapters of *Modern System-on-Chip Design on Arm* — see `examples.md` for the quality bar.

## Install

Clone this repository into your personal Cursor skills directory:

```bash
# Windows
git clone https://github.com/<your-user>/reading-spec-or-book.git "%USERPROFILE%\.cursor\skills\reading-spec-or-book"

# macOS / Linux
git clone https://github.com/<your-user>/reading-spec-or-book.git ~/.cursor/skills/reading-spec-or-book
```

Cursor will pick the skill up automatically on the next agent session.

## Requirements

The skill expects two things to be present in the working directory where you ask it to read a section:

- A source document (PDF or `.txt`).
- A text-to-speech script with this signature:

  ```bash
  python read_aloud.py --file <input.txt> -o <output.mp3>
  ```

  Any script that accepts those flags works. A reference implementation using [`edge-tts`](https://pypi.org/project/edge-tts/) is short enough to write in ~30 lines of Python.

## How to use

Once installed, just ask the agent things like:

- *"Do section 3.4."*
- *"Explain chapter 5 of `my-spec.pdf`."*
- *"Go through section 2.1 extra carefully."*
- *"Do the next section."*

The agent will follow the workflow in `SKILL.md` and produce the text + MP3 in your working directory.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill instructions loaded by Cursor. |
| `EXPLANATION_TEMPLATE.md` | Literal skeleton for the `section_X_Y_text.txt` output. |
| `examples.md` | Verbatim excerpts from production runs as the quality bar. |

## License

MIT.
