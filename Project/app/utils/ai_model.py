# 📦 Импорт на NumPy за числови операции и масиви
import numpy as np
# 💾 Импорт на joblib за запис и зареждане на обучени модели
import joblib
# 📂 За проверка на съществуване на файл
import os
# 📊 За изчисляване на метрики
from sklearn.metrics import accuracy_score, mean_squared_error, log_loss, precision_score, recall_score, f1_score, confusion_matrix
# 📌 Път до файла, в който се пази моделът
MODEL_PATH = 'instance/model.pkl'
from sklearn.linear_model import LogisticRegression

class SklearnSoftmaxLogisticRegression:
    def __init__(self):
        self.model = None
        self.training_history = {'loss': [], 'accuracy': []}

    def fit(self, X, y):
        self.model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200)
        self.model.fit(X, y)
        # Optionally store training metrics if needed

    def predict_proba(self, X):
        if self.model is None:
            raise ValueError('Model not trained!')
        return self.model.predict_proba(X)

    def predict(self, X):
        if self.model is None:
            raise ValueError('Model not trained!')
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'log_loss': log_loss(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        return metrics

    def save(self):
        joblib.dump(self.model, MODEL_PATH)

    def load(self):
        if os.path.exists(MODEL_PATH):
            loaded = joblib.load(MODEL_PATH)
            if isinstance(loaded, tuple):
                print("Error: The loaded model is in an old format (tuple). Please delete 'instance/model.pkl' and retrain the model.")
                self.model = None
            else:
                self.model = loaded

model = SklearnSoftmaxLogisticRegression()

def predict_click_probability(survey):
    interests_len = len(survey.interests or "") / 256
    ad_count = len((survey.selected_ads or "").split(',')) / 3
    device_score = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2
    social_names = (survey.social_media_names or "").split(',')
    social_lengths = [float(x) for x in (survey.social_media_lengths or "").split(',') if x.strip().replace('.', '', 1).isdigit()]
    num_social = len([s for s in social_names if s.strip()]) / 10
    total_social_time = sum(social_lengths) / 24
    X = np.array([
        survey.age / 100,
        survey.daily_online_hours / 24,
        device_score,
        interests_len,
        ad_count,
        num_social,
        total_social_time
    ]).reshape(1, -1)
    model.load()
    proba = model.predict_proba(X)
    # Return the probability of the most likely class (for binary, class 1)
    return round(float(proba[0, 1]), 2) if proba.shape[1] > 1 else round(float(proba[0, 0]), 2)
