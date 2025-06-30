# 📦 Импорт на NumPy за числови операции и масиви
import numpy as np
# 💾 Импорт на joblib за запис и зареждане на обучени модели
import joblib
# 📂 За проверка на съществуване на файл
import os
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from app import db
from app.models import SurveyResponse, ModelWeights, AdClick
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

MODEL_PATH = 'instance/model.pkl'

class SoftmaxLogisticRegression:
    def __init__(self, num_classes=2):
        # Инициализация на теглата и bias-а (те ще се обучат при нужда)
        self.weights = None
        self.bias = None
        self.num_classes = num_classes
        self.scaler = StandardScaler()
        self.feature_names = [
            'age_normalized', 'daily_online_hours_normalized', 'device_score',
            'interests_length', 'ad_count', 'streaming_apps_count_normalized',
            'video_clip_length_normalized'
        ]
        self.metrics = {}
        self.training_history = {'loss': [], 'accuracy': []}
        self.feature_importance = {}

    def softmax(self, z):
        """Softmax activation function for multi-class classification"""
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # Numerical stability
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def sigmoid(self, z):
        """Sigmoid activation function for binary classification"""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))  # Clip for numerical stability

    def predict_proba(self, X):
        """Predict class probabilities"""
        if self.weights is None or self.bias is None:
            self.load_from_db()
            if self.weights is None:
                # Initialize with dummy data if no trained model exists
                X_dummy = np.random.rand(10, len(self.feature_names))
                y_dummy = (X_dummy[:, 0] + X_dummy[:, 1] > 1).astype(int)
                self.fit(X_dummy, y_dummy)

        if self.num_classes == 2:
            # Binary classification
            return self.sigmoid(np.dot(X, self.weights) + self.bias)
        else:
            # Multi-class classification
            logits = np.dot(X, self.weights) + self.bias
            return self.softmax(logits)

    def predict(self, X):
        """Predict class labels"""
        if self.num_classes == 2:
            # Binary classification
            return (self.predict_proba(X) >= 0.5).astype(int)
        else:
            # Multi-class classification
            return np.argmax(self.predict_proba(X), axis=1)

    def cross_entropy_loss(self, y_true, y_pred):
        """Calculate cross-entropy loss (log loss)"""
        epsilon = 1e-15  # Small value to prevent log(0)
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        
        if self.num_classes == 2:
            # Binary cross-entropy
            return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        else:
            # Multi-class cross-entropy
            return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))

    def fit(self, X, y, lr=0.01, epochs=1000, batch_size=32):
        """Train the model using gradient descent with mini-batches"""
        n_samples, n_features = X.shape
        
        # Initialize weights and bias
        if self.num_classes == 2:
            self.weights = np.zeros(n_features)
            self.bias = 0
        else:
            self.weights = np.zeros((n_features, self.num_classes))
            self.bias = np.zeros(self.num_classes)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Convert y to one-hot encoding for multi-class
        if self.num_classes > 2:
            y_one_hot = np.eye(self.num_classes)[y]
        else:
            y_one_hot = y

        # Clear training history
        self.training_history = {'loss': [], 'accuracy': []}

        for epoch in range(epochs):
            # Mini-batch gradient descent
            for i in range(0, n_samples, batch_size):
                batch_X = X_scaled[i:i+batch_size]
                batch_y = y_one_hot[i:i+batch_size] if self.num_classes > 2 else y[i:i+batch_size]
                
                # Forward pass
                if self.num_classes == 2:
                    linear_model = np.dot(batch_X, self.weights) + self.bias
                    y_predicted = self.sigmoid(linear_model)
                    
                    # Gradients
                    dw = (1 / len(batch_X)) * np.dot(batch_X.T, (y_predicted - batch_y))
                    db = (1 / len(batch_X)) * np.sum(y_predicted - batch_y)
                else:
                    logits = np.dot(batch_X, self.weights) + self.bias
                    y_predicted = self.softmax(logits)
                    
                    # Gradients
                    dw = (1 / len(batch_X)) * np.dot(batch_X.T, (y_predicted - batch_y))
                    db = (1 / len(batch_X)) * np.sum(y_predicted - batch_y, axis=0)

                # Update parameters
                self.weights -= lr * dw
                self.bias -= lr * db

            # Calculate metrics every 100 epochs
            if epoch % 100 == 0:
                y_pred_proba = self.predict_proba(X_scaled)
                loss = self.cross_entropy_loss(y_one_hot, y_pred_proba)
                accuracy = accuracy_score(y, self.predict(X_scaled))
                
                self.training_history['loss'].append(loss)
                self.training_history['accuracy'].append(accuracy)

        # Calculate final metrics
        self.calculate_metrics(X_scaled, y)

    def calculate_metrics(self, X, y_true):
        """Calculate comprehensive model metrics"""
        y_pred = self.predict(X)
        y_pred_proba = self.predict_proba(X)
        
        # For binary classification, we need to handle the case where there's only one class
        if self.num_classes == 2:
            # Ensure we have both classes for metrics calculation
            if len(np.unique(y_true)) == 1:
                # Only one class present
                self.metrics = {
                    'accuracy': accuracy_score(y_true, y_pred),
                    'precision': 1.0 if y_true[0] == 1 else 0.0,
                    'recall': 1.0 if y_true[0] == 1 else 0.0,
                    'f1_score': 1.0 if y_true[0] == 1 else 0.0,
                    'logloss': log_loss(y_true, y_pred_proba, labels=[0, 1]),
                    'confusion_matrix': confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()
                }
            else:
                self.metrics = {
                    'accuracy': accuracy_score(y_true, y_pred),
                    'precision': precision_score(y_true, y_pred, zero_division=0),
                    'recall': recall_score(y_true, y_pred, zero_division=0),
                    'f1_score': f1_score(y_true, y_pred, zero_division=0),
                    'logloss': log_loss(y_true, y_pred_proba, labels=[0, 1]),
                    'confusion_matrix': confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()
                }
        else:
            # Multi-class metrics
            self.metrics = {
                'accuracy': accuracy_score(y_true, y_pred),
                'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
                'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
                'logloss': log_loss(y_true, y_pred_proba),
                'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
            }
        
        return self.metrics

    def information_gain(self, X, y, feature_idx):
        """Calculate information gain for a specific feature"""
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
        
        self.feature_importance = importance
        return importance

    def save_to_db(self):
        """Save model weights and metrics to database"""
        weights_json = json.dumps(self.weights.tolist())
        
        model_weights = ModelWeights(
            weights=weights_json,
            bias=float(self.bias) if self.num_classes == 2 else json.dumps(self.bias.tolist()),
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
            if isinstance(latest_model.bias, str):
                self.bias = np.array(json.loads(latest_model.bias))
            else:
                self.bias = latest_model.bias
            self.metrics = {
                'accuracy': latest_model.accuracy,
                'precision': latest_model.precision,
                'recall': latest_model.recall,
                'f1_score': latest_model.f1_score,
                'logloss': latest_model.logloss
            }

    def save(self):
        """Save model to file"""
        model_data = {
            'weights': self.weights,
            'bias': self.bias,
            'scaler': self.scaler,
            'training_history': self.training_history,
            'feature_importance': self.feature_importance,
            'metrics': self.metrics,
            'num_classes': self.num_classes
        }
        joblib.dump(model_data, MODEL_PATH)

    def load(self):
        """Load model from file"""
        if os.path.exists(MODEL_PATH):
            model_data = joblib.load(MODEL_PATH)
            if isinstance(model_data, dict):
                self.weights = model_data['weights']
                self.bias = model_data['bias']
                self.scaler = model_data.get('scaler', StandardScaler())
                self.training_history = model_data.get('training_history', {'loss': [], 'accuracy': []})
                self.feature_importance = model_data.get('feature_importance', {})
                self.metrics = model_data.get('metrics', {})
                self.num_classes = model_data.get('num_classes', 2)
            else:
                # Backward compatibility
                self.weights, self.bias = model_data
                self.training_history = {'loss': [], 'accuracy': []}

    def plot_training_history(self, save_path=None):
        """Plot training history"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Loss plot
        ax1.plot(self.training_history['loss'])
        ax1.set_title('Training Loss (Cross-Entropy)')
        ax1.set_xlabel('Epoch (x100)')
        ax1.set_ylabel('Loss')
        ax1.grid(True)
        
        # Accuracy plot
        ax2.plot(self.training_history['accuracy'])
        ax2.set_title('Training Accuracy')
        ax2.set_xlabel('Epoch (x100)')
        ax2.set_ylabel('Accuracy')
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def plot_confusion_matrix(self, X, y_true, save_path=None):
        """Plot confusion matrix"""
        y_pred = self.predict(X)
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['No Click', 'Click'], 
                   yticklabels=['No Click', 'Click'])
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def plot_feature_importance(self, save_path=None):
        """Plot feature importance"""
        if not self.feature_importance:
            return
        
        features = list(self.feature_importance.keys())
        importance = list(self.feature_importance.values())
        
        # Sort by importance
        sorted_indices = np.argsort(importance)[::-1]
        features = [features[i] for i in sorted_indices]
        importance = [importance[i] for i in sorted_indices]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(range(len(features)), importance)
        plt.xlabel('Features')
        plt.ylabel('Information Gain')
        plt.title('Feature Importance (Information Gain)')
        plt.xticks(range(len(features)), [f.replace('_', ' ').title() for f in features], rotation=45, ha='right')
        plt.tight_layout()
        
        # Add value labels on bars
        for bar, imp in zip(bars, importance):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001, 
                    f'{imp:.4f}', ha='center', va='bottom')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()


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
        return None, None
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = SoftmaxLogisticRegression(num_classes=2)
    model.fit(X_train, y_train, epochs=500)
    
    # Calculate feature importance
    model.calculate_feature_importance(X_train, y_train)
    
    # Calculate metrics on test set
    metrics = model.calculate_metrics(X_test, y_test)
    
    # Save to database
    model.save_to_db()
    
    # Save model to file
    model.save()
    
    return model, metrics

model = SoftmaxLogisticRegression(num_classes=2)

def predict_click_probability(survey):
    """Predict click probability for a survey response"""
    interests_len = len(survey.interests or "") / 256
    ad_count = len((survey.selected_ads or "").split(',')) / 3
    device_score = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2

    # Create input vector for the model
    X = np.array([
        survey.age / 100,
        survey.daily_online_hours / 24,
        device_score,
        interests_len,
        ad_count,
        survey.streaming_apps_count / 20,
        survey.video_clip_length / 300
    ]).reshape(1, -1)

    # Return rounded probability
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
    
    model = SoftmaxLogisticRegression()
    return model.calculate_feature_importance(X, y)

def generate_model_plots():
    """Generate and save model visualization plots"""
    X, y = prepare_training_data()
    if X is None:
        return None
    
    model = SoftmaxLogisticRegression()
    model.load()
    
    # Generate plots
    plots = {}
    
    # Training history plot
    if model.training_history['loss']:
        history_path = 'static/results/training_history.png'
        model.plot_training_history(history_path)
        plots['training_history'] = history_path
    
    # Confusion matrix plot
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    cm_path = 'static/results/confusion_matrix.png'
    model.plot_confusion_matrix(X_test, y_test, cm_path)
    plots['confusion_matrix'] = cm_path
    
    # Feature importance plot
    if model.feature_importance:
        fi_path = 'static/results/feature_importance.png'
        model.plot_feature_importance(fi_path)
        plots['feature_importance'] = fi_path
    
    return plots
