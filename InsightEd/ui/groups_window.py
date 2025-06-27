import tkinter as tk

from typing import Callable, Optional, Dict, List
from ui.components.group_tile import GroupTile


class GroupsWindow(tk.Frame):

    def __init__(self, parent: tk.Widget, show_students_callback: Callable[[str, Optional[str]], None],
                 current_user: str, user_groups: Dict[str, List[str]]) -> None:

        super().__init__(parent)
        self.configure(bg="#f5f7fb")

        self.show_students_callback = show_students_callback
        self.current_user = current_user
        self.user_groups = user_groups

        self.selected_team = None

        self.create_header()
        self.create_content()

        self.bind("<Configure>", self.on_resize)



    def create_header(self) -> None:
        self.header = tk.Frame(self, bg="#f5f7fb", height=50)
        self.header.pack(side="top", fill="x")

        title = tk.Label(self.header, text="Your Groups", bg="#f5f7fb", fg="#5e2d92", font=("Verdana", 20))

        title.pack(side="left", padx=30, pady=10)



    def create_content(self) -> None:
        self.canvas = tk.Canvas(self, bg="#f5f7fb", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f7fb")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.scrollbar.pack(side="right", fill="y")

        self.group_tiles = []

        groups = self.user_groups.get(self.current_user, [])

        for g in groups:
            tile = GroupTile(self.scrollable_frame, g, self.toggle_group, self.show_context_menu)
            self.group_tiles.append(tile)

        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        self.arrange_groups()



    def arrange_groups(self) -> None:
        width = self.canvas.winfo_width()

        if width == 1:
            width = self.winfo_width() - 40

        tile_width = 200

        columns = max(1, width // tile_width)

        for idx, tile in enumerate(self.group_tiles):
            tile.grid_forget()
            row = idx // columns
            col = idx % columns
            tile.grid(row=row, column=col, padx=10, pady=10)



    def toggle_group(self, group_name: str) -> None:
        for tile in self.group_tiles:
            if tile.group_name == group_name:
                if tile.expanded:
                    tile.collapse()
                    self.selected_team = None
                else:
                    tile.expand()
                    self.selected_team = group_name
            else:
                tile.collapse()



    def on_resize(self, event: tk.Event) -> None:
        if hasattr(self, 'group_tiles'):
            self.arrange_groups()



    def show_context_menu(self, event: tk.Event, group_name: str) -> None:
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Students & Grades", command=lambda: self.show_students_callback("Students", group_name))
        menu.add_command(label="Attendance", command=lambda: self.show_students_callback("Attendance", group_name))
        menu.add_command(label="Reports", command=lambda: self.show_students_callback("Reports", group_name))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()



    def _bind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event: tk.Event) -> None:
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
