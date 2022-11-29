from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "games_connect.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.eZae_lkw7J-QAbi2NXcEfVyxNhYjyMOOHd9we9rsZy0'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #'postgresql://postgres:awdasdawd2602@localhost:5433/TopicosDb'
    
    db.init_app(app)

    from .controller import views, auth
    from .models import User

    app.register_blueprint(views.views,url_prefix='/')
    app.register_blueprint(auth.auth,url_prefix='/')
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


