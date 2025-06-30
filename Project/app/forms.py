from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, SelectField, TextAreaField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

# Форма за регистрация на нов потребител
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Поле за потребителско име, задължително
    email = StringField('Email', validators=[Email()])  # Поле за имейл с валидатор за правилен формат
    password = PasswordField('Password', validators=[DataRequired()])  # Поле за парола, задължително
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])  # Поле за потвърждение на паролата (трябва да съвпада с password)
    share_results = BooleanField('I agree to share my survey results with other users')  # Чекбокс за съгласие за споделяне на резултати
    submit = SubmitField('Register')  # Бутон за изпращане на формата

# Форма за вход в системата
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])  # Поле за имейл с валидатор за формат
    password = PasswordField('Password', validators=[DataRequired()])  # Поле за парола, задължително
    remember = BooleanField('Remember Me')  # Чекбокс за запомняне на сесията
    submit = SubmitField('Login')  # Бутон за вход

# Форма за попълване на анкета
class SurveyForm(FlaskForm):
    age = IntegerField('Your Age', validators=[DataRequired(), NumberRange(min=10, max=100)])
    daily_online_hours = FloatField('Hours Online per Day', validators=[DataRequired()])
    device = SelectField('Device', choices=[('PC', 'PC'), ('Mobile', 'Mobile'), ('Tablet', 'Tablet')])
    interests = TextAreaField('Your Interests (comma separated)', validators=[DataRequired()])
    social_media = TextAreaField('Social Media Platforms (comma separated, e.g., Facebook, Instagram, TikTok)', validators=[DataRequired()])
    selected_ads = SelectMultipleField('Which Ads Do You Like?', choices=[
        ('ad1.jpg', 'Ad 1'), ('ad2.jpg', 'Ad 2'), ('ad3.jpg', 'Ad 3')
    ])
    streaming_apps_count = IntegerField('Number of Streaming Applications You Use', validators=[DataRequired(), NumberRange(min=0, max=20)])
    video_clip_length = FloatField('Average Video Clip Length (minutes)', validators=[DataRequired(), NumberRange(min=0, max=300)])
    submit = SubmitField('Submit Survey')

# Форма за редактиране на потребителски данни (от администратор или потребител)
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    email_confirmed = BooleanField('Email Confirmed')
    is_admin = BooleanField('Make Admin')
    submit = SubmitField('Save Changes')

# Форма за обновяване на профила (например от потребителя самия)
class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Поле за потребителско име
    email = StringField('Email', validators=[Email()])  # Поле за имейл
    share_results = BooleanField('I agree to share my survey results with other users')  # Чекбокс за съгласие за споделяне на резултати
    submit = SubmitField('Update Profile')  # Бутон за обновяване

# Форма за качване на рекламно изображение
class AdUploadForm(FlaskForm):
    ad_image = FileField('Upload Ad Image', validators=[
        FileRequired(),  # Качването на файл е задължително
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')  # Позволени са само изображения с разширения jpg, jpeg, png
    ])
    submit = SubmitField('Upload Ad')  # Бутон за качване
