# ============================================================
#  BMI Calculator - Basic Version (Command Line)
#  Concepts: Input, Calculation, Categorization, Validation
# ============================================================

def calculate_bmi(weight_kg, height_m):
    """
    Formula: BMI = weight (kg) / height² (m²)
    """
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    """
    WHO standard BMI categories.
    Returns the category name and a short health note.
    """
    if bmi < 18.5:
        return "Underweight", "Consider consulting a nutritionist."
    elif 18.5 <= bmi < 25.0:
        return "Normal weight", "Great! Keep maintaining a healthy lifestyle."
    elif 25.0 <= bmi < 30.0:
        return "Overweight", "Consider a balanced diet and regular exercise."
    else:
        return "Obese", "Please consult a healthcare professional."


def get_positive_float(prompt, min_val, max_val):
    """
    Keeps asking until the user enters a valid number
    within the allowed range. Handles non-numeric input too.
    """
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"  ⚠  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  That doesn't look like a number. Try again.")


def main():
    print("=" * 45)
    print("       BMI CALCULATOR — Basic Version")
    print("=" * 45)

    # ---------- Collect inputs ----------
    weight = get_positive_float(
        "Enter your weight (kg)  [1 – 500]: ",
        min_val=1, max_val=500
    )
    height = get_positive_float(
        "Enter your height (m)   [0.5 – 3.0]: ",
        min_val=0.5, max_val=3.0
    )

    # ---------- Calculate ----------
    bmi = calculate_bmi(weight, height)
    category, advice = classify_bmi(bmi)

    # ---------- Display result ----------
    print("\n" + "-" * 45)
    print(f"  Your BMI       : {bmi:.2f}")
    print(f"  Category       : {category}")
    print(f"  Health Note    : {advice}")
    print("-" * 45)

    # ---------- Visual scale ----------
    print("\n  BMI Scale:")
    print("  < 18.5   →  Underweight")
    print("  18.5–24.9 → Normal weight  ✓")
    print("  25.0–29.9 → Overweight")
    print("  ≥ 30.0   →  Obese")
    print("=" * 45)


if __name__ == "__main__":
    main()