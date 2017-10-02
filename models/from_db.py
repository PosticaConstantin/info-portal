import models
import tornado
from tornado.gen import coroutine

@coroutine
def get_news(skip, take, lang):
    news = yield models.mongo.parsing_db_news.find({"lang": lang}, sort=[('date', -1)], skip=skip, limit=take).to_list(take)
    total = yield models.mongo.parsing_db_news.find({"lang": lang}).count()
    result = {"news": news, "total": total}
    raise tornado.gen.Return(result)