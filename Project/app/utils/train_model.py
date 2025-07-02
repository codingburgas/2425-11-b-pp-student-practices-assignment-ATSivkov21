import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# 📂 За работа с пътища и файловата система
import os
# 🔢 За работа с числови масиви и обучение на модела
import numpy as np
# ⚙️ Създаване на Flask приложението и достъп до базата
from app import create_app, db
# 📋 Моделът за съхранени отговори от анкетата
from app.models import SurveyResponse
# 🧠 Импорт на логистичния модел и пътя, където се записва
from app.utils.ai_model import model, MODEL_PATH
from sklearn.feature_selection import mutual_info_classif


def get_training_data():
    # Взимане на всички попълнени анкети от базата
    surveys = SurveyResponse.query.all()

    X = []  # Характеристики (inputs)
    y = []  # Целева стойност (кликнато или не)

    for s in surveys:
        # 📏 Нормализация на текстови и числови стойности
        interests_len = len(s.interests or "") / 256
        ad_count = len((s.selected_ads or "").split(',')) / 3
        device_score = 0 if s.device == 'PC' else (1 if s.device == 'Mobile' else 2) / 2
        # Нови социални медии
        social_names = (s.social_media_names or "").split(',')
        social_lengths = [float(x) for x in (s.social_media_lengths or "").split(',') if x.strip().replace('.', '', 1).isdigit()]
        num_social = len([n for n in social_names if n.strip()]) / 10  # max 10
        total_social_time = sum(social_lengths) / 24  # max 24h
        X.append([
            s.age / 100,
            s.daily_online_hours / 24,
            device_score,
            interests_len,
            ad_count,
            num_social,
            total_social_time
        ])
        y.append(1 if ad_count > 0 else 0)

    return np.array(X), np.array(y)


def main():
    # Създаване на Flask приложението
    app = create_app()

    # Влизане в контекста на приложението за достъп до базата
    with app.app_context():
        # Извличане на данни от базата
        X, y = get_training_data()

        # Проверка дали има достатъчно данни за обучение
        if len(X) == 0:
            print("No survey data found. Please collect data first.")
            return

        using_fake = False
        # Проверка дали има поне два класа в целевия вектор
        if len(set(y)) < 2:
            print("Warning: Not enough class diversity in real data. Using a small fake dataset for training.")
            # Generate a small fake dataset with both classes
            X = np.array([
                [0.18, 0.2, 0.5, 0.3, 0.33, 0.3, 0.2],  # class 0
                [0.25, 0.4, 0.0, 0.5, 0.66, 0.6, 0.4],  # class 1
                [0.30, 0.1, 1.0, 0.1, 0.0, 0.1, 0.1],   # class 0
                [0.40, 0.8, 0.5, 0.8, 1.0, 0.8, 0.7]    # class 1
            ])
            y = np.array([0, 1, 0, 1])
            using_fake = True

        # Разделяне на данните за обучение и тестване (80/20), освен ако е фалшив сет
        if using_fake:
            X_train, X_test = X, X
            y_train, y_test = y, y
            print("Warning: Using all fake data for both training and evaluation. Metrics are not meaningful.")
        else:
            split_idx = int(0.8 * len(X))
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]

        # Обучение на модела с реалните потребителски данни
        model.fit(X_train, y_train)

        # Оценяване на модела
        metrics = model.evaluate(X_test, y_test)
        
        # Запазване на модела във файл (model.pkl)
        model.save()
        
        print(f"Model trained and saved to {MODEL_PATH}")
        print("\nModel Performance Metrics:")
        for k, v in metrics.items():
            print(f"{k}: {v}")
        
        # Запазване на метриките в отделен файл
        import json
        metrics_file = 'instance/model_metrics.json'
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics saved to {metrics_file}")

        # Information gain (mutual information)
        feature_names = [
            'age', 'daily_online_hours', 'device', 'interests_len', 'ad_count', 'num_social', 'total_social_time'
        ]
        info_gain = mutual_info_classif(X_train, y_train, discrete_features=False)
        metrics['information_gain'] = dict(zip(feature_names, info_gain.tolist()))


if __name__ == "__main__":
    main() 