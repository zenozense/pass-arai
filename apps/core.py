import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import math
from datetime import datetime

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
    if bits < 40: return "อ่อน (Weak)"
    elif bits < 60: return "ปานกลาง (Medium)"
    elif bits < 80: return "แข็งแรง (Strong)"
    else: return "แข็งแกร่งมาก (Very Strong)"

COMMON_PASSWORDS = {"123456","password","123456789","12345678","12345","111111","1234567","qwerty","abc123","password1","iloveyou","000000","admin"}

def analyze_password(pw):
    if not pw:
        return {"entropy":0.0, "pool_size":0, "label":"Empty", "issues":["รหัสว่าง"]}
    sets = {"lower": any(c.islower() for c in pw),
            "upper": any(c.isupper() for c in pw),
            "digit": any(c.isdigit() for c in pw),
            "symbol": any(c in SYMBOLS for c in pw)}
    pool_size = 0
    if sets["lower"]: pool_size += 26
    if sets["upper"]: pool_size += 26
    if sets["digit"]: pool_size += 10
    if sets["symbol"]: pool_size += len(SYMBOLS)
    bits = entropy_bits(len(pw), pool_size if pool_size>0 else 1)
    issues = []
    if len(pw) < 8: issues.append("ความยาวน้อยกว่า 8")
    if pw.lower() in COMMON_PASSWORDS: issues.append("รหัสผ่านนี้เป็นรหัสยอดนิยม")
    if len(set(pw)) < max(3, len(pw)//2): issues.append("มีตัวอักษรซ้ำเยอะ")
    recs = []
    if bits < 40: recs.append("เพิ่มความยาวหรือใช้ตัวอักษรหลากหลาย")
    return {"entropy":bits, "pool_size":pool_size, "label":strength_label(bits), "issues":issues, "recs":recs}

# ---------------- UI ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator & Checker")
        self.geometry("650x450")
        self.create_ui()

    def create_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # Generator
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

        ttk.Checkbutton(gen_box, text="a-z", variable=self.v_lower).grid(row=1,column=0, sticky="w")
        ttk.Checkbutton(gen_box, text="A-Z", variable=self.v_upper).grid(row=1,column=1, sticky="w")
        ttk.Checkbutton(gen_box, text="0-9", variable=self.v_digits).grid(row=2,column=0, sticky="w")
        ttk.Checkbutton(gen_box, text="symbols", variable=self.v_sym).grid(row=2,column=1, sticky="w")
        ttk.Checkbutton(gen_box, text="หลีกเลี่ยงตัวกำกวม", variable=self.v_amb).grid(row=3,column=0,columnspan=2, sticky="w")

        ttk.Button(gen_box, text="สร้าง", command=self.generate_password).grid(row=4,column=0,pady=8)
        ttk.Button(gen_box, text="คัดลอก", command=self.copy_generated).grid(row=4,column=1,pady=8)

        # Output
        out_box = ttk.LabelFrame(frm, text="Password / Analysis", padding=8)
        out_box.pack(fill="both", expand=True, pady=6)

        self.generated_var = tk.StringVar()
        ttk.Entry(out_box, textvariable=self.generated_var, font=("Consolas",12)).pack(fill="x", padx=6, pady=(0,6))

        ttk.Button(out_box, text="วิเคราะห์รหัสนี้", command=self.check_current_password).pack(padx=6,pady=6)
        ttk.Button(out_box, text="Export เป็น .txt", command=self.export_password).pack(padx=6,pady=6)

        self.strength_var = tk.StringVar(value="Entropy: 0.00 bits • -")
        self.str_pb = ttk.Progressbar(out_box, maximum=100)
        self.str_pb.pack(fill="x", padx=6, pady=(0,4))
        ttk.Label(out_box, textvariable=self.strength_var, anchor="e").pack(fill="x", padx=6)

    # Actions
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
            s += "ปัญหา:\n" + "\n".join("- "+i for i in res["issues"]) + "\n\n"
        if res["recs"]:
            s += "คำแนะนำ:\n" + "\n".join("- "+r for r in res["recs"])
        messagebox.showinfo("วิเคราะห์รหัส", s)

    def update_strength_display(self, bits):
        self.strength_var.set(f"Entropy: {bits:.2f} bits • {strength_label(bits)}")
        self.str_pb["value"] = max(0,min(100,int(bits)))

    def export_password(self):
        pw = self.generated_var.get().strip()
        if not pw:
            messagebox.showinfo("Info", "ไม่มีรหัสให้ส่งออก")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file","*.txt")], initialfile=f"password_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if not path: return
        with open(path,"w", encoding="utf-8") as f:
            f.write(pw)
        messagebox.showinfo("Exported", f"บันทึกรหัสไปยัง {path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
