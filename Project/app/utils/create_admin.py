# 📦 Импортиране на приложението и базата данни
from app import create_app, db
# 👤 Импортиране на моделите за потребител и роля
from app.models import User, Role


def ensure_admin():
    # 🛠️ Създаване на Flask приложението (ако още не е създадено)
    app = create_app()

    # 📦 Влизане в контекста на приложението, за да работим с базата
    with app.app_context():
        
        # 🔍 Търсене на роля "admin"
        admin_role = Role.query.filter_by(name='admin').first()

        # 🆕 Ако не съществува, я създаваме и записваме
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()

        # 🔍 Проверка дали съществува потребител с име "admin"
        admin = User.query.filter_by(username='admin').first()

        # 🧾 Ако не съществува, го създаваме с начални данни
        if not admin:
            admin = User(
                username='admin',
                email='ATSivkov21@codingburgas.bg',
                email_confirmed=True,  # Потвърден имейл по подразбиране
                role=admin_role        # Свързване с ролята
            )
            admin.set_password('Gun71648')  # Задаване на парола
            db.session.add(admin)
            db.session.commit()
            print('Admin user created.')

        else:
            # 🔁 Ако вече съществува – актуализираме данните му
            admin.email = 'ATSivkov21@codingburgas.bg'
            admin.set_password('Gun71648')
            admin.role = admin_role
            admin.email_confirmed = True
            db.session.commit()
            print('Admin user updated.')


if __name__ == '__main__':
    ensure_admin() 