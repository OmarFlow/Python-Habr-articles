from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate

from webapp.db import db
from webapp.user.models import User
from .python_org_news import get_python_news
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    login = LoginManager()
    login.init_app(app)
    login.login_view = 'user.login'
    
    migrate = Migrate(app, db)
    
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)
    
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    
    return app
