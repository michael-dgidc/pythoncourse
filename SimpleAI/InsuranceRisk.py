
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------
# Generate training data
# -----------------------------------

customers = []

for _ in range(500):

    age = random.randint(18, 80)
    years_driving = max(age - 17, 1)

    accidents = random.randint(0, 5)

    car_value = random.randint(3000, 80000)

    annual_mileage = random.randint(2000, 30000)

    # Artificial business rule
    high_risk = (
        accidents >= 3
        or (age < 25 and annual_mileage > 15000)
    )

    customers.append({
        "age": age,
        "years_driving": years_driving,
        "accidents": accidents,
        "car_value": car_value,
        "annual_mileage": annual_mileage,
        "high_risk": int(high_risk)
    })

df = pd.DataFrame(customers)

# -----------------------------------
# Train Model
# -----------------------------------

X = df[
    [
        "age",
        "years_driving",
        "accidents",
        "car_value",
        "annual_mileage"
    ]
]

y = df["high_risk"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# -----------------------------------
# Interactive Prediction Loop
# -----------------------------------

print("Insurance Risk Predictor")
print("Enter q to quit")

while True:

    age = input("\nAge: ")

    if age.lower() == "q":
        break

    years_driving = int(input("Years driving: "))
    accidents = int(input("Number of accidents: "))
    car_value = float(input("Car value (£): "))
    annual_mileage = int(input("Annual mileage: "))

    features = [[
        int(age),
        years_driving,
        accidents,
        car_value,
        annual_mileage
    ]]

    prediction = model.predict(features)[0]

    confidence = max(
        model.predict_proba(features)[0]
    )

    if prediction == 1:
        print(
            f"\nHIGH RISK ({confidence:.1%} confidence)"
        )
    else:
        print(
            f"\nLOW RISK ({confidence:.1%} confidence)"
        )

