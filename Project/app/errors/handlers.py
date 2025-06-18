# Импорт на Blueprint за грешки и рендиране на шаблони
from flask import Blueprint, render_template

# Blueprint за грешки
errors = Blueprint('errors', __name__)

# 🔴 Обработчик за грешка 404 (страница не е намерена)
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# ⚫ Обработчик за грешка 500 (вътрешна грешка на сървъра)
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
