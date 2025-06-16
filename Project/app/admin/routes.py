from flask import render_template, redirect, url_for, flash, request, send_file, make_response
from flask_login import login_required, current_user
from app.admin import admin_bp
from app.models import User, SurveyResponse
from app.forms import EditUserForm
from app import db
import csv
import os

#@admin_bp.route('/dashboard')
#@login_required
#def dashboard():
#    if not current_user.role.name == 'admin':
#        flash('Access denied.', 'danger')
#        return redirect(url_for('main.index'))

#    users = User.query.all()
#    surveys = SurveyResponse.query.all()
#    return render_template('admin/dashboard.html', users=users, surveys=surveys)

#@admin_bp.route('/user/delete/<int:user_id>')
#@login_required
#def delete_user(user_id):
#    if not current_user.role.name == 'admin':
#        flash('Unauthorized', 'danger')
#        return redirect(url_for('main.index'))
#
#    user = User.query.get_or_404(user_id)
#    db.session.delete(user)
#    db.session.commit()
#    flash('User deleted.', 'info')
#    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/user/download_all')
@login_required
def download_all_users():
    if not current_user.role.name == 'admin':
        flash('Unauthorized', 'danger')
        return redirect(url_for('main.index'))

    filepath = 'app/static/results/users.csv'
    users = User.query.all()

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Username', 'Email', 'Confirmed'])
        for user in users:
            writer.writerow([user.id, user.username, user.email, user.email_confirmed])

    return send_file(filepath, as_attachment=True)

@admin_bp.route('/user/download_image/<int:user_id>')
@login_required
def download_image(user_id):
    if not current_user.role.name == 'admin' and user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('main.index'))

    path = os.path.join('app/static/results', f'user_{user_id}.png')
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    flash('Image not found.', 'warning')
    return redirect(url_for('admin.dashboard'))


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@admin_bp.route('/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted", "info")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/export_users')
@login_required
@admin_required
def export_users():
    users = User.query.all()
    response = make_response()
    response.headers["Content-Disposition"] = "attachment; filename=users.csv"
    response.headers["Content-Type"] = "text/csv"
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Confirmed'])
    for u in users:
        writer.writerow([u.username, u.email, u.email_confirmed])
    return response

@admin_bp.route('/download_regression/<int:user_id>')
@login_required
@admin_required
def download_user_plot(user_id):
    filepath = os.path.join('app', 'static', 'results', f'user_{user_id}.png')
    return send_file(filepath, as_attachment=True)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.email_confirmed = form.email_confirmed.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_user.html', form=form, user=user)