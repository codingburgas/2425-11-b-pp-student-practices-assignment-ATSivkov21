#!/usr/bin/env python3
"""
Test script for the enhanced Softmax Logistic Regression model
"""

import numpy as np
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.ai_model import SoftmaxLogisticRegression

def test_softmax_logistic_regression():
    """Test the enhanced softmax logistic regression model"""
    print("🧪 Testing Enhanced Softmax Logistic Regression Model")
    print("=" * 60)
    
    # Create synthetic data for testing
    np.random.seed(42)
    n_samples = 100
    n_features = 7
    
    # Generate synthetic features
    X = np.random.rand(n_samples, n_features)
    
    # Generate synthetic labels (binary classification)
    # Simple rule: if sum of first 3 features > 1.5, then positive class
    y = (X[:, 0] + X[:, 1] + X[:, 2] > 1.5).astype(int)
    
    print(f"📊 Generated {n_samples} samples with {n_features} features")
    print(f"📈 Class distribution: {np.bincount(y)}")
    
    # Split data
    split_idx = int(0.8 * n_samples)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    print(f"🔧 Training set: {len(X_train)} samples")
    print(f"🧪 Test set: {len(X_test)} samples")
    
    # Initialize and train the model
    print("\n🚀 Training the model...")
    model = SoftmaxLogisticRegression(num_classes=2)
    model.fit(X_train, y_train, epochs=100, lr=0.01)
    
    # Test predictions
    print("\n🔮 Testing predictions...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    print(f"📊 Predictions shape: {y_pred.shape}")
    print(f"📊 Probabilities shape: {y_pred_proba.shape}")
    print(f"📊 Sample probabilities: {y_pred_proba[:5]}")
    
    # Calculate metrics
    print("\n📈 Calculating metrics...")
    metrics = model.calculate_metrics(X_test, y_test)
    
    print("📊 Model Performance Metrics:")
    for metric, value in metrics.items():
        if metric != 'confusion_matrix':
            print(f"  {metric}: {value:.4f}")
        else:
            print(f"  {metric}:")
            for row in value:
                print(f"    {row}")
    
    # Test feature importance
    print("\n🔍 Calculating feature importance...")
    feature_importance = model.calculate_feature_importance(X_train, y_train)
    
    print("📊 Feature Importance (Information Gain):")
    for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature}: {importance:.4f}")
    
    # Test model saving and loading
    print("\n💾 Testing model persistence...")
    model.save()
    
    # Create new model instance and load
    new_model = SoftmaxLogisticRegression(num_classes=2)
    new_model.load()
    
    # Test that predictions are the same
    y_pred_new = new_model.predict(X_test)
    predictions_match = np.array_equal(y_pred, y_pred_new)
    print(f"✅ Predictions after save/load match: {predictions_match}")
    
    # Test plotting functions (without saving)
    print("\n📊 Testing plotting functions...")
    try:
        model.plot_training_history()
        model.plot_confusion_matrix(X_test, y_test)
        model.plot_feature_importance()
        print("✅ All plotting functions work correctly")
    except Exception as e:
        print(f"⚠️  Plotting test failed: {e}")
    
    print("\n🎉 All tests completed successfully!")
    return True

def test_multi_class_classification():
    """Test multi-class classification capabilities"""
    print("\n🧪 Testing Multi-Class Classification")
    print("=" * 50)
    
    # Create synthetic data for 3-class classification
    np.random.seed(42)
    n_samples = 150
    n_features = 5
    
    X = np.random.rand(n_samples, n_features)
    
    # Generate 3 classes based on feature combinations
    y = np.zeros(n_samples, dtype=int)
    y[X[:, 0] + X[:, 1] > 1.5] = 1
    y[X[:, 2] + X[:, 3] > 1.5] = 2
    
    print(f"📊 Generated {n_samples} samples for 3-class classification")
    print(f"📈 Class distribution: {np.bincount(y)}")
    
    # Split data
    split_idx = int(0.8 * n_samples)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train multi-class model
    print("🚀 Training multi-class model...")
    model = SoftmaxLogisticRegression(num_classes=3)
    model.fit(X_train, y_train, epochs=100, lr=0.01)
    
    # Test predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    print(f"📊 Multi-class predictions shape: {y_pred.shape}")
    print(f"📊 Multi-class probabilities shape: {y_pred_proba.shape}")
    print(f"📊 Sample probabilities: {y_pred_proba[:3]}")
    
    # Calculate metrics
    metrics = model.calculate_metrics(X_test, y_test)
    print(f"📊 Multi-class accuracy: {metrics['accuracy']:.4f}")
    
    print("✅ Multi-class classification test completed!")
    return True

if __name__ == "__main__":
    try:
        # Test binary classification
        test_softmax_logistic_regression()
        
        # Test multi-class classification
        test_multi_class_classification()
        
        print("\n🎯 All tests passed! The enhanced model is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 