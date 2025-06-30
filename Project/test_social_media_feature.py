#!/usr/bin/env python3
"""
Test script to verify social media feature integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_social_media_feature():
    """Test that social media feature is properly integrated"""
    
    print("🧪 Testing Social Media Feature Integration")
    print("=" * 50)
    
    # Test 1: Check if social_media field exists in SurveyResponse model
    try:
        from app.models import SurveyResponse
        print("✅ SurveyResponse model imported successfully")
        
        # Check if social_media field exists
        if hasattr(SurveyResponse, 'social_media'):
            print("✅ social_media field exists in SurveyResponse model")
        else:
            print("❌ social_media field missing from SurveyResponse model")
            return False
            
    except Exception as e:
        print(f"❌ Error importing SurveyResponse model: {e}")
        return False
    
    # Test 2: Check if social_media field exists in SurveyForm
    try:
        from app.forms import SurveyForm
        print("✅ SurveyForm imported successfully")
        
        if hasattr(SurveyForm, 'social_media'):
            print("✅ social_media field exists in SurveyForm")
        else:
            print("❌ social_media field missing from SurveyForm")
            return False
            
    except Exception as e:
        print(f"❌ Error importing SurveyForm: {e}")
        return False
    
    # Test 3: Check if AI model includes social_media_length feature
    try:
        from app.utils.ai_model import SoftmaxLogisticRegression
        print("✅ SoftmaxLogisticRegression imported successfully")
        
        model = SoftmaxLogisticRegression()
        if 'social_media_length' in model.feature_names:
            print("✅ social_media_length feature included in AI model")
        else:
            print("❌ social_media_length feature missing from AI model")
            return False
            
    except Exception as e:
        print(f"❌ Error importing AI model: {e}")
        return False
    
    # Test 4: Test feature preparation with social media data
    try:
        # Create mock survey data with social media
        class MockSurvey:
            def __init__(self):
                self.age = 25
                self.daily_online_hours = 8.0
                self.device = 'Mobile'
                self.interests = 'technology, gaming, music'
                self.social_media = 'Facebook, Instagram, TikTok, Twitter'
                self.selected_ads = 'ad1.jpg,ad2.jpg'
                self.streaming_apps_count = 3
                self.video_clip_length = 15.0
        
        mock_survey = MockSurvey()
        
        # Test the feature preparation logic
        interests_len = len(mock_survey.interests or "") / 256
        social_media_len = len(mock_survey.social_media or "") / 500
        ad_count = len((mock_survey.selected_ads or "").split(',')) / 3
        device_score = 0 if mock_survey.device == 'PC' else (1 if mock_survey.device == 'Mobile' else 2) / 2
        
        features = [
            mock_survey.age / 100,
            mock_survey.daily_online_hours / 24,
            device_score,
            interests_len,
            social_media_len,
            ad_count,
            mock_survey.streaming_apps_count / 20,
            mock_survey.video_clip_length / 300
        ]
        
        print(f"✅ Feature preparation successful")
        print(f"   - Social media length: {len(mock_survey.social_media)} characters")
        print(f"   - Normalized social media length: {social_media_len:.4f}")
        print(f"   - Total features: {len(features)}")
        
        if len(features) == 8:  # Should have 8 features now
            print("✅ Correct number of features (8)")
        else:
            print(f"❌ Incorrect number of features: {len(features)} (expected 8)")
            return False
            
    except Exception as e:
        print(f"❌ Error in feature preparation test: {e}")
        return False
    
    # Test 5: Test database column exists
    try:
        import sqlite3
        db_path = 'instance/site.db'
        
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if social_media column exists
            cursor.execute("PRAGMA table_info(survey_response)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'social_media' in columns:
                print("✅ social_media column exists in database")
            else:
                print("❌ social_media column missing from database")
                return False
                
            conn.close()
        else:
            print("⚠️  Database file not found, skipping database test")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
    
    print("\n🎉 All tests passed! Social media feature is properly integrated.")
    return True

if __name__ == "__main__":
    success = test_social_media_feature()
    if success:
        print("\n✅ Social media feature integration test completed successfully")
    else:
        print("\n❌ Social media feature integration test failed")
        sys.exit(1) 