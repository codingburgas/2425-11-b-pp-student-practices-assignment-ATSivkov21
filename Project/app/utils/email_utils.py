# 📧 Enhanced Email Utilities for Ad Predictor
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for, flash, render_template_string
from app import mail
import smtplib
from smtplib import SMTPAuthenticationError, SMTPSenderRefused
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email templates
WELCOME_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Ad Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #2563eb, #06b6d4); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }
        .btn { display: inline-block; padding: 12px 24px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
        .logo { font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🧠 Ad Predictor</div>
            <h1>Welcome to Ad Predictor!</h1>
        </div>
        <div class="content">
            <h2>Hello {{ username }}!</h2>
            <p>Thank you for joining Ad Predictor - the AI-powered platform for predicting ad engagement and optimizing marketing campaigns.</p>
            
            <h3>What you can do with Ad Predictor:</h3>
            <ul>
                <li>📊 Take surveys to predict ad engagement</li>
                <li>🤖 Get AI-powered predictions and insights</li>
                <li>📈 View detailed metrics and analytics</li>
                <li>📋 Generate comprehensive reports</li>
                <li>🔍 Monitor model performance</li>
            </ul>
            
            <p><strong>Ready to get started?</strong></p>
            <a href="{{ login_url }}" class="btn">Login to Your Account</a>
            
            <p>If you have any questions, feel free to contact our support team.</p>
        </div>
        <div class="footer">
            <p>&copy; 2025 Ad Predictor. All rights reserved.</p>
            <p>This email was sent to {{ email }}. If you didn't sign up for Ad Predictor, please ignore this email.</p>
        </div>
    </div>
</body>
</html>
"""

CONFIRMATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirm Your Email - Ad Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #2563eb, #06b6d4); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }
        .btn { display: inline-block; padding: 12px 24px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
        .warning { background: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Confirm Your Email Address</h1>
        </div>
        <div class="content">
            <h2>Hello {{ username }}!</h2>
            <p>Please confirm your email address by clicking the button below:</p>
            
            <a href="{{ confirm_url }}" class="btn">Confirm Email Address</a>
            
            <div class="warning">
                <strong>Important:</strong> This link will expire in 1 hour for security reasons.
            </div>
            
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #2563eb;">{{ confirm_url }}</p>
            
            <p>If you didn't create an account with Ad Predictor, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>&copy; 2025 Ad Predictor. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

PASSWORD_RESET_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Your Password - Ad Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #dc2626, #ef4444); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }
        .btn { display: inline-block; padding: 12px 24px; background: #dc2626; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
        .warning { background: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Reset Your Password</h1>
        </div>
        <div class="content">
            <h2>Hello {{ username }}!</h2>
            <p>You requested to reset your password. Click the button below to create a new password:</p>
            
            <a href="{{ reset_url }}" class="btn">Reset Password</a>
            
            <div class="warning">
                <strong>Security Notice:</strong> This link will expire in 1 hour. If you didn't request a password reset, please ignore this email.
            </div>
            
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #dc2626;">{{ reset_url }}</p>
        </div>
        <div class="footer">
            <p>&copy; 2025 Ad Predictor. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

NOTIFICATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }} - Ad Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #2563eb, #06b6d4); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
        .highlight { background: #dbeafe; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ subject }}</h1>
        </div>
        <div class="content">
            <h2>Hello {{ username }}!</h2>
            {{ content | safe }}
        </div>
        <div class="footer">
            <p>&copy; 2025 Ad Predictor. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

# 🔐 Generate confirmation token
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

# 🔐 Generate password reset token
def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset')

# 🔓 Confirm token and extract email
def confirm_token(token, expiration=3600, salt='email-confirm'):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=salt, max_age=expiration)
    except Exception as e:
        logger.error(f"Token confirmation failed: {e}")
        return None
    return email

# 📧 Send welcome email
def send_welcome_email(user):
    """Send welcome email to new user"""
    try:
        login_url = url_for('auth.login', _external=True)
        
        html = render_template_string(WELCOME_EMAIL_TEMPLATE, 
                                    username=user.username,
                                    email=user.email,
                                    login_url=login_url)
        
        msg = Message(
            subject='Welcome to Ad Predictor! 🧠',
            recipients=[user.email],
            html=html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@adpredictor.com')
        )
        
        mail.send(msg)
        logger.info(f"Welcome email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {e}")
        return False

# 📧 Send confirmation email
def send_confirmation_email(user):
    """Send email confirmation to user"""
    try:
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        
        html = render_template_string(CONFIRMATION_EMAIL_TEMPLATE,
                                    username=user.username,
                                    confirm_url=confirm_url)
        
        msg = Message(
            subject='Confirm Your Email - Ad Predictor',
            recipients=[user.email],
            html=html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@adpredictor.com')
        )
        
        mail.send(msg)
        logger.info(f"Confirmation email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {user.email}: {e}")
        return False

# 📧 Send password reset email
def send_password_reset_email(user):
    """Send password reset email to user"""
    try:
        token = generate_password_reset_token(user.email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        
        html = render_template_string(PASSWORD_RESET_TEMPLATE,
                                    username=user.username,
                                    reset_url=reset_url)
        
        msg = Message(
            subject='Reset Your Password - Ad Predictor',
            recipients=[user.email],
            html=html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@adpredictor.com')
        )
        
        mail.send(msg)
        logger.info(f"Password reset email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {user.email}: {e}")
        return False

# 📧 Send notification email
def send_notification_email(user, subject, content):
    """Send general notification email to user"""
    try:
        html = render_template_string(NOTIFICATION_EMAIL_TEMPLATE,
                                    username=user.username,
                                    subject=subject,
                                    content=content)
        
        msg = Message(
            subject=f"{subject} - Ad Predictor",
            recipients=[user.email],
            html=html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@adpredictor.com')
        )
        
        mail.send(msg)
        logger.info(f"Notification email sent to {user.email}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send notification email to {user.email}: {e}")
        return False

# 📧 Send survey completion email
def send_survey_completion_email(user, survey_results):
    """Send email notification when user completes survey"""
    try:
        subject = "Survey Completed - Your Ad Prediction Results"
        
        content = f"""
        <p>Thank you for completing the ad engagement survey!</p>
        
        <div class="highlight">
            <h3>Your Prediction Results:</h3>
            <p><strong>Engagement Score:</strong> {survey_results.get('engagement_score', 'N/A')}</p>
            <p><strong>Confidence Level:</strong> {survey_results.get('confidence', 'N/A')}</p>
            <p><strong>Recommended Actions:</strong> {survey_results.get('recommendations', 'N/A')}</p>
        </div>
        
        <p>You can view detailed analytics and generate reports from your dashboard.</p>
        <p>Thank you for using Ad Predictor!</p>
        """
        
        return send_notification_email(user, subject, content)
        
    except Exception as e:
        logger.error(f"Failed to send survey completion email to {user.email}: {e}")
        return False

# 📧 Send model update notification
def send_model_update_notification(user, model_info):
    """Send notification about model updates"""
    try:
        subject = "Model Update Notification"
        
        content = f"""
        <p>The AI model has been updated with new data and improved algorithms.</p>
        
        <div class="highlight">
            <h3>Update Details:</h3>
            <p><strong>Model Version:</strong> {model_info.get('version', 'N/A')}</p>
            <p><strong>Accuracy Improvement:</strong> {model_info.get('accuracy_improvement', 'N/A')}</p>
            <p><strong>New Features:</strong> {model_info.get('new_features', 'N/A')}</p>
        </div>
        
        <p>Your predictions will now be more accurate and reliable.</p>
        """
        
        return send_notification_email(user, subject, content)
        
    except Exception as e:
        logger.error(f"Failed to send model update notification to {user.email}: {e}")
        return False

# 📧 Send weekly report email
def send_weekly_report_email(user, report_data):
    """Send weekly activity report to user"""
    try:
        subject = "Your Weekly Ad Predictor Report"
        
        content = f"""
        <p>Here's your weekly activity summary:</p>
        
        <div class="highlight">
            <h3>Weekly Statistics:</h3>
            <p><strong>Surveys Completed:</strong> {report_data.get('surveys_completed', 0)}</p>
            <p><strong>Average Engagement Score:</strong> {report_data.get('avg_engagement', 'N/A')}</p>
            <p><strong>Reports Generated:</strong> {report_data.get('reports_generated', 0)}</p>
            <p><strong>Model Accuracy:</strong> {report_data.get('model_accuracy', 'N/A')}</p>
        </div>
        
        <p>Keep up the great work! Your data helps improve our AI model.</p>
        """
        
        return send_notification_email(user, subject, content)
        
    except Exception as e:
        logger.error(f"Failed to send weekly report email to {user.email}: {e}")
        return False

# 📧 Send admin notification
def send_admin_notification(subject, content, admin_emails=None):
    """Send notification to admin users"""
    try:
        if admin_emails is None:
            # Get admin emails from database or config
            admin_emails = current_app.config.get('ADMIN_EMAILS', [])
        
        if not admin_emails:
            logger.warning("No admin emails configured for notification")
            return False
        
        html = render_template_string(NOTIFICATION_EMAIL_TEMPLATE,
                                    username="Admin",
                                    subject=subject,
                                    content=content)
        
        msg = Message(
            subject=f"Admin Notification: {subject}",
            recipients=admin_emails,
            html=html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@adpredictor.com')
        )
        
        mail.send(msg)
        logger.info(f"Admin notification sent: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send admin notification: {e}")
        return False

# 📧 Test email functionality
def test_email_configuration():
    """Test email configuration and send test email"""
    try:
        test_email = current_app.config.get('TEST_EMAIL', 'test@example.com')
        
        content = """
        <p>This is a test email to verify that the email configuration is working correctly.</p>
        <p>If you receive this email, the email system is properly configured.</p>
        <p>Timestamp: {}</p>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        html = render_template_string(NOTIFICATION_EMAIL_TEMPLATE,
                                    username="Test User",
                                    subject="Email Configuration Test",
                                    content=content)
        
        msg = Message(
            subject='Email Configuration Test - Ad Predictor',
            recipients=[test_email],
            html=html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@adpredictor.com')
        )
        
        mail.send(msg)
        logger.info("Test email sent successfully")
        return True
        
    except Exception as e:
        logger.error(f"Email configuration test failed: {e}")
        return False

# 📧 Check email configuration
def is_email_configured():
    """Check if email configuration is properly set up"""
    try:
        if not current_app.config.get('EMAIL_CONFIRMATION_ENABLED', False):
            return False
            
        required_settings = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD']
        for setting in required_settings:
            if not current_app.config.get(setting):
                logger.warning(f"Missing email configuration: {setting}")
                return False
        return True
    except Exception as e:
        logger.error(f"Email configuration check failed: {e}")
        return False

# 📧 Get email statistics
def get_email_statistics():
    """Get email sending statistics"""
    try:
        # This would typically connect to a database or log file
        # For now, return mock data
        return {
            'total_sent': 0,
            'successful': 0,
            'failed': 0,
            'last_sent': None,
            'email_types': {
                'welcome': 0,
                'confirmation': 0,
                'password_reset': 0,
                'notifications': 0
            }
        }
    except Exception as e:
        logger.error(f"Failed to get email statistics: {e}")
        return None 