"""MyOneNote — a small command-line notes manager.

This starter project stores notes in a local JSON file and supports
adding, listing, searching, and deleting notes.

Usage:
    python main.py add "My first note"
    python main.py list
    python main.py search "first"
    python main.py delete 1
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).with_name("notes.json")


def load_notes() -> list[dict[str, Any]]:
    """Read notes from disk, returning an empty list when no file exists."""
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"Could not read {DATA_FILE.name}: {exc}") from exc
    if not isinstance(data, list):
        raise RuntimeError(f"{DATA_FILE.name} must contain a JSON list.")
    return data


def save_notes(notes: list[dict[str, Any]]) -> None:
    """Write notes to disk as readable UTF-8 JSON."""
    DATA_FILE.write_text(
        json.dumps(notes, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def add_note(text: str) -> None:
    text = text.strip()
    if not text:
        raise ValueError("Note text cannot be empty.")
    notes = load_notes()
    next_id = max((int(note.get("id", 0)) for note in notes), default=0) + 1
    notes.append(
        {
            "id": next_id,
            "text": text,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    )
    save_notes(notes)
    print(f"Added note #{next_id}.")


def list_notes() -> None:
    notes = load_notes()
    if not notes:
        print("No notes yet. Add one with: python main.py add \"Your note\"")
        return
    for note in notes:
        print(f"[{note.get('id', '?')}] {note.get('text', '')}")
        if note.get("created_at"):
            print(f"    Created: {note['created_at']}")


def search_notes(query: str) -> None:
    query = query.casefold().strip()
    if not query:
        raise ValueError("Search query cannot be empty.")
    matches = [note for note in load_notes() if query in str(note.get("text", "")).casefold()]
    if not matches:
        print("No matching notes found.")
        return
    for note in matches:
        print(f"[{note.get('id', '?')}] {note.get('text', '')}")


def delete_note(note_id: int) -> None:
    notes = load_notes()
    updated = [note for note in notes if int(note.get("id", -1)) != note_id]
    if len(updated) == len(notes):
        raise ValueError(f"No note found with ID {note_id}.")
    save_notes(updated)
    print(f"Deleted note #{note_id}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A simple local notes manager.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a note.")
    add_parser.add_argument("text", help="Text of the note.")

    subparsers.add_parser("list", help="List all notes.")

    search_parser = subparsers.add_parser("search", help="Search note text.")
    search_parser.add_argument("query", help="Text to search for.")

    delete_parser = subparsers.add_parser("delete", help="Delete a note by ID.")
    delete_parser.add_argument("id", type=int, help="ID of the note to delete.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "add":
            add_note(args.text)
        elif args.command == "list":
            list_notes()
        elif args.command == "search":
            search_notes(args.query)
        elif args.command == "delete":
            delete_note(args.id)
        else:
            parser.error("Unknown command.")
    except (OSError, RuntimeError, ValueError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
