import tkinter as tk
from tkinter import ttk
from datetime import datetime

# ---------- Window & center ----------
root = tk.Tk()
root.title("Register")
W, H = 420, 300
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
x, y = (sw - W)//2, (sh - H)//2
root.geometry(f"{W}x{H}+{x}+{y}")
root.minsize(380, 280)

# ---------- Card centered ----------
wrap = ttk.Frame(root, padding=20)
wrap.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(wrap, text="Create Account", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
card = ttk.Frame(wrap, padding=10)
card.pack()

# ---------- Vars ----------
user  = tk.StringVar()
password1 = tk.StringVar()
password2 = tk.StringVar()
dob = tk.StringVar() #date of birth
c_password = tk.BooleanVar(value=False) #ตัวเช็คว่า password เหมือนกันมั้ย
text = tk.StringVar(value="") #ข้อความแสดงผล

# ---------- Form ----------
row = 0
ttk.Label(card, text="Username").grid(row=row, column=0, padx=8, pady=6, sticky="e")
ttk.Entry(card, textvariable=user, width=28).grid(row=row, column=1, padx=8, pady=6); row += 1

ttk.Label(card, text="Password").grid(row=row, column=0, padx=8, pady=6, sticky="e")
e_p1 = ttk.Entry(card, textvariable=password1, width=28, show="*")
e_p1.grid(row=row, column=1, padx=8, pady=6); row += 1

ttk.Label(card, text="Password (Verify)").grid(row=row, column=0, padx=8, pady=6, sticky="e")
e_p2 = ttk.Entry(card, textvariable=password2, width=28, show="*")
e_p2.grid(row=row, column=1, padx=8, pady=6); row += 1

ttk.Label(card, text="Birth of Date (YYYY-MM-DD)").grid(row=row, column=0, padx=8, pady=6, sticky="e")
ttk.Entry(card, textvariable=dob, width=28).grid(row=row, column=1, padx=8, pady=6); row += 1

def toggle_show():
    show = "" if c_password.get() else "*"
    e_p1.config(show=show)
    e_p2.config(show=show)

ttk.Checkbutton(card, text="Show passwords", variable=c_password,
                command=toggle_show).grid(row=row, column=1, sticky="w", padx=8); row += 1

text_label = ttk.Label(card, textvariable=text, foreground="#c62828")
text_label.grid(row=row, column=0, columnspan=2, pady=(2, 6)); row += 1

def save():
    u, p1, p2, dateofbirth = user.get().strip(), password1.get(), password2.get(), dob.get().strip()

    if not u or not p1 or not p2 or not dateofbirth: # ตรวจช่องว่าง
        text.set("Please fill all fields."); text_label.configure(foreground="#c62828"); return

    if len(p1) < 8:
        text.set("Password must be at least 8 characters."); text_label.configure(foreground="#c62828"); return
    # ตรวจรหัสซ้ำ
    if p1 != p2:
        text.set("Passwords do not match."); text_label.configure(foreground="#c62828"); return
    # ตรวจรูปแบบวันเกิด
    try:
        datetime.strptime(dateofbirth, "%Y-%m-%d")
    except ValueError:
        text.set("Invalid date. Use YYYY-MM-DD."); text_label.configure(foreground="#c62828"); return

    # ผ่านทั้งหมด
    text.set(f"Registered successfully: {u}")
    text_label.configure(foreground="#2e7d32")



btns = ttk.Frame(card)
btns.grid(row=row, column=0, columnspan=2, pady=6)
ttk.Button(btns, text="Save", width=12, command=save).pack(side="left", padx=6)


# ให้โฟกัสช่องแรก
entry_user = card.grid_slaves(row=0, column=1)[0]
entry_user.focus()

# Enter = Save
root.bind("<Return>", lambda e: save())
root.mainloop()
