from app.utils.email_utils import send_confirmation_email, confirm_token
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from app import db
from app.auth import auth_bp
from app.forms import RegistrationForm, LoginForm
from app.models import User, Role

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        user.role = Role.query.filter_by(name='user').first()
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists. Please choose another.", "danger")
            return render_template('auth/register.html', form=form)

        send_confirmation_email(user)
        flash("Account created! Check your email to confirm.", "info")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

#@auth_bp.route('/confirm/<token>')
#def confirm_email(token):
#    email = confirm_token(token)
#    if not email:
#        flash('The confirmation link is invalid or expired.', 'danger')
#        return redirect(url_for('auth.login'))
#
#   user = User.query.filter_by(email=email).first_or_404()
#    if user.email_confirmed:
#        flash('Account already confirmed. Please log in.', 'info')
#    else:
#        user.email_confirmed = True
#        db.session.commit()
#        flash('Email confirmed successfully!', 'success')
#    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.role and user.role.name == 'admin':
                login_user(user, remember=form.remember.data)
                flash('Welcome, admin!', 'success')
                return redirect(url_for('admin.dashboard'))
            if not user.email_confirmed:
                flash('Please confirm your email before logging in.', 'warning')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember.data)
            flash('Welcome!', 'success')
            return redirect(url_for('main.survey'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or expired.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account already confirmed. Please log in.', 'info')
    else:
        user.email_confirmed = True
        db.session.commit()
        flash('Email confirmed successfully!', 'success')
    return redirect(url_for('auth.login'))