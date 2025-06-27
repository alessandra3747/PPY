import tkinter as tk
from typing import Callable


def create_sidebar(main_frame: tk.Widget, on_select_callback: Callable[[str], None]) -> None:
    sidebar = tk.Frame(main_frame, bg="#5e2d92", width=180)
    sidebar.pack(side="left", fill="y")

    options = [("🏠", "Dashboard"), ("📁", "Groups"), ("👥", "Students"), ("📑", "Reports"), ("⚠️", "Warnings")]

    for icon, label in options:
        font_size = 15 if label == "Dashboard" else 13

        btn = tk.Label(sidebar, text=f"{icon}  {label}",
                       font=("Verdana", font_size, "bold" if label == "Dashboard" else "normal"),
                       bg="#5e2d92", fg="white", pady=20, padx=10, anchor="w", cursor="hand2")

        btn.pack(fill="x", padx=10, pady=2)

        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#7648b0"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#5e2d92"))
        btn.bind("<Button-1>", lambda e, view=label: on_select_callback(view))


    exit_btn = tk.Button(sidebar, text="🚪 Exit", font=("Verdana", 12), bg="#5e2d92", fg="white", bd=0, cursor="hand2",
                         activebackground="#7648b0", activeforeground="white", command=main_frame.quit)
    exit_btn.pack(side="bottom", fill="x", padx=10, pady=10)
