from flask import Flask, render_template, request, redirect, url_for, session, make_response, send_file, jsonify
from database import db, User, Site
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from users import create_users
from admin_panel import admin_panel_bp
import qrcode
import os
import hashlib
from users import users_bp
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = r'C:\Users\owod3\PycharmProjects\опенаи\.venv\avarats'
app = Flask(__name__)
app.register_blueprint(admin_panel_bp)
app.register_blueprint(users_bp)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sites.db'

# Инициализация базы данных
db.init_app(app)

# Initialize the migration object
migrate = Migrate(app, db)

# Создаем папку для хранения QR-кодов
QR_CODES_DIR = os.path.join(app.static_folder, 'qr_codes')
if not os.path.exists(QR_CODES_DIR):
    os.makedirs(QR_CODES_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    remember_me = request.form.get('remember_me')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        response = make_response(redirect(url_for('dashboard', username=username)))
        if remember_me:
            response.set_cookie('username', username)
        return response
    else:
        return 'Invalid username or password'

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    sites = Site.query.all()  # Получаем все сайты из базы данных

    return render_template('dashboard.html', username=username, sites=sites)

@app.route('/add_site', methods=['POST'])
def add_site():
    username = session.get('username')
    if username:
        site_url = request.form['site_url']
        site = Site(url=site_url, added_by_admin=username == 'admin')
        db.session.add(site)
        db.session.commit()
        return redirect(url_for('dashboard', username=username))
    else:
        return 'Please login to add a site'

@app.route('/delete_site/<int:id>')
def delete_site(id):
    username = session.get('username')
    if username == 'admin':
        Site.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('dashboard', username=username))
    else:
        return 'Only admin can delete sites'

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Функция для генерации QR-кода и сохранения его в файл
def generate_qr_code(url):
    # Создаем хэш от URL, чтобы получить уникальное имя файла
    hash_value = hashlib.sha256(url.encode()).hexdigest()
    img_path = os.path.join(QR_CODES_DIR, f"{hash_value}.png")

    # Создаем QR-код и сохраняем его в файл
    qr = qrcode.make(url)
    qr.save(img_path)

    # Возвращаем путь к файлу с QR-кодом
    return img_path

@app.route('/generate_qr/<path:url>')
def generate_qr(url):
    # Генерируем QR-код и получаем путь к файлу с QR-кодом
    img_path = generate_qr_code(url)
    # Отправляем файл с QR-кодом клиенту
    return send_file(img_path, mimetype='image/png')


@app.route('/admin_panel')
def admin_panel():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=username).first()
    if not user or not user.is_admin:
        return 'Access denied'

    return render_template('admin_panel.html')

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    print("Received upload_avatar request")

    # Проверяем, что файл был отправлен с запросом
    if 'avatar' not in request.files:
        return jsonify({'message': 'No file part', 'success': False}), 400

    avatar_file = request.files['avatar']

    # Проверяем, что файл имеет допустимое расширение
    if avatar_file.filename == '':
        return jsonify({'message': 'No selected file', 'success': False}), 400

    if avatar_file and allowed_file(avatar_file.filename):
        filename = secure_filename(avatar_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("File saved to:", filepath)  # Добавим эту строку для отладки
        avatar_file.save(filepath)

        # Создаем URL для отображения файла на сайте
        avatar_url = url_for('uploaded_avatar', filename=filename)

        return jsonify({'message': 'Avatar uploaded successfully', 'success': True, 'avatar_url': avatar_url})

    return jsonify({'message': 'Invalid file type', 'success': False}), 400


@app.route('/uploads/<filename>')
def uploaded_avatar(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


if __name__ == '__main__':
    # Create users if they don't exist
    create_users(app)
    app.run(debug=True)
