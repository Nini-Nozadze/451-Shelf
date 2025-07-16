from flask import Flask
from flask_login import LoginManager
from routes import main
from auth import auth
from models import User
from ext import db
from blog import blog
from upload import upload
import os

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)

    # 📌 პროექტის ძირითადი დირექტორია
    basedir = os.path.abspath(os.path.dirname(__file__))

    # 📌 ბაზის სრული ბილიკი
    db_path = os.path.join(basedir, 'instance', 'books.db')

    # 📌 ატვირთული ფაილების ფოლდერი
    upload_folder = os.path.join(basedir, 'static', 'uploads')

    # ✅ Flask კონფიგურაცია
    app.config['SECRET_KEY'] = 'devkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    # ✅ მოდულების ინიციალიზაცია
    db.init_app(app)
    login_manager.init_app(app)

    # 🔐 მომხმარებლის ჩატვირთვა
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ ბლუპრინტების რეგისტრაცია
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(blog)
    app.register_blueprint(upload)

    # ✅ შექმენი instance ფოლდერი თუ არ არსებობს
    instance_dir = os.path.join(basedir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)

    # ✅ შექმენი ატვირთვების ფოლდერი თუ არ არსებობს
    os.makedirs(upload_folder, exist_ok=True)

    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')

    with app.app_context():
        db.create_all()

    return app
