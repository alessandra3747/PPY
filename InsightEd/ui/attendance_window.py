import datetime
import tkinter as tk

from tkinter import messagebox
from typing import List, Dict, Any, Optional, Callable
from tkcalendar import Calendar
from utils.exceptions import JsonFileEmptyError
from utils.file_utils import save_students_to_file, load_students_from_file
from utils.window_utils import center_window
from utils.attendance_utils import STATUS_COLORS, STATUS_ICONS, STATUS_TEXTS


class AttendanceWindow(tk.Frame):

    def __init__(self, parent: tk.Widget, students_list: List[Dict[str, Any]], group_name: Optional[str] = None,
                 title_text: Optional[str] = None) -> None:

        super().__init__(parent, bg="white")

        self.students = students_list
        self.group_name = group_name
        self.current_date = datetime.date.today().isoformat()
        self.title_text = title_text or f"📅 Attendance for {self.group_name}"

        self.create_widgets()



    def create_widgets(self) -> None:
        self.title_label = tk.Label(self, text=f"{self.title_text}\n{self.current_date}",font=("Verdana", 16, "bold"), bg="white", fg="#5e2d92")
        self.title_label.pack(pady=10)

        calendar_frame = tk.Frame(self, bg="white")
        calendar_frame.pack(pady=5)

        tk.Label(calendar_frame, text="Choose date:", bg="white", font=("Verdana", 12)).pack()

        self.calendar = Calendar(calendar_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.selection_set(self.current_date)
        self.calendar.pack(pady=5)
        self.calendar.bind("<<CalendarSelected>>", self.on_calendar_date_selected)

        if len(self.students) > 1:
            tk.Button(self, text="✔️ Check attendance", font=("Verdana", 10), command=self.check_attendance_for_unset).pack(pady=5)

        list_container = tk.Frame(self, bg="white")
        list_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(list_container, bg="white", highlightthickness=0)
        self.v_scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        self.update_attendance()



    def check_attendance_for_unset(self) -> None:
        self.unchecked_students = [
            student for student in self.students
            if all(rec.get("date") != self.current_date for rec in student.get("attendance_records", []))
        ]

        if not self.unchecked_students:
            messagebox.showinfo("Info", "✔️ Attendance already checked for all students.")
            return

        self._check_next_student()


    def _check_next_student(self) -> None:
        if not self.unchecked_students:
            self.update_attendance()
            return
        student = self.unchecked_students.pop(0)
        self.show_attendance_dialog(student, callback=self._check_next_student)



    def on_calendar_date_selected(self, event: tk.Event) -> None:
        self.current_date = self.calendar.get_date()
        self.title_label.config(text=f"{self.title_text}\n{self.current_date}")
        self.update_attendance()



    def update_attendance(self) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for idx, student in enumerate(self.students):
            row = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
            row.pack(fill="x", pady=2)

            student_str = f"{student['first_name']} {student['last_name']} ({student['pesel']})"
            tk.Label(row, text=student_str, bg="white", anchor="w", width=30).pack(side="left", padx=5)

            status = None
            for rec in student.get("attendance_records", []):
                if rec.get("date") == self.current_date:
                    status = rec.get("status")
                    break

            color = STATUS_COLORS.get(status, "white")
            icon = STATUS_ICONS.get(status, "")

            status_frame = tk.Frame(row, width=25, height=25, bg="white")
            status_frame.pack_propagate(False)
            status_frame.pack(side="left", padx=10)
            tk.Label(status_frame, text=icon, bg=color, font=("Segoe UI Emoji", 12)).pack(fill="both", expand=True)

            tk.Button(row, text="Edit Attendance", width=15, command=lambda i=idx: self.edit_attendance(i)).pack(side="right", padx=5, pady=2)



    def edit_attendance(self, index: int) -> None:
        student = self.students[index]
        self.show_attendance_dialog(student, callback=self.update_attendance)



    def show_attendance_dialog(self, student: Dict[str, Any], callback: Optional[Callable[[], None]] = None) -> None:
        name = f"{student['first_name']} {student['last_name']}"

        top = tk.Toplevel(self)
        top.title("Attendance")
        center_window(top, 400, 300)
        top.transient(self)
        top.grab_set()

        tk.Label(top, text=f"Set attendance for\n{name}\non {self.current_date}", font=("Verdana", 12)).pack(pady=15)

        current_status = None
        for rec in student.get("attendance_records", []):
            if rec.get("date") == self.current_date:
                current_status = rec.get("status")
                break

        if current_status is not None:
            tk.Label(top, text=f"Current status: {STATUS_TEXTS.get(current_status, 'Not set')}", font=("Verdana", 10, "italic"), fg="gray").pack()

        def on_status_chosen(status):
            self.set_attendance_status(student, status)
            top.destroy()
            if callback:
                callback()

        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=10)

        for btn in self._create_status_buttons(btn_frame, on_status_chosen):
            btn.pack(side="left", padx=5)

        tk.Button(top, text="❌Clear", command=lambda: on_status_chosen(None)).pack(pady=10)
        tk.Button(top, text="⏭️ Skip", command=lambda: (top.destroy(), callback() if callback else None)).pack(pady=5)



    def set_attendance_status(self, student: Dict[str, Any], status: Optional[str]) -> None:
        try:
            all_students = load_students_from_file()
        except JsonFileEmptyError:
            all_students = []

        target_pesel = student.get("pesel")

        for s in all_students:
            if s.get("pesel") == target_pesel:
                records = s.setdefault("attendance_records", [])
                for rec in records:
                    if rec.get("date") == self.current_date:
                        if status is None:
                            records.remove(rec)
                        else:
                            rec["status"] = status
                        break
                else:
                    if status is not None:
                        records.append({"date": self.current_date, "status": status})
                break

        student["attendance_records"] = [rec.copy() for rec in s.get("attendance_records", [])]

        save_students_to_file(all_students)



    def _create_status_buttons(self, parent: tk.Widget, set_status_func: Callable[[Optional[str]], None]) -> List[tk.Button]:
        btn_specs = [ ("✔️Present", "present", "#a6d785"), ("✖️Absent", "absent", "#f28b82"),
                     ("⏱️Late", "late", "#fdd663"), ("📝Excused", "excused", "#a7c7e7") ]
        btns = []
        for text, status, color in btn_specs:
            btn = tk.Button(parent, text=text, width=10, bg=color, command=lambda st=status: set_status_func(st))
            btns.append(btn)

        return btns



    def _bind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")