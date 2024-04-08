from news_server import news

highlights=news()

print(highlights.save_all())

print("Done Crawling.. Your news are now saved in the database. please refresh the site to se the news")
