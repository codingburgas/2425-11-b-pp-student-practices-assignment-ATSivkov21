from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.main import main_bp
from app.forms import SurveyForm
from app import db
from app.models import SurveyResponse, AdClick
from app.utils.ai_model import predict_click_probability
import random

ADS = ['ad1.jpg', 'ad2.jpg', 'ad3.jpg']  # Примерни реклами

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        survey = SurveyResponse(
            age=form.age.data,
            daily_online_hours=form.daily_online_hours.data,
            device=form.device.data,
            interests=form.interests.data,
            user_id=current_user.id
        )
        db.session.add(survey)
        db.session.commit()
        flash("Survey submitted successfully!", "success")
        return redirect(url_for('main.result', survey_id=survey.id))
    return render_template('main/survey.html', form=form)

@main_bp.route('/result/<int:survey_id>')
@login_required
def result(survey_id):
    survey = SurveyResponse.query.get_or_404(survey_id)
    prob = predict_click_probability(survey)
    selected_ad = random.choice(ADS)
    return render_template('main/result.html', prob=prob, ad=selected_ad)

@main_bp.route('/ad_click/<ad_name>')
@login_required
def ad_click(ad_name):
    click = AdClick(ad_name=ad_name, user_id=current_user.id)
    db.session.add(click)
    db.session.commit()
    flash("Ad click recorded!", "info")
    return redirect(url_for('main.index'))