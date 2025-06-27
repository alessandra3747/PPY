import tkinter as tk
from ui.login_window import LoginWindow
from utils.exceptions import UnknownWindowError


def main():
    root = tk.Tk()

    try:
        LoginWindow(root)
    except UnknownWindowError as e:
        return print(e)

    root.mainloop()

if __name__ == "__main__":
    main()
