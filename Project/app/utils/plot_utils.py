import os
import numpy as np
import matplotlib.pyplot as plt
from app.utils.ai_model import model

RESULTS_PATH = "app/static/results"

def generate_user_plot(user_id, survey):
    # 1. Prepare data point
    x_user = np.array([
        survey.age / 100,
        survey.daily_online_hours / 24,
        0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2,
        len(survey.interests) / 256
    ])

    x_user = x_user.reshape(1, -1)

    # 2. Create dummy training data for decision boundary (just for visual)
    np.random.seed(42)
    X = np.random.rand(100, 4)
    y = (X[:, 0] + X[:, 1] > 1).astype(int)
    model.fit(X, y)

    # 3. Predict grid for plotting decision boundary (using only 2 dims)
    x0 = X[:, 0]
    x1 = X[:, 1]
    grid_x, grid_y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    Z = model.sigmoid(grid_x * model.weights[0] + grid_y * model.weights[1] + model.bias)

    # 4. Plot
    plt.figure(figsize=(6, 5))
    plt.contourf(grid_x, grid_y, Z, levels=50, cmap='Blues', alpha=0.6)
    plt.colorbar(label='Click Probability')
    plt.scatter(x_user[0][0], x_user[0][1], color='red', label='You', edgecolors='black')
    plt.title('Logistic Regression Decision Space')
    plt.xlabel('Normalized Age')
    plt.ylabel('Normalized Hours Online')
    plt.legend()

    # 5. Save figure
    os.makedirs(RESULTS_PATH, exist_ok=True)
    filename = f"user_{user_id}.png"
    filepath = os.path.join(RESULTS_PATH, filename)
    plt.savefig(filepath)
    plt.close()

    return filename  # Return relative path to be shown in HTML
