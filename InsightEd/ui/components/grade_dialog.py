import datetime
import tkinter as tk

from tkinter import StringVar, simpledialog, messagebox
from typing import Optional, Dict, Any, List

from utils.exceptions import WrongGradeError


class GradeDialog(simpledialog.Dialog):

    def __init__(self, parent: tk.Widget, title: str ="Add Grade", grade: Optional[Dict[str, Any]]=None) -> None:
        self.grade = grade
        super().__init__(parent, title=title)


    def body(self, master: tk.Widget) -> tk.Widget:
        self.var_value = StringVar(value=str(self.grade["value"]) if self.grade else "5")
        self.var_form = StringVar(value=self.grade["form"] if self.grade else "Test")
        self.notes = tk.Text(master, height=4, width=30)

        tk.Label(master, text="Grade:").grid(row=0, column=0)
        tk.OptionMenu(master, self.var_value, *["2", "2.5", "3", "3.5", "4", "4.5", "5"]).grid(row=0, column=1)

        tk.Label(master, text="Form:").grid(row=1, column=0)
        tk.OptionMenu(master, self.var_form, "Exam", "Test", "Homework").grid(row=1, column=1)

        tk.Label(master, text="Notes:").grid(row=2, column=0, sticky="n")
        self.notes.grid(row=2, column=1)

        return self.notes


    def apply(self) -> None:
        import datetime
        self.result = {
            "value": float(self.var_value.get()),
            "form": self.var_form.get(),
            "notes": self.notes.get("1.0", "end").strip(),
            "date": datetime.date.today().isoformat()
        }




class EditGradesDialog(simpledialog.Dialog):

    def __init__(self, parent: tk.Widget, grades: List[Dict[str, Any]]) -> None:
        self.original_grades = grades
        self.edited_grades = [dict(g) for g in grades]
        super().__init__(parent, title="Edit Grades")


    def body(self, master: tk.Widget) -> None:
        self.entries = []
        self.frames = []

        self.container = tk.Frame(master)
        self.container.pack(padx=10, pady=10)

        self.draw_grades()

        add_btn = tk.Button(master, text="Add New Grade", command=self.add_new_grade)
        add_btn.pack(pady=(0, 10), anchor="center")


    def draw_grades(self) -> None:
        for f in self.frames:
            f.destroy()
        self.entries.clear()
        self.frames.clear()

        for idx, grade in enumerate(self.edited_grades):
            frame = tk.Frame(self.container)
            frame.pack(fill="x", pady=5)
            self.frames.append(frame)

            val_var = tk.StringVar(value=str(grade.get("value", "")))
            form_var = tk.StringVar(value=grade.get("form", "Test"))
            notes_var = tk.StringVar(value=grade.get("notes", ""))

            tk.Label(frame, text=f"Grade #{idx + 1}:", width=10, anchor="center").grid(row=0, column=0, padx=5)

            val_entry = tk.Entry(frame, textvariable=val_var, width=5, justify="center")
            val_entry.grid(row=0, column=1, padx=5)

            form_menu = tk.OptionMenu(frame, form_var, "Exam", "Test", "Homework")
            form_menu.grid(row=0, column=2, padx=5)

            notes_entry = tk.Entry(frame, textvariable=notes_var, width=30)
            notes_entry.grid(row=0, column=3, padx=5, sticky="ew")

            del_btn = tk.Button(frame, text="Delete", command=lambda i=idx: self.delete_grade(i), width=6)
            del_btn.grid(row=0, column=4, padx=5)

            frame.grid_columnconfigure(3, weight=1)

            self.entries.append((val_var, form_var, notes_var))


    def add_new_grade(self) -> None:
        self.edited_grades.append({"value": 5.0, "form": "Test", "notes": ""})
        self.draw_grades()


    def delete_grade(self, index: int) -> None:
        del self.edited_grades[index]
        self.draw_grades()


    def validate(self) -> bool:
        try:
            for val, _, _ in self.entries:
                v = float(val.get())
                if v < 2 or v > 5:
                    raise WrongGradeError("Grade value must be between 2 and 5.")
            return True

        except Exception as e:
            messagebox.showerror("Invalid input", str(e))
            return False


    def apply(self) -> None:
        new_grades = []
        for val, form_var, notes_var in self.entries:
            new_grades.append({"value": float(val.get()), "form": form_var.get(), "notes": notes_var.get(),
                               "date": datetime.date.today().isoformat()})
        self.result = new_grades
