# # avatar.py
#
# from flask import Blueprint, request, redirect, url_for, session
# from werkzeug.utils import secure_filename
# import os
#
# avatar_bp = Blueprint('avatar', __name__)
#
# # Место для хранения загруженных аватарок
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
#
# @avatar_bp.route('/upload', methods=['POST'])
# def upload_avatar():
#     if 'username' not in session:
#         return redirect(url_for('index'))
#
#     # Проверяем, загрузил ли пользователь файл
#     if 'avatar' not in request.files:
#         return redirect(request.url)
#
#     avatar_file = request.files['avatar']
#
#     # Если файл не выбран
#     if avatar_file.filename == '':
#         return redirect(request.url)
#
#     # Проверяем, что файл имеет допустимое расширение
#     if '.' not in avatar_file.filename or avatar_file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
#         return 'Invalid file format'
#
#     # Защищаем имя файла от возможных атак
#     filename = secure_filename(avatar_file.filename)
#     # Сохраняем файл на сервере
#     avatar_file.save(os.path.join(UPLOAD_FOLDER, filename))
#
#     # Обновляем путь к аватарке в базе данных
#     user = User.query.filter_by(username=session['username']).first()
#     user.avatar_path = os.path.join(UPLOAD_FOLDER, filename)
#     db.session.commit()
#
#     return redirect(url_for('dashboard'))
