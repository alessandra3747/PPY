import tkinter as tk

from tkinter import messagebox
from utils.auth import AuthService
from ui.dashboard_window import DashboardWindow
from PIL import Image, ImageTk
from utils.exceptions import AuthorizationError
from utils.window_utils import center_window


class LoginWindow:

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("InsightEd – Login")
        self.master.configure(bg="#f5f7fb")

        center_window(self.master,800,600)

        self.auth = AuthService()
        self.show_password = False


        self.build_ui()



    def build_ui(self) -> None:

        main_frame = tk.Frame(self.master, bg="#f5f7fb")
        main_frame.pack(expand=True, fill="both")

        left_frame = tk.Frame(main_frame, bg="#f5f7fb", width=400)
        left_frame.pack(side="left", fill="both", padx=(40, 20), pady=40)


        try:
            logo_img = Image.open("assets/logo2.png")
            logo_img = logo_img.resize((350, 300))
            self.illustration = ImageTk.PhotoImage(logo_img)
            tk.Label(left_frame, image=self.illustration, bg="#f5f7fb").pack(pady=(0,80))
        except Exception:
            tk.Label(left_frame, text="InsightEd", font=("Verdana", 24, "bold"), bg="#f5f7fb", fg="#5e2d92").pack(pady=40)


        tk.Label(left_frame, text="Welcome back!", font=("Verdana", 18, "bold"), bg="#f5f7fb", fg="#333").pack()
        tk.Label(left_frame, text="Log in to your teaching space", font=("Verdana", 12), bg="#f5f7fb", fg="#666").pack(pady=5)

        right_frame = tk.Frame(main_frame, bg="white", bd=0, relief="flat")
        right_frame.pack(side="right", fill="both", expand=True, padx=(20, 40), pady=40)
        tk.Label(right_frame, text="Sign in", font=("Verdana", 24, "bold"),bg="white", fg="#5e2d92").pack(pady=(50, 40))


        tk.Label(right_frame, text="Login", font=("Verdana", 10), bg="white", anchor="w").pack(fill="x", padx=40)
        self.login_entry = tk.Entry(right_frame, font=("Verdana", 12), width=30, bd=1, relief="solid")
        self.login_entry.pack(pady=5, padx=40)


        tk.Label(right_frame, text="Password", font=("Verdana", 10), bg="white", anchor="w").pack(fill="x", padx=40,
                                                                                                pady=(10, 0))
        self.password_entry = tk.Entry(right_frame, show="*", font=("Verdana", 12), width=30, bd=1, relief="solid")
        self.password_entry.pack(pady=5, padx=40)

        self.toggle_password = tk.Button(right_frame, text="👁 Show password", command=self.toggle_password_visibility,bg="white", bd=0, fg="#5e2d92", font=("Verdana", 9, "underline"), cursor="hand2")
        self.toggle_password.pack(anchor="e", padx=40, pady=(0, 40))


        tk.Button(right_frame, text="Sign in", bg="#5e2d92", fg="white", font=("Verdana", 12, "bold"), width=25, height=2, bd=0, command=self.login).pack(pady=10, padx=40)

        forgot_label = tk.Label(right_frame, text="Forgot your password?", font=("Verdana", 9), fg="gray", bg="white", cursor="hand2")
        forgot_label.pack(pady=10)
        forgot_label.bind("<Button-1>", lambda e: self.forgot_password())



    def toggle_password_visibility(self) -> None:
        if self.show_password:
            self.password_entry.config(show="*")
            self.toggle_password.config(text="👁 Show password")
        else:
            self.password_entry.config(show="")
            self.toggle_password.config(text="🙈 Hide password")

        self.show_password = not self.show_password



    def login(self) -> None:
        username = self.login_entry.get()
        password = self.password_entry.get()

        try:
            auth_result = self.auth.authenticate(username, password)

            if auth_result[0] == "success":
                self.master.destroy()
                root = tk.Tk()
                DashboardWindow(root, username)
                root.mainloop()
            elif auth_result[0] == "blocked":
                messagebox.showerror("Error", f"Too many failed attempts. Please wait {auth_result[1]} seconds before trying again.")

        except AuthorizationError as e:
            messagebox.showerror("Error", e.args[0])



    def forgot_password(self) -> None:
        username = self.login_entry.get().strip()

        if not username:
            messagebox.showwarning("Missing Login", "Please enter your login first.")
            return

        user_data = self.auth.get_user_data(username)

        if not user_data:
            messagebox.showerror("User Not Found", f"No user found with login: {username}")
            return

        question = user_data.get("question")
        correct_answer = user_data.get("answer")

        if not question or not correct_answer:
            messagebox.showinfo("No Recovery Info", "No security question set for this user.")
            return

        answer = tk.simpledialog.askstring("Security Question", question)

        if answer and answer.strip().lower() == correct_answer.lower():
            messagebox.showinfo("Password Recovery", f"Your password: {user_data['password']}")
        else:
            messagebox.showerror("Wrong Answer", "Incorrect answer to the security question.")
