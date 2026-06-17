
import random
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# -----------------------------
# Generate training data
# -----------------------------
customers = []

for customer_id in range(1, 101):
    age = random.randint(18, 70)
    monthly_spend = random.randint(10, 200)
    months_as_customer = random.randint(1, 60)
    order_count = random.randint(0, 50)

    churned = (
        monthly_spend < 40 and
        months_as_customer < 12
    )

    customers.append({
        "age": age,
        "monthly_spend": monthly_spend,
        "months_as_customer": months_as_customer,
        "order_count": order_count,
        "churned": int(churned)
    })

df = pd.DataFrame(customers)

X = df[
    [
        "age",
        "monthly_spend",
        "months_as_customer",
        "order_count"
    ]
]

y = df["churned"]

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# -----------------------------
# Interactive prediction loop
# -----------------------------
print("Customer Churn Predictor")
print("Type 'q' to quit")

while True:

    age = input("\nCustomer age: ")

    if age.lower() == "q":
        break

    monthly_spend = input("Monthly spend (£): ")
    months_as_customer = input("Months as customer: ")
    order_count = input("Number of orders: ")

    features = [[
        int(age),
        float(monthly_spend),
        int(months_as_customer),
        int(order_count)
    ]]

    prediction = model.predict(features)

    if prediction[0] == 1:
        print("\nPrediction: Customer likely to CHURN")
    else:
        print("\nPrediction: Customer likely to STAY")

