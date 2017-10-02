import motor
import funcy
import tornado.httpclient
import tornado.gen
import settings

# client = motor.motor_tornado.MotorClient()
# connection = motor.motor_tornado.MotorClient(settings.MongoConfig.HOST, settings.MongoConfig.PORT)
# db = connection[settings.MongoConfig.DB_NAME]
# db.authenticate(settings.MongoConfig.USER, settings.MongoConfig.PASS)


connection = motor.motor_tornado.MotorClient("mongodb://%s:%s@ds147454.mlab.com:47454/parsing_db" % (settings.MongoConfig.USER,settings.MongoConfig.PASS))
db = connection[settings.MongoConfig.DB_NAME]


class AsyncHTTPClient(object):
    @funcy.cached_property
    def client(self):
        tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient", max_clients=200)
        return tornado.httpclient.AsyncHTTPClient()

async_http = AsyncHTTPClient()


class Mongo(object):
    """Use funcy.cached_property for lazy-load of modules which starts Tornado IOLoop such as Motor and tornado.httpclient.

    Without this workaround, Tornado in multiprocessing mode raises exception "IOLoop already initialized".

    """

    # client = motor.motor_tornado.MotorClient()
    # connection = motor.motor_tornado.MotorClient(settings.MongoConfig.HOST, settings.MongoConfig.PORT)
    # db = connection[settings.MongoConfig.DB_NAME]
    # db = db.authenticate(settings.MongoConfig.USER, settings.MongoConfig.PASS)


    @funcy.cached_property
    def parsing_db_news(self):
        global db
        return db.news


mongo = Mongo()
