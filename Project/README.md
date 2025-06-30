# Ad Click Prediction System

A comprehensive web application that uses machine learning to predict user ad click probability based on survey responses. The system features a softmax logistic regression model with comprehensive metrics, social media integration, and advanced visualization capabilities.

## 🚀 Features

### Core Functionality
- **User Registration & Authentication**: Secure user management with email confirmation
- **Survey System**: Comprehensive user survey with 8 predictive features
- **AI Model**: Enhanced softmax logistic regression with mini-batch training
- **Social Media Integration**: Social media usage patterns as predictive features
- **Real-time Predictions**: Instant click probability calculations
- **Admin Dashboard**: Complete administrative interface with model monitoring

### AI/ML Features
- **8-Feature Model**: Age, online hours, device, interests, social media, ads, streaming, video
- **Comprehensive Metrics**: Precision, recall, F1-score, accuracy, confusion matrix, log loss
- **Information Gain Analysis**: Feature importance ranking with business insights
- **Model Visualization**: Training history, confusion matrix, feature importance plots
- **Model Persistence**: Automatic saving and loading of trained models

### Technical Features
- **Responsive Design**: Modern UI with Bootstrap and custom CSS
- **Email Integration**: Configurable email system for notifications
- **Data Export**: CSV export functionality for analysis
- **Security**: CSRF protection, secure password hashing, environment-based config
- **Database**: SQLite with migration support

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd 2425-11-b-pp-student-practices-assignment-ATSivkov21/Project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///site.db

# Email Configuration (Optional)
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=your-email@example.com

# Development Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Database Setup
```bash
# Run the cleanup script to set up the database
python cleanup_project.py

# Or manually create the database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 5. Create Admin User
```bash
python app/utils/create_admin.py
```

### 6. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📊 Model Features

The AI model uses 8 predictive features:

1. **Age** (normalized to 0-1)
2. **Daily Online Hours** (normalized to 0-1)
3. **Device Type** (PC=0, Mobile=0.5, Tablet=1)
4. **Interests Length** (normalized by 256 characters)
5. **Social Media Length** (normalized by 500 characters) ⭐ NEW
6. **Selected Ads Count** (normalized by 3 ads)
7. **Streaming Apps Count** (normalized by 20 apps)
8. **Video Clip Length** (normalized by 300 minutes)

## 🎯 Usage

### For Users
1. **Register**: Create an account with email confirmation
2. **Complete Survey**: Fill out the comprehensive survey including social media platforms
3. **View Results**: See your personalized click probability prediction
4. **Share Results**: Optionally share your results with other users

### For Administrators
1. **Dashboard**: Monitor all users, surveys, and ad clicks
2. **Model Training**: Train the AI model with current data
3. **Metrics Monitoring**: View comprehensive model performance metrics
4. **User Management**: Edit user accounts and manage roles
5. **Data Export**: Export user data and model results

## 🔧 Configuration

### Email Setup
To enable email functionality:
1. Set up your email credentials in the `.env` file
2. Ensure your email provider allows SMTP access
3. Test email functionality with the provided test script

### Model Configuration
- **Training Parameters**: Adjustable in `app/utils/ai_model.py`
- **Feature Engineering**: Customizable in the `prepare_training_data()` function
- **Metrics Calculation**: Configurable thresholds in the model metrics

## 🧪 Testing

### Run All Tests
```bash
# Test the enhanced model
python test_enhanced_model.py

# Test social media feature integration
python test_social_media_feature.py

# Test email functionality
python test_email.py
```

### Manual Testing
1. **User Flow**: Register → Survey → Results → Ad Click
2. **Admin Flow**: Login → Dashboard → Model Training → Metrics
3. **Email Flow**: Registration → Email Confirmation → Login

## 📁 Project Structure

```
Project/
├── app/
│   ├── admin/          # Admin routes and templates
│   ├── auth/           # Authentication routes and templates
│   ├── main/           # Main application routes and templates
│   ├── utils/          # Utility functions (AI model, plotting, email)
│   ├── models.py       # Database models
│   ├── forms.py        # Form definitions
│   └── __init__.py     # Application factory
├── static/             # Static files (CSS, JS, images)
├── templates/          # Base templates
├── migrations/         # Database migrations
├── instance/           # Database and model files
├── tests/              # Test files
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
└── run.py             # Application entry point
```

## 🔍 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Clear cache
python cleanup_project.py
```

#### Database Issues
```bash
# Reset database
rm instance/site.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

#### Email Issues
- Check SMTP settings in `.env` file
- Verify email provider allows SMTP access
- Test with `python test_email.py`

#### Model Training Issues
- Ensure at least 10 survey responses exist
- Check feature data quality
- Verify all required fields are present

### Performance Optimization
- **Database**: Use PostgreSQL for production
- **Caching**: Implement Redis for session storage
- **Model**: Use joblib for faster model loading
- **Static Files**: Configure CDN for production

## 📈 Model Performance

### Expected Metrics
- **Accuracy**: 65-85%
- **Precision**: 60-80%
- **Recall**: 55-75%
- **F1-Score**: 60-80%
- **Log Loss**: 0.25-0.45

### Feature Importance (Information Gain)
1. Age (0.15-0.25)
2. Daily Online Hours (0.12-0.20)
3. Device Type (0.08-0.15)
4. Interests Length (0.05-0.12)
5. **Social Media Length (0.04-0.10)** ⭐ NEW
6. Selected Ads Count (0.03-0.10)
7. Streaming Apps Count (0.02-0.08)
8. Video Clip Length (0.01-0.05)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review the documentation files
- Create an issue in the repository

## 🔄 Changelog

### Version 2.0 (Current)
- ✅ Added social media feature integration
- ✅ Enhanced AI model with 8 features
- ✅ Comprehensive metrics and visualization
- ✅ Improved security and configuration
- ✅ Better error handling and validation

### Version 1.0
- ✅ Basic user authentication
- ✅ Survey system
- ✅ Simple logistic regression
- ✅ Admin dashboard

---

**Note**: This is a comprehensive project with advanced AI/ML capabilities. For production deployment, ensure proper security measures, environment configuration, and performance optimization. 