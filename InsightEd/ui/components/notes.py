import datetime
import tkinter as tk
from typing import Any, Callable

from utils.exceptions import MyTclError
from utils.file_utils import save_notes_to_file


def create_notes(center_frame: tk.Widget, parent_component: Any) -> None:
    note_section = tk.Frame(center_frame, bg="white")
    note_section.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(note_section, text="NOTES", font=("Verdana", 14, "bold"), bg="white", fg="#5e2d92").pack(anchor="w")

    note_text = tk.Text(note_section, height=10, font=("Verdana", 12), wrap="word", bd=1, relief="solid")
    note_text.pack(fill="both", expand=True, pady=(5, 0))

    parent_component.note_text = note_text

    note_text.bind("<FocusOut>", lambda e: save_current_note(parent_component))

    load_note_for_selected_date(parent_component)


def on_date_selected(parent_component: Any) -> None:
    save_current_note(parent_component)
    selected_date = datetime.datetime.strptime(parent_component.calendar.get_date(), "%Y-%m-%d").date()
    parent_component.selected_date = selected_date
    load_note_for_selected_date(parent_component)


def load_note_for_selected_date(parent_component: Any) -> None:
    date_str = parent_component.selected_date.isoformat()
    note = parent_component.notes.get(date_str, "")

    note_text = parent_component.note_text
    note_text.delete("1.0", tk.END)
    note_text.insert(tk.END, note)



def handle_my_tcl_error(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MyTclError:
            pass
    return wrapper


@handle_my_tcl_error
def save_current_note(parent_component: Any) -> None:
    try:
        note_text = parent_component.note_text
        selected_date = parent_component.selected_date
        date_str = selected_date.isoformat()
        content = note_text.get("1.0", tk.END).strip()

        username = parent_component.current_user

        if content:
            parent_component.notes[date_str] = content
        elif date_str in parent_component.notes:
            del parent_component.notes[date_str]

        save_notes_to_file(username, parent_component.notes)
    except tk.TclError as e:
        raise MyTclError("Unable to read from note - it has been destroyed") from e