from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, SurveyResponse, AdClick
from app.admin import admin_bp
from app import db

@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.role or current_user.role.name != 'admin':
        flash("Admins only!", "danger")
        return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
def dashboard():
    users = User.query.all()
    surveys = SurveyResponse.query.all()
    clicks = AdClick.query.all()
    return render_template('admin/dashboard.html', users=users, surveys=surveys, clicks=clicks)

@admin_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "info")
    return redirect(url_for('admin.dashboard'))