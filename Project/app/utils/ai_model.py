# 📦 Импорт на NumPy за числови операции и масиви
import numpy as np
# 💾 Импорт на joblib за запис и зареждане на обучени модели
import joblib
# 📂 За проверка на съществуване на файл
import os
# 📊 За изчисляване на метрики
from sklearn.metrics import accuracy_score, mean_squared_error, log_loss
# 📌 Път до файла, в който се пази моделът
MODEL_PATH = 'instance/model.pkl'

class SimpleLogisticRegression:
    def __init__(self):
        # Инициализация на теглата и bias-а (те ще се обучат при нужда)
        self.weights = None
        self.bias = None
        self.training_history = {'loss': [], 'accuracy': []}

    def sigmoid(self, z):
        # Сигмоида — активационна функция за логистична регресия
        return 1 / (1 + np.exp(-z))

    def predict_proba(self, X):
        # Ако моделът не е обучен, обучаваме с dummy данни
        if self.weights is None or self.bias is None:
            X_dummy = np.random.rand(10, X.shape[1])  # 10 примера със същите характеристики
            y_dummy = (X_dummy[:, 0] + X_dummy[:, 1] > 1).astype(int)  # проста логика за target
            self.fit(X_dummy, y_dummy)

        # Връща вероятността (между 0 и 1)
        return self.sigmoid(np.dot(X, self.weights) + self.bias)

    def predict(self, X):
        # Връща 0 или 1 според това дали вероятността е >= 0.5
        return (self.predict_proba(X) >= 0.5).astype(int)

    def fit(self, X, y, lr=0.1, epochs=100):
        # Обучение с градиентен спуск
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # Изчистване на историята на обучението
        self.training_history = {'loss': [], 'accuracy': []}

        for epoch in range(epochs):
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self.sigmoid(linear_model)

            # Градиенти за теглата и bias-а
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)

            # Обновяване на параметрите
            self.weights -= lr * dw
            self.bias -= lr * db
            
            # Изчисляване на метрики за мониторинг
            if epoch % 10 == 0:  # Записваме на всеки 10 епохи
                loss = log_loss(y, y_predicted)
                accuracy = accuracy_score(y, self.predict(X))
                self.training_history['loss'].append(loss)
                self.training_history['accuracy'].append(accuracy)

    def evaluate(self, X_test, y_test):
        """Оценяване на модела с различни метрики"""
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred_proba),
            'log_loss': log_loss(y_test, y_pred_proba),
            'training_loss': self.training_history['loss'][-1] if self.training_history['loss'] else None,
            'training_accuracy': self.training_history['accuracy'][-1] if self.training_history['accuracy'] else None
        }
        
        return metrics

    def save(self):
        # Записване на теглата и bias-а във файл
        joblib.dump((self.weights, self.bias, self.training_history), MODEL_PATH)

    def load(self):
        # Зареждане на модела, ако файлът съществува
        if os.path.exists(MODEL_PATH):
            loaded_data = joblib.load(MODEL_PATH)
            if len(loaded_data) == 3:
                self.weights, self.bias, self.training_history = loaded_data
            else:
                # Backward compatibility
                self.weights, self.bias = loaded_data
                self.training_history = {'loss': [], 'accuracy': []}


model = SimpleLogisticRegression()

def predict_click_probability(survey):
    # 📏 Нормализиране: брой символи в интересите (до 256)
    interests_len = len(survey.interests or "") / 256

    # 📊 Брой избрани реклами, нормализиран (приемаме, че са до 3)
    ad_count = len((survey.selected_ads or "").split(',')) / 3

    # 💻 Кодиране на устройството:
    # PC → 0, Mobile → 0.5, Tablet → 1
    device_score = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2

    # 🧮 Създаване на входен вектор за модела
    X = np.array([
        survey.age / 100,                  # Възрастта като стойност от 0 до 1
        survey.daily_online_hours / 24,   # Онлайн време като стойност от 0 до 1
        device_score,                     # Устройство като числова стойност
        interests_len,                    # Дължина на интересите (0 до 1)
        ad_count                          # Брой реклами (0 до 1)
    ]).reshape(1, -1)  # Преобразуване във формат [1, N]

    # Връщане на закръглената вероятност (примерно: 0.76)
    return round(float(model.predict_proba(X)[0]), 2)
