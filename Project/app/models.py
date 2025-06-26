from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean, default=False)
    share_predictions = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    survey_responses = db.relationship('SurveyResponse', backref='user', lazy=True)
    ad_clicks = db.relationship('AdClick', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    daily_online_hours = db.Column(db.Float)
    device = db.Column(db.String(64))
    interests = db.Column(db.String(256))
    selected_ads = db.Column(db.String(200), nullable=True)
    streaming_apps_count = db.Column(db.Integer, default=0)  # Number of streaming applications
    video_clip_length = db.Column(db.Float, default=0.0)  # Average video clip length in minutes
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class AdClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_name = db.Column(db.String(100), nullable=False)
    clicked_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ModelWeights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weights = db.Column(db.Text)  # JSON string of weights
    bias = db.Column(db.Float)
    training_date = db.Column(db.DateTime, default=datetime.utcnow)
    model_version = db.Column(db.String(50), default='1.0')
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    logloss = db.Column(db.Float)