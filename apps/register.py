import tkinter as tk
from tkinter import ttk
from database import zitttpymongo
from ui_utilities import center_window
import subprocess


def create_register_ui():
    """Create Register UI"""
    root = tk.Tk()
    root.title("Register")
    center_window(root, 475, 250)
    root.resizable(False, False)

    # ---------- Wrapper ----------
    wrap = ttk.Frame(root, padding=20)
    wrap.place(relx=0.5, rely=0.5, anchor="center")

    card = ttk.Frame(wrap, padding=10)
    card.pack()

    # ---------- Variables ----------
    username = tk.StringVar()
    password1 = tk.StringVar()
    password2 = tk.StringVar()
    password_visible = tk.BooleanVar(value=False)
    message = tk.StringVar(value="")

    # ---------- Form ----------
    row = 0
    ttk.Label(card, text="Username").grid(row=row, column=0, padx=8, pady=6, sticky="e")
    ttk.Entry(card, textvariable=username, width=28).grid(row=row, column=1, padx=8, pady=6); row += 1

    ttk.Label(card, text="Password").grid(row=row, column=0, padx=8, pady=6, sticky="e")
    e_p1 = ttk.Entry(card, textvariable=password1, width=28, show="*")
    e_p1.grid(row=row, column=1, padx=8, pady=6); row += 1

    ttk.Label(card, text="Password (Verify)").grid(row=row, column=0, padx=8, pady=6, sticky="e")
    e_p2 = ttk.Entry(card, textvariable=password2, width=28, show="*")
    e_p2.grid(row=row, column=1, padx=8, pady=6); row += 1

    # ---------- Functions ----------
    def set_message(msg, color="#c62828"):
        message.set(msg)
        text_label.configure(foreground=color)

    def toggle_show():
        show = "" if password_visible.get() else "*"
        e_p1.config(show=show)
        e_p2.config(show=show)

    def back():
        root.destroy()
        subprocess.run(["python","login.py"])

    def save():
        u, p1, p2 = username.get().strip(), password1.get(), password2.get()

        if not all([u, p1, p2]):
            return set_message("Please fill all fields.")
        if len(p1) < 8:
            return set_message("Password must be at least 8 characters.")
        if p1 != p2:
            return set_message("Passwords do not match.")
        if len(u) < 3:
            return set_message("Username must be at least 3 characters.")

        if not zitttpymongo.create_register_user(u, p1):
            return set_message(f"Username '{u}' already exists.")
        set_message("Registered successfully", "#2e7d32")

    # ---------- Check Button ----------
    ttk.Checkbutton(
        card,
        text="Show passwords",
        variable=password_visible,
        command=toggle_show
    ).grid(row=row, column=1, sticky="w", padx=8); row += 1

    # ---------- Message ----------
    text_label = ttk.Label(card, textvariable=message, foreground="#c62828")
    text_label.grid(row=row, column=0, columnspan=2, pady=(2, 6)); row += 1

    # ---------- Buttons ----------
    btns = ttk.Frame(card)
    btns.grid(row=row, column=1, columnspan=2, pady=6)
    ttk.Button(btns, text="Back", width=6, command=back).pack(side="left", padx=6)

    btns.grid(row=row, column=0, columnspan=2, pady=0)
    ttk.Button(btns, text="Save", width=6, command=save).pack(side="left", padx=0)

    # ---------- Focus & Bind ----------
    card.grid_slaves(row=0, column=1)[0].focus()
    root.bind("<Return>", lambda e: save())

    return root


if __name__ == '__main__':
    app = create_register_ui()
    app.mainloop()
