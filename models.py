import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("dataset.csv")

# Features and label
X = data.drop("disease", axis=1)
y = data["disease"]

# Convert disease names to numeric codes (required by your Flask project)
disease_mapping = {disease: idx for idx, disease in enumerate(y.unique())}
y = y.map(disease_mapping)

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train SVC model
svc = SVC(kernel='linear')
svc.fit(X_train, y_train)

# Prediction
y_pred = svc.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("SVC Accuracy:", accuracy)

# Save model
with open("models/svc.pkl", "wb") as file:
    pickle.dump(svc, file)

print("Model saved as models/svc.pkl")