# ============================================================
#  🔐 ADVANCED PASSWORD GENERATOR
#  No installations needed — runs straight away!
#  Just run: python password_advanced.py
# ============================================================

import tkinter as tk
from tkinter import messagebox
import random
import string
import time

# ─────────────────────────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────────────────────────
BG_MAIN   = "#0D1117"
BG_CARD   = "#161B22"
BG_INPUT  = "#21262D"
BG_BORDER = "#30363D"
TEXT_W    = "#E6EDF3"
TEXT_GRAY = "#8B949E"
TEXT_DIM  = "#484F58"
ACC_GREEN = "#3FB950"
ACC_BLUE  = "#58A6FF"
ACC_RED   = "#F85149"
ACC_AMBER = "#D29922"

FONT_TITLE = ("Georgia", 20, "bold")
FONT_LABEL = ("Helvetica", 11)
FONT_SMALL = ("Helvetica", 10)
FONT_PWD   = ("Courier New", 14, "bold")
FONT_BTN   = ("Helvetica", 11, "bold")
FONT_MED   = ("Helvetica", 12, "bold")

# ─────────────────────────────────────────────────────────────
#  PASSWORD LOGIC
# ─────────────────────────────────────────────────────────────
SYMBOLS_SAFE   = "!@#$%^&*"
SYMBOLS_ALL    = string.punctuation
SIMILAR_CHARS  = "il1Lo0O"

def build_charset(upper, lower, digits, symbols, symbol_type, exclude_similar):
    chars = ""
    if upper:   chars += string.ascii_uppercase
    if lower:   chars += string.ascii_lowercase
    if digits:  chars += string.digits
    if symbols:
        chars += SYMBOLS_SAFE if symbol_type == "safe" else SYMBOLS_ALL
    if exclude_similar:
        chars = ''.join(c for c in chars if c not in SIMILAR_CHARS)
    return chars

def generate_password(length, chars, must_include):
    if not chars:
        return None

    while True:
        pwd = ''.join(random.choice(chars) for _ in range(length))
        # Check must-include conditions
        ok = True
        if must_include.get("upper")   and not any(c.isupper() for c in pwd): ok = False
        if must_include.get("lower")   and not any(c.islower() for c in pwd): ok = False
        if must_include.get("digit")   and not any(c.isdigit() for c in pwd): ok = False
        if must_include.get("symbol")  and not any(c in string.punctuation for c in pwd): ok = False
        if ok:
            return pwd

def check_strength(password):
    score = 0
    tips  = []

    if any(c.isupper() for c in password):         score += 1
    else: tips.append("Add uppercase letters")

    if any(c.islower() for c in password):         score += 1
    else: tips.append("Add lowercase letters")

    if any(c.isdigit() for c in password):         score += 1
    else: tips.append("Add numbers")

    if any(c in string.punctuation for c in password): score += 1
    else: tips.append("Add symbols")

    if len(password) >= 12: score += 1
    else: tips.append("Make it 12+ characters")

    if len(password) >= 16: score += 1

    if score <= 2:
        return "Weak",   ACC_RED,   score, tips
    elif score <= 4:
        return "Medium", ACC_AMBER, score, tips
    else:
        return "Strong", ACC_GREEN, score, tips

password_history = []

# ─────────────────────────────────────────────────────────────
#  APP
# ─────────────────────────────────────────────────────────────
class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced Password Generator")
        self.root.geometry("580x780")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        # Variables
        self.use_upper    = tk.BooleanVar(value=True)
        self.use_lower    = tk.BooleanVar(value=True)
        self.use_digits   = tk.BooleanVar(value=True)
        self.use_symbols  = tk.BooleanVar(value=True)
        self.excl_similar = tk.BooleanVar(value=False)
        self.symbol_type  = tk.StringVar(value="safe")
        self.length_var   = tk.IntVar(value=16)
        self.count_var    = tk.IntVar(value=5)
        self.pwd_vars     = []

        self.build_ui()

    def build_ui(self):
        # ── Title ──────────────────────────────────────────
        tk.Label(self.root, text="🔐 Password Generator",
                 font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_W).pack(pady=(20, 2))
        tk.Label(self.root, text="Generate strong secure passwords instantly",
                 font=FONT_SMALL, bg=BG_MAIN, fg=TEXT_GRAY).pack()

        tk.Frame(self.root, bg=BG_BORDER, height=1).pack(fill="x", padx=24, pady=12)

        # ── Length Slider ──────────────────────────────────
        len_frame = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=12)
        len_frame.pack(fill="x", padx=24)

        top = tk.Frame(len_frame, bg=BG_CARD)
        top.pack(fill="x")
        tk.Label(top, text="Password Length", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")
        self.len_display = tk.Label(top, text="16",
                 font=FONT_MED, bg=BG_CARD, fg=ACC_BLUE)
        self.len_display.pack(side="right")

        slider = tk.Scale(
            len_frame, from_=4, to=64,
            orient="horizontal", variable=self.length_var,
            bg=BG_CARD, fg=TEXT_W, troughcolor=BG_INPUT,
            highlightthickness=0, sliderrelief="flat",
            activebackground=ACC_BLUE, showvalue=False,
            command=lambda v: self.len_display.config(text=str(int(float(v))))
        )
        slider.pack(fill="x", pady=(4, 0))

        # ── Count ──────────────────────────────────────────
        count_frame = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=10)
        count_frame.pack(fill="x", padx=24, pady=(4, 0))

        tk.Label(count_frame, text="How many passwords?",
                 font=FONT_LABEL, bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")

        for n in [1, 3, 5, 10]:
            tk.Radiobutton(
                count_frame, text=str(n), variable=self.count_var, value=n,
                bg=BG_CARD, fg=TEXT_W, selectcolor=BG_INPUT,
                activebackground=BG_CARD, font=FONT_SMALL
            ).pack(side="left", padx=8)

        # ── Character Options ──────────────────────────────
        opt_frame = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=12)
        opt_frame.pack(fill="x", padx=24, pady=(4, 0))

        tk.Label(opt_frame, text="Include:", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w", pady=(0, 6))

        checks = [
            (self.use_upper,   "ABC  Uppercase letters"),
            (self.use_lower,   "abc  Lowercase letters"),
            (self.use_digits,  "123  Numbers"),
            (self.use_symbols, "!@#  Symbols"),
        ]
        grid = tk.Frame(opt_frame, bg=BG_CARD)
        grid.pack(fill="x")
        for i, (var, text) in enumerate(checks):
            tk.Checkbutton(
                grid, text=text, variable=var,
                bg=BG_CARD, fg=TEXT_W, selectcolor=BG_INPUT,
                activebackground=BG_CARD, font=FONT_SMALL
            ).grid(row=i//2, column=i%2, sticky="w", padx=8, pady=2)

        # Symbol type
        sym_frame = tk.Frame(opt_frame, bg=BG_CARD)
        sym_frame.pack(anchor="w", pady=(6, 0))
        tk.Label(sym_frame, text="Symbol type:",
                 font=FONT_SMALL, bg=BG_CARD, fg=TEXT_GRAY).pack(side="left")
        for text, val in [("Safe (!@#$%^&*)", "safe"), ("All symbols", "all")]:
            tk.Radiobutton(
                sym_frame, text=text, variable=self.symbol_type, value=val,
                bg=BG_CARD, fg=TEXT_W, selectcolor=BG_INPUT,
                activebackground=BG_CARD, font=FONT_SMALL
            ).pack(side="left", padx=8)

        # Exclude similar
        tk.Checkbutton(
            opt_frame, text="Exclude similar characters (i, l, 1, L, o, 0, O)",
            variable=self.excl_similar,
            bg=BG_CARD, fg=TEXT_GRAY, selectcolor=BG_INPUT,
            activebackground=BG_CARD, font=FONT_SMALL
        ).pack(anchor="w", pady=(6, 0))

        # ── Generate Button ────────────────────────────────
        tk.Button(
            self.root, text="⚡ GENERATE PASSWORDS",
            font=FONT_BTN, bg=ACC_GREEN, fg="#000000",
            relief="flat", bd=0, padx=20, pady=12,
            cursor="hand2", command=self.generate
        ).pack(fill="x", padx=24, pady=12)

        # ── Password Results ───────────────────────────────
        self.results_frame = tk.Frame(self.root, bg=BG_MAIN)
        self.results_frame.pack(fill="x", padx=24)

        # ── Strength Meter ─────────────────────────────────
        str_frame = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=10)
        str_frame.pack(fill="x", padx=24, pady=(8, 0))

        tk.Label(str_frame, text="Strength Meter",
                 font=FONT_LABEL, bg=BG_CARD, fg=TEXT_GRAY).pack(anchor="w")

        self.strength_canvas = tk.Canvas(
            str_frame, height=16, bg=BG_CARD, highlightthickness=0
        )
        self.strength_canvas.pack(fill="x", pady=(4, 0))

        self.strength_label = tk.Label(
            str_frame, text="Generate a password to see strength",
            font=FONT_SMALL, bg=BG_CARD, fg=TEXT_GRAY
        )
        self.strength_label.pack(anchor="w", pady=(4, 0))

        # ── History ────────────────────────────────────────
        tk.Button(
            self.root, text="📋 View History",
            font=FONT_SMALL, bg=BG_INPUT, fg=TEXT_GRAY,
            relief="flat", bd=0, padx=12, pady=8,
            cursor="hand2", command=self.show_history
        ).pack(pady=(10, 4))

    def generate(self):
        # Clear previous results
        for w in self.results_frame.winfo_children():
            w.destroy()
        self.pwd_vars.clear()

        chars = build_charset(
            self.use_upper.get(), self.use_lower.get(),
            self.use_digits.get(), self.use_symbols.get(),
            self.symbol_type.get(), self.excl_similar.get()
        )

        if not chars:
            messagebox.showerror("Error", "Please select at least one character type!")
            return

        must = {
            "upper" : self.use_upper.get(),
            "lower" : self.use_lower.get(),
            "digit" : self.use_digits.get(),
            "symbol": self.use_symbols.get(),
        }

        count  = self.count_var.get()
        length = self.length_var.get()

        for i in range(count):
            pwd = generate_password(length, chars, must)

            row = tk.Frame(self.results_frame, bg=BG_CARD, padx=10, pady=8)
            row.pack(fill="x", pady=(0, 4))

            var = tk.StringVar(value=pwd)
            self.pwd_vars.append(var)

            # Number
            tk.Label(row, text=f"{i+1}.",
                     font=FONT_SMALL, bg=BG_CARD, fg=TEXT_GRAY,
                     width=2).pack(side="left")

            # Password entry (selectable)
            entry = tk.Entry(
                row, textvariable=var,
                font=FONT_PWD, bg=BG_INPUT, fg=ACC_BLUE,
                relief="flat", bd=6, state="readonly",
                readonlybackground=BG_INPUT,
                insertbackground=TEXT_W, width=28
            )
            entry.pack(side="left", padx=(4, 8))

            # Copy button
            def make_copy(v=var, r=row):
                def copy():
                    self.root.clipboard_clear()
                    self.root.clipboard_append(v.get())
                    password_history.append(v.get())
                    r.configure(bg="#1C3A1C")
                    self.root.after(600, lambda: r.configure(bg=BG_CARD))
                return copy

            tk.Button(
                row, text="Copy",
                font=FONT_SMALL, bg=ACC_BLUE, fg="#000000",
                relief="flat", bd=0, padx=10, pady=4,
                cursor="hand2", command=make_copy()
            ).pack(side="left")

        # Update strength for first password
        if self.pwd_vars:
            first_pwd = self.pwd_vars[0].get()
            strength, color, score, tips = check_strength(first_pwd)
            self.update_strength(strength, color, score, tips)

    def update_strength(self, strength, color, score, tips):
        self.strength_canvas.delete("all")
        w = 520
        # Background
        self.strength_canvas.create_rectangle(0, 4, w, 12, fill=BG_INPUT, outline="")
        # Fill based on score (max 6)
        fill_w = int((score / 6) * w)
        self.strength_canvas.create_rectangle(0, 4, fill_w, 12, fill=color, outline="")

        tip_text = " | ".join(tips[:2]) if tips else "Great password!"
        self.strength_label.config(
            text=f"Strength: {strength}   💡 {tip_text}",
            fg=color
        )

    def show_history(self):
        if not password_history:
            messagebox.showinfo("History", "No passwords copied yet!\nCopy a password first.")
            return

        win = tk.Toplevel(self.root)
        win.title("📋 Password History")
        win.geometry("460x360")
        win.configure(bg=BG_MAIN)

        tk.Label(win, text="📋 Copied Passwords",
                 font=FONT_MED, bg=BG_MAIN, fg=TEXT_W).pack(pady=12)

        text = tk.Text(win, font=("Courier New", 12),
                       bg=BG_INPUT, fg=ACC_BLUE,
                       relief="flat", bd=12)
        text.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        for i, pwd in enumerate(reversed(password_history), 1):
            strength, color, _, _ = check_strength(pwd)
            text.insert(tk.END, f"  {i}. {pwd}  [{strength}]\n")

        text.config(state="disabled")


# ─────────────────────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = PasswordApp(root)
    root.mainloop()