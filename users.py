from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from database import db, User  # Импортируем объект db

avatar_bp = Blueprint('avatar', __name__)

# Место для хранения загруженных аватарок
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



def create_users(app):
    with app.app_context():
        # Check if users already exist
        existing_users = User.query.all()
        if not existing_users:
            # Create users
            user1 = User(username='user', password='user123')
            user2 = User(username='admin', password='admin123')
            user3 = User(username='a', password='a1')

            # Add users to the session and commit changes to the database
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.commit()

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Обработка запроса на изменение аватара пользователя
        pass
    else:
        # Отображение профиля пользователя
        user = User.query.filter_by(username='example_user').first()
        return render_template('profile.html', user=user)


@avatar_bp.route('/upload', methods=['POST'])
def upload_avatar():
    if 'username' not in session:
        return redirect(url_for('index'))

    # Проверяем, загрузил ли пользователь файл
    if 'avatar' not in request.files:
        return redirect(request.url)

    avatar_file = request.files['avatar']

    # Если файл не выбран
    if avatar_file.filename == '':
        return redirect(request.url)

    # Проверяем, что файл имеет допустимое расширение
    if '.' not in avatar_file.filename or avatar_file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return 'Invalid file format'

    # Защищаем имя файла от возможных атак
    filename = secure_filename(avatar_file.filename)
    # Сохраняем файл на сервере
    avatar_file.save(os.path.join(UPLOAD_FOLDER, filename))

    # Обновляем путь к аватарке в базе данных
    user = User.query.filter_by(username=session['username']).first()
    user.avatar_path = os.path.join(UPLOAD_FOLDER, filename)
    db.session.commit()

    return redirect(url_for('dashboard'))
