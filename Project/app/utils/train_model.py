# 📂 За работа с пътища и файловата система
import os
# 🔢 За работа с числови масиви и обучение на модела
import numpy as np
# ⚙️ Създаване на Flask приложението и достъп до базата
from app import create_app, db
# 📋 Моделът за съхранени отговори от анкетата
from app.models import SurveyResponse
# 🧠 Импорт на логистичния модел и пътя, където се записва
from ai_model import model, MODEL_PATH


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

        # Добавяне на входен вектор
        X.append([
            s.age / 100,
            s.daily_online_hours / 24,
            device_score,
            interests_len,
            ad_count
        ])

        # 👉 Целева стойност: 1 ако има избрани реклами, 0 иначе
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

        # Обучение на модела с реалните потребителски данни
        model.fit(X, y)

        # Запазване на модела във файл (model.pkl)
        model.save()

        print(f"Model trained and saved to {MODEL_PATH}")


if __name__ == "__main__":
    main() 