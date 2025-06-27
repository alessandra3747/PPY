import tkinter as tk
import datetime
from typing import Optional

from ui.attendance_window import AttendanceWindow
from ui.components.calendar import create_calendar
from ui.components.notes import create_notes, save_current_note
from ui.components.sidebar import create_sidebar
from ui.groups_window import GroupsWindow
from ui.reports_window import ReportsWindow
from ui.students_window import StudentsWindow
from utils.exceptions import JsonFileEmptyError, NoWarningsFoundException, UnknownWindowError, UsersFileNotFoundError
from utils.file_utils import load_students_from_file, load_notes_from_file, load_users
from utils.window_utils import center_window
from utils.warning_utils import generate_warnings


class DashboardWindow(tk.Frame):

    def __init__(self, master: tk.Tk, current_user: str) -> None:
        super().__init__(master)

        self.master.title("InsightEd – Dashboard")
        self.master.configure(bg="#f5f7fb")

        self.content_frame = None
        self.current_user = current_user

        center_window(self.master,1000,800)
        self.pack(fill="both", expand=True)

        self.create_widgets()



    def create_widgets(self) -> None:
        main_frame = tk.Frame(self, bg="#f5f7fb")
        main_frame.pack(fill="both", expand=True)

        create_sidebar(main_frame, self.show_window)

        self.content_frame = tk.Frame(main_frame, bg="white", bd=2, relief="solid")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.show_window("Dashboard")



    def show_window(self, window_name: str, group_name: Optional[str] = None) -> None:
        if hasattr(self, 'notes') and hasattr(self, 'selected_date'):
            save_current_note(self)

        self.master.unbind_all("<MouseWheel>")

        for widget in self.content_frame.winfo_children():
            widget.destroy()



        if window_name == "Dashboard":
            self.notes = load_notes_from_file(self.current_user)
            self.selected_date = datetime.date.today()
            create_calendar(self.content_frame, self)
            create_notes(self.content_frame, self)



        elif window_name == "Students":
            try:
                all_students = load_students_from_file()
            except JsonFileEmptyError:
                all_students = []

            students_view = StudentsWindow(self.content_frame, all_students, group_name=group_name)
            students_view.pack(fill="both", expand=True)



        elif window_name == "Groups":
            try:
                users_data = load_users()
            except UsersFileNotFoundError:
                users_data = {}

            user_groups = {self.current_user: users_data.get(self.current_user, {}).get("groups", [])}
            groups_view = GroupsWindow(self.content_frame, show_students_callback=self.show_window, current_user=self.current_user, user_groups=user_groups)
            groups_view.pack(fill="both", expand=True)



        elif window_name == "Attendance":
            try:
                all_students = load_students_from_file()
            except JsonFileEmptyError:
                all_students = []

            if group_name:
                all_students = [s for s in all_students if s.get("group") == group_name]
            attendance_view = AttendanceWindow(self.content_frame, all_students, group_name=group_name)
            attendance_view.pack(fill="both", expand=True)



        elif window_name == "Reports":
            reports_view = ReportsWindow(self.content_frame, group_name=group_name)
            reports_view.pack(fill="both", expand=True)



        elif window_name == "Warnings":
            try:
                all_students = load_students_from_file()
            except JsonFileEmptyError:
                all_students = []

            try:
                warnings = generate_warnings(all_students)

                tk.Label(self.content_frame, text="⚠️ Students warnings", font=("Verdana", 16, "bold"),
                         bg="white").pack(pady=(20, 10))

                for warning in warnings:
                    frame = tk.Frame(self.content_frame, bg="#fff5f5", bd=1, relief="solid")
                    frame.pack(padx=20, pady=10, fill="x")
                    name = warning['name']
                    index = warning['index']
                    reason = warning['reason']
                    tk.Label(frame, text=f"{name} ({index})", font=("Verdana", 12, "bold"), bg="#fff5f5", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
                    tk.Label(frame, text=f"Reason: {reason}", font=("Verdana", 11), bg="#fff5f5", anchor="w", fg="red").pack(fill="x", padx=10, pady=(0, 5))

            except NoWarningsFoundException:
                tk.Label(self.content_frame, text="No warnings.", font=("Verdana", 12), bg="white").pack(pady=20)

        else:
            raise UnknownWindowError("Unknown window type")