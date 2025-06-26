import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Configuration
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'ATSivkov21@codingburgas.bg'
    MAIL_PASSWORD = 'Gun71648'
    MAIL_DEFAULT_SENDER = 'ATSivkov21@codingburgas.bg'
    
    # Disable email confirmation if no email credentials are provided
    EMAIL_CONFIRMATION_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    # For development, you can disable email confirmation entirely
    EMAIL_CONFIRMATION_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False