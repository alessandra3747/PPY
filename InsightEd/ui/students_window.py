import tkinter as tk

from tkinter import simpledialog, messagebox
from typing import List, Dict, Optional

from ui.attendance_window import AttendanceWindow
from ui.components.grade_dialog import GradeDialog, EditGradesDialog
from ui.components.student_dialog import StudentDialog
from utils.file_utils import save_students_to_file
from utils.window_utils import center_window


class StudentsWindow(tk.Frame):

    def __init__(self, parent: tk.Widget, students_list: List[Dict[str, any]], group_name: Optional[str] = None) -> None:
        super().__init__(parent, bg="white")

        self.all_students = students_list
        self.group_name = group_name

        self.student_frames = {}

        self.selected_student_index = None

        self.filter_students()
        self.create_widgets()


    @property
    def all_students(self) -> List[Dict[str, any]]:
        return self._all_students

    @all_students.setter
    def all_students(self, value: List[Dict[str, any]]) -> None:
        print("Setting all_students with", len(value), "students")
        self._all_students = value



    def create_widgets(self) -> None:
        title = f"📋 Students in {self.group_name}" if self.group_name else "📋 All Students"
        tk.Label(self, text=title, font=("Verdana", 16, "bold"), bg="white", fg="#5e2d92").pack(pady=30)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var, width=40)
        search_entry.pack(pady=(10, 0))
        search_entry.bind("<KeyRelease>", self.perform_search)

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=5)

        self.edit_button = tk.Button(button_frame, text="Edit Student", state="disabled", command=self.edit_student)
        self.edit_button.pack(side="left", padx=5)

        tk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)

        list_container = tk.Frame(self, bg="white")
        list_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(list_container, bg="white", highlightthickness=0)


        self.v_scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(list_container, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")

        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        self.update_students()



    def perform_search(self, event: Optional[tk.Event] = None) -> None:
        query = self.search_var.get().strip().lower()

        if not query:
            self.filter_students()
        else:
            def matches(student):
                full_name = f"{student['first_name']} {student['last_name']}".lower()
                return (query in full_name or query in student["pesel"])

            self.students = [s for s in self._all_students if
                    ( not self.group_name or self.group_name.lower() == "all" or s.get( "group") == self.group_name )
                    and matches(s) ]

        self.update_students()



    def update_students(self) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.student_frames = {}

        for idx, student in enumerate(self.students):
            row = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
            row.pack(fill="x", pady=2)

            student_str = f"{student['first_name']} {student['last_name']} ({student['pesel']})"

            label = tk.Label(row, text=student_str, bg="white", anchor="w", width=30)
            label.pack(side="left", padx=5)
            label.bind("<Button-1>", lambda e, i=idx: self.select_student(i))

            self.student_frames[idx] = {"frame": row, "label": label}

            grades_frame = tk.Frame(row, bg="white")
            grades_frame.pack(side="left", padx=5)

            for g in student["grades"]:
                color = "#e0e0ff"
                btn = tk.Button(grades_frame, text=str(g["value"]), bg=color, width=3, command=lambda g=g: self.show_grade_details(g))
                btn.pack(side="left", padx=2)

            buttons_frame = tk.Frame(row, bg="white")
            buttons_frame.pack(side="right", padx=5)

            btn_add = tk.Button(buttons_frame, text="Add Grade", width=10, command=lambda i=idx: self.add_grade(i))
            btn_edit = tk.Button(buttons_frame, text="Edit Grades", width=10, command=lambda i=idx: self.edit_grades(i))
            btn_avg = tk.Button(buttons_frame, text="Calc Average", width=10, command=lambda i=idx: self.calc_average(i))
            btn_attendance = tk.Button(buttons_frame, text="Attendance", width=10, command=lambda i=idx: self.show_attendance_window(i))

            for b in (btn_add, btn_edit, btn_avg, btn_attendance):
                b.pack(side="left", padx=2, pady=2)



    def show_attendance_window(self, index: int) -> None:
        student = self.students[index]
        group = student.get("group", "Unknown")

        top = tk.Toplevel(self)
        title_text = f"Attendance for {student['first_name']} {student['last_name']}"
        top.title(title_text)

        center_window(top, 600, 400)

        view = AttendanceWindow(top, [student], group_name=group, title_text=title_text)
        view.pack(fill="both", expand=True)



    def filter_students(self) -> None:
        if not self.group_name or self.group_name.lower() == "all":
            self.students = self._all_students.copy()
        else:
            self.students = [s for s in self._all_students if s.get("group") == self.group_name]



    def select_student(self, index: int) -> None:
        self.selected_student_index = index
        self.edit_button.config(state="normal")

        for i, widgets in self.student_frames.items():
            if i == index:
                widgets["frame"].config(highlightbackground="#5e2d92", highlightthickness=1, bd=1)
            else:
                widgets["frame"].config(highlightthickness=0, bd=1)



    def add_student(self) -> None:
        group = self.group_name

        if not group or group.lower() == "all":
            group_input = simpledialog.askstring("Group", "Enter group (number) for the new student:")

            if not group_input or not group_input.strip():
                messagebox.showerror("Error", "Group is required!")
                return

            try:
                group = "Group " + str(int(group_input.strip()))
            except ValueError:
                messagebox.showerror("Error", "Group must be a number!")
                return


        dialog = StudentDialog(self, title="Add Student")
        if dialog.result:
            student = dialog.result
            student["group"] = group
            self._all_students.append(student)
            save_students_to_file(self._all_students)

            self.filter_students()
            self.update_students()
            messagebox.showinfo("Success", f"Added student to group {group}.")



    def edit_student(self) -> None:
        if self.selected_student_index is None:
            messagebox.showwarning("Warning", "No student selected!")
            return

        student = self.students[self.selected_student_index]
        dialog = StudentDialog(self, title="Edit Student", student=student, all_students=self._all_students, save_callback=save_students_to_file)

        if dialog.result is None:
            self.filter_students()
            self.update_students()
            return

        idx_in_all = self._all_students.index(student)
        self._all_students[idx_in_all] = dialog.result

        save_students_to_file(self._all_students)

        self.filter_students()
        self.update_students()

        messagebox.showinfo("Success", "Student updated.")



    def add_grade(self, index):
        student = self.students[index]
        dialog = GradeDialog(self, title="Add Grade")
        if dialog.result:
            student["grades"].append(dialog.result)
            save_students_to_file(self._all_students)
            self.update_students()
            messagebox.showinfo("Success", f"Added new grade for {student['first_name']}.")



    def edit_grades(self, index: int) -> None:
        student = self.students[index]
        dialog = EditGradesDialog(self, student["grades"])
        if dialog.result is not None:
            student["grades"] = dialog.result
            save_students_to_file(self._all_students)
            self.update_students()
            messagebox.showinfo("Success", "Grades updated successfully.")



    def show_grade_details(self, grade: Dict[str, any]) -> None:
        details = f"Grade: {grade['value']}\nForm: {grade['form']}\nDate: {grade['date']}\nNotes: {grade['notes']}"
        messagebox.showinfo("Grade Details", details)



    def calc_average(self, index: int) -> None:
        grades = self.students[index]["grades"]
        values = [g["value"] for g in grades if isinstance(g["value"], (int, float))]
        avg = sum(values) / len(values) if values else 0
        messagebox.showinfo("Average", f"Student's average: {avg:.2f}")



    def _bind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
