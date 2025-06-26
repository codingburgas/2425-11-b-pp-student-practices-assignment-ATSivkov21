# 📧 Импорт на Message за изпращане на имейл съобщения
from flask_mail import Message
# 🔐 Импорт на библиотека за създаване и валидиране на токени с изтичане (напр. за имейл потвърждение)
from itsdangerous import URLSafeTimedSerializer
# 🔧 Импорти от Flask за конфигурация и създаване на пълен URL
from flask import current_app, url_for, flash
# 📬 Импортиране на mail обекта, дефиниран във Flask приложението
from app import mail
# ⚠️ За обработка на грешки при изпращане на имейли
import smtplib
from smtplib import SMTPAuthenticationError, SMTPSenderRefused

# 🔐 Създаване на токен за потвърждаване на имейл
def generate_confirmation_token(email):
    # Използваме секретен ключ на приложението за защита на токена
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    # Връщаме криптиран токен, специфичен за имейл потвърждение
    return serializer.dumps(email, salt='email-confirm')

# 🔓 Потвърждение на токен и извличане на имейл от него
def confirm_token(token, expiration=3600):
    # Валидиране със същия ключ
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        # Дешифриране на имейла, ако токенът е валиден и не е изтекъл
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
    except Exception:
        return None  # Ако токенът е невалиден или изтекъл
    return email

# 📬 Изпращане на имейл за потвърждение до даден потребител
def send_confirmation_email(user):
    # Генерираме токен за имейл адреса на потребителя
    token = generate_confirmation_token(user.email)

    # Създаваме пълен URL към рутата за потвърждение с токена
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    # 📧 Създаване на имейл съобщението с универсален подател
    html = f'''
        <p>Hello, {user.username}!</p>
        <p>Please confirm your email by clicking the link below:</p>
        <a href="{confirm_url}">{confirm_url}</a>
        <p>If the link doesn't work, copy and paste it into your browser.</p>
        <p>This link will expire in 1 hour.</p>
    '''

    # Използваме конфигурирания подател от настройките
    sender = current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')
    
    msg = Message('Confirm Your Email', recipients=[user.email], html=html, sender=sender)

    try:
        # 🚀 Изпращане на имейла чрез mail обекта
        mail.send(msg)
        return True
    except (SMTPAuthenticationError, SMTPSenderRefused) as e:
        # Ако има проблем с автентикацията, връщаме False
        print(f"Email authentication failed: {e}")
        return False
    except Exception as e:
        # За други грешки при изпращане
        print(f"Email sending failed: {e}")
        return False

# 📧 Функция за проверка дали имейл конфигурацията е валидна
def is_email_configured():
    """Проверява дали имейл конфигурацията е правилно настроена"""
    try:
        # Проверяваме дали имейл потвърждението е активирано
        if not current_app.config.get('EMAIL_CONFIRMATION_ENABLED', False):
            return False
            
        # Проверяваме дали имаме необходимите настройки
        required_settings = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD']
        for setting in required_settings:
            if not current_app.config.get(setting):
                return False
        return True
    except Exception:
        return False
