import tkinter as tk

def center_window(window, width=450, height=230):
    """จัดหน้าต่างให้อยู่ตรงกลางจอ"""
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def toggle_password(entry, var):
    """สลับการแสดงรหัสผ่าน"""
    entry.config(show="" if var.get() else "*")


def login(username_var, password_var, msg_label, valid_users):
    """ตรวจสอบบัญชี"""
    username = username_var.get()
    password = password_var.get()

    if valid_users.get(username) == password:
        msg_label.config(text="Login successful!", fg="green")
    else:
        msg_label.config(text="Incorrect username or password.", fg="red")


def register():
    """ไปยัง Register UI"""
    print("555")


def create_login_ui(root):
    """Main UI"""
    center_window(root, 450, 230)
    root.title("Pass Arai – Login")
    root.resizable(False, False)

    valid_users = {"admin": "1234", "tian": "pscp"}  # mock data

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
        frame, text="Show password", variable=show_var,
        command=lambda: toggle_password(password_entry, show_var)
    ).grid(row=2, column=1, sticky="w", padx=5)

    # Login Status Labels
    msg_label = tk.Label(frame, text="", fg="red")
    msg_label.grid(row=3, column=0, columnspan=2, pady=8)

    # Login , Register
    btn_row = tk.Frame(frame)
    btn_row.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Button(
        btn_row, text="Login", width=10,
        command=lambda: login(username_var, password_var, msg_label, valid_users)
    ).pack(side="left", padx=6)

    tk.Button(
        btn_row, text="Register", width=10,
        command=register
    ).pack(side="left", padx=6)

    # Trigger ปุ่ม Login
    root.bind("<Return>", lambda e: login(username_var, password_var, msg_label, valid_users))
    username_entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    create_login_ui(root)
    root.mainloop()
