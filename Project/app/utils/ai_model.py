import numpy as np
import joblib
import os

MODEL_PATH = 'instance/model.pkl'

class SimpleLogisticRegression:
    def __init__(self):
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict_proba(self, X):
        if self.weights is None or self.bias is None:
            # Automatically fit dummy data if not trained
            X_dummy = np.random.rand(10, X.shape[1])
            y_dummy = (X_dummy[:, 0] + X_dummy[:, 1] > 1).astype(int)
            self.fit(X_dummy, y_dummy)
        return self.sigmoid(np.dot(X, self.weights) + self.bias)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)

    def fit(self, X, y, lr=0.1, epochs=100):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        for _ in range(epochs):
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self.sigmoid(linear_model)
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)
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
