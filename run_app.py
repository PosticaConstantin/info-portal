
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import logging
import newrelic.agent

import settings
import controllers.index as index


logger = logging.getLogger('tornado.general')

handlers = [
    tornado.web.url('/', index.Index, name='index')
]

application_settings = {
    'handlers': handlers,

    'template_path': 'templates/',
    'static_path': 'static',

    'xsrf_cookie': True,
    'autorelaod': False,
    'default_handler_class': index.DefaultHandlerClass,
    'websocket_ping_interval': 60


}
application = tornado.web.Application(**application_settings)

if __name__ == "__main__":
    print('Starting Server', 'http://%s:%s' % (settings.ServerConfig.ADDRESS,settings.ServerConfig.PORT))
    application = newrelic.agent.wsgi_application()(application)
    application.listen(settings.ServerConfig.PORT)
    tornado.ioloop.IOLoop.instance().start()





    # http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    # logger.info('Tornado version : %s' % tornado.version)
    # http_server.bind(port=settings.ServerConfig.PORT,
    #                  address=settings.ServerConfig.ADDRESS)
    # http_server.start(num_processes=0)

    # tornado.ioloop.IOLoop.instance().start()

    # container = tornado.wsgi.WSGIContainer(application)
    # http_server = tornado.httpserver.HTTPServer(container)
    # http_server.listen(8888)
    # tornado.ioloop.IOLoop.current().start()



