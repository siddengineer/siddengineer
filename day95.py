import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Sample Dataset: Risk assessment based on historical event data
data = {
    "Crowd_Size": [100, 500, 1000, 700, 1500],
    "Venue_Capacity": [200, 1000, 1200, 800, 2000],
    "Security_Personnel": [5, 20, 15, 10, 25],
    "Risk_Level": [0, 0, 1, 1, 1]  # 0: Low Risk, 1: High Risk
}

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Features and Labels
X = df[["Crowd_Size", "Venue_Capacity", "Security_Personnel"]]
y = df["Risk_Level"]

# Split into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model: Random Forest Classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test the Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Display Results
print(f"Accuracy: {accuracy * 100:.2f}%")

# Predict Risk for New Event
new_event = [[800, 1000, 12]]  # Example Input: 800 attendees, 1000 capacity, 12 security personnel
risk_prediction = model.predict(new_event)

if risk_prediction[0] == 1:
    print("Risk Level: High. Take additional safety measures!")
else:
    print("Risk Level: Low. Event is manageable.")