from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.main import main_bp
from app.forms import SurveyForm
from app import db
from app.models import SurveyResponse, AdClick
from app.utils.ai_model import predict_click_probability
from app.utils.plot_utils import generate_user_plot
import random
import os

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
            selected_ads=','.join(form.selected_ads.data),
            user_id=current_user.id
        )
        db.session.add(survey)
        db.session.commit()
        return redirect(url_for('main.result', survey_id=survey.id))
    return render_template('main/survey.html', form=form)

#@main_bp.route('/result/<int:survey_id>')
#@login_required
#def result(survey_id):
#    survey = SurveyResponse.query.get_or_404(survey_id)
#    prob = predict_click_probability(survey)
#    selected_ad = random.choice(ADS)

    # 🖼️ generate and return image path
#    user_result_path = generate_user_plot(current_user.id, survey)

#    return render_template('main/result.html', prob=prob, ad=selected_ad, user_result_path=user_result_path)
@main_bp.route('/result/<int:survey_id>')
@login_required
def result(survey_id):
    survey = SurveyResponse.query.get_or_404(survey_id)
    prob = predict_click_probability(survey)
    image_name = generate_user_plot(current_user.id, survey)
    return render_template('main/result.html', prob=prob, ad='ad1.jpg', user_result_path=image_name)

@main_bp.route('/download_regression/<int:user_id>')
@login_required
def download_regression(user_id):
    file_path = os.path.join('app', 'static', 'results', f'user_{user_id}.png')
    return send_file(file_path, as_attachment=True)

@main_bp.route('/ad_click/<ad_name>')
@login_required
def ad_click(ad_name):
    click = AdClick(ad_name=ad_name, user_id=current_user.id)
    db.session.add(click)
    db.session.commit()
    flash("Ad click recorded!", "info")
    return redirect(url_for('main.index'))