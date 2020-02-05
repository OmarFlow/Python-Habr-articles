import requests

from flask import current_app

from webapp.db import db
from webapp.news.models import News


def get_html(url):
    headers = {
        'User-Agent': current_app.config['USER_AGENT']
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(ValueError, requests.RequestException):
        print('network error')
        return False


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()
