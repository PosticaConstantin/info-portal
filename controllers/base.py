import tornado.web
from tornado.gen import coroutine


class BaseHandler(tornado.web.RequestHandler):
    @coroutine
    def write_error(self, status_code, **kwargs):
        if status_code in [404, 500, 503, 403]:
            self.render('pages/errors/http_error.html', status_code=status_code)