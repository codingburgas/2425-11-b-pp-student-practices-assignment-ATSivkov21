import os
import numpy as np
from app import create_app, db
from app.models import SurveyResponse
from ai_model import model, MODEL_PATH

def get_training_data():
    # Fetch all survey responses
    surveys = SurveyResponse.query.all()
    X = []
    y = []
    for s in surveys:
        interests_len = len(s.interests or "") / 256
        ad_count = len((s.selected_ads or "").split(',')) / 3
        device_score = 0 if s.device == 'PC' else (1 if s.device == 'Mobile' else 2) / 2
        X.append([
            s.age / 100,
            s.daily_online_hours / 24,
            device_score,
            interests_len,
            ad_count
        ])
        # For demo: if user selected any ad, treat as 'clicked' (1), else 0
        y.append(1 if ad_count > 0 else 0)
    return np.array(X), np.array(y)

def main():
    app = create_app()
    with app.app_context():
        X, y = get_training_data()
        if len(X) == 0:
            print("No survey data found. Please collect data first.")
            return
        model.fit(X, y)
        model.save()
        print(f"Model trained and saved to {MODEL_PATH}")

if __name__ == "__main__":
    main() 