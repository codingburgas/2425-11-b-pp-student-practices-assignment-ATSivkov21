from datetime import datetime 
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Функция за зареждане на потребител по ID за flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Връща потребител с дадения ID от базата

# Модел за роля на потребител (например админ, потребител и т.н.)
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникален идентификатор на ролята
    name = db.Column(db.String(64), unique=True)  # Име на ролята, уникално
    users = db.relationship('User', backref='role', lazy=True)  # Всички потребители с тази роля

# Модел за потребител в системата
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникален ID на потребителя
    username = db.Column(db.String(64), unique=True, nullable=False)  # Потребителско име, задължително и уникално
    email = db.Column(db.String(120), unique=True, nullable=False)  # Имейл, задължителен и уникален
    password_hash = db.Column(db.String(128))  # Хеширана парола
    email_confirmed = db.Column(db.Boolean, default=False)  # Дали имейлът е потвърден (по подразбиране False)
    share_results = db.Column(db.Boolean, default=False)  # Дали потребителят дава съгласие за споделяне на резултати
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # Външен ключ към ролята на потребителя
    survey_responses = db.relationship('SurveyResponse', backref='user', lazy=True)  # Всички отговори на анкети, свързани с този потребител
    ad_clicks = db.relationship('AdClick', backref='user', lazy=True)  # Всички кликвания на реклами от този потребител

    # Метод за задаване на парола (хеширане)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Метод за проверка на парола срещу съхранения хеш
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Модел за отговор от анкета на потребител
class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникален ID на отговора
    age = db.Column(db.Integer)  # Възраст на потребителя
    daily_online_hours = db.Column(db.Float)  # Часове онлайн на ден
    device = db.Column(db.String(64))  # Използвано устройство (PC, Mobile и т.н.)
    interests = db.Column(db.String(256))  # Интереси (текст)
    selected_ads = db.Column(db.String(200), nullable=True)  # Избрани реклами (по избор)
    social_media_names = db.Column(db.String(256), nullable=True)  # Имена на социални мрежи (CSV)
    social_media_lengths = db.Column(db.String(256), nullable=True)  # Продължителност на използване на всяка мрежа (CSV)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Време на попълване, по подразбиране текущо време
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Външен ключ към потребителя, който е попълнил анкетата

# Модел за запис на кликвания върху реклами
class AdClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникален ID на кликването
    ad_name = db.Column(db.String(100), nullable=False)  # Име на рекламата, задължително поле
    clicked_at = db.Column(db.DateTime, server_default=db.func.now())  # Време на кликването, задава се автоматично
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Външен ключ към потребителя, който е кликнал
