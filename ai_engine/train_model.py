import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load Data
df = pd.read_csv('training_data.csv')
X = df[['budget', 'email_clicks', 'days_on_market']]
y = df['converted']

# 2. Split (80% for training, 20% for testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 3. Train
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# 4. Validate
accuracy = clf.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 5. Export the Brain
joblib.dump(clf, 'lead_scoring_model.joblib')
print("Model saved to lead_scoring_model.joblib")