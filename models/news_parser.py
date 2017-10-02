import re
import urllib.request
import xml.etree.ElementTree as et
import datetime
import models
import constants
from tornado.gen import coroutine
import time

@coroutine
def parse_point():
    for url_lang in constants.NewsUrls.POINT:
        web_data = urllib.request.urlopen(constants.NewsUrls.POINT[url_lang])
        str_data = web_data.read()
        xml_data = et.fromstring(str_data)
        channel = xml_data.find("channel")
        items = channel.findall("item")

        for x in items:
            title = x.find('title').text
            link = x.find('link').text
            description = x.find('description').text
            image_found = re.findall('src="(.*)"', description, flags=re.U)
            image = None
            if image_found:
                image = image_found[0]
                description = description.strip('<img src= "%s" /><br />' % image)
            pub_date = x.find('pubDate').text
            pub_date = pub_date.split(',')[1].strip().rstrip(' GMT')
            date = datetime.datetime.strptime(pub_date, "%d %b %Y %H:%M:%S")
            item = {"title": title,
                    "link": link,
                    "description": description,
                    "date": date,
                    "source": "point.md",
                    "image": image,
                    "lang": url_lang}
            exists_news = yield models.mongo.parsing_db_news.find_one({'link': link})
            if not exists_news:
                yield models.mongo.parsing_db_news.insert(item)
        time.sleep(1)
        print('<<< Parsing www.point.md, Done!!! >>>')
    t = 1


@coroutine
def parse_protv():
    web_data = urllib.request.urlopen("http://rss.protv.md/")
    str_data = web_data.read()
    xml_data = et.fromstring(str_data)
    channel = xml_data.find("channel")
    items = channel.findall("item")

    for x in items:
        title = x.find('title').text
        link = x.find('link').text
        description = x.find('description').text
        image_found = re.findall('src="(.*)"', description, flags=re.U)
        image = None
        if image_found:
            image = image_found[0]
            description = description.strip('<img src= "%s" /><br />' % image)
        pub_date = x.find('pubDate').text
        pub_date = pub_date.split(',')[1].strip().rstrip(' GMT').replace(' EES', '')
        date = datetime.datetime.strptime(pub_date, "%d %b %Y %H:%M:%S")
        item = {"title": title,
                "link": link,
                "description": description,
                "date": date,
                "source": "protv.md",
                "image": image,
                "lang": "ro"}
        exists_news = yield models.mongo.parsing_db_news.find_one({'link': link})
        if not exists_news:
            yield models.mongo.parsing_db_news.insert(item)
    time.sleep(1)
    print('<<< Parsing www.protv.md, Done!!! >>>')
    t = 1

#
# @coroutine
# def parse_unimedia():
#     web_data = urllib.request.urlopen("http://unimedia.info/rss/news.xml")
#     str_data = web_data.read()
#     xml_data = et.fromstring(str_data)
#     channel = xml_data.find("channel")
#     items = channel.findall("item")
#
#     for x in items:
#         title = x.find('title').text
#         link = x.find('link').text
#         description = x.find('description').text
#         image_found = re.findall('src="(.*)"', description, flags=re.U)
#         image = None
#         if image_found:
#             image = image_found[0]
#             description = description.strip('<img src= "%s" /><br />' % image)
#         pub_date = x.find('pubDate').text
#         pub_date = pub_date.split(',')[1].strip().rstrip(' GMT').replace(' EES', '')
#         date = datetime.datetime.strptime(pub_date, "%d %b %Y %H:%M:%S")
#         item = {"title": title,
#                 "link": link,
#                 "description": description,
#                 "date": date,
#                 "source": "protv.md",
#                 "image": image,
#                 "lang": "ro"}
#         exists_news = yield models.mongo.parsing_db_news.find_one({'link': link})
#         if not exists_news:
#             yield models.mongo.parsing_db_news.insert(item)
#     time.sleep(1)
#     print('<<< Parsing www.protv.md, Done!!! >>>')
#     t = 1