import tkinter as tk
from tkinter import ttk, messagebox
import math
import datetime

# ──────────────────────────────────────────────────────────────
#  COLORS & FONTS
# ──────────────────────────────────────────────────────────────
BG_MAIN    = "#0D1117"
BG_CARD    = "#161B22"
BG_INPUT   = "#21262D"
BG_BORDER  = "#30363D"
TEXT_W     = "#E6EDF3"
TEXT_GRAY  = "#8B949E"
TEXT_DIM   = "#484F58"

COLOR_UNDER  = "#58A6FF"
COLOR_NORMAL = "#3FB950"
COLOR_OVER   = "#D29922"
COLOR_OBESE  = "#F85149"

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_LABEL  = ("Helvetica", 11)
FONT_SMALL  = ("Helvetica", 10)
FONT_BIG    = ("Georgia", 48, "bold")
FONT_MED    = ("Helvetica", 13, "bold")
FONT_BTN    = ("Helvetica", 12, "bold")


# ──────────────────────────────────────────────────────────────
#  BMI LOGIC
# ──────────────────────────────────────────────────────────────
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight",   COLOR_UNDER,  "🔵"
    elif bmi < 25:
        return "Normal Weight", COLOR_NORMAL, "🟢"
    elif bmi < 30:
        return "Overweight",    COLOR_OVER,   "🟡"
    else:
        return "Obese",         COLOR_OBESE,  "🔴"

def get_ideal_weight(height_cm):
    h = height_cm / 100
    return round(18.5 * h * h, 1), round(24.9 * h * h, 1)

def get_advice(category):
    advice = {
        "Underweight": [
            "🥗 Eat more nutrient-rich foods",
            "🏋 Do strength training exercises",
            "🥛 Increase protein intake daily",
            "😴 Get 7-8 hours of sleep",
            "👨‍⚕️ Consult a nutritionist"
        ],
        "Normal Weight": [
            "✅ You are in a healthy range!",
            "🏃 Keep up regular exercise",
            "🥦 Maintain balanced diet",
            "💧 Drink 8 glasses of water daily",
            "😊 Keep up the great work!"
        ],
        "Overweight": [
            "🏃 Exercise at least 30 mins/day",
            "🥗 Reduce processed food intake",
            "💧 Drink more water",
            "🍽 Control portion sizes",
            "👨‍⚕️ Consider a diet plan"
        ],
        "Obese": [
            "👨‍⚕️ Consult a doctor immediately",
            "🏃 Start with light walking daily",
            "🥗 Follow a structured diet plan",
            "🍎 Cut sugar and junk food",
            "💪 Set small achievable goals"
        ]
    }
    return advice.get(category, [])

def get_calories(category, gender, weight_kg):
    base = weight_kg * 24
    if gender == "Male":
        base *= 1.1
    if category == "Underweight":
        return int(base * 1.3), "Increase calories to gain weight"
    elif category == "Normal Weight":
        return int(base * 1.1), "Maintain current calorie intake"
    elif category == "Overweight":
        return int(base * 0.9), "Reduce calories to lose weight"
    else:
        return int(base * 0.8), "Significantly reduce calorie intake"


# ──────────────────────────────────────────────────────────────
#  HISTORY
# ──────────────────────────────────────────────────────────────
bmi_history = []


# ──────────────────────────────────────────────────────────────
#  MAIN APP
# ──────────────────────────────────────────────────────────────
class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("620x860")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)
        self.unit   = tk.StringVar(value="metric")
        self.gender = tk.StringVar(value="Male")
        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(header, text="BMI Calculator",
                 font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_W).pack()
        tk.Label(header, text="Advanced Body Mass Index Analyzer",
                 font=FONT_SMALL, bg=BG_MAIN, fg=TEXT_GRAY).pack(pady=(2, 0))

        tk.Frame(self.root, bg=BG_BORDER, height=1).pack(fill="x", padx=24, pady=12)

        # Unit Toggle
        unit_frame = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=10)
        unit_frame.pack(fill="x", padx=24)
        tk.Label(unit_frame, text="Units:", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_GRAY).pack(side="left", padx=(0, 12))
        for text, val in [("Metric (kg, cm)", "metric"), ("Imperial (lbs, ft)", "imperial")]:
            tk.Radiobutton(
                unit_frame, text=text, variable=self.unit, value=val,
                bg=BG_CARD, fg=TEXT_W, selectcolor=BG_INPUT,
                activebackground=BG_CARD, font=FONT_SMALL,
                command=self.toggle_units
            ).pack(side="left", padx=8)

        # Gender
        gender_frame = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=10)
        gender_frame.pack(fill="x", padx=24, pady=(4, 0))
        tk.Label(gender_frame, text="Gender:", font=FONT_LABEL,
                 bg=BG_CARD, fg=TEXT_GRAY).pack(side="left", padx=(0, 12))
        for g in ["Male", "Female"]:
            tk.Radiobutton(
                gender_frame, text=g, variable=self.gender, value=g,
                bg=BG_CARD, fg=TEXT_W, selectcolor=BG_INPUT,
                activebackground=BG_CARD, font=FONT_SMALL
            ).pack(side="left", padx=8)

        # ✅ Input Fields — all packed correctly now
        input_frame = tk.Frame(self.root, bg=BG_MAIN)
        input_frame.pack(fill="x", padx=24, pady=12)

        self.name_entry         = self.make_input(input_frame, "Your Name")
        self.age_entry          = self.make_input(input_frame, "Age")
        self.weight_lbl_var     = tk.StringVar(value="Weight (kg)")
        self.weight_entry       = self.make_input_dynamic(input_frame, self.weight_lbl_var)
        self.height_lbl_var     = tk.StringVar(value="Height (cm)")
        self.height_entry       = self.make_input_dynamic(input_frame, self.height_lbl_var)

        # Calculate Button
        tk.Button(
            self.root, text="CALCULATE BMI",
            font=FONT_BTN, bg=COLOR_NORMAL, fg="#000000",
            relief="flat", bd=0, padx=20, pady=12,
            cursor="hand2", command=self.calculate
        ).pack(fill="x", padx=24, pady=(4, 12))

        # Result Card
        self.result_frame = tk.Frame(self.root, bg=BG_CARD, padx=20, pady=16)
        self.result_frame.pack(fill="x", padx=24)

        self.bmi_value_label = tk.Label(
            self.result_frame, text="--",
            font=FONT_BIG, bg=BG_CARD, fg=TEXT_DIM)
        self.bmi_value_label.pack()

        self.category_label = tk.Label(
            self.result_frame, text="Enter your details above",
            font=FONT_MED, bg=BG_CARD, fg=TEXT_GRAY)
        self.category_label.pack(pady=(0, 8))

        self.scale_canvas = tk.Canvas(
            self.result_frame, height=24, bg=BG_CARD, highlightthickness=0)
        self.scale_canvas.pack(fill="x", pady=(4, 8))
        self.draw_scale_bar()

        detail_frame = tk.Frame(self.result_frame, bg=BG_CARD)
        detail_frame.pack(fill="x", pady=(4, 0))

        self.ideal_label = tk.Label(
            detail_frame, text="Ideal weight: --",
            font=FONT_SMALL, bg=BG_CARD, fg=TEXT_GRAY)
        self.ideal_label.pack(side="left")

        self.calories_label = tk.Label(
            detail_frame, text="Calories: --",
            font=FONT_SMALL, bg=BG_CARD, fg=TEXT_GRAY)
        self.calories_label.pack(side="right")

        # Advice Box
        advice_frame = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=12)
        advice_frame.pack(fill="x", padx=24, pady=(8, 0))

        tk.Label(advice_frame, text="Health Tips",
                 font=FONT_MED, bg=BG_CARD, fg=TEXT_W).pack(anchor="w")

        self.advice_text = tk.Text(
            advice_frame, height=5, font=FONT_SMALL,
            bg=BG_INPUT, fg=TEXT_GRAY, relief="flat",
            state="disabled", bd=8, wrap="word")
        self.advice_text.pack(fill="x", pady=(6, 0))

        # History Button
        tk.Button(
            self.root, text="View History",
            font=FONT_SMALL, bg=BG_INPUT, fg=TEXT_GRAY,
            relief="flat", bd=0, padx=12, pady=8,
            cursor="hand2", command=self.show_history
        ).pack(pady=(8, 4))

    # ✅ FIXED — frame.pack() is now called so fields appear on screen
    def make_input(self, parent, label_text):
        frame = tk.Frame(parent, bg=BG_MAIN)
        frame.pack(fill="x", pady=(0, 8))   # <-- THE FIX
        tk.Label(frame, text=label_text, font=FONT_SMALL,
                 bg=BG_MAIN, fg=TEXT_GRAY).pack(anchor="w", pady=(0, 2))
        entry = tk.Entry(frame, font=FONT_LABEL,
                         bg=BG_INPUT, fg=TEXT_W,
                         insertbackground=TEXT_W, relief="flat", bd=8)
        entry.pack(fill="x")
        return entry

    def make_input_dynamic(self, parent, label_var):
        """Input whose label text can change (used for unit toggle)."""
        frame = tk.Frame(parent, bg=BG_MAIN)
        frame.pack(fill="x", pady=(0, 8))   # <-- THE FIX
        tk.Label(frame, textvariable=label_var, font=FONT_SMALL,
                 bg=BG_MAIN, fg=TEXT_GRAY).pack(anchor="w", pady=(0, 2))
        entry = tk.Entry(frame, font=FONT_LABEL,
                         bg=BG_INPUT, fg=TEXT_W,
                         insertbackground=TEXT_W, relief="flat", bd=8)
        entry.pack(fill="x")
        return entry

    def toggle_units(self):
        if self.unit.get() == "metric":
            self.weight_lbl_var.set("Weight (kg)")
            self.height_lbl_var.set("Height (cm)")
        else:
            self.weight_lbl_var.set("Weight (lbs)")
            self.height_lbl_var.set("Height (ft)")

    def draw_scale_bar(self, bmi=None):
        self.scale_canvas.delete("all")
        w = 560
        zones = [
            (0,    18.5, COLOR_UNDER),
            (18.5, 25,   COLOR_NORMAL),
            (25,   30,   COLOR_OVER),
            (30,   40,   COLOR_OBESE),
        ]
        max_bmi = 40
        for start, end, color in zones:
            x1 = int((start / max_bmi) * w)
            x2 = int((end   / max_bmi) * w)
            self.scale_canvas.create_rectangle(x1, 6, x2, 20, fill=color, outline="")
        if bmi:
            x = int((min(bmi, max_bmi) / max_bmi) * w)
            self.scale_canvas.create_polygon(
                x-6, 22, x+6, 22, x, 4, fill=TEXT_W, outline="")

    def calculate(self):
        try:
            name   = self.name_entry.get().strip() or "User"
            age    = self.age_entry.get().strip()
            weight = float(self.weight_entry.get().strip())
            height = float(self.height_entry.get().strip())
            gender = self.gender.get()
            unit   = self.unit.get()

            if unit == "imperial":
                weight = weight * 0.453592
                height = height * 30.48

            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be greater than 0!")
                return
            if height > 300 or weight > 500:
                messagebox.showerror("Error", "Please enter realistic values!")
                return

            bmi                    = calculate_bmi(weight, height)
            category, color, emoji = get_category(bmi)
            ideal_low, ideal_high  = get_ideal_weight(height)
            calories, cal_advice   = get_calories(category, gender, weight)
            advice                 = get_advice(category)

            self.bmi_value_label.config(text=str(bmi), fg=color)
            self.category_label.config(text=f"{emoji} {category}", fg=color)
            self.draw_scale_bar(bmi)
            self.ideal_label.config(
                text=f"Ideal weight: {ideal_low}-{ideal_high} kg", fg=TEXT_GRAY)
            self.calories_label.config(text=f"~{calories} cal/day", fg=TEXT_GRAY)

            self.advice_text.config(state="normal")
            self.advice_text.delete("1.0", tk.END)
            self.advice_text.insert(tk.END, f"For {name} ({category}):\n\n")
            for tip in advice:
                self.advice_text.insert(tk.END, f"  {tip}\n")
            self.advice_text.insert(tk.END, f"\n  {cal_advice}")
            self.advice_text.config(state="disabled")

            bmi_history.append({
                "name"    : name,
                "age"     : age,
                "gender"  : gender,
                "weight"  : round(weight, 1),
                "height"  : round(height, 1),
                "bmi"     : bmi,
                "category": category,
                "date"    : datetime.datetime.now().strftime("%d %b %Y %I:%M %p")
            })

        except ValueError:
            messagebox.showerror("Input Error",
                                 "Please enter valid numbers for weight and height!")

    def show_history(self):
        if not bmi_history:
            messagebox.showinfo("History", "No history yet! Calculate BMI first.")
            return

        win = tk.Toplevel(self.root)
        win.title("BMI History")
        win.geometry("500x400")
        win.configure(bg=BG_MAIN)

        tk.Label(win, text="BMI History",
                 font=FONT_MED, bg=BG_MAIN, fg=TEXT_W).pack(pady=12)

        text = tk.Text(win, font=FONT_SMALL, bg=BG_INPUT,
                       fg=TEXT_W, relief="flat", bd=12)
        text.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        for h in reversed(bmi_history):
            _, color, emoji = get_category(h["bmi"])
            text.insert(tk.END, f"{'─'*40}\n")
            text.insert(tk.END, f"  {emoji} {h['name']} | {h['date']}\n")
            text.insert(tk.END, f"  BMI: {h['bmi']}  |  {h['category']}\n")
            text.insert(tk.END, f"  Weight: {h['weight']} kg  |  Height: {h['height']} cm\n")
            text.insert(tk.END, f"  Age: {h['age']}  |  Gender: {h['gender']}\n")

        text.config(state="disabled")


# ──────────────────────────────────────────────────────────────
#  RUN
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = BMIApp(root)
    root.mainloop()