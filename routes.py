from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Photo, Folder
import os
from config import Config

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return redirect(url_for('routes.album'))  # Перенаправлення на галерею

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@routes_bp.route('/album', defaults={'folder_id': None})
@routes_bp.route('/album/<int:folder_id>')
@login_required
def album(folder_id):
    if folder_id:
        current_folder = Folder.query.get_or_404(folder_id)
        folders = Folder.query.filter_by(user_id=current_user.id, parent_id=folder_id).all()
        photos = Photo.query.filter_by(user_id=current_user.id, folder_id=folder_id).all()
    else:
        current_folder = None
        folders = Folder.query.filter_by(user_id=current_user.id, parent_id=None).all()
        photos = Photo.query.filter_by(user_id=current_user.id, folder_id=None).all()

    all_folders = Folder.query.filter_by(user_id=current_user.id).all()
    return render_template('album.html', folders=folders, photos=photos, all_folders=all_folders, current_folder=current_folder)

@routes_bp.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    folder_name = request.form.get('folder_name')
    parent_id = request.form.get('parent_id') or None

    new_folder = Folder(name=folder_name, user_id=current_user.id, parent_id=parent_id)
    db.session.add(new_folder)
    db.session.commit()
    flash('Папка створена!', 'success')

    return redirect(url_for('routes.album', folder_id=parent_id) if parent_id else url_for('routes.album'))

@routes_bp.route('/upload', methods=['POST'])
@login_required
def upload_photo():
    if 'file' not in request.files:
        flash('Файл не завантажено', 'danger')
        return redirect(url_for('routes.album'))

    file = request.files['file']
    if file.filename == '':
        flash('Файл не вибрано', 'danger')
        return redirect(url_for('routes.album'))

    folder_id = request.form.get('folder_id')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)

        new_photo = Photo(filename=filename, user_id=current_user.id, folder_id=folder_id if folder_id else None)
        db.session.add(new_photo)
        db.session.commit()
        flash('Фото успішно завантажене!', 'success')
    else:
        flash('Неприпустимий формат файлу', 'danger')

    return redirect(url_for('routes.album', folder_id=folder_id) if folder_id else url_for('routes.album'))
