import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Training data
data = {
    "hours_studied": [1, 2, 3, 4, 5, 6, 7, 8],
    "passed": [0, 0, 0, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

# Features (X) and labels (y)
X = df[["hours_studied"]]
y = df["passed"]

# Create and train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Make predictions
prediction1 = model.predict([[2]])
prediction2 = model.predict([[6]])

print("Student studying 2 hours:", prediction1[0])
print("Student studying 6 hours:", prediction2[0])