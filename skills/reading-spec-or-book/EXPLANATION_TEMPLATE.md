# Explanation Template

This is the literal skeleton for every `section_<X>_<Y>_text.txt` file. Fill in the placeholders in angle brackets. Do not include any of the `<...>` markers or the comment lines in the final output.

The output is read aloud by a text-to-speech engine, so:

- Use plain prose, not Markdown headings (no `#`, `##`, `###`).
- Use bold sub-headers `**Like This**` to separate concepts — they get spoken as natural pauses.
- Do not include code fences, tables, or bullet lists with `-` or `*`. Spell them out as sentences instead ("There are three reasons. First, ... Second, ... Third, ...").
- Spell out every acronym on first use, then it's fine to use the short form after.
- Em-dashes (`—`) are fine; the TTS handles them as a short pause.

## Template

```
Section <X.Y>: <Title> — explained very carefully, with everyday analogies.

<One paragraph framing what this section is really about, written like you're explaining it to a curious friend. Mention what came before if it builds on prior sections, and tease what comes next.>

**The Big Picture: <plain-English question this section answers>**

<2-4 paragraphs. Start with an everyday-life analogy that sets up the same problem the section solves. Then connect it to the chip/system context. Introduce the core vocabulary only after the analogy has landed.>

**<Subconcept 1 name>**

<Analogy first. Then the technical definition. Then a concrete example or worked scenario. Then any nuance or gotcha the textbook glosses over.>

**<Subconcept 2 name>**

<Same shape: analogy, definition, example, nuance.>

**<... more subconcepts as needed ...>**

<For long sections, group related subconcepts under a higher-level bold header like "**Section 3.4.4: Credit-Based Flow Control**" matching the source document's own numbering.>

**Final Thoughts**

<One paragraph summarizing the 3-5 key takeaways in plain language. No new concepts here.>

<One-line teaser: "Next we'll look at <topic>, which <one-sentence why it matters>.">
```

## Length guidance

| Section type                  | Target characters |
|-------------------------------|-------------------|
| Short / introductory          | 6,000-10,000      |
| Standard technical section    | 10,000-18,000     |
| Dense (protocols, algorithms) | 18,000-25,000     |

If the explanation would exceed 25,000 characters, split by subsection (3.4.1, 3.4.2, ...) and emit one text/MP3 pair per part.

## Forbidden in the text file

- Markdown headings (`#`, `##`, `###`).
- Bullet lists with `-`, `*`, or `1.` markers.
- Code blocks, tables, inline backticks.
- Page numbers, figure numbers, or PDF extraction artifacts like `[fig 3.5]`.
- Citations like "(p. 142)" or footnote markers.
- Phrases that refer to the document layout ("see the diagram above", "as shown in Figure 3.7") — describe the picture in words instead.
