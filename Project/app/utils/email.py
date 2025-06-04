from flask_mail import Message
from flask import url_for, current_app
from app import mail
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def generate_confirmation_token(email):
    return serializer.dumps(email, salt='email-confirmation')

def confirm_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=expiration)
    except:
        return False
    return email

def send_confirmation_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = f'<p>Welcome! Please confirm your email: <a href="{confirm_url}">Confirm Email</a></p>'
    msg = Message("Confirm Your Email", recipients=[user.email], html=html)
    mail.send(msg)