import numpy as np
import joblib
import os
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, log_loss
from sklearn.model_selection import train_test_split
from app import db
from app.models import SurveyResponse, ModelWeights, AdClick
import pandas as pd

MODEL_PATH = 'instance/model.pkl'

class EnhancedLogisticRegression:
    def __init__(self):
        self.weights = None
        self.bias = None
        self.feature_names = [
            'age_normalized', 'daily_online_hours_normalized', 'device_score',
            'interests_length', 'ad_count', 'streaming_apps_count_normalized',
            'video_clip_length_normalized'
        ]
        self.metrics = {}

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict_proba(self, X):
        if self.weights is None or self.bias is None:
            self.load_from_db()
            if self.weights is None:
                # Initialize with dummy data if no trained model exists
                X_dummy = np.random.rand(10, len(self.feature_names))
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
        joblib.dump((self.weights, self.bias), MODEL_PATH)

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.weights, self.bias = joblib.load(MODEL_PATH)

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
    """Predict click probability for a survey response"""
    interests_len = len(survey.interests or "") / 256
    ad_count = len((survey.selected_ads or "").split(',')) / 3
    device_score = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2

    X = np.array([
        survey.age / 100,
        survey.daily_online_hours / 24,
        device_score,
        interests_len,
        ad_count,
        survey.streaming_apps_count / 20,
        survey.video_clip_length / 300
    ]).reshape(1, -1)

    return round(float(model.predict_proba(X)[0]), 2)

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

