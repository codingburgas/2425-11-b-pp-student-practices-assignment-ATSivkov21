# 🌐 Импорти от Flask за визуализация, пренасочване, съобщения, заявки, файлове и достъп до конфигурацията
from flask import render_template, redirect, url_for, flash, request, send_file, current_app, jsonify
# 🔐 Импорти за логин функционалност
from flask_login import login_required, current_user
# 📘 Blueprint за основната част на приложението
from app.main import main_bp
# 📝 Форми: анкета, регистрация, редакция на профил
from app.forms import SurveyForm, RegistrationForm, ProfileForm
# 🗃️ SQLAlchemy базата данни
from app import db
# 👥 Модели: отговори от анкета и кликнати реклами
from app.models import SurveyResponse, AdClick, User
# 🤖 Модел за прогнозиране на вероятност за кликване
from app.utils.ai_model import predict_click_probability, train_model, get_model_metrics, get_feature_importance, generate_model_plots
from app.utils.plot_utils import generate_user_plot
# 🎲 За избор на произволна реклама
import random
# 📂 За работа с файлове и пътища
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


ADS = ['ad1.jpg', 'ad2.jpg', 'ad3.jpg']  # Примерни реклами

@main_bp.route('/')
def index():
    return render_template('main/index.html') # Показва index.html

@main_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()
    ads_dir = os.path.join('static', 'ads')
    ad_images = [f for f in os.listdir(os.path.join(os.path.dirname(__file__), '..', ads_dir)) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    if request.method == 'POST':
        form.selected_ads.data = request.form.getlist('selected_ads')
    if form.selected_ads.data is None:
        form.selected_ads.data = []
    if form.validate_on_submit():
        # Създаване на нов запис в SurveyResponse
        survey = SurveyResponse(
            age=form.age.data,
            daily_online_hours=form.daily_online_hours.data,
            device=form.device.data,
            interests=form.interests.data,
            social_media=form.social_media.data,
            selected_ads=','.join(form.selected_ads.data),
            streaming_apps_count=form.streaming_apps_count.data,
            video_clip_length=form.video_clip_length.data,
            user_id=current_user.id
        )
        db.session.add(survey)
        db.session.commit()

        # Генериране на графика от резултата
        plot_path = os.path.join(current_app.root_path, 'static', 'results', f'user_{current_user.id}.png')
        generate_user_plot(survey, plot_path)

        # Пренасочване към страницата с резултата
        return redirect(url_for('main.result', survey_id=survey.id))
    return render_template('main/survey.html', form=form, ad_images=ad_images)

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
        current_user.share_results = form.share_results.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('main.profile'))

    # Зареждане на анкетите и кликовете на текущия потребител
    surveys = SurveyResponse.query.filter_by(user_id=current_user.id).all()
    ad_clicks = AdClick.query.filter_by(user_id=current_user.id).all()
    return render_template('main/profile.html', form=form, surveys=surveys, ad_clicks=ad_clicks)

@main_bp.route('/toggle_sharing', methods=['POST'])
@login_required
def toggle_sharing():
    current_user.share_results = not current_user.share_results
    db.session.commit()
    return jsonify({'status': 'success', 'sharing': current_user.share_results})

@main_bp.route('/view_predictions')
@login_required
def view_predictions():
    # Get all users who have consented to share their predictions
    users = User.query.filter_by(share_results=True).all()
    predictions = []
    
    for user in users:
        if user.id != current_user.id:  # Don't show current user's predictions
            latest_survey = SurveyResponse.query.filter_by(user_id=user.id).order_by(SurveyResponse.timestamp.desc()).first()
            if latest_survey:
                prob = predict_click_probability(latest_survey)
                predictions.append({
                    'username': user.username,
                    'probability': prob,
                    'timestamp': latest_survey.timestamp,
                    'user_id': user.id
                })
    
    return render_template('main/view_predictions.html', predictions=predictions)

@main_bp.route('/train_model')
@login_required
def train_model_route():
    if not current_user.role or current_user.role.name != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('main.index'))
    
    try:
        model, metrics = train_model()
        if model:
            flash('Model trained successfully!', 'success')
        else:
            flash('Not enough data to train model. Need at least 10 survey responses.', 'warning')
    except Exception as e:
        flash(f'Error training model: {str(e)}', 'danger')
    
    return redirect(url_for('main.model_metrics'))

@main_bp.route('/model_metrics')
@login_required
def model_metrics():
    if not current_user.role or current_user.role.name != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('main.index'))
    
    metrics = get_model_metrics()
    feature_importance = get_feature_importance()
    
    # Generate model plots
    plots = generate_model_plots()
    
    return render_template('main/model_metrics.html', 
                         metrics=metrics, 
                         feature_importance=feature_importance,
                         plots=plots)

@main_bp.route('/generate_report')
@login_required
def generate_report():
    # Create a PDF report
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("Ad Click Prediction System Report", title_style))
    story.append(Spacer(1, 20))
    
    # User Statistics
    story.append(Paragraph("User Statistics", styles['Heading2']))
    total_users = User.query.count()
    active_users = User.query.filter(User.surveys.any()).count()
    sharing_users = User.query.filter_by(share_predictions=True).count()
    
    user_stats = [
        ["Total Users", str(total_users)],
        ["Active Users", str(active_users)],
        ["Users Sharing Predictions", str(sharing_users)]
    ]
    
    t = Table(user_stats, colWidths=[200, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Model Metrics
    metrics = get_model_metrics()
    if metrics:
        story.append(Paragraph("Model Performance Metrics", styles['Heading2']))
        model_stats = [
            ["Metric", "Value"],
            ["Accuracy", f"{metrics['accuracy']:.3f}"],
            ["Precision", f"{metrics['precision']:.3f}"],
            ["Recall", f"{metrics['recall']:.3f}"],
            ["F1-Score", f"{metrics['f1_score']:.3f}"],
            ["Log Loss (Entropy)", f"{metrics['logloss']:.3f}"]
        ]
        
        t = Table(model_stats, colWidths=[150, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
    
    # Recent Predictions
    story.append(Paragraph("Recent Predictions", styles['Heading2']))
    recent_surveys = SurveyResponse.query.order_by(SurveyResponse.timestamp.desc()).limit(10).all()
    
    if recent_surveys:
        predictions_data = [["User", "Age", "Device", "Click Probability", "Date"]]
        for survey in recent_surveys:
            prob = predict_click_probability(survey)
            predictions_data.append([
                survey.user.username,
                str(survey.age),
                survey.device,
                f"{prob*100:.1f}%",
                survey.timestamp.strftime("%Y-%m-%d %H:%M")
            ])
        
        t = Table(predictions_data, colWidths=[100, 50, 80, 100, 120])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'ad_predictor_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        mimetype='application/pdf'
    )

@main_bp.route('/shared_results')
@login_required
def shared_results():
    # Взимане на резултати от потребители, които са дали съгласие за споделяне
    shared_surveys = SurveyResponse.query.join(User).filter(
        User.share_results == True,
        SurveyResponse.user_id != current_user.id
    ).all()
    
    # Групиране по потребител
    user_results = {}
    for survey in shared_surveys:
        if survey.user.username not in user_results:
            user_results[survey.user.username] = []
        user_results[survey.user.username].append({
            'age': survey.age,
            'device': survey.device,
            'interests': survey.interests,
            'click_probability': predict_click_probability(survey),
            'timestamp': survey.timestamp
        })
    
    return render_template('main/shared_results.html', user_results=user_results)
