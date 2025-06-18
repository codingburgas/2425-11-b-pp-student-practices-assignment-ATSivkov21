# 📂 За работа с файловата система (създаване на папки, пътища и т.н.)
import os
# 📊 Импорт на NumPy за векторни и числови операции
import numpy as np
# 🎨 Импорт на matplotlib за генериране на графики
import matplotlib
matplotlib.use('Agg')  # Използва неинтерактивен бекенд (за сървърни среди без GUI)
import matplotlib.pyplot as plt  # Импорт на pyplot за създаване на графики
# 🧠 Импорт на логистичния модел, използван за обучение и предсказване
from app.utils.ai_model import model
# 📁 Папка, в която ще се записват изображенията
RESULTS_PATH = "app/static/results"

def generate_user_plot(survey, plot_path):
    # 1. Prepare data point
    x = np.array([
        survey.age / 100,
        survey.daily_online_hours / 24,
        0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2,
        len(survey.interests.split(',')) / 10,  # Normalize by expected max number of interests
        1 if survey.selected_ads else 0  # Binary feature for ad selection
    ]).reshape(1, -1)

    # 2. Create dummy training data for decision boundary (just for visual)
    np.random.seed(42)
    X = np.random.rand(100, 5)
    y = (X[:, 0] + X[:, 1] + X[:, 4] > 1.5).astype(int)
    model.fit(X, y)

    # 3. Plot
    plt.figure(figsize=(6, 5))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', alpha=0.5)
    plt.scatter(x[0][0], x[0][1], color='black', label='You', s=100)
    plt.xlabel('Age (normalized)')
    plt.ylabel('Hours Online (normalized)')
    plt.title('User Survey Results Visualization')
    plt.legend()

    # 4. Save figure
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()

    return os.path.basename(plot_path)  # Return just the filename
