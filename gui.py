import tkinter as tk
from tkinter import messagebox
import re

DATA_FILE = "students.data"


# ---------- Student and Database Class ----------
from data import Database, Student
# ---------- Main GUI Controller ----------
class GUIUniApp:
    def __init__(self, master,db: Database):
        self.master = master
        self.db = db
        db.load()
        self.login_window()

    # --- Window 1: Login ---
    def login_window(self):
        self.clear_window()
        self.master.title("GUIUniApp - Login")

        tk.Label(self.master, text="Login to GUIUniApp", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.master, text="Email:").pack()
        self.email_entry = tk.Entry(self.master, width=30)
        self.email_entry.pack()
        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master, show="*", width=30)
        self.password_entry.pack()
        self.password_entry.bind("<Return>", lambda event: self.login())

        tk.Button(self.master, text="Login", command=self.login).pack(pady=10)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Email and password cannot be empty!")
            return
        if not re.fullmatch(r'^[A-Za-z0-9._-]+@university.com$',email) or not re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',password) and len(password)>=5:
            messagebox.showerror("Error", "Invalid email format!")
            return
        try:
            student = self.db.login(email,password)
        except ValueError:
            messagebox.showerror("Error", "Incorrect email or password.")
            return

        self.current_student = student
        self.menu_window()

    # --- Window 2: Menu ---
    def menu_window(self):
        self.clear_window()
        self.master.title("GUIUniApp - Main Menu")

        tk.Label(self.master, text=f"Welcome, {self.current_student.email}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.master, text="Enrol in Subjects", command=self.enrolment_window).pack(pady=5)
        tk.Button(self.master, text="Change Password", command=self.change_password_window).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.login_window).pack(pady=5)

    # --- Window 3: Enrolment ---
    def enrolment_window(self):
        self.clear_window()
        self.master.title("GUIUniApp - Enrolment")

        tk.Label(self.master, text="Type Subject ID to Enrol", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.master, text="Subid:").pack()
        self.subid_entry = tk.Entry(self.master, width=30)
        self.subid_entry.pack()

        tk.Button(self.master, text="Enrol", command=self.enrol_subject).pack(pady=5)
        tk.Button(self.master, text="Remove", command=self.remove_subject, width=15).pack(pady=5)
        tk.Button(self.master, text="Show Enrolments", command=self.show_subjects, width=15).pack(pady=5)
        tk.Button(self.master, text="Back to Menu", command=self.menu_window).pack(pady=5)

        tk.Label(self.master, text="Your Enrolled Subjects:", font=("Arial", 12)).pack(pady=10)
        self.subject_listbox = tk.Listbox(self.master, width=40, height=6)
        self.subject_listbox.pack()
        self.update_subject_list()
    
    # --- Window 43: Change Passwod ---
    def change_password_window(self):
        self.clear_window()
        self.master.title("GUIUniApp - Change Password")

        tk.Label(self.master, text="Change Password", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.master, text="Old Password:").pack()
        self.old_password_entry = tk.Entry(self.master, show="*", width=30)
        self.old_password_entry.pack()

        tk.Label(self.master, text="New Password:").pack()
        self.new_password_entry = tk.Entry(self.master, show="*", width=30)
        self.new_password_entry.pack()

        tk.Button(self.master, text="Change Password", command=self.change_password).pack(pady=10)
        tk.Button(self.master, text="Back to Menu", command=self.menu_window).pack(pady=5)

    def change_password(self):
        old_password = self.old_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()

        if not re.fullmatch(r'^[A-Z][A-Za-z0-9._-]+[0-9]{3}$',new_password) and len(new_password)>=5:
            messagebox.showerror("Error", "New password format is invalid!")
            return
        try:
            self.current_student.change_password(old_password, new_password)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        self.db.datasave(self.current_student)
        messagebox.showinfo("Success", "Password changed successfully!")
        self.menu_window()
    def enrol_subject(self):
        try:
            self.current_student.enrol(self.subid_entry.get().strip().zfill(3))
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

        self.db.datasave(self.current_student)
        self.update_subject_list()
        messagebox.showinfo("Success", f"Successfully enrolled in {self.subid_entry.get().strip().zfill(3)}!")
    
    def remove_subject(self):
        try:
            self.current_student.drop(self.subid_entry.get().strip().zfill(3))
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

        self.db.datasave(self.current_student)
        self.update_subject_list()
        messagebox.showinfo("Success", f"Successfully removed {self.subid_entry.get().strip().zfill(3)}!")

    def show_subjects(self):
            if not self.current_student.subjects:
                messagebox.showinfo("Enrolments", "You are not enrolled in any subjects.")
            else:
                enrolled = ""
                for subject in self.current_student.subjects.values():
                    enrolled += f"[{subject.id}: mark={subject.mark}, grade={subject.grade}]\n"
                messagebox.showinfo("Enrolments", f"Currently enrolled subjects:\n\n{enrolled}")

    def update_subject_list(self):
        self.subject_listbox.delete(0, tk.END)
        for s in self.current_student.subjects:
            self.subject_listbox.insert(tk.END, s)

    # --- Utility ---
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    db= Database()
    app = GUIUniApp(root,db)
    root.geometry("400x400")
    root.mainloop()
