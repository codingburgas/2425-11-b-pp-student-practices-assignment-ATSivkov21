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
    # 1. Prepare data point with all 8 features
    interests_len = len(survey.interests or "") / 256
    social_media_len = len(survey.social_media or "") / 500
    ad_count = len((survey.selected_ads or "").split(',')) / 3
    device_score = 0 if survey.device == 'PC' else (1 if survey.device == 'Mobile' else 2) / 2
    
    x = np.array([
        survey.age / 100,  # Normalized age
        survey.daily_online_hours / 24,  # Normalized hours
        device_score,  # Device type
        interests_len,  # Interests length
        social_media_len,  # Social media length
        ad_count,  # Selected ads count
        survey.streaming_apps_count / 20,  # Normalized streaming apps
        survey.video_clip_length / 300  # Normalized video length
    ]).reshape(1, -1)

    # 2. Create dummy training data for decision boundary (just for visual)
    np.random.seed(42)
    X = np.random.rand(100, 8)  # Updated to 8 features
    y = (X[:, 0] + X[:, 1] + X[:, 4] + X[:, 5] > 2.0).astype(int)  # Updated decision boundary
    model.fit(X, y)

    # 3. Plot
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', alpha=0.5)
    plt.scatter(x[0][0], x[0][1], color='black', label='You', s=100)
    plt.xlabel('Age (normalized)')
    plt.ylabel('Hours Online (normalized)')
    plt.title('User Survey Results Visualization\n(8 Features: Age, Hours, Device, Interests, Social Media, Ads, Streaming, Video)')
    plt.legend()

    # 4. Save figure
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()

    return os.path.basename(plot_path)  # Return just the filename
