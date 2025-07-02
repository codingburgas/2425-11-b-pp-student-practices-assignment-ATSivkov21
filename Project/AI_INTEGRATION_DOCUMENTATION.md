# AI Module Integration Documentation

## Overview
This document explains the integration between the AI module and the web application for predicting ad click probabilities based on user survey responses.

## Architecture

### 1. AI Model (`app/utils/ai_model.py`)
The core AI module implements a custom logistic regression model with the following components:

#### Model Class: `SimpleLogisticRegression`
- **Purpose**: Binary classification for predicting ad click probability
- **Algorithm**: Gradient descent optimization with sigmoid activation
- **Features**: 5 normalized features from user survey data
- **Output**: Probability between 0 and 1

#### Key Methods:
- `fit(X, y)`: Trains the model using gradient descent
- `predict(X)`: Returns binary predictions (0 or 1)
- `predict_proba(X)`: Returns probability scores
- `evaluate(X_test, y_test)`: Calculates performance metrics
- `save()/load()`: Model persistence

### 2. Data Flow Integration

#### Survey Data Collection
```
User fills survey → SurveyResponse model → Database storage
```

#### Feature Engineering (`predict_click_probability()`)
The function transforms survey data into model features:

1. **Age**: Normalized to [0,1] range (age/100)
2. **Daily Online Hours**: Normalized to [0,1] range (hours/24)
3. **Device**: Categorical encoding (PC=0, Mobile=0.5, Tablet=1)
4. **Interests Length**: Normalized text length (chars/256)
5. **Selected Ads Count**: Normalized ad selection (count/3)

#### Prediction Pipeline
```
Survey Data → Feature Engineering → Model Input → Prediction → Result Display
```

### 3. Training Integration (`app/utils/train_model.py`)

#### Training Process:
1. **Data Extraction**: Retrieves all survey responses from database
2. **Data Preprocessing**: Applies same feature engineering as prediction
3. **Train/Test Split**: 80/20 split for evaluation
4. **Model Training**: Fits model with gradient descent
5. **Performance Evaluation**: Calculates accuracy, MSE, log loss
6. **Model Persistence**: Saves trained model and metrics

#### Training Command:
```bash
python -m app.utils.train_model
```

### 4. Model Monitoring

#### Metrics Tracked:
- **Accuracy**: Classification accuracy on test set
- **Precision**: Proportion of positive identifications that were actually correct
- **Recall**: Proportion of actual positives that were identified correctly
- **F1-Score**: Harmonic mean of precision and recall
- **Log Loss (Entropy)**: Cross-entropy loss for probabilistic predictions
- **Confusion Matrix**: Table showing correct and incorrect predictions for each class
- **Information Gain**: Feature importance measured by mutual information

#### Monitoring Dashboard:
- **Location**: `/admin/model_monitoring`
- **Features**: Real-time metrics display, confusion matrix, information gain, model health status
- **Recommendations**: Automated suggestions for model improvement

### 5. Model Algorithm

- **Algorithm**: Softmax (multinomial) logistic regression using scikit-learn
- **Features Used**:
    - Age (normalized)
    - Daily online hours (normalized)
    - Device (encoded)
    - Interests length (normalized)
    - Selected ads count (normalized)
    - Number of social media platforms used (normalized)
    - Total time spent on social media (normalized)
- **Feature Justification**: Information gain is calculated for each feature to justify its inclusion. Features with higher information gain contribute more to the model's predictive power.

### 6. Conclusions

- The model's performance is evaluated using accuracy, precision, recall, F1-score, log loss, and confusion matrix.
- Information gain analysis shows which features are most informative for predicting ad clicks.
- Social media usage (number and time) provides additional predictive value, as shown by its information gain.
- The model is monitored via the admin dashboard, allowing for ongoing evaluation and retraining as new data is collected.

### 7. Web Application Integration

#### Routes Integration:
- **Survey Route** (`/survey`): Collects data for training
- **Result Route** (`/result/<id>`): Displays AI predictions
- **Profile Route** (`/profile`): Shows user's prediction history
- **Shared Results** (`/shared_results`): Shows other users' results with consent

#### Database Integration:
```python
# Survey data collection
survey = SurveyResponse(
    age=form.age.data,
    daily_online_hours=form.daily_online_hours.data,
    device=form.device.data,
    interests=form.interests.data,
    selected_ads=form.selected_ad.data,
    user_id=current_user.id
)

# AI prediction
prob = predict_click_probability(survey)
```

### 8. User Consent System

#### Consent Management:
- **Registration**: Users can opt-in to share results
- **Profile Settings**: Users can modify consent preferences
- **Data Sharing**: Only users with consent can view others' results

#### Implementation:
```python
# User model includes consent field
share_results = db.Column(db.Boolean, default=False)

# Filtering shared results
shared_surveys = SurveyResponse.query.join(User).filter(
    User.share_results == True,
    SurveyResponse.user_id != current_user.id
).all()
```

### 9. Error Handling

#### Model Loading:
- **Fallback**: If no trained model exists, uses dummy data for training
- **Compatibility**: Handles both old and new model formats
- **Validation**: Checks for required data before training

#### Prediction Errors:
- **Missing Data**: Graceful handling of incomplete survey responses
- **Model Errors**: Fallback predictions when model fails
- **User Feedback**: Clear error messages for users

### 10. Performance Considerations

#### Optimization:
- **Model Caching**: Trained model loaded once and reused
- **Batch Processing**: Efficient training on collected data
- **Memory Management**: Proper cleanup of training data

#### Scalability:
- **Incremental Training**: Model can be retrained with new data
- **Feature Scaling**: Normalized features for consistent performance
- **Database Efficiency**: Optimized queries for large datasets

### 11. Security and Privacy

#### Data Protection:
- **User Consent**: Explicit permission for data sharing
- **Anonymization**: No personal data in model training
- **Access Control**: Admin-only access to model monitoring

#### Model Security:
- **Input Validation**: Sanitized survey inputs
- **Output Validation**: Bounded probability outputs
- **Error Handling**: Secure error messages

### 12. Future Enhancements

#### Planned Improvements:
- **Advanced Models**: Support for neural networks
- **Real-time Training**: Continuous model updates
- **A/B Testing**: Model comparison capabilities
- **Feature Engineering**: More sophisticated feature extraction

#### Monitoring Enhancements:
- **Performance Alerts**: Automated notifications for model degradation
- **Drift Detection**: Monitoring for data distribution changes
- **Model Versioning**: Support for multiple model versions

## Conclusion

The AI module is fully integrated with the web application, providing:
- Seamless data collection through surveys
- Real-time predictions for users
- Comprehensive monitoring for administrators
- User consent management for data sharing
- Robust error handling and security measures

The integration follows best practices for ML model deployment in web applications, ensuring reliability, performance, and user privacy. 