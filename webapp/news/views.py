from flask import (
    abort,
    Blueprint,
    flash,
    current_app,
    render_template,
    redirect
)
from flask_login import current_user

from webapp.news.models import News, Comment
from webapp.news.forms import CommentForm
from webapp.weather import weather_by_city
from webapp.db import db
from webapp.utils import get_redirect_target

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    title = 'Новости Питон'
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news = News.query.filter(News.text.isnot(None)
                             ).order_by(News.published.desc()).all()
    return render_template('news/index.html',
                           page_title=title, weather=weather, news=news)


@blueprint.route('/news/<int:news_id>', methods=['GET', 'POST'])
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()

    if not my_news:
        abort(404)

    form = CommentForm(news_id=my_news.id)

    if form.validate_on_submit():
        comment = Comment(
            news_id=form.news_id.data,
            user_id=current_user.id,
            text=form.text.datas
        )

        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен')
        return redirect(get_redirect_target())
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в заполнении поля "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(get_redirect_target())

    return render_template('news/single_news.html', page_title=my_news.title,
                           news=my_news, form=form)
