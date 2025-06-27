import tkinter as tk

from tkinter import simpledialog, messagebox
from typing import Optional, Dict, Any, List, Callable


class StudentDialog(simpledialog.Dialog):

    def __init__(self, parent: tk.Widget, title: Optional[str] = None, student: Optional[Dict[str, Any]] = None,
                 all_students: Optional[List[Dict[str, Any]]] = None,
                 save_callback: Optional[Callable[[List[Dict[str, Any]]], None]] = None) -> None:

        self.student = student
        self.all_students = all_students
        self.save_callback = save_callback
        super().__init__(parent, title)



    def body(self, master: tk.Widget) -> Optional[tk.Entry]:
        tk.Label(master, text="First Name:").grid(row=0, column=0)
        tk.Label(master, text="Last Name:").grid(row=1, column=0)
        tk.Label(master, text="PESEL:").grid(row=2, column=0)

        self.entry_first = tk.Entry(master)
        self.entry_last = tk.Entry(master)
        self.entry_pesel = tk.Entry(master)

        self.entry_first.grid(row=0, column=1)
        self.entry_last.grid(row=1, column=1)
        self.entry_pesel.grid(row=2, column=1)

        if self.student:
            self.entry_first.insert(0, self.student["first_name"])
            self.entry_last.insert(0, self.student["last_name"])
            self.entry_pesel.insert(0, self.student["pesel"])

            self.delete_btn = tk.Button(master, text="Delete Student", fg="white", bg="red", command=self.on_delete)
            self.delete_btn.grid(row=3, column=0, columnspan=2, pady=10)

        return self.entry_first



    def on_delete(self) -> None:
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            if self.all_students:
                self.all_students[:] = [s for s in self.all_students if s["pesel"] != self.student["pesel"]]
            if self.save_callback:
                self.save_callback(self.all_students)
            messagebox.showinfo("Deleted", "Student has been deleted.")
            self.result = None
            self.destroy()



    def validate(self) -> bool:
        first_name = self.entry_first.get().strip()
        last_name = self.entry_last.get().strip()
        pesel = self.entry_pesel.get().strip()

        if not first_name or not last_name or not pesel:
            messagebox.showerror("Validation error", "All fields are required.")
            return False

        if len(pesel) != 11 or not pesel.isdigit():
            messagebox.showerror("Validation error", "PESEL must be 11 digits.")
            return False

        if self.all_students:
            for s in self.all_students:
                if s == self.student:
                    continue
                if s["pesel"] == pesel:
                    messagebox.showerror("Validation error", "PESEL must be unique.")
                    return False

        return True



    def apply(self) -> None:
        self.result = {
            "first_name": self.entry_first.get().strip(),
            "last_name": self.entry_last.get().strip(),
            "pesel": self.entry_pesel.get().strip(),
            "grades": self.student.get("grades", []) if self.student else [],
            "group": self.student.get("group", "") if self.student else "",
        }

