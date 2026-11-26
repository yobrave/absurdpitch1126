"""Deliver the One-Sentence Absurd Invention Pitch entry for make.fun.

The pitch lives in entry.txt next to this script; this program validates
the 220-character gate and copies the sentence into the judge's inbox.
"""
import json
import os
from pathlib import Path

SPONSOR = "u-suroso-69"
CONTEST = "One-Sentence Absurd Invention Pitch"
CEILING = 220
RUN_ID = "ainp-r32-1126"


class Guard:
    def __init__(self, text):
        self.text = text.strip()
        self.notes = []

    def enforce(self):
        if len(self.text) < 1:
            self.notes.append("no sentence found")
        if len(self.text) > CEILING:
            self.notes.append("sentence over %d characters" % CEILING)
        return not self.notes


def ship(text, folder):
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or folder)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "entry.txt").write_text(text + "\n", encoding="utf-8", newline="\n")


def main():
    home = Path(__file__).resolve().parent
    pitch = (home / "entry.txt").read_text(encoding="utf-8").strip()
    guard = Guard(pitch)
    if guard.enforce():
        ship(guard.text, "out")
        print("absurd invention pitch shipped, run", RUN_ID)
        print(json.dumps({"status": "valid", "contest": CONTEST, "sponsor": SPONSOR, "size": len(guard.text), "run": RUN_ID}))
    else:
        print(json.dumps({"status": "invalid", "notes": guard.notes}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
