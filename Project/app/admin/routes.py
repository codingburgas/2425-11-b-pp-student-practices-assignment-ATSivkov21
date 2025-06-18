from flask import render_template, redirect, url_for, flash, request, send_file, make_response, current_app
from flask_login import login_required, current_user
from app.admin import admin_bp
from app.models import User, SurveyResponse, AdClick
from app.forms import EditUserForm, AdUploadForm
from app import db
import csv
import os
import io
from werkzeug.utils import secure_filename
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated

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
@admin_required
def download_all_users():
    filepath = os.path.join(current_app.root_path, 'static', 'results', 'users.csv')
    users = User.query.all()
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
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

@admin_bp.route('/view_user_plot/<int:user_id>')
@login_required
@admin_required
def view_user_plot(user_id):
    plot_path = os.path.join(current_app.root_path, 'static', 'results', f'user_{user_id}.png')
    if not os.path.exists(plot_path):
        flash('Result image not found. Please generate the result first.', 'danger')
        return redirect(url_for('admin.dashboard'))
    return send_file(plot_path, mimetype='image/png')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    surveys = SurveyResponse.query.all()
    clicks = AdClick.query.all()
    return render_template('admin/dashboard.html', users=users, surveys=surveys, clicks=clicks)

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
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Username', 'Email', 'Confirmed'])
    for u in users:
        writer.writerow([u.username, u.email, u.email_confirmed])
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=users.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@admin_bp.route('/download_regression/<int:user_id>')
@login_required
@admin_required
def download_user_plot(user_id):
    filepath = os.path.join(current_app.root_path, 'static', 'results', f'user_{user_id}.png')
    if not os.path.exists(filepath):
        flash('Result image not found. Please generate the result first.', 'danger')
        return redirect(url_for('admin.dashboard'))
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

@admin_bp.route('/upload_ad', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_ad():
    form = AdUploadForm()
    if form.validate_on_submit():
        file = form.ad_image.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.root_path, 'static', 'ads', filename)
        file.save(file_path)
        flash('Ad image uploaded successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/upload_ad.html', form=form)