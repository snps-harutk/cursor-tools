"""
Generic text-to-speech script.
Usage:
    python read_aloud.py "Your text here"
    python read_aloud.py --file input.txt
    python read_aloud.py --file input.txt --voice en-GB-RyanNeural --rate "-10%"
    python read_aloud.py --list-voices
"""

import asyncio
import argparse
import subprocess
import sys
import os
import edge_tts


DEFAULT_VOICE = "en-CA-LiamNeural"
DEFAULT_RATE = "-5%"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


async def list_voices(lang_filter=None):
    voices = await edge_tts.list_voices()
    if lang_filter:
        voices = [v for v in voices if lang_filter.lower() in v["Locale"].lower()]
    for v in voices:
        print(f"  {v['ShortName']:30s}  {v['Locale']:10s}  {v['Gender']}")
    print(f"\nTotal: {len(voices)} voices")


async def text_to_speech(text: str, output_file: str, voice: str, rate: str):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)


def sanitize_filename(text: str) -> str:
    slug = text[:50].strip().replace(" ", "_")
    return "".join(c for c in slug if c.isalnum() or c in "_-") + ".mp3"


def play_file(filepath: str):
    if sys.platform == "win32":
        subprocess.Popen(["start", "", filepath], shell=True)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", filepath])
    else:
        subprocess.Popen(["xdg-open", filepath])


def main():
    parser = argparse.ArgumentParser(description="Read text aloud using edge-tts")
    parser.add_argument("text", nargs="?", help="Text to read aloud")
    parser.add_argument("--file", "-f", help="Read text from a file instead")
    parser.add_argument("--output", "-o", help="Output MP3 filename")
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE, help=f"Voice name (default: {DEFAULT_VOICE})")
    parser.add_argument("--rate", "-r", default=DEFAULT_RATE, help=f"Speech rate (default: {DEFAULT_RATE})")
    parser.add_argument("--no-play", action="store_true", help="Don't auto-play the file")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--lang", default=None, help="Filter voices by language code (e.g. en, fr, de)")

    args = parser.parse_args()

    if args.list_voices:
        asyncio.run(list_voices(args.lang))
        return

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.error("Provide text as an argument or use --file to read from a file")

    if not text.strip():
        print("Error: empty text")
        sys.exit(1)

    output_file = args.output or os.path.join(OUTPUT_DIR, sanitize_filename(text))

    print(f"Voice:  {args.voice}")
    print(f"Rate:   {args.rate}")
    print(f"Length: {len(text)} characters")
    print(f"Output: {output_file}")

    asyncio.run(text_to_speech(text, output_file, args.voice, args.rate))
    print("Audio generated.")

    if not args.no_play:
        play_file(output_file)
        print("Playing...")


if __name__ == "__main__":
    main()
