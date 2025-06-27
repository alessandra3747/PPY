import tkinter as tk
from typing import Optional

import matplotlib.pyplot as plt

from tkinter import ttk, messagebox
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.exceptions import JsonFileEmptyError
from utils.file_utils import load_students_from_file
from utils.reports_utils import *


class ReportsWindow(tk.Frame):

    def __init__(self, master: tk.Misc, group_name: Optional[str] = None) -> None:
        super().__init__(master, bg="white")

        self.pack(fill="both", expand=True)

        try:
            all_students = load_students_from_file()
        except JsonFileEmptyError:
            all_students = []

        self.students = [s for s in all_students if s.get("group") == group_name] if group_name else all_students

        self.current_chart = None

        self.top_frame = tk.Frame(self, bg="white")
        self.top_frame.pack(side="top", fill="x", padx=30, pady=(10, 5))

        self.create_button(text="📊 Average Grades", command=self.show_average_grades_chart, parent=self.top_frame)
        self.create_button(text="📘 Grades per Student", command=self.show_grades_per_student_chart, parent=self.top_frame)
        self.create_button(text="📍 Attendance Summary", command=self.show_attendance_chart, parent=self.top_frame)
        self.create_button(text="🎓 Attendance per Student", command=self.show_attendance_per_student_chart, parent=self.top_frame)

        self.bottom_frame = tk.Frame(self, bg="white")
        self.bottom_frame.pack(side="top", fill="x", padx=30, pady=(5, 10))

        self.create_button(text="📤 Export to Excel", command=self.export_to_excel, parent=self.bottom_frame)

        self.chart_frame = tk.Frame(self, bg="white")
        self.chart_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)



    def create_button(self, **kwargs) -> ttk.Button:
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Segoe UI", 10), padding=(5, 4), background="#E0E0E0", foreground="#333", relief="flat")
        style.map("Custom.TButton", background=[("active", "#d6d6d6")], relief=[("pressed", "sunken")])

        parent = kwargs.pop("parent", None)
        if parent is None:
            raise ValueError("You must provide a 'parent' argument.")

        text = kwargs.get("text", "")
        button = ttk.Button(parent, style="Custom.TButton", **kwargs)

        if text == "📤 Export to Excel":
            button.pack(side="top", padx=5)
        else:
            button.pack(side="left", padx=5)

        return button



    def draw_chart(self) -> None:
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)



    def show_average_grades_chart(self) -> None:
        try:
            data = calculate_average_grades(self.students)
        except NoGradesToAnalyzeError:
            return

        labels = [d["Student"] for d in data]
        averages = [d["Average Grade"] for d in data]

        plt.close('all')
        plt.figure(figsize=(8, 4), dpi=100)

        if not averages:
            plt.text(0.5, 0.5, "No grades to analyze", ha='center', va='center')
            plt.axis('off')
        else:
            plt.barh(labels, averages, color="#2196F3")
            plt.title("Average grades of students")
            plt.xlabel("Average")
            plt.ylabel("Student")
            plt.yticks(rotation=45, ha="right", fontsize=7)

            plt.gca().invert_yaxis()

        self.draw_chart()
        self.current_chart = "average_grades"



    def show_grades_per_student_chart(self) -> None:
        data = grades_per_student(self.students)

        if not data:
            plt.close('all')
            plt.figure(figsize=(6, 5), dpi=100)
            plt.text(0.5, 0.5, "No grades data to analyze", ha='center', va='center')
            plt.axis('off')
            self.draw_chart()
            self.current_chart = "grades_per_student"
            return

        labels = [d["Student"] for d in data]
        all_grades = sorted({grade for d in data for grade in d if grade != "Student"}, key=float)

        plt.close('all')
        plt.figure(figsize=(10, 5), dpi=100)

        bottom = [0] * len(labels)

        for grade in all_grades:
            values = [d.get(grade, 0) for d in data]
            plt.bar(labels, values, bottom=bottom, label=grade)
            bottom = [b + v for b, v in zip(bottom, values)]

        plt.title("Grades per student")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right", fontsize=7)
        plt.legend(title="Grade")

        self.draw_chart()
        self.current_chart = "grades_per_student"



    def show_attendance_chart(self) -> None:
        try:
            counts = count_attendance_summary(self.students)
        except AttendanceError:
            return

        plt.close('all')
        plt.figure(figsize=(5, 5), dpi=100)

        total = sum(counts.values())
        if total == 0:
            plt.text(0.5, 0.5, "No attendance data to analyze", ha='center', va='center')
            plt.axis('off')
        else:
            labels, values, colors = [], [], []

            if counts["Present"] > 0:
                labels.append("Present")
                values.append(counts["Present"])
                colors.append("#4CAF50")
            if counts["Absent"] > 0:
                labels.append("Absent")
                values.append(counts["Absent"])
                colors.append("#FF5722")
            if counts["Late"] > 0:
                labels.append("Late")
                values.append(counts["Late"])
                colors.append("#FFC107")
            if counts["Excused"] > 0:
                labels.append("Excused")
                values.append(counts["Excused"])
                colors.append("#9E9E9E")

            plt.pie(values, labels=labels, autopct="%1.1f%%", colors=colors)
            plt.title("Attendance summary")

        self.draw_chart()
        self.current_chart = "attendance_summary"



    def show_attendance_per_student_chart(self) -> None:
        data = attendance_per_student(self.students)

        labels = [d["Student"] for d in data]
        present = [d["Present"] for d in data]
        absent = [d["Absent"] for d in data]
        late = [d["Late"] for d in data]
        excused = [d["Excused"] for d in data]

        plt.close('all')
        plt.figure(figsize=(8, 5), dpi=100)

        if not any(present + absent + late + excused):
            plt.text(0.5, 0.5, "No attendance data to analyze", ha='center', va='center')
            plt.axis('off')
        else:
            x = list(range(len(labels)))
            p = plt.bar(x, present, color="#4CAF50", label="Present")
            a = plt.bar(x, absent, bottom=present, color="#F44336", label="Absent")
            bottom_late = [p + a for p, a in zip(present, absent)]
            l = plt.bar(x, late, bottom=bottom_late, color="#FFC107", label="Late")
            bottom_excused = [p + a + l for p, a, l in zip(present, absent, late)]
            e = plt.bar(x, excused, bottom=bottom_excused, color="#9E9E9E", label="Excused")

            plt.title("Students attendance")
            plt.ylabel("Amount of occurrences")
            plt.xticks(x, labels, rotation=45, ha="right", fontsize=7)
            plt.legend()

        self.draw_chart()
        self.current_chart = "attendance_per_student"



    def export_to_excel(self) -> None:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        file_name = f"reports/report_{self.current_chart}_{now}.xlsx"

        try:

            if self.current_chart == "average_grades":
                try:
                    data = calculate_average_grades(self.students)
                except NoGradesToAnalyzeError:
                    return
                export_data_to_excel(data, file_name)


            elif self.current_chart == "grades_per_student":
                data = grades_per_student(self.students)
                export_data_to_excel(data, file_name)



            elif self.current_chart == "attendance_summary":
                try:
                    counts = count_attendance_summary(self.students)
                except AttendanceError:
                    return

                data = [{"Status": k, "Count": v} for k, v in counts.items()]
                export_data_to_excel(data, file_name)


            elif self.current_chart == "attendance_per_student":
                data = attendance_per_student(self.students)
                export_data_to_excel(data, file_name)


            else:
                messagebox.showinfo("Export", "No data to export.")
                return


            messagebox.showinfo("Export", f"Exported file to:\n{file_name}")

        except Exception as e:
            messagebox.showerror("Error while exporting xlsx file", str(e))
