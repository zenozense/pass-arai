import tkinter as tk

root = tk.Tk()
root.title("Login")
root.geometry("400x250")

valid_users = {"admin": "1234", "tian": "pscp"} #ตัวอย่างทดลอง user : password

# ---------- ทำให้อยู่ตรงกลาง ----------
frame = tk.Frame(root)
frame.pack(expand=True)


tk.Label(frame, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Label(frame, text="Password").grid(row=1, column=0, padx=10, pady=5, sticky="e")

#---------u = user, p = password----------
u_var = tk.StringVar()
p_var = tk.StringVar()
u_entry = tk.Entry(frame, textvariable=u_var, width=22)
p_entry = tk.Entry(frame, textvariable=p_var, width=22, show="*")
u_entry.grid(row=0, column=1, padx=5, pady=10)
p_entry.grid(row=1, column=1, padx=5, pady=5)

msg = tk.Label(frame, text="", fg="red")
msg.grid(row=3, column=0, columnspan=2, pady=8)

#-------------ปุ่มแสดง password------------
show_var = tk.BooleanVar(value=False)
tk.Checkbutton(
    frame, text="Show password", variable=show_var,
    command=lambda: p_entry.config(show="" if show_var.get() else "*")
).grid(row=2, column=1, sticky="w", padx=5)

#-------------login and regis-------------------
btn_row = tk.Frame(frame)
btn_row.grid(row=4, column=0, columnspan=2, pady=5)

login_btn = tk.Button(
    btn_row, text="Login", width=10,
    command=lambda: (
        msg.config(
            text=("login successful" if valid_users.get(u_var.get()) == p_var.get() else "Incorrect username or password."),
            fg=("green" if valid_users.get(u_var.get()) == p_var.get() else "red")
        )
    )
)
login_btn.pack(side="left", padx=6)

register_btn = tk.Button(
    btn_row, text="Register", width=10,
    command=lambda: msg.config(text="Go to Register (not done)", fg="blue")
)
register_btn.pack(side="left", padx=6)

root.bind("<Return>", lambda e: login_btn.invoke())
u_entry.focus()
root.mainloop()
