#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   nihaowua_spider.py
@Time    :   2020/07/21 19:56:26
@Author  :   waleslau 
@Version :   1.0
@Contact :   waleslau@foxmail.com
"""

import logging
import coloredlogs
import requests
import re
import pymongo
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
from conf import *
from time import sleep

FIELD_STYLES = dict(
    asctime=dict(color="green"),
    hostname=dict(color="magenta"),
    levelname=dict(color="green"),
    filename=dict(color="magenta"),
    name=dict(color="blue"),
    threadName=dict(color="green"),
)

LEVEL_STYLES = dict(
    debug=dict(color="green"),
    info=dict(color="cyan"),
    warning=dict(color="yellow"),
    error=dict(color="red"),
    critical=dict(color="red"),
)

logger = logging.getLogger("nihaowua")
coloredlogs.install(
    level=logging.DEBUG,
    fmt="[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s",
    level_styles=LEVEL_STYLES,
    field_styles=FIELD_STYLES,
)


def get_random_ua():
    ua = UserAgent()
    return ua.random


headers = {"User-Agent": get_random_ua()}


def get_html(url):
    # logger.info('scraping %s...', url)
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        logging.error("get invalid status code %s while scraping %s",
                      response.status_code, url)
    except requests.RequestException:
        logging.error("error occurred while scraping %s", url, exc_info=True)


def parse(html):
    doc = pq(html)
    post = doc("section div").text()
    return {"post": post}


client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]


def save_data_to_mongo(data):
    if TYPE == 0:
        collection = db[MONGO_COLLECTION_NAME_WU]
    if TYPE == 1:
        collection = db[MONGO_COLLECTION_NAME_DU]

    collection.update_one({"post": data.get("post")}, {"$set": data},
                          upsert=True)


def save_data_to_file(data):
    if TYPE == 0:
        fo = open('你好污啊.txt', 'a+', encoding='utf-8')
        fo.write(data)
        fo.close()
    if TYPE == 1:
        fo = open('毒鸡汤.txt', 'a+', encoding='utf-8')
        fo.write(data)
        fo.close()


def main():
    global TIMES
    while TIMES > 0:
        TIMES -= 1
        if TYPE == 0:
            html = get_html("https://www.nihaowua.com")
            data = parse(html)
        if TYPE == 1:
            html = get_html("https://www.nihaowua.com/home.html")
            data = parse(html)
        logger.info("get data：\n \n \t %s\n", data["post"])
        if SAVE_TO_MONGO:
            logger.info("saving data to mongodb..")
            save_data_to_mongo(data)
            logger.info("data saved successfully")
        if SAVE_TO_FILE:
            logger.info("writing data to file..")
            save_data_to_file(str(data['post']) + '\n')
            logger.info("writing successfully")
        sleep(0.5)


if __name__ == "__main__":
    main()
