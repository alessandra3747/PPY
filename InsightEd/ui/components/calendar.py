import os
import tkinter as tk

from typing import Any
from tkcalendar import Calendar
from PIL import Image, ImageTk
from ui.components.notes import on_date_selected
from utils.exceptions import LogoFileNotFoundError


def create_calendar(center_frame: tk.Widget, parent_component: Any) -> None:
    try:
        logo_path = os.path.join("assets", "logo.png")

        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((160, 130))
            parent_component.logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(center_frame, image=parent_component.logo_img, bg="white")
            logo_label.pack(pady=(15, 5))
        else:
            raise LogoFileNotFoundError

    except LogoFileNotFoundError:
        logo_label = tk.Label(center_frame, text="InsightEd", font=("Verdana", 24, "bold"), bg="#f5f7fb", fg="#5e2d92")
        logo_label.pack(pady=(15, 5))


    parent_component.calendar = Calendar(center_frame, selectmode="day", year=parent_component.selected_date.year,
                             month=parent_component.selected_date.month, day=parent_component.selected_date.day,
                             date_pattern="yyyy-mm-dd", font=("Verdana", 13), selectforeground="white", selectbackground="#5e2d92")

    parent_component.calendar.pack(pady=(40, 10))
    parent_component.calendar.bind("<<CalendarSelected>>", lambda event: on_date_selected(parent_component))

