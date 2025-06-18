# 📧 Импорт на Message за изпращане на имейл съобщения
from flask_mail import Message
# 🔐 Импорт на библиотека за създаване и валидиране на токени с изтичане (напр. за имейл потвърждение)
from itsdangerous import URLSafeTimedSerializer
# 🔧 Импорти от Flask за конфигурация и създаване на пълен URL
from flask import current_app, url_for
# 📬 Импортиране на mail обекта, дефиниран във Flask приложението
from app import mail

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

    # 🎯 Избор на подател и HTML съдържание според имейл домейна
    if user.email.lower().endswith('@gmail.com'):
        sender = 'alexsanderdaskalo@gmail.com'  # Gmail подател
        html = f'''
            <p>Hello, {user.username}!</p>
            <p>Please confirm your Gmail account by clicking the link below:</p>
            <a href="{confirm_url}">{confirm_url}</a>
        '''
    elif user.email.lower().endswith('@outlook.com') or user.email.lower().endswith('@hotmail.com') or user.email.lower().endswith('@codingburgas.bg'):
        sender = 'ATSivkov21@codingburgas.bg'  # Outlook подател
        html = f'''
            <p>Hello, {user.username}!</p>
            <p>Please confirm your Outlook account by clicking the link below:</p>
            <a href="{confirm_url}">{confirm_url}</a>
        '''
    else:
        # 📬 Стандартен подател от конфигурацията на приложението
        sender = current_app.config['MAIL_USERNAME']
        html = f'''
            <p>Hello, {user.username}!</p>
            <p>Please confirm your email by clicking the link below:</p>
            <a href="{confirm_url}">{confirm_url}</a>
        '''

    # 📧 Създаване на имейл съобщението
    msg = Message('Confirm Your Email', recipients=[user.email], html=html, sender=sender)

    # 🚀 Изпращане на имейла чрез mail обекта
    mail.send(msg)
