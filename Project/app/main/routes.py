# 🌐 Импорти от Flask за визуализация, пренасочване, съобщения, заявки, файлове и достъп до конфигурацията
from flask import render_template, redirect, url_for, flash, request, send_file, current_app
# 🔐 Импорти за логин функционалност
from flask_login import login_required, current_user
# 📘 Blueprint за основната част на приложението
from app.main import main_bp
# 📝 Форми: анкета, регистрация, редакция на профил
from app.forms import SurveyForm, RegistrationForm, ProfileForm
# 🗃️ SQLAlchemy базата данни
from app import db
# 👥 Модели: отговори от анкета и кликнати реклами
from app.models import SurveyResponse, AdClick
# 🤖 Модел за прогнозиране на вероятност за кликване
from app.utils.ai_model import predict_click_probability
# 📊 Функция за генериране и запис на графики (логистична регресия)
from app.utils.plot_utils import generate_user_plot
# 🎲 За избор на произволна реклама
import random
# 📂 За работа с файлове и пътища
import os


ADS = ['ad1.jpg', 'ad2.jpg', 'ad3.jpg']  # Примерни реклами

@main_bp.route('/')
def index():
    return render_template('main/index.html') # Показва index.html

@main_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()  # Създаване на форма за анкета

    # Взимане на всички рекламни изображения от директорията
    ads_dir = os.path.join(current_app.root_path, 'static', 'ads')
    ad_images = [f for f in os.listdir(ads_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Попълване на избираемите опции в анкетата с реклами
    form.selected_ad.choices = [(img, f'Ad {i+1}') for i, img in enumerate(ad_images)]

    # Ако потребителят е попълнил формата и тя е валидна
    if form.validate_on_submit():
        # Създаване на нов запис в SurveyResponse
        survey = SurveyResponse(
            age=form.age.data,
            daily_online_hours=form.daily_online_hours.data,
            device=form.device.data,
            interests=form.interests.data,
            selected_ads=form.selected_ad.data,
            user_id=current_user.id
        )
        db.session.add(survey)
        db.session.commit()

        # Генериране на графика от резултата
        plot_path = os.path.join(current_app.root_path, 'static', 'results', f'user_{current_user.id}.png')
        generate_user_plot(survey, plot_path)

        # Пренасочване към страницата с резултата
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
    # Взимане на анкетата от базата
    survey = SurveyResponse.query.get_or_404(survey_id)

    # Изчисляване на вероятност за кликване (чрез ML модел)
    prob = predict_click_probability(survey)

    # Генериране и запис на логистичната регресия като изображение
    plot_path = os.path.join(current_app.root_path, 'static', 'results', f'user_{current_user.id}.png')
    image_name = generate_user_plot(survey, plot_path)

    return render_template('main/result.html', prob=prob, ad='ad1.jpg', user_result_path=image_name)


@main_bp.route('/download_regression/<int:user_id>')
@login_required
def download_regression(user_id):
    # Път до изображението с регресията
    file_path = os.path.join(current_app.root_path, 'static', 'results', f'user_{user_id}.png')
    
    if not os.path.exists(file_path):
        flash("Result image not found. Please generate your result first.", "danger")
        return redirect(url_for('main.profile'))

    return send_file(file_path, as_attachment=True)  # Изпращане като файл за сваляне

@main_bp.route('/ad_click/<ad_name>')
@main_bp.route('/ad_click/<ad_name>')
@login_required
def ad_click(ad_name):
    # Създаване на запис за клик върху реклама
    click = AdClick(ad_name=ad_name, user_id=current_user.id)
    db.session.add(click)
    db.session.commit()

    flash("Ad click recorded!", "info")
    return redirect(url_for('main.index'))

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Попълване на формата с текущите данни
    form = ProfileForm(obj=current_user)

    # При изпратена и валидна форма – обновяване на потребителските данни
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('main.profile'))

    # Зареждане на анкетите и кликовете на текущия потребител
    surveys = SurveyResponse.query.filter_by(user_id=current_user.id).all()
    ad_clicks = AdClick.query.filter_by(user_id=current_user.id).all()

    return render_template('main/profile.html', form=form, surveys=surveys, ad_clicks=ad_clicks)
