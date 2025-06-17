from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
from app import mail

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
    except Exception:
        return None
    return email

def send_confirmation_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    if user.email.lower().endswith('@gmail.com'):
        sender = 'alexsanderdaskalo@gmail.com'  # Set this to your Gmail sender
        html = f'''
            <p>Hello, {user.username}!</p>
            <p>Please confirm your Gmail account by clicking the link below:</p>
            <a href="{confirm_url}">{confirm_url}</a>
        '''
    elif user.email.lower().endswith('@outlook.com') or user.email.lower().endswith('@hotmail.com') or user.email.lower().endswith('@codingburgas.bg'):
        sender = 'ATSivkov21@codingburgas.bg'  # Set this to your Outlook sender
        html = f'''
            <p>Hello, {user.username}!</p>
            <p>Please confirm your Outlook account by clicking the link below:</p>
            <a href="{confirm_url}">{confirm_url}</a>
        '''
    else:
        sender = current_app.config['MAIL_USERNAME']
        html = f'''
            <p>Hello, {user.username}!</p>
            <p>Please confirm your email by clicking the link below:</p>
            <a href="{confirm_url}">{confirm_url}</a>
        '''
    msg = Message('Confirm Your Email', recipients=[user.email], html=html, sender=sender)
    mail.send(msg)
