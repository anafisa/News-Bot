import feedparser
from nltk import SnowballStemmer

url = "https://lenta.ru/rss/news"
feed = feedparser.parse(url)

# def parse(rss):
#     return feedparser.parse(rss)
#
#
# print (parse(url))
# stemmer = SnowballStemmer("russian")
# word = "деньги"
# category = "Экономика"
# w = stemmer.stem(word)
# news = []
print(feed)

# for post in feed.entries:
#     if post.category == category:
#         lst = list(map(stemmer.stem, (post.title + post.description).split()))
#         if w in lst:
#             news.append([post.title, post.description, post.link])




