#!/usr/bin/env python3
"""
📧 Email Testing Script for Ad Predictor
This script tests the email functionality of the Ad Predictor application.
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_smtp_connection(server, port, username, password):
    """Test SMTP connection with provided credentials"""
    try:
        print(f"🔗 Testing SMTP connection to {server}:{port}...")
        
        # Create SMTP connection
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        
        # Login
        smtp.login(username, password)
        
        print("✅ SMTP connection successful!")
        smtp.quit()
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication failed. Check username and password.")
        return False
    except smtplib.SMTPConnectError:
        print("❌ SMTP Connection failed. Check server and port.")
        return False
    except Exception as e:
        print(f"❌ SMTP test failed: {e}")
        return False

def send_test_email(server, port, username, password, recipient_email):
    """Send a test email"""
    try:
        print(f"📧 Sending test email to {recipient_email}...")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Ad Predictor - Email Test ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})'
        msg['From'] = username
        msg['To'] = recipient_email
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Ad Predictor Email Test</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2563eb, #06b6d4); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 10px 10px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .success {{ background: #d1fae5; border: 1px solid #10b981; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧠 Ad Predictor</h1>
                    <h2>Email Configuration Test</h2>
                </div>
                <div class="content">
                    <div class="success">
                        <h3>✅ Email System Working!</h3>
                        <p>This is a test email to verify that the email configuration is working correctly.</p>
                    </div>
                    
                    <h3>Test Details:</h3>
                    <ul>
                        <li><strong>Server:</strong> {server}:{port}</li>
                        <li><strong>Sender:</strong> {username}</li>
                        <li><strong>Recipient:</strong> {recipient_email}</li>
                        <li><strong>Timestamp:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</li>
                    </ul>
                    
                    <p>If you receive this email, the email system is properly configured and ready to use.</p>
                    
                    <h3>What this means:</h3>
                    <ul>
                        <li>✅ SMTP server connection is working</li>
                        <li>✅ Authentication is successful</li>
                        <li>✅ Email sending functionality is operational</li>
                        <li>✅ HTML email templates will work correctly</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>&copy; 2025 Ad Predictor. All rights reserved.</p>
                    <p>This is an automated test email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Create SMTP connection and send
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.login(username, password)
        
        # Send email
        smtp.send_message(msg)
        smtp.quit()
        
        print("✅ Test email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

def test_gmail_configuration():
    """Test Gmail SMTP configuration"""
    print("\n📧 Testing Gmail SMTP Configuration")
    print("=" * 50)
    
    # Gmail SMTP settings
    server = "smtp.gmail.com"
    port = 587
    
    # Get credentials from environment or user input
    username = os.getenv('GMAIL_USERNAME')
    password = os.getenv('GMAIL_APP_PASSWORD')  # Use App Password, not regular password
    
    if not username or not password:
        print("⚠️  Gmail credentials not found in environment variables.")
        print("Please set GMAIL_USERNAME and GMAIL_APP_PASSWORD environment variables.")
        print("\nTo set up Gmail App Password:")
        print("1. Go to Google Account settings")
        print("2. Enable 2-factor authentication")
        print("3. Generate an App Password for 'Mail'")
        print("4. Use the App Password instead of your regular password")
        return False
    
    # Test connection
    if test_smtp_connection(server, port, username, password):
        # Send test email
        recipient = input("Enter recipient email address for test: ").strip()
        if recipient:
            return send_test_email(server, port, username, password, recipient)
    
    return False

def test_outlook_configuration():
    """Test Outlook/Hotmail SMTP configuration"""
    print("\n📧 Testing Outlook SMTP Configuration")
    print("=" * 50)
    
    # Outlook SMTP settings
    server = "smtp-mail.outlook.com"
    port = 587
    
    # Get credentials from environment or user input
    username = os.getenv('OUTLOOK_USERNAME')
    password = os.getenv('OUTLOOK_PASSWORD')
    
    if not username or not password:
        print("⚠️  Outlook credentials not found in environment variables.")
        print("Please set OUTLOOK_USERNAME and OUTLOOK_PASSWORD environment variables.")
        return False
    
    # Test connection
    if test_smtp_connection(server, port, username, password):
        # Send test email
        recipient = input("Enter recipient email address for test: ").strip()
        if recipient:
            return send_test_email(server, port, username, password, recipient)
    
    return False

def test_custom_smtp():
    """Test custom SMTP configuration"""
    print("\n📧 Testing Custom SMTP Configuration")
    print("=" * 50)
    
    # Get SMTP details from user
    server = input("Enter SMTP server (e.g., smtp.example.com): ").strip()
    port = int(input("Enter SMTP port (e.g., 587): ").strip())
    username = input("Enter SMTP username: ").strip()
    password = input("Enter SMTP password: ").strip()
    
    if not all([server, port, username, password]):
        print("❌ All fields are required.")
        return False
    
    # Test connection
    if test_smtp_connection(server, port, username, password):
        # Send test email
        recipient = input("Enter recipient email address for test: ").strip()
        if recipient:
            return send_test_email(server, port, username, password, recipient)
    
    return False

def generate_config_file(server, port, username, password):
    """Generate Flask configuration for email"""
    config = {
        'MAIL_SERVER': server,
        'MAIL_PORT': port,
        'MAIL_USE_TLS': True,
        'MAIL_USE_SSL': False,
        'MAIL_USERNAME': username,
        'MAIL_PASSWORD': password,
        'MAIL_DEFAULT_SENDER': username,
        'EMAIL_CONFIRMATION_ENABLED': True
    }
    
    config_file = 'email_config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Email configuration saved to {config_file}")
    print("You can use this configuration in your Flask app.")
    
    return config

def main():
    """Main function to run email tests"""
    print("🧠 Ad Predictor - Email Testing Tool")
    print("=" * 50)
    print("This tool helps you test and configure email functionality.")
    print()
    
    while True:
        print("\nChoose an option:")
        print("1. Test Gmail SMTP")
        print("2. Test Outlook SMTP")
        print("3. Test Custom SMTP")
        print("4. Generate Configuration File")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            test_gmail_configuration()
        elif choice == '2':
            test_outlook_configuration()
        elif choice == '3':
            test_custom_smtp()
        elif choice == '4':
            print("\n📝 Generate Configuration File")
            print("Enter your SMTP details:")
            server = input("SMTP Server: ").strip()
            port = int(input("SMTP Port: ").strip())
            username = input("SMTP Username: ").strip()
            password = input("SMTP Password: ").strip()
            
            if all([server, port, username, password]):
                generate_config_file(server, port, username, password)
            else:
                print("❌ All fields are required.")
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 