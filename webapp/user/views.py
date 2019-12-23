from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.urls import url_parse

from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Авторизация'
    print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Не верный логин или пароль')
            return redirect(url_for('user.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('news.index')
        return redirect(next_page)
    return render_template('user/login.html', page_title=title, form=form)

    @blueprint.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('user.login'))