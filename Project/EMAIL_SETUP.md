# Email Configuration Guide

## Overview
This application uses Flask-Mail for sending email confirmations. By default, email confirmation is disabled in development mode to avoid authentication issues.

## Development Mode (Default)
In development mode, email confirmation is automatically disabled. Users can register and login without email confirmation.

## Production Email Setup

### Option 1: Gmail SMTP
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Set environment variables:
   ```bash
   export MAIL_SERVER=smtp.gmail.com
   export MAIL_PORT=587
   export MAIL_USE_TLS=true
   export MAIL_USERNAME=your-email@gmail.com
   export MAIL_PASSWORD=your-app-password
   export MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

### Option 2: Other SMTP Providers
Set the appropriate SMTP settings for your email provider:
```bash
export MAIL_SERVER=your-smtp-server.com
export MAIL_PORT=587
export MAIL_USE_TLS=true
export MAIL_USERNAME=your-email@domain.com
export MAIL_PASSWORD=your-password
export MAIL_DEFAULT_SENDER=your-email@domain.com
```

### Option 3: Environment File (.env)
Create a `.env` file in the project root:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

## Testing Email Configuration
1. Set up your email credentials
2. Restart the Flask application
3. Try registering a new user
4. Check if confirmation email is sent

## Troubleshooting
- **Authentication Error**: Check your email credentials and app passwords
- **Connection Error**: Verify SMTP server and port settings
- **Sender Refused**: Ensure the sender email matches your authenticated account

## Security Notes
- Never commit email passwords to version control
- Use environment variables for sensitive data
- Consider using email service providers like SendGrid for production 