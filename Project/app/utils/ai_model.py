import numpy as np
import joblib
import os

MODEL_PATH = 'instance/model.pkl'

class SimpleLogisticRegression:
    def __init__(self):
        self.weights = None
        self.bias = 0

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict_proba(self, X):
        return self.sigmoid(np.dot(X, self.weights) + self.bias)

    def predict(self, X):
        return self.predict_proba(X) >= 0.5

    def fit(self, X, y, epochs=1000, lr=0.01):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(epochs):
            model = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(model)
            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
            db = (1 / n_samples) * np.sum(predictions - y)

            self.weights -= lr * dw
            self.bias -= lr * db

    def save(self):
        joblib.dump((self.weights, self.bias), MODEL_PATH)

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.weights, self.bias = joblib.load(MODEL_PATH)

model = SimpleLogisticRegression()
model.load()

def predict_click_probability(survey):
    # Dummy feature engineering
    age = survey.age / 100
    hours = survey.daily_online_hours / 24
    device = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2)
    interests = len(survey.interests) / 256
    
    X = np.array([[age, hours, device / 2, interests]])
    return round(float(model.predict_proba(X)[0]), 2)
