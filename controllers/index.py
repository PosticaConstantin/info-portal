from tornado.gen import coroutine

import controllers.base as base
import constants
import models
import models.from_db
import models.news_parser as news_parser


class Index(base.BaseHandler):
    @coroutine
    def get(self):
        # parse_news = yield news_parser.parse_point()
        # parse_news = yield news_parser.parse_protv()
        # parse_news = yield news_parser.parse_unimedia()

        lang = self.get_argument('lang', 'ro')
        page = int(self.get_argument("page", default="1"))
        take = constants.news_per_page
        skip = (page - 1) * take
        news_result = yield models.from_db.get_news(skip=skip, take=take, lang=lang)
        news = news_result["news"]
        total_count = news_result["total"]
        total_pages = int(total_count / take)
        self.render('pages/index.html', news=news, page=page, take=take, total_pages=total_pages, lang=lang)


class DefaultHandlerClass(base.BaseHandler):
    @coroutine
    def get(self):
        self.write('<html>'
                   '<body>'
                   '<h1>This page doesnt exists</h1>'
                    '<a href="http://127.0.0.1:5000">Go_to_main_page</a>'
                   
                   '</body>'
                   '</html>')
