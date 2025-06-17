import unittest
from app import create_app, db
from app.models import User, Role, SurveyResponse, AdClick
from flask import url_for

class FeaturesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            role_admin = Role(name='admin')
            role_user = Role(name='user')
            db.session.add_all([role_admin, role_user])
            db.session.commit()
            self.admin = User(username='admin', email='admin@test.com', email_confirmed=True, role=role_admin)
            self.admin.set_password('adminpass')
            self.user = User(username='user', email='user@test.com', email_confirmed=True, role=role_user)
            self.user.set_password('userpass')
            db.session.add_all([self.admin, self.user])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self, email, password):
        return self.client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)

    def test_email_confirmation_required(self):
        with self.app.app_context():
            user = User(username='unconfirmed', email='unconfirmed@test.com', email_confirmed=False, role=Role.query.filter_by(name='user').first())
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
        response = self.client.post('/login', data={'email': 'unconfirmed@test.com', 'password': 'pass'}, follow_redirects=True)
        self.assertIn(b'Please confirm your email', response.data)

    def test_ad_click_recording(self):
        self.login('user@test.com', 'userpass')
        with self.app:
            response = self.client.get('/ad_click/ad1.jpg', follow_redirects=True)
            self.assertIn(b'Ad click recorded', response.data)
            with self.app.app_context():
                clicks = AdClick.query.filter_by(user_id=self.user.id).all()
                self.assertTrue(any(c.ad_name == 'ad1.jpg' for c in clicks))

    def test_profile_page(self):
        self.login('user@test.com', 'userpass')
        response = self.client.get('/profile')
        self.assertIn(b'My Profile', response.data)
        self.assertIn(b'user@test.com', response.data)

    def test_admin_dashboard_access(self):
        # User should not access admin dashboard
        self.login('user@test.com', 'userpass')
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b'Admin access required', response.data)
        # Admin should access
        self.login('admin@test.com', 'adminpass')
        response = self.client.get('/admin/dashboard')
        self.assertIn(b'Admin Dashboard', response.data)

    def test_survey_with_ad_selection(self):
        self.login('user@test.com', 'userpass')
        response = self.client.post('/survey', data={
            'age': 30,
            'daily_online_hours': 4,
            'device': 'Mobile',
            'interests': 'sports, music',
            'selected_ads': ['ad1.jpg', 'ad2.jpg']
        }, follow_redirects=True)
        self.assertIn(b'Prediction Result', response.data)

    def test_prediction_result_clickable_ad(self):
        self.login('user@test.com', 'userpass')
        # Submit survey to get result page
        response = self.client.post('/survey', data={
            'age': 22,
            'daily_online_hours': 3,
            'device': 'PC',
            'interests': 'tech',
            'selected_ads': ['ad1.jpg']
        }, follow_redirects=True)
        self.assertIn(b'Click the ad above to simulate an ad click', response.data) 