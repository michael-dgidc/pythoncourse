import numpy as np

# -----------------------------
# INGREDIENT DATABASE (per 100g)
# -----------------------------
# [cal, protein, carbs, fat, fiber, sugar, iron, potassium, cost]

ingredients = {
    "black_beans":      [130, 9, 23, 0.5, 8, 1, 3.7, 350, 0.40],
    "chickpeas":        [164, 9, 27, 3, 8, 5, 2.9, 290, 0.45],
    "oats":             [380, 13, 67, 7, 10, 1, 4.0, 350, 0.30],
    "walnuts":          [650, 15, 14, 65, 7, 2, 2.9, 440, 1.20],
    "cashews":          [550, 18, 30, 44, 3, 5, 6.7, 550, 1.10],
    "onion":            [40, 1, 9, 0, 2, 4, 0.2, 140, 0.10],
    "olive_oil":        [900, 0, 0, 100, 0, 0, 0, 0, 0.15],
    "nutritional_yeast":[350, 50, 35, 5, 20, 0, 5.0, 2100, 2.00],
    "egg":              [143, 13, 1, 10, 0, 1, 1.8, 138, 0.35],
    "whey_protein":     [400, 80, 8, 6, 0, 4, 0.5, 500, 1.80],
    "broccoli":         [34, 2.8, 7, 0.4, 2.6, 1.7, 0.7, 316, 0.30],
    "spinach":          [23, 2.9, 3.6, 0.4, 2.2, 0.4, 2.7, 558, 0.40],
}

labels = [
    "Calories", "Protein", "Carbs", "Fat",
    "Fibre", "Sugar", "Iron", "Potassium", "Cost (£)"
]

# -----------------------------
# RDA VALUES
# -----------------------------
RDA = {
    "calories": 2000,
    "protein": 50,
    "carbs": 260,
    "fat": 70,
    "fiber": 30,
    "sugar": 90,
    "iron": 14,
    "potassium": 3500
}

metric_keys = ["calories", "protein", "carbs", "fat", "fiber", "sugar", "iron", "potassium"]

# -----------------------------
# INPUT FUNCTION
# -----------------------------
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except:
            print("Enter a number.")

# -----------------------------
# BUILD RECIPE
# -----------------------------
def build_recipe():
    print("\nEnter ingredient percentages (can exceed 100%):\n")

    recipe = {}
    total = 0

    for item in ingredients:
        val = get_float(f"{item:20s}: ")
        recipe[item] = val
        total += val

    # normalize if needed
    if total > 100:
        print("\n⚠ Normalising recipe to 100%\n")
        for k in recipe:
            recipe[k] = recipe[k] / total * 100

    return recipe

# -----------------------------
# CALCULATE NUTRITION
# -----------------------------
def calculate(recipe, burger_size, batch_size):

    total = np.zeros(9)
    total_weight = burger_size * batch_size

    for item, pct in recipe.items():
        grams = total_weight * pct / 100
        total += np.array(ingredients[item]) * grams / 100

    return total

# -----------------------------
# REPORT
# -----------------------------
def print_report(nutrition, burger_size, batch_size):

    print("\n" + "="*45)
    print(" BLIMPO BURGER STUDIO")
    print("="*45)

    print(f"Burger size : {burger_size} g")
    print(f"Batch size  : {batch_size}")
    print(f"Total mix   : {burger_size * batch_size} g")

    per_burger = nutrition / batch_size

    print("\n--- PER BURGER NUTRITION + RDA ---\n")

    for i, key in enumerate(metric_keys):
        val = per_burger[i]

        if key in RDA:
            pct = (val / RDA[key]) * 100
            print(f"{key:12s}: {val:6.1f}  ({pct:5.1f}% RDA)")
        else:
            print(f"{key:12s}: {val:6.1f}")

    cost_per_burger = nutrition[-1] / batch_size

    print("\n--- COST ---")
    print(f"Cost per burger: £{cost_per_burger:.2f}")

    print("\n--- HEALTH FEEDBACK ---")

    if per_burger[1] > 25:
        print("✔ High protein")
    else:
        print("⚠ Low protein")

    if per_burger[4] > 8:
        print("✔ Good fibre")

    if per_burger[6] > 4:
        print("✔ Good iron")

    if per_burger[0] > 600:
        print("⚠ High calorie")

    if cost_per_burger < 1.5:
        print("✔ Budget friendly")
    else:
        print("⚠ Expensive")

# -----------------------------
# MAIN PROGRAM
# -----------------------------
print("🍔 BLIMPO BURGER STUDIO\n")

burger_size = get_float("Burger size (g): ")
batch_size = int(get_float("Batch size (number of burgers): "))

recipe = build_recipe()

nutrition = calculate(recipe, burger_size, batch_size)

print_report(nutrition, burger_size, batch_size)