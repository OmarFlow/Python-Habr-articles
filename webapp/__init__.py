from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.urls import url_parse

from.forms import LoginForm
from .models import db, News, User
from .python_org_news import get_python_news
from .weather import weather_by_city

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    login = LoginManager()
    login.init_app(app)
    login.login_view = 'login'
    
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    
    @app.route('/')
    def index():
        title = 'Новости Питон'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news=news)
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        title = 'Авторизация'
        print(current_user)
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Не верный логин или пароль')
                return redirect(url_for('login'))
            login_user(user)
            next_page = request.args.get('next')
            if url_parse(next_page).netloc != '' or not next_page:
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', page_title=title, form=form)
    
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:    
            return 'Привет админ'
        return 'ты не админ'
    
    
    return app
