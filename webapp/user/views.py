from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user
from werkzeug.urls import url_parse

from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Авторизация'
    if current_user.is_authenticated:
        return redirect(get_redirect_target())

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Не верный логин или пароль')
            return redirect(get_redirect_target())

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


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())

    form = RegistrationForm()
    title = 'Регистрация'

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(get_redirect_target())
    return render_template('user/registration.html',
                           page_title=title, form=form)
