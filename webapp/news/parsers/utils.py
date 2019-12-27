import requests

from webapp.db import db
from webapp.news.models import News

def get_html(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'
    }
    try:
        result = requests.get(url,headers=headers)
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