# 📦 Импортиране на помощни функции за изпращане и потвърждаване на имейл
from app.utils.email_utils import send_confirmation_email, confirm_token
# 🌐 Основни функции за уеб интерфейс
from flask import render_template, redirect, url_for, flash, request
# 🔐 Управление на потребители (логване, текущ потребител и достъп)
from flask_login import login_user, logout_user, current_user, login_required
# ⚠️ За улавяне на грешка при дублиращи се данни (напр. имейл вече съществува)
from sqlalchemy.exc import IntegrityError
# 📧 Имейл съобщения (тук не се използва директно, но може да се използва в send_confirmation_email)
from flask_mail import Message
# 🔐 Създаване и валидиране на токени за потвърждение по имейл
from itsdangerous import URLSafeTimedSerializer
# 🔧 Достъп до текущата Flask конфигурация
from flask import current_app
# 🗃️ Базата данни (SQLAlchemy)
from app import db
# 🔗 Blueprint за auth маршрути
from app.auth import auth_bp
# 📝 Форми за регистрация и логин
from app.forms import RegistrationForm, LoginForm
# 👤 Модели: потребител и роля
from app.models import User, Role


# 📌 Рут за регистрация на нов потребител
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Ако потребителят вече е логнат, го пренасочваме към началната страница
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # Създаване на инстанция на формата за регистрация
    form = RegistrationForm()

    # Проверка дали формата е изпратена и е валидна
    if form.validate_on_submit():
        # Създаване на потребител със зададени потребителско име и имейл
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        # Задаване на хеширана парола
        user.set_password(form.password.data)

        # Даване на роля "user" по подразбиране
        user.role = Role.query.filter_by(name='user').first()

        # Добавяне към базата данни
        db.session.add(user)
        try:
            # Опит за запис в базата
            db.session.commit()
        except IntegrityError:
            # Ако имейлът или потребителското име вече съществуват
            db.session.rollback()
            flash("Username or email already exists. Please choose another.", "danger")
            return render_template('auth/register.html', form=form)

        # Изпращане на имейл за потвърждение
        send_confirmation_email(user)
        flash("Account created! Check your email to confirm.", "info")
        return redirect(url_for('auth.login'))

    # Ако GET заявка или невалидна форма, показваме формата отново
    return render_template('auth/register.html', form=form)


# ✅ Потвърждение на имейл чрез токен
@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    # Опит за валидиране на токена
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or expired.', 'danger')
        return redirect(url_for('auth.login'))

    # Търсим потребителя с дадения имейл
    user = User.query.filter_by(email=email).first_or_404()

    # Ако вече е потвърдил имейла
    if user.email_confirmed:
        flash('Account already confirmed. Please log in.', 'info')
    else:
        # Потвърждаваме и запазваме в базата
        user.email_confirmed = True
        db.session.commit()
        flash('Email confirmed successfully!', 'success')

    return redirect(url_for('auth.login'))


# 🔐 Вход на потребител
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Ако вече е логнат, няма нужда да влиза отново
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # Създаваме формата за логин
    form = LoginForm()

    # Ако формата е подадена и е валидна
    if form.validate_on_submit():
        # Търсим потребителя по имейл
        user = User.query.filter_by(email=form.email.data).first()

        # Проверка за съществуване и правилна парола
        if user and user.check_password(form.password.data):
            # Ако е админ – пренасочваме към admin dashboard
            if user.role and user.role.name == 'admin':
                login_user(user, remember=form.remember.data)
                flash('Welcome, admin!', 'success')
                return redirect(url_for('admin.dashboard'))

            # Ако не е потвърдил имейла си
            if not user.email_confirmed:
                flash('Please confirm your email before logging in.', 'warning')
                return redirect(url_for('auth.login'))

            # Всичко е наред – влизаме
            login_user(user, remember=form.remember.data)
            flash('Welcome!', 'success')
            return redirect(url_for('main.survey'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    # Показваме отново формата
    return render_template('auth/login.html', form=form)


# 🚪 Изход от акаунта
@auth_bp.route('/logout')
@login_required
def logout():
    # Излизане на потребителя и пренасочване към началната страница
    logout_user()
    return redirect(url_for('main.index'))
