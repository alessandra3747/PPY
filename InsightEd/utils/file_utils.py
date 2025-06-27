import json
import os

from tkinter import messagebox
from typing import List, Dict, Any

from utils.exceptions import JsonFileEmptyError, UsersFileNotFoundError


def load_students_from_file(filepath: str = "data/students.json") -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        raise JsonFileEmptyError

    return data



def save_students_to_file(all_students: List[Dict[str, Any]]) -> None:
    filepath = "data/students.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(all_students, f, ensure_ascii=False, indent=4)



def load_users() -> Dict[str, Any]:
    if not os.path.exists("data/users.json"):
        raise UsersFileNotFoundError

    with open("data/users.json", "r") as f:
        return json.load(f)



def save_notes_to_file(username: str, user_notes: Dict[str, Any]) -> None:
    all_notes = {}
    if os.path.exists("data/notes.json"):
        try:
            with open("data/notes.json", "r", encoding="utf-8") as f:
                all_notes = json.load(f)
        except Exception:
            all_notes = {}

    all_notes[username] = user_notes

    try:
        with open("data/notes.json", "w", encoding="utf-8") as f:
            json.dump(all_notes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Error while saving notes", f"The notes could not be saved:\n{e}")


def load_notes_from_file(username: str) -> Dict[str, Any]:
    if os.path.exists("data/notes.json"):
        try:
            with open("data/notes.json", "r", encoding="utf-8") as f:
                all_notes = json.load(f)
            return all_notes.get(username, {})
        except Exception as e:
            messagebox.showwarning("Error while loading notes", f"The notes could not be loaded:\n{e}")
    return {}

