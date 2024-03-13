from flask import Blueprint, render_template, redirect, url_for, session
from database import User

admin_panel_bp = Blueprint('admin_panel', __name__, template_folder='templates')

@admin_panel_bp.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')

@admin_panel_bp.route('/admin', methods=['POST'])
def add_user():
    # Обработка добавления пользователя
    # Ваш код здесь
    return redirect(url_for('admin_panel.admin_panel'))

@admin_panel_bp.route('/save', methods=['POST'])
def save_changes():
    # Обработка сохранения изменений
    # Ваш код здесь
    return redirect(url_for('admin_panel.admin_panel'))

@admin_panel_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
