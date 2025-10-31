import tkinter as tk
from tkinter import messagebox
from database import zitttpymongo
from ui_utilities import center_window
import subprocess

def toggle_password(entry, var):
    """สลับการแสดงรหัสผ่าน"""
    entry.config(show="" if var.get() else "*")

def login(username_var, password_var):
    """ตรวจสอบบัญชี"""
    username = username_var.get()
    password = password_var.get()

    is_valid_user = zitttpymongo.is_exists_user(username,password)
    if is_valid_user:
        root.destroy()
        subprocess.run(["python", "core.py", username])
    else:
        # msg_label.config(text="Incorrect username or password.", fg="red")
        messagebox.showinfo("Info", "Incorrect username or password.")


def open_register():
    """ไปยัง Register UI"""
    root.destroy()
    subprocess.run(["python", "register.py"])

def create_login_ui(root):
    """Main UI"""
    center_window(root, 450, 230)
    root.title("เข้าสู่ระบบ")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(expand=True)

    # Labels
    tk.Label(frame, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    tk.Label(frame, text="Password").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # Users Input
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    username_entry = tk.Entry(frame, textvariable=username_var, width=22)
    password_entry = tk.Entry(frame, textvariable=password_var, width=22, show="*")

    username_entry.grid(row=0, column=1, padx=5, pady=10)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Checkbox show password
    show_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        frame, text="แสดงรหัสผ่าน", variable=show_var,
        command=lambda: toggle_password(password_entry, show_var)
    ).grid(row=2, column=1, sticky="w", padx=5)

    # Login , Register
    btn_row = tk.Frame(frame)
    btn_row.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Button(
        btn_row, text="เข้าสู่ระบบ", width=10,
        command=lambda: login(username_var, password_var)
    ).pack(side="left", padx=6)

    tk.Button(
        btn_row, text="ลงทะเบียน", width=10,
        command=open_register
    ).pack(side="left", padx=6)

    # Trigger ปุ่ม Login
    root.bind("<Return>", lambda e: login(username_var, password_var))
    username_entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    create_login_ui(root)
    root.mainloop()
