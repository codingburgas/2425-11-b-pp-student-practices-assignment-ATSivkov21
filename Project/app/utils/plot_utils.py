import os
import numpy as np
import matplotlib.pyplot as plt
from app.utils.ai_model import model

RESULTS_PATH = "app/static/results"

def generate_user_plot(user_id, survey):
    # 1. Prepare data point
    x = np.array([
        survey.age / 100,
        survey.daily_online_hours / 24,
        0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2,
        len(survey.interests) / 256,
        len(survey.selected_ads.split(',')) / 3
    ]).reshape(1, -1)

    # 2. Create dummy training data for decision boundary (just for visual)
    np.random.seed(42)
    X = np.random.rand(100, 5)
    y = (X[:, 0] + X[:, 1] + X[:, 4] > 1.5).astype(int)
    model.fit(X, y)

    # 3. Predict grid for plotting decision boundary (using only 2 dims)
    # 4. Plot
    plt.figure(figsize=(6, 5))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', alpha=0.5)
    plt.scatter(x[0][0], x[0][1], color='black', label='You', s=100)
    plt.xlabel('Age')
    plt.ylabel('Hours Online')
    plt.title('Logistic Regression - Decision Plot')
    plt.legend()

    # 5. Save figure
    os.makedirs(RESULTS_PATH, exist_ok=True)
    filename = f'user_{user_id}.png'
    filepath = os.path.join(RESULTS_PATH, filename)
    plt.savefig(filepath)
    plt.close()

    return filename  # Return relative path to be shown in HTML
