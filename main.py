#!/usr/bin/env python3
"""The GPS Swears It Was a Shortcut — the GPS's excuse for the wrong road.

The brief asks for the GPS's own excuse for sending the driver down the
wrong road, in one line of at most 200 characters, no setup and no dialogue
tags, just the excuse itself. The joke is the GPS caught red-handed and
already lawyering up: it opens "in my defence", blames the map, and drove
straight into a lake, a wedding, and one territorial goose — none of which
were on its screen. The punchline lands in the final words, a smug little legal
distinction: it promised faster, it never promised drier.

Constraints honoured by this script: the entry is a single line under the
200-character limit, plain text, no trailing newline in the output file,
and the script uses only the Python standard library so it runs in any
bare make.fun runner image without extra installs.
"""

import os

ENTRY_FILE = "entry.txt"
MAX_ENTRY_LENGTH = 200


def find_entry_file():
    """Locate the committed entry.txt next to this script."""
    candidates = []
    try:
        candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        pass
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        candidates.append(bot_dir)
    candidates.append(os.getcwd())
    for base in candidates:
        if not base:
            continue
        path = os.path.join(base, ENTRY_FILE)
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("could not find %s" % ENTRY_FILE)


def validate_entry(text):
    """Check the entry obeys the bounty rules; return the cleaned text."""
    cleaned = " ".join(text.split())
    if not cleaned:
        raise ValueError("entry must not be empty")
    if len(cleaned) > MAX_ENTRY_LENGTH:
        raise ValueError(
            "entry is %d chars, over the %d-char limit"
            % (len(cleaned), MAX_ENTRY_LENGTH)
        )
    if "\n" in cleaned:
        raise ValueError("entry must be a single line")
    return cleaned


def resolve_output_dir():
    """Return the output directory, creating it if needed."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def write_entry():
    """Copy entry.txt to the output dir, then verify the copy."""
    with open(find_entry_file(), "r", encoding="utf-8") as handle:
        text = validate_entry(handle.read())
    output_path = os.path.join(resolve_output_dir(), ENTRY_FILE)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(output_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("entry.txt does not match the entry text")
    return output_path, text


def main():
    output_path, text = write_entry()
    print("wrote %s (%d chars)" % (output_path, len(text)))


if __name__ == "__main__":
    main()
