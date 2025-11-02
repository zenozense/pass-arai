import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import db
import secrets
import string
import math
from datetime import datetime
import pytz

# ---------- Global Functions ----------
def center_window(window, width, height): # 450, 230
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def toggle_password(entry, var):
    entry.config(show="" if var.get() else "*")

def login(root, username_var, password_var):
    username = username_var.get()
    password = password_var.get()

    is_valid_user = db.is_exists_user(username, password)
    if is_valid_user:
        root.destroy()
        app = App(username)
        app.mainloop()
    else:
        messagebox.showinfo("Info", "Incorrect username or password.")

def open_register(root):
    root.destroy()
    register_root = create_register_ui()
    register_root.mainloop()

def create_login_ui(root):
    center_window(root, 450, 230)
    root.title("เข้าสู่ระบบ")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(expand=True)

    # ---------- Labels ----------
    tk.Label(frame, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    tk.Label(frame, text="Password").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # ---------- User Input ----------
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    username_entry = tk.Entry(frame, textvariable=username_var, width=22)
    password_entry = tk.Entry(frame, textvariable=password_var, width=22, show="*")

    username_entry.grid(row=0, column=1, padx=5, pady=10)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # ---------- Show Password ----------
    show_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        frame, text="แสดงรหัสผ่าน", variable=show_var,
        command=lambda: toggle_password(password_entry, show_var)
    ).grid(row=2, column=1, sticky="w", padx=5)

    # ---------- Register / Login Buttons ----------
    btn_row = tk.Frame(frame)
    btn_row.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Button(
        btn_row, text="เข้าสู่ระบบ", width=10,
        command=lambda: login(root, username_var, password_var)
    ).pack(side="left", padx=6)

    tk.Button(
        btn_row, text="ลงทะเบียน", width=10,
        command=lambda: open_register(root)
    ).pack(side="left", padx=6)

    # Trigger ปุ่ม Login
    root.bind("<Return>", lambda e: login(root, username_var, password_var))
    username_entry.focus()

def create_register_ui():
    root = tk.Tk()
    root.title("ลงทะเบียน")
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
    ttk.Entry(card, textvariable=username, width=28).grid(row=row, column=1, padx=8, pady=6);
    row += 1

    ttk.Label(card, text="Password").grid(row=row, column=0, padx=8, pady=6, sticky="e")
    e_p1 = ttk.Entry(card, textvariable=password1, width=28, show="*")
    e_p1.grid(row=row, column=1, padx=8, pady=6);
    row += 1

    ttk.Label(card, text="Password (Verify)").grid(row=row, column=0, padx=8, pady=6, sticky="e")
    e_p2 = ttk.Entry(card, textvariable=password2, width=28, show="*")
    e_p2.grid(row=row, column=1, padx=8, pady=6);
    row += 1

    # ---------- FunctionsFunctions ----------
    def set_message(msg, color="#c62828"):
        message.set(msg)
        text_label.configure(foreground=color)

    def toggle_show():
        show = "" if password_visible.get() else "*"
        e_p1.config(show=show)
        e_p2.config(show=show)

    def back():
        root.destroy()
        main()

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

        if not db.create_register_user(u, p1):
            return set_message(f"Username '{u}' already exists.")
        set_message("Registered successfully", "#2e7d32")

    # ---------- Check Buttons ----------
    ttk.Checkbutton(
        card,
        text="แสดงรหัสผ่าน",
        variable=password_visible,
        command=toggle_show
    ).grid(row=row, column=1, sticky="w", padx=8);
    row += 1

    # ---------- Message ----------
    text_label = ttk.Label(card, textvariable=message, foreground="#c62828")
    text_label.grid(row=row, column=0, columnspan=2, pady=(2, 6));
    row += 1

    # ---------- Buttons ----------
    btns = ttk.Frame(card)
    btns.grid(row=row, column=1, columnspan=2, pady=6)
    ttk.Button(btns, text="ย้อนกลับ", width=6, command=back).pack(side="left", padx=6)

    btns.grid(row=row, column=0, columnspan=2, pady=0)
    ttk.Button(btns, text="บันทึก", width=6, command=save).pack(side="left", padx=0)

    # ---------- Focus & Bind ----------
    card.grid_slaves(row=0, column=1)[0].focus()
    root.bind("<Return>", lambda e: save())

    return root

# ---------------- Configs ----------------
SYMBOLS = "!@#$%^&*+-_=?:/\\"
AMBITUOUS = set("Il1O0`'\"[]{}()<>~,.;:")


# ---------------- Pass gen & strength ----------------
def build_pool(use_lower, use_upper, use_digits, use_symbols, avoid_amb):
    pool = ""
    if use_lower: pool += string.ascii_lowercase
    if use_upper: pool += string.ascii_uppercase
    if use_digits: pool += string.digits
    if use_symbols: pool += SYMBOLS
    if avoid_amb and pool:
        pool = "".join(ch for ch in pool if ch not in AMBITUOUS)
    return pool


def generate_password(length, use_lower, use_upper, use_digits, use_symbols, avoid_amb):
    pool = build_pool(use_lower, use_upper, use_digits, use_symbols, avoid_amb)
    if not pool:
        raise ValueError("โปรดเลือกชุดตัวอักษรอย่างน้อย 1 ชุด")
    rng = secrets.SystemRandom()
    chosen = [rng.choice(pool) for _ in range(length)]
    return "".join(chosen), pool


def entropy_bits(length, pool_size):
    if length <= 0 or pool_size <= 1: return 0.0
    return length * math.log2(pool_size)


def strength_label(bits):
    if bits < 40:
        return "อ่อน (Weak)"
    elif bits < 60:
        return "ปานกลาง (Medium)"
    elif bits < 80:
        return "แข็งแรง (Strong)"
    else:
        return "แข็งแกร่งมาก (Very Strong)"


COMMON_PASSWORDS = {"123456", "password", "123456789", "12345678", "12345", "111111", "1234567", "qwerty", "abc123",
                    "password1", "iloveyou", "000000", "admin"}


def analyze_password(pw):
    if not pw:
        return {"entropy": 0.0, "pool_size": 0, "label": "Empty", "issues": ["รหัสว่าง"]}
    sets = {"lower": any(c.islower() for c in pw),
            "upper": any(c.isupper() for c in pw),
            "digit": any(c.isdigit() for c in pw),
            "symbol": any(c in SYMBOLS for c in pw)}
    pool_size = 0
    if sets["lower"]: pool_size += 26
    if sets["upper"]: pool_size += 26
    if sets["digit"]: pool_size += 10
    if sets["symbol"]: pool_size += len(SYMBOLS)
    bits = entropy_bits(len(pw), pool_size if pool_size > 0 else 1)
    issues = []
    if len(pw) < 8: issues.append("ความยาวน้อยกว่า 8")
    if pw.lower() in COMMON_PASSWORDS: issues.append("รหัสผ่านนี้เป็นรหัสยอดนิยม")
    if len(set(pw)) < max(3, len(pw) // 2): issues.append("มีตัวอักษรซ้ำเยอะ")
    recs = []
    if bits < 40: recs.append("เพิ่มความยาวหรือใช้ตัวอักษรหลากหลาย")
    return {"entropy": bits, "pool_size": pool_size, "label": strength_label(bits), "issues": issues, "recs": recs}


# ---------------- UI ----------------
class App(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.current_user = username
        self.title("Password Generator & Checker")
        center_window(self, 420, 450)
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # ---------- Input ----------
        gen_box = ttk.LabelFrame(frm, text="Password Generator", padding=8)
        gen_box.pack(fill="x", pady=6)

        ttk.Label(gen_box, text="ความยาว:").grid(row=0, column=0, sticky="w")
        self.len_var = tk.IntVar(value=16)
        ttk.Spinbox(gen_box, from_=4, to=128, textvariable=self.len_var, width=6).grid(row=0, column=1, padx=6)

        self.v_lower = tk.BooleanVar(value=True)
        self.v_upper = tk.BooleanVar(value=True)
        self.v_digits = tk.BooleanVar(value=True)
        self.v_sym = tk.BooleanVar(value=True)
        self.v_amb = tk.BooleanVar(value=True)

        ttk.Checkbutton(gen_box, text="a-z", variable=self.v_lower).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(gen_box, text="A-Z", variable=self.v_upper).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(gen_box, text="0-9", variable=self.v_digits).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(gen_box, text="symbols", variable=self.v_sym).grid(row=2, column=1, sticky="w")
        ttk.Checkbutton(gen_box, text="หลีกเลี่ยงตัวกำกวม", variable=self.v_amb).grid(row=3, column=0, columnspan=2,
                                                                                      sticky="w")
        ttk.Button(gen_box, text="สร้าง", command=self.generate_password).grid(row=4, column=0, pady=8)
        ttk.Button(gen_box, text="คัดลอก", command=self.copy_generated).grid(row=4, column=1, pady=8)
        ttk.Button(gen_box, text="บันทึก", command=self.save_note_popup).grid(row=4, column=2, pady=8)
        ttk.Button(gen_box, text="ประวัติ", command=self.open_history_window).grid(row=4, column=3, pady=8)

        # ---------- Output ----------
        out_box = ttk.LabelFrame(frm, text="Password / Analysis", padding=8)
        out_box.pack(fill="both", expand=True, pady=6)

        self.generated_var = tk.StringVar()
        ttk.Entry(out_box, textvariable=self.generated_var, font=("Consolas", 12)).pack(fill="x", padx=6, pady=(0, 6))

        ttk.Button(out_box, text="วิเคราะห์รหัสนี้", command=self.check_current_password).pack(padx=6, pady=6)
        ttk.Button(out_box, text="Export เป็น .txt", command=self.export_password).pack(padx=6, pady=6)

        self.strength_var = tk.StringVar(value="Entropy: 0.00 bits • -")
        self.str_pb = ttk.Progressbar(out_box, maximum=100)
        self.str_pb.pack(fill="x", padx=6, pady=(0, 4))
        ttk.Label(out_box, textvariable=self.strength_var, anchor="e").pack(fill="x", padx=6)

        ttk.Button(self, text="Logout", command=self.logout).pack(side='right', pady=3)

    def logout(self):
        self.destroy()
        main()

    def save_note_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add Note")
        popup.geometry("300x200")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text="หมายเหตุ").pack(pady=10)
        note_entry = tk.Text(popup, height=5, width=30)
        note_entry.pack(pady=5)

        def save_note_and_password():
            note = note_entry.get("1.0", tk.END).strip()
            password = self.generated_var.get().strip()
            user = self.current_user

            if not password:
                messagebox.showerror("Error", "ไม่มีรหัสผ่านให้บันทึก", parent=popup)
                return
            if not user:
                messagebox.showerror("Error", "ไม่พบข้อมูลผู้ใช้ (User not found)", parent=popup)
                return

            try:
                inserted_id = db.save_new_generated_password(
                    users=user,
                    password=password,
                    note=note
                )

                if inserted_id:

                    messagebox.showinfo("Status", "บันทึกรหัสผ่านสำเร็จ", parent=popup)
                    popup.destroy()
                else:
                    messagebox.showwarning("Warning", "ไม่สามารถบันทึกไปยังฐานข้อมูลได้", parent=popup)

            except Exception as e:
                messagebox.showerror("Database Error", f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}", parent=popup)
                print(f"Error saving to DB: {e}")

        ttk.Button(popup, text="บันทึก", command=save_note_and_password).pack(pady=10)

    def open_history_window(self):
        history_win = tk.Toplevel(self)
        history_win.title(f"History for {self.current_user}")
        history_win.geometry("550x350")
        history_win.resizable(False, False)

        history_win.transient(self)
        history_win.grab_set()

        ttk.Label(history_win, text=f"🔑 Password History ({self.current_user})", font=("Arial", 12, "bold")).pack(
            pady=10)

        columns = ("password", "note", "created_at")
        tree = ttk.Treeview(history_win, columns=columns, show="headings", height=8)
        tree.pack(fill="both", expand=True, padx=10, pady=5)

        tree.heading("password", text="รหัสผ่าน")
        tree.heading("note", text="หมายเหตุ")
        tree.heading("created_at", text="วันที่สร้าง")

        tree.column("password", width=120, anchor="center")
        tree.column("note", width=200)
        tree.column("created_at", width=140, anchor="center")

        tree_id_map = {}

        local_tz = pytz.timezone("Asia/Bangkok")
        utc_tz = pytz.timezone("UTC")

        if not self.current_user:
            messagebox.showerror("Error", "ไม่พบผู้ใช้งาน (No user logged in)", parent=history_win)
            history_win.destroy()
            return

        try:
            all_logs = db.get_all_logs_for_user(self.current_user)
            tree.delete(*tree.get_children())
            if not all_logs:
                tree.insert("", tk.END, values=("(ยังไม่มีข้อมูล)", "", ""))
            else:
                for log in all_logs:
                    password = log.get("generated_password", "N/A")
                    note = log.get("note", "")
                    created_at_dt = log.get("created at")
                    formatted_date = "N/A"
                    if created_at_dt:
                        aware_utc_dt = created_at_dt.replace(tzinfo=utc_tz)
                        local_dt = aware_utc_dt.astimezone(local_tz)
                        formatted_date = local_dt.strftime("%Y-%m-%d %H:%M:%S")

                    values = (password, note, formatted_date)

                    item_id = tree.insert("", tk.END, values=values)
                    tree_id_map[item_id] = log.get("_id")

        except Exception as e:
            messagebox.showerror("Database Error", f"ไม่สามารถดึงข้อมูลประวัติได้: {e}", parent=history_win)
            print(f"Error fetching history: {e}")

        def copy_to_clipboard(password_to_copy):
            try:
                history_win.clipboard_clear()
                history_win.clipboard_append(password_to_copy)
                history_win.update()
                print(f"Copied '{password_to_copy}' to clipboard.")
            except tk.TclError:
                print("Clipboard error. Maybe the window was closed?")

        def on_right_click(event):
            item_id = tree.identify_row(event.y)
            if not item_id:
                return
            column_id_str = tree.identify_column(event.x)

            if column_id_str == "#1":
                password = tree.item(item_id, "values")[0]
                if password == "(ยังไม่มีข้อมูล)": return

                popup_menu = tk.Menu(history_win, tearoff=0)
                popup_menu.add_command(
                    label=f"Copy '{password[:10]}...'",
                    command=lambda: copy_to_clipboard(password)
                )
                popup_menu.post(event.x_root, event.y_root)

        # Detect ของ Linux/Windows
        tree.bind("<Button-3>", on_right_click)

        # Detect ของ Mac
        tree.bind("<Button-2>", on_right_click)

        # Detect Trackpad
        tree.bind("<Control-Button-1>", on_right_click)

        def delete_selected_log():
            selected_items = tree.selection()

            if not selected_items:
                messagebox.showwarning("No Selection", "กรุณาเลือกแถวที่ต้องการลบ", parent=history_win)
                return
            item_id = selected_items[0]
            log_id_to_delete = tree_id_map.get(item_id)

            if not log_id_to_delete:
                messagebox.showerror("Error", "ไม่พบ ID ของข้อมูลนี้", parent=history_win)
                return

            password_to_show = tree.item(item_id, "values")[0]
            if not messagebox.askyesno("ยืนยันการลบ",
                                       f"คุณแน่ใจหรือว่าต้องการลบ:\n\n'{password_to_show}'\n\n(การกระทำนี้ไม่สามารถย้อนกลับได้)",
                                       parent=history_win):
                return

            try:
                success = db.delete_specific_generated_password(str(log_id_to_delete))

                if success:
                    tree.delete(item_id)
                    del tree_id_map[item_id]
                    print(f"Deleted log {log_id_to_delete}")
                else:
                    messagebox.showerror("Delete Failed", "ไม่สามารถลบข้อมูลออกจากฐานข้อมูลได้", parent=history_win)

            except Exception as e:
                messagebox.showerror("Database Error", f"เกิดข้อผิดพลาดขณะลบ: {e}", parent=history_win)

        button_frame = ttk.Frame(history_win)
        button_frame.pack(fill="x", padx=10, pady=(5, 10))

        def open_edit_note_popup(item_id, log_id, current_note):
            popup = tk.Toplevel(history_win)
            popup.title("Edit Note")
            popup.geometry("300x200")
            popup.resizable(False, False)

            popup.transient(history_win)
            popup.grab_set()

            ttk.Label(popup, text="แก้ไขหมายเหตุ:").pack(pady=10, padx=10)
            note_text = tk.Text(popup, height=5, width=35)
            note_text.pack(pady=5, padx=10, fill="x", expand=True)

            note_text.insert("1.0", current_note)

            def save_new_note():
                new_note = note_text.get("1.0", tk.END).strip()

                try:
                    modified_count = db.update_note(log_id, new_note)

                    if modified_count > 0:

                        current_values = list(tree.item(item_id, "values"))
                        current_values[1] = new_note
                        tree.item(item_id, values=tuple(current_values))

                        print(f"Updated note for {log_id}")
                        popup.destroy()
                    else:
                        messagebox.showwarning("No Change", "ไม่สามารถอัปเดตโน้ตได้ (หรือข้อมูลเหมือนเดิม)",
                                               parent=popup)

                except Exception as e:
                    messagebox.showerror("Database Error", f"เกิดข้อผิดพลาดขณะอัปเดต: {e}", parent=popup)

            ttk.Button(popup, text="บันทึก", command=save_new_note).pack(pady=10)

        def on_double_click(event):
            item_id = tree.identify_row(event.y)
            if not item_id: return

            column_id_str = tree.identify_column(event.x)

            if column_id_str == "#2":
                log_id = tree_id_map.get(item_id)
                current_note = tree.item(item_id, "values")[1]

                if log_id:
                    open_edit_note_popup(item_id, log_id, current_note)
                else:
                    print(f"Could not find log_id for item {item_id}")

        tree.bind("<Double-1>", on_double_click)

        def edit_selected_log():
            selected_items = tree.selection()

            if not selected_items:
                messagebox.showwarning("No Selection", "กรุณาเลือกแถวที่ต้องการแก้ไข", parent=history_win)
                return

            item_id = selected_items[0]
            log_id = tree_id_map.get(item_id)

            if not log_id:
                messagebox.showerror("Error", "ไม่พบ ID ของข้อมูลนี้", parent=history_win)
                return

            current_note = tree.item(item_id, "values")[1]

            open_edit_note_popup(item_id, log_id, current_note)

        button_frame = ttk.Frame(history_win)
        button_frame.pack(fill="x", padx=10, pady=(5, 10))

        ttk.Button(
            button_frame,
            text="Close",
            command=history_win.destroy
        ).pack(side="right")

        ttk.Button(
            button_frame,
            text="ลบรหัสที่เลือก(Delete)",
            command=delete_selected_log
        ).pack(side="right", padx=(0, 5))

        ttk.Button(
            button_frame,
            text="แก้ไขโน้ต (Edit)",
            command=edit_selected_log
        ).pack(side="right")

    def generate_password(self):
        try:
            pw, pool = generate_password(
                self.len_var.get(),
                self.v_lower.get(),
                self.v_upper.get(),
                self.v_digits.get(),
                self.v_sym.get(),
                self.v_amb.get()
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.generated_var.set(pw)
        bits = entropy_bits(len(pw), len(set(pool)))
        self.update_strength_display(bits)

    def copy_generated(self):
        pw = self.generated_var.get().strip()
        if not pw:
            messagebox.showinfo("Info", "ไม่มีรหัสให้คัดลอก")
            return
        self.clipboard_clear()
        self.clipboard_append(pw)
        self.update()
        messagebox.showinfo("Copied", "คัดลอกรหัสไปยังคลิปบอร์ดแล้ว")

    def check_current_password(self):
        pw = self.generated_var.get().strip()
        if not pw:
            messagebox.showinfo("Info", "ไม่มีรหัสให้วิเคราะห์")
            return
        res = analyze_password(pw)
        self.update_strength_display(res["entropy"])
        s = f"Entropy: {res['entropy']:.2f} bits\nStrength: {res['label']}\n\n"
        if res["issues"]:
            s += "ปัญหา:\n" + "\n".join("- " + i for i in res["issues"]) + "\n\n"
        if res["recs"]:
            s += "คำแนะนำ:\n" + "\n".join("- " + r for r in res["recs"])
        messagebox.showinfo("วิเคราะห์รหัส", s)

    def update_strength_display(self, bits):
        self.strength_var.set(f"Entropy: {bits:.2f} bits • {strength_label(bits)}")
        self.str_pb["value"] = max(0, min(100, int(bits)))

    def export_password(self):
        pw = self.generated_var.get().strip()
        if not pw:
            messagebox.showinfo("Info", "ไม่มีรหัสให้ส่งออก")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")],
                                            initialfile=f"password_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            f.write(pw)
        messagebox.showinfo("Exported", f"บันทึกรหัสไปยัง {path}")

def main():
    root = tk.Tk()
    create_login_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
