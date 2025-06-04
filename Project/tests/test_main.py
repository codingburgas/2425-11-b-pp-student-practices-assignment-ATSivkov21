import unittest
from app import create_app, db
from app.models import User, SurveyResponse
from flask_login import login_user

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.user = User(username='tester', email='tester@test.com')
            self.user.set_password('123456')
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self):
        self.client.post('/login', data={
            'email': 'tester@test.com',
            'password': '123456'
        })

    def test_survey_page(self):
        self.login()
        response = self.client.get('/survey')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tell Us About Yourself', response.data)

    def test_submit_survey(self):
        self.login()
        response = self.client.post('/survey', data={
            'age': 25,
            'daily_online_hours': 5,
            'device': 'PC',
            'interests': 'gaming, tech'
        }, follow_redirects=True)
        self.assertIn(b'Prediction Result', response.data)