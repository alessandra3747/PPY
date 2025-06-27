import tkinter as tk
from typing import Callable


class GroupTile(tk.Frame):

    def __init__(self, parent: tk.Widget, group_name: str, toggle_callback: Callable[[str], None],
                 right_click_callback: Callable[[tk.Event, str], None]) -> None:

        super().__init__(parent, width=180, height=100, bg="#ffffff", highlightthickness=1, highlightbackground="#ddd")

        self.group_name = group_name
        self.toggle_callback = toggle_callback
        self.right_click_callback = right_click_callback
        self.expanded = False

        self.pack_propagate(False)

        self.label = tk.Label(self, text=group_name, bg="#ffffff", fg="#5e2d92", font=("Segoe UI", 12, "bold"), wraplength=160, justify="center")
        self.label.pack(expand=True, fill="both", padx=10, pady=10)

        self.bind("<Button-1>", self.on_left_click)
        self.label.bind("<Button-1>", self.on_left_click)

        self.bind("<Button-3>", self.on_right_click)
        self.label.bind("<Button-3>", self.on_right_click)



    def on_left_click(self, event: tk.Event) -> None:
        self.toggle_callback(self.group_name)
        self.right_click_callback(event, self.group_name)
        self.toggle_callback(self.group_name)


    def on_right_click(self, event: tk.Event) -> None:
        self.right_click_callback(event, self.group_name)



    def expand(self) -> None:
        self.config(bg="#e5d8f7", highlightbackground="#5e2d92")
        self.label.config(bg="#e5d8f7")
        self.expanded = True



    def collapse(self) -> None:
        self.config(bg="#ffffff", highlightbackground="#ddd")
        self.label.config(bg="#ffffff")
        self.expanded = False
