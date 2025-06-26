# 📦 Импорт на NumPy за числови операции и масиви
import numpy as np
# 💾 Импорт на joblib за запис и зареждане на обучени модели
import joblib
# 📂 За проверка на съществуване на файл
import os
<<<<<<< HEAD
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, log_loss
from sklearn.model_selection import train_test_split
from app import db
from app.models import SurveyResponse, ModelWeights, AdClick
import pandas as pd

MODEL_PATH = 'instance/model.pkl'

class EnhancedLogisticRegression:
=======
# 📊 За изчисляване на метрики
from sklearn.metrics import accuracy_score, mean_squared_error, log_loss
# 📌 Път до файла, в който се пази моделът
MODEL_PATH = 'instance/model.pkl'

class SimpleLogisticRegression:
>>>>>>> b9fdf71cb45a9dbe4f7b1a8245ed9de52c9b2818
    def __init__(self):
        # Инициализация на теглата и bias-а (те ще се обучат при нужда)
        self.weights = None
        self.bias = None
<<<<<<< HEAD
        self.feature_names = [
            'age_normalized', 'daily_online_hours_normalized', 'device_score',
            'interests_length', 'ad_count', 'streaming_apps_count_normalized',
            'video_clip_length_normalized'
        ]
        self.metrics = {}
=======
        self.training_history = {'loss': [], 'accuracy': []}
>>>>>>> b9fdf71cb45a9dbe4f7b1a8245ed9de52c9b2818

    def sigmoid(self, z):
        # Сигмоида — активационна функция за логистична регресия
        return 1 / (1 + np.exp(-z))

    def predict_proba(self, X):
        # Ако моделът не е обучен, обучаваме с dummy данни
        if self.weights is None or self.bias is None:
<<<<<<< HEAD
            self.load_from_db()
            if self.weights is None:
                # Initialize with dummy data if no trained model exists
                X_dummy = np.random.rand(10, len(self.feature_names))
                y_dummy = (X_dummy[:, 0] + X_dummy[:, 1] > 1).astype(int)
                self.fit(X_dummy, y_dummy)
=======
            X_dummy = np.random.rand(10, X.shape[1])  # 10 примера със същите характеристики
            y_dummy = (X_dummy[:, 0] + X_dummy[:, 1] > 1).astype(int)  # проста логика за target
            self.fit(X_dummy, y_dummy)

        # Връща вероятността (между 0 и 1)
>>>>>>> b9fdf71cb45a9dbe4f7b1a8245ed9de52c9b2818
        return self.sigmoid(np.dot(X, self.weights) + self.bias)

    def predict(self, X):
        # Връща 0 или 1 според това дали вероятността е >= 0.5
        return (self.predict_proba(X) >= 0.5).astype(int)

    def fit(self, X, y, lr=0.1, epochs=100):
        # Обучение с градиентен спуск
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
<<<<<<< HEAD
        for _ in range(epochs):
=======
        # Изчистване на историята на обучението
        self.training_history = {'loss': [], 'accuracy': []}

        for epoch in range(epochs):
>>>>>>> b9fdf71cb45a9dbe4f7b1a8245ed9de52c9b2818
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
                loss = log_loss(y, y_predicted, labels=[0, 1])
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
            'log_loss': log_loss(y_test, y_pred_proba, labels=[0, 1]),
            'training_loss': self.training_history['loss'][-1] if self.training_history['loss'] else None,
            'training_accuracy': self.training_history['accuracy'][-1] if self.training_history['accuracy'] else None
        }
        
        return metrics

    def calculate_metrics(self, X, y_true):
        y_pred = self.predict(X)
        y_pred_proba = self.predict_proba(X)
        
        self.metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0),
            'logloss': log_loss(y_true, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
        return self.metrics

    def information_gain(self, X, y, feature_idx):
        """Calculate information gain for a specific feature"""
        from sklearn.tree import DecisionTreeClassifier
        
        # Calculate entropy of the target variable
        def entropy(y):
            classes, counts = np.unique(y, return_counts=True)
            probabilities = counts / len(y)
            return -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        initial_entropy = entropy(y)
        
        # Split on the feature
        feature_values = X[:, feature_idx]
        unique_values = np.unique(feature_values)
        
        weighted_entropy = 0
        for value in unique_values:
            mask = feature_values == value
            subset_y = y[mask]
            if len(subset_y) > 0:
                weighted_entropy += (len(subset_y) / len(y)) * entropy(subset_y)
        
        return initial_entropy - weighted_entropy

    def calculate_feature_importance(self, X, y):
        """Calculate information gain for all features"""
        importance = {}
        for i, feature_name in enumerate(self.feature_names):
            importance[feature_name] = self.information_gain(X, y, i)
        return importance

    def save_to_db(self):
        """Save model weights and metrics to database"""
        weights_json = json.dumps(self.weights.tolist())
        
        model_weights = ModelWeights(
            weights=weights_json,
            bias=float(self.bias),
            accuracy=self.metrics.get('accuracy', 0.0),
            precision=self.metrics.get('precision', 0.0),
            recall=self.metrics.get('recall', 0.0),
            f1_score=self.metrics.get('f1_score', 0.0),
            logloss=self.metrics.get('logloss', 0.0)
        )
        
        db.session.add(model_weights)
        db.session.commit()

    def load_from_db(self):
        """Load the latest model weights from database"""
        latest_model = ModelWeights.query.order_by(ModelWeights.training_date.desc()).first()
        if latest_model:
            self.weights = np.array(json.loads(latest_model.weights))
            self.bias = latest_model.bias
            self.metrics = {
                'accuracy': latest_model.accuracy,
                'precision': latest_model.precision,
                'recall': latest_model.recall,
                'f1_score': latest_model.f1_score,
                'logloss': latest_model.logloss
            }

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


def prepare_training_data():
    """Prepare training data from survey responses and ad clicks"""
    surveys = SurveyResponse.query.all()
    
    if len(surveys) < 10:  # Need minimum data for training
        return None, None
    
    X_data = []
    y_data = []
    
    for survey in surveys:
        # Get ad clicks for this user
        ad_clicks = AdClick.query.filter_by(user_id=survey.user_id).count()
        has_clicked = 1 if ad_clicks > 0 else 0
        
        # Prepare features
        interests_len = len(survey.interests or "") / 256
        ad_count = len((survey.selected_ads or "").split(',')) / 3
        device_score = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2
        
        features = [
            survey.age / 100,  # Normalized age
            survey.daily_online_hours / 24,  # Normalized hours
            device_score,
            interests_len,
            ad_count,
            survey.streaming_apps_count / 20,  # Normalized streaming apps
            survey.video_clip_length / 300  # Normalized video length
        ]
        
        X_data.append(features)
        y_data.append(has_clicked)
    
    return np.array(X_data), np.array(y_data)

def train_model():
    """Train the model with current data"""
    X, y = prepare_training_data()
    
    if X is None or len(X) < 10:
        return None
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = EnhancedLogisticRegression()
    model.fit(X_train, y_train, epochs=200)
    
    # Calculate metrics
    metrics = model.calculate_metrics(X_test, y_test)
    
    # Save to database
    model.save_to_db()
    
    return model, metrics

model = EnhancedLogisticRegression()

def predict_click_probability(survey):
<<<<<<< HEAD
    """Predict click probability for a survey response"""
    interests_len = len(survey.interests or "") / 256
    ad_count = len((survey.selected_ads or "").split(',')) / 3
=======
    # 📏 Нормализиране: брой символи в интересите (до 256)
    interests_len = len(survey.interests or "") / 256

    # 📊 Брой избрани реклами, нормализиран (приемаме, че са до 3)
    ad_count = len((survey.selected_ads or "").split(',')) / 3

    # 💻 Кодиране на устройството:
    # PC → 0, Mobile → 0.5, Tablet → 1
>>>>>>> b9fdf71cb45a9dbe4f7b1a8245ed9de52c9b2818
    device_score = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2

    # 🧮 Създаване на входен вектор за модела
    X = np.array([
<<<<<<< HEAD
        survey.age / 100,
        survey.daily_online_hours / 24,
        device_score,
        interests_len,
        ad_count,
        survey.streaming_apps_count / 20,
        survey.video_clip_length / 300
    ]).reshape(1, -1)
=======
        survey.age / 100,                  # Възрастта като стойност от 0 до 1
        survey.daily_online_hours / 24,   # Онлайн време като стойност от 0 до 1
        device_score,                     # Устройство като числова стойност
        interests_len,                    # Дължина на интересите (0 до 1)
        ad_count                          # Брой реклами (0 до 1)
    ]).reshape(1, -1)  # Преобразуване във формат [1, N]
>>>>>>> b9fdf71cb45a9dbe4f7b1a8245ed9de52c9b2818

    # Връщане на закръглената вероятност (примерно: 0.76)
    return round(float(model.predict_proba(X)[0]), 2)
<<<<<<< HEAD

def get_model_metrics():
    """Get the latest model metrics"""
    latest_model = ModelWeights.query.order_by(ModelWeights.training_date.desc()).first()
    if latest_model:
        return {
            'accuracy': latest_model.accuracy,
            'precision': latest_model.precision,
            'recall': latest_model.recall,
            'f1_score': latest_model.f1_score,
            'logloss': latest_model.logloss,
            'training_date': latest_model.training_date
        }
    return None

def get_feature_importance():
    """Calculate and return feature importance"""
    X, y = prepare_training_data()
    if X is None:
        return {}
    
    model = EnhancedLogisticRegression()
    return model.calculate_feature_importance(X, y)

=======
>>>>>>> b9fdf71cb45a9dbe4f7b1a8245ed9de52c9b2818
