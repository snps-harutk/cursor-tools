---
name: reading-spec-or-book
description: Read a section of a spec, book, or PDF and produce an extra-clear written explanation plus an auto-playing audio version. Use when the user asks to "read", "explain", "do section X.Y", or walk through a chapter/section of a PDF, book, or specification document, especially when they want analogies and beyond-the-textbook clarity.
---

# Reading a Spec or Book

This skill turns a request like "do section 3.4" or "explain chapter 5" into a consistent two-artifact deliverable: an extra-clear written explanation file and an auto-playing MP3 generated from it.

## Trigger phrases

Apply this skill when the user says any of these (or a close variant):

- "do section X.Y" / "do X.Y" / "do chapter N"
- "read section X.Y" / "explain section X.Y" / "walk me through ..."
- "go through ... extra carefully", "be extra understandable", "explain like I'm new to this"
- "do the next section" (continue from the most recently produced `section_*.txt`)

## Required workspace state

Before starting, confirm both of these exist in the user's working directory (or ask where they are):

1. A source document (PDF or `.txt`) — for example `arm-modern-soc-design-on-arm.pdf`.
2. A text-to-speech script. The default expected script is `read_aloud.py` with this signature:

   ```bash
   python read_aloud.py --file <input.txt> -o <output.mp3>
   ```

   It auto-plays the resulting MP3 unless `--no-play` is passed.

If `read_aloud.py` is missing, produce only the text file and ask the user how they want audio generated.

## Workflow checklist

Copy this into your todos and track progress:

```
- [ ] Locate the section in the source document
- [ ] Draft section_<X>_<Y>_text.txt following the explanation template
- [ ] Generate section_<X>_<Y>_<topic>.mp3 with read_aloud.py
- [ ] Briefly summarize what was covered (analogies used, concepts clarified)
```

### Step 1: Locate the section

Use the `Read` tool with `offset` and `limit` to window into the PDF or document. PDFs can be large, so start with a reasonable window (e.g. 500-700 lines) around where the section is expected and widen if the section spans the boundary. If you don't know the offset, check the most recently produced `section_*_text.txt` for context on how far you've already read, or scan the table of contents.

### Step 2: Draft the explanation text file

Write to `section_<X>_<Y>_text.txt` in the same directory as the source document and `read_aloud.py`. Follow [EXPLANATION_TEMPLATE.md](EXPLANATION_TEMPLATE.md) for structure and [examples.md](examples.md) for tone and quality.

### Step 3: Generate audio

Run from the directory containing `read_aloud.py`:

```bash
python read_aloud.py --file section_<X>_<Y>_text.txt -o section_<X>_<Y>_<topic>.mp3
```

`<topic>` is a short slug describing the section (e.g. `noc`, `serdes`, `topology_synthesis`, `packet_switched`). Keep it lowercase with underscores.

Generation can take 60-120 seconds for large texts. Monitor the terminal output with `Await` and look for one of:

- `Playing...` — success, the MP3 is generated and playback started.
- `Error:` or a traceback — generation failed; report the error and stop.

### Step 4: Summarize

After playback starts, send a short message to the user that:

- Names the two produced files.
- Bullets the analogies you used (e.g. "city roads / packet switching", "restaurant tokens / credit flow control").
- Bullets the concepts clarified beyond what the textbook says.
- Offers to continue with the next section.

## Writing-style rules

These are the non-negotiable rules that give the output its "extra-clear" voice. Examples for each are in [examples.md](examples.md).

- **Open with a "Big Picture" paragraph** framing the core question in plain English before any technical term appears.
- **Lead every technical term with an everyday analogy first**, then connect it to the formal definition. Re-use families of analogies — city roads, conveyor belts, talking sticks, restaurant tokens, urban planning, three houses on a field — wherever they fit.
- **Spell out every acronym on first use** (e.g. PPA = Power, Performance, Area; NoC = Network-on-Chip; FIFO = First In, First Out).
- **Go beyond the textbook when needed.** The goal is understanding, not paraphrase. If the textbook is terse on a point, expand it with a worked example or analogy.
- **Use bold sub-headers (`**Subconcept**`)**, not Markdown H1/H2/H3. The text is read aloud — headers should feel like spoken section breaks, not document structure.
- **End with a "Final Thoughts" paragraph** that summarizes the 3-5 key takeaways, followed by a one-line teaser for the next section ("Next we'll look at ...").
- **Target length: 8,000-25,000 characters** per section text file. Shorter sections can be ~8k; dense ones like deadlock-avoidance or topology synthesis go to ~20-25k.
- **Write in conversational second-person/first-person plural** ("Let me explain ...", "Imagine you're ..."). Avoid passive academic voice.
- **Never include LINE_NUMBER prefixes, page-number artifacts, or PDF extraction junk** in the text file — the TTS will read them literally.

## File naming conventions

Derived from the existing files in the reference workspace:

- Text file: `section_<X>_<Y>_text.txt` (e.g. `section_3_4_text.txt`).
- Audio file: `section_<X>_<Y>_<topic>.mp3` (e.g. `section_3_4_noc.mp3`, `section_3_9_topology_synthesis.mp3`).

For figure-based explanations rather than full sections, use `figure_<N>_<M>_explained.mp3` / `figure_<N>_<M>_text.txt`.

## When the section is too large for one file

If the section is unusually long (e.g. 30k+ characters of explanation), split into subsections following the source document's own numbering (3.4.1, 3.4.2, ...) and produce one text/MP3 pair per subsection. Otherwise keep them combined.

## Additional resources

- [EXPLANATION_TEMPLATE.md](EXPLANATION_TEMPLATE.md) — the literal template for `section_X_Y_text.txt`.
- [examples.md](examples.md) — verbatim excerpts from production runs as the quality bar.
