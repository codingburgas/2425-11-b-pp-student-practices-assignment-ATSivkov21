from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SurveyForm(FlaskForm):
    age = IntegerField('Your Age', validators=[DataRequired(), NumberRange(min=10, max=100)])
    daily_online_hours = FloatField('Hours Online per Day', validators=[DataRequired()])
    device = SelectField('Device', choices=[('PC', 'PC'), ('Mobile', 'Mobile'), ('Tablet', 'Tablet')])
    interests = TextAreaField('Your Interests (comma separated)', validators=[DataRequired()])
    selected_ads = SelectMultipleField('Which Ads Do You Like?', choices=[
        ('ad1.jpg', 'Ad 1'), ('ad2.jpg', 'Ad 2'), ('ad3.jpg', 'Ad 3')
    ])
    submit = SubmitField('Submit Survey')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    email_confirmed = BooleanField('Email Confirmed')
    submit = SubmitField('Save Changes')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Update Profile')

