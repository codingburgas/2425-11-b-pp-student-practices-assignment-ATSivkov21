from app import create_app, db
from app.models import User, Role

def ensure_admin():
    app = create_app()
    with app.app_context():
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@gmail.com', email_confirmed=True, role=admin_role)
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created.')
        else:
            admin.email = 'admin@gmail.com'
            admin.set_password('admin')
            admin.role = admin_role
            admin.email_confirmed = True
            db.session.commit()
            print('Admin user updated.')

if __name__ == '__main__':
    ensure_admin() 