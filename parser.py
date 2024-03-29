import feedparser
from nltk import SnowballStemmer


def news(category, word):
    stemmer = SnowballStemmer("russian")
    w = stemmer.stem(word)
    news = []
    feed = feedparser.parse('https://lenta.ru/rss/news')
    for post in feed.entries:
        if post.category == category:
            lst = list(map(stemmer.stem, (post.title + post.description).split()))
            if w in lst:
                news.append(post.link)
    return news


def rss_news(rss, word):
    stemmer = SnowballStemmer("russian")
    w = stemmer.stem(word)
    news = []
    feed = feedparser.parse(rss)
    for post in feed.entries:
        lst = list(map(stemmer.stem, (post.title + post.description).split()))
        if w in lst:
            news.append(f"{post.title} \n{post.description}")
    return news

