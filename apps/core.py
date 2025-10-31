import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import math
from datetime import datetime
import sys
from ui_utilities import center_window
from database import zitttpymongo
import pytz

# ---------------- รับค่าจาก Subprocess ----------------
if len(sys.argv) > 1:
    current_user = sys.argv[1]
else:
    print("test only !!!!!!!!!!!!!")
    current_user = "haneen"

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
    def __init__(self):
        super().__init__()
        self.title("Password Generator & Checker")
        center_window(self, 420, 450)
        self.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # Input
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

        # Output
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

        ttk.Button(self, text="Quit", command=self.destroy).pack(side='right', padx=12, pady=3)


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

        def save_note():
            note = note_entry.get("1.0", tk.END).strip()
            password = self.generated_var.get().strip()
            user = current_user

            if not password:
                messagebox.showerror("Error", "ไม่มีรหัสผ่านให้บันทึก", parent=popup)
                return
            if not user:
                messagebox.showerror("Error", "ไม่พบข้อมูลผู้ใช้ (User not found)", parent=popup)
                return

            try:
                inserted_id = zitttpymongo.save_new_generated_password(
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

        ttk.Button(popup, text="บันทึก", command=save_note).pack(pady=10)

    def open_history_window(self):
        history_win = tk.Toplevel(self)
        history_win.title(f"History for {current_user}")
        history_win.geometry("550x300")
        history_win.resizable(False, False)

        history_win.transient(self)
        history_win.grab_set()

        ttk.Label(history_win, text=f"🔑 Password History ({current_user})", font=("Arial", 12, "bold")).pack(pady=10)

        columns = ("password", "note", "created_at")
        tree = ttk.Treeview(history_win, columns=columns, show="headings", height=8)
        tree.pack(fill="both", expand=True, padx=10, pady=5)
        tree.heading("password", text="รหัสผ่าน")
        tree.heading("note", text="หมายเหตุ")
        tree.heading("created_at", text="วันที่สร้าง")
        tree.column("password", width=120, anchor="center")
        tree.column("note", width=200)
        tree.column("created_at", width=140, anchor="center")

        local_tz = pytz.timezone("Asia/Bangkok")
        utc_tz = pytz.timezone("UTC")

        if not current_user:
            messagebox.showerror("Error", "ไม่พบผู้ใช้งาน (No user logged in)", parent=history_win)
            history_win.destroy()
            return

        try:
            all_logs = zitttpymongo.get_all_logs_for_user(current_user)
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
                    tree.insert("", tk.END, values=values)
        
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

        # button for Linux/Windows
        tree.bind("<Button-3>", on_right_click)
        
        # button for mac mouse 
        tree.bind("<Button-2>", on_right_click) 
        
        # button for mac trakcpad
        tree.bind("<Control-Button-1>", on_right_click)

        ttk.Button(history_win, text="Close", command=history_win.destroy).pack(pady=10)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
